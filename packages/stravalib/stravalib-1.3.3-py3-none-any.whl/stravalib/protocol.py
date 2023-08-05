"""
Protocol
==============
Low-level classes for interacting directly with the Strava API webservers.
"""
from __future__ import annotations

import abc
import functools
import logging
from typing import TYPE_CHECKING, Any, Callable, Literal, TypedDict
from urllib.parse import urlencode, urljoin, urlunsplit

import requests

from stravalib import exc

if TYPE_CHECKING:
    from _typeshed import SupportsRead

Scope = Literal[
    "read",
    "read_all",
    "profile:read_all",
    "profile:write",
    "activity:read",
    "activity:read_all",
    "activity:write",
]


class AccessInfo(TypedDict):
    """Dictionary containing token exchange response from Strava."""

    access_token: str
    """A short live token the access Strava API"""

    refresh_token: str
    """The refresh token for this user, to be used to get the next access token for this
    user. Please expect that this value can change anytime you retrieve a new access
    token. Once a new refresh token code has been returned, the older code will no
    longer work.
    """

    expires_at: int
    """The number of seconds since the epoch when the provided access token will expire"""


class ApiV3(metaclass=abc.ABCMeta):
    """
    This class is responsible for performing the HTTP requests, rate limiting, and error handling.
    """

    server = "www.strava.com"
    api_base = "/api/v3"

    def __init__(
        self,
        access_token: str | None = None,
        requests_session: requests.Session | None = None,
        rate_limiter: Callable[[dict[str, str]], None] | None = None,
    ):
        """
        Initialize this protocol client, optionally providing a (shared) :class:`requests.Session`
        object.

        :param access_token: The token that provides access to a specific Strava account.
        :type access_token: str

        :param requests_session: An existing :class:`requests.Session` object to use.
        :type requests_session::class:`requests.Session`
        """
        self.log = logging.getLogger(
            "{0.__module__}.{0.__name__}".format(self.__class__)
        )
        self.access_token = access_token
        if requests_session:
            self.rsession: requests.Session = requests_session
        else:
            self.rsession = requests.Session()

        if rate_limiter is None:
            # Make it a dummy function, so we don't have to check if it's defined before
            # calling it later
            rate_limiter = lambda x: None

        self.rate_limiter = rate_limiter

    def authorization_url(
        self,
        client_id: int,
        redirect_uri: str,
        approval_prompt: Literal["auto", "force"] = "auto",
        scope: list[Scope] | Scope | None = None,
        state: str | None = None,
    ) -> str:
        """
        Get the URL needed to authorize your application to access a Strava user's information.

        See https://developers.strava.com/docs/authentication/

        :param client_id: The numeric developer client id.
        :type client_id: int

        :param redirect_uri: The URL that Strava will redirect to after successful (or failed) authorization.
        :type redirect_uri: str

        :param approval_prompt: Whether to prompt for approval even if approval already granted to app.
                                Choices are 'auto' or 'force'.  (Default is 'auto')
        :type approval_prompt: str

        :param scope: The access scope required.  Omit to imply "read" and "activity:read"
                      Valid values are 'read', 'read_all', 'profile:read_all', 'profile:write', 'activity:read',
                      'activity:read_all', 'activity:write'.
        :type scope: list[str]

        :param state: An arbitrary variable that will be returned to your application in the redirect URI.
        :type state: str

        :return: The URL to use for authorization link.
        :rtype: str
        """
        assert approval_prompt in ("auto", "force")
        if scope is None:
            scope = ["read", "activity:read"]
        elif isinstance(scope, (str, bytes)):
            scope = [scope]

        unsupported = set(scope) - {
            "read",
            "read_all",
            "profile:read_all",
            "profile:write",
            "activity:read",
            "activity:read_all",
            "activity:write",
        }

        assert not unsupported, "Unsupported scope value(s): {}".format(
            unsupported
        )

        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "approval_prompt": approval_prompt,
            "scope": ",".join(scope),
            "response_type": "code",
        }
        if state is not None:
            params["state"] = state

        return urlunsplit(
            ("https", self.server, "/oauth/authorize", urlencode(params), "")
        )

    def exchange_code_for_token(
        self, client_id: int, client_secret: str, code: str
    ) -> AccessInfo:
        """
        Exchange the temporary authorization code (returned with redirect from strava authorization URL)
        for a short-lived access token and a refresh token (used to obtain the next access token later on).

        :param client_id: The numeric developer client id.
        :type client_id: int

        :param client_secret: The developer client secret
        :type client_secret: str

        :param code: The temporary authorization code
        :type code: str

        :return: Dictionary containing the access_token, refresh_token
                 and expires_at (number of seconds since Epoch when the provided access token will expire)
        :rtype: dict
        """
        response = self._request(
            "https://{0}/oauth/token".format(self.server),
            params={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "grant_type": "authorization_code",
            },
            method="POST",
        )
        access_info: AccessInfo = {
            "access_token": response["access_token"],
            "refresh_token": response["refresh_token"],
            "expires_at": response["expires_at"],
        }
        self.access_token = response["access_token"]
        return access_info

    def refresh_access_token(
        self, client_id: int, client_secret: str, refresh_token: str
    ) -> AccessInfo:
        """
        Exchanges the previous refresh token for a short-lived access token and a new
        refresh token (used to obtain the next access token later on).

        :param client_id: The numeric developer client id.
        :type client_id: int

        :param client_secret: The developer client secret
        :type client_secret: str

        :param refresh_token: The refresh token obtain from a previous authorization request
        :type refresh_token: str

        :return: Dictionary containing the access_token, refresh_token
                 and expires_at (number of seconds since Epoch when the provided access token will expire)
        :rtype: dict
        """
        response = self._request(
            "https://{0}/oauth/token".format(self.server),
            params={
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            },
            method="POST",
        )
        access_info: AccessInfo = {
            "access_token": response["access_token"],
            "refresh_token": response["refresh_token"],
            "expires_at": response["expires_at"],
        }
        self.access_token = response["access_token"]

        return access_info

    def resolve_url(self, url: str) -> str:
        if not url.startswith("http"):
            url = urljoin(
                "https://{0}".format(self.server),
                self.api_base + "/" + url.strip("/"),
            )
        return url

    def _request(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        files: dict[str, SupportsRead[str | bytes]] | None = None,
        method: Literal["GET", "POST", "PUT", "DELETE"] = "GET",
        check_for_errors: bool = True,
    ) -> Any:
        """
        Perform the underlying request, returning the parsed JSON results.

        :param url: The request URL.
        :type url: str

        :param params: Request parameters
        :type params: Dict[str,Any]

        :param files: Dictionary of file name to file-like objects.
        :type files: Dict[str,file]

        :param method: The request method (GET/POST/etc.)
        :type method: str

        :param check_for_errors: Whether to raise
        :type check_for_errors: bool

        :return: The parsed JSON response.
        :rtype: Dict[str,Any]
        """
        url = self.resolve_url(url)
        self.log.info(
            "{method} {url!r} with params {params!r}".format(
                method=method, url=url, params=params
            )
        )
        if params is None:
            params = {}
        if self.access_token:
            params["access_token"] = self.access_token

        methods = {
            "GET": self.rsession.get,
            "POST": functools.partial(self.rsession.post, files=files),
            "PUT": self.rsession.put,
            "DELETE": self.rsession.delete,
        }

        try:
            requester = methods[method.upper()]
        except KeyError:
            raise ValueError(
                "Invalid/unsupported request method specified: {0}".format(
                    method
                )
            )

        raw = requester(url, params=params)  # type: ignore[operator]
        # Rate limits are taken from HTTP response headers
        # https://developers.strava.com/docs/rate-limits/
        self.rate_limiter(raw.headers)

        if check_for_errors:
            self._handle_protocol_error(raw)

        # 204 = No content
        if raw.status_code in [204]:
            resp = {}
        else:
            resp = raw.json()

        return resp

    def _handle_protocol_error(
        self, response: requests.Response
    ) -> requests.Response:
        """
        Parses the raw response from the server, raising a :class:`stravalib.exc.Fault` if the
        server returned an error.

        :param response: The response object.
        :raises Fault: If the response contains an error.
        """
        error_str = None
        try:
            json_response = response.json()
        except ValueError:
            pass
        else:
            if "message" in json_response or "errors" in json_response:
                error_str = "{0}: {1}".format(
                    json_response.get("message", "Undefined error"),
                    json_response.get("errors"),
                )

        # Special subclasses for some errors
        if response.status_code == 404:
            msg = "%s: %s" % (response.reason, error_str)
            raise exc.ObjectNotFound(msg, response=response)
        elif response.status_code == 401:
            msg = "%s: %s" % (response.reason, error_str)
            raise exc.AccessUnauthorized(msg, response=response)
        elif 400 <= response.status_code < 500:
            msg = "%s Client Error: %s [%s]" % (
                response.status_code,
                response.reason,
                error_str,
            )
            raise exc.Fault(msg, response=response)
        elif 500 <= response.status_code < 600:
            msg = "%s Server Error: %s [%s]" % (
                response.status_code,
                response.reason,
                error_str,
            )
            raise exc.Fault(msg, response=response)
        elif error_str:
            msg = error_str
            raise exc.Fault(msg, response=response)

        return response

    def _extract_referenced_vars(self, s: str) -> list[str]:
        """
        Utility method to find the referenced format variables in a string.
        (Assumes string.format() format vars.)
        :param s: The string that contains format variables. (e.g. "{foo}-text")
        :return: The list of referenced variable names. (e.g. ['foo'])
        :rtype: list
        """
        d: dict[str, int] = {}
        while True:
            try:
                s.format(**d)
            except KeyError as exc:
                # exc.args[0] contains the name of the key that was not found;
                # 0 is used because it appears to work with all types of placeholders.
                d[exc.args[0]] = 0
            else:
                break
        return list(d.keys())

    def get(
        self, url: str, check_for_errors: bool = True, **kwargs: Any
    ) -> Any:
        """
        Performs a generic GET request for specified params, returning the response.
        """
        referenced = self._extract_referenced_vars(url)
        url = url.format(**kwargs)
        params = dict(
            [(k, v) for k, v in kwargs.items() if not k in referenced]
        )
        return self._request(
            url, params=params, check_for_errors=check_for_errors
        )

    def post(
        self,
        url: str,
        files: dict[str, SupportsRead[str | bytes]] | None = None,
        check_for_errors: bool = True,
        **kwargs: Any,
    ) -> Any:
        """
        Performs a generic POST request for specified params, returning the response.
        """
        referenced = self._extract_referenced_vars(url)
        url = url.format(**kwargs)
        params = dict(
            [(k, v) for k, v in kwargs.items() if not k in referenced]
        )
        return self._request(
            url,
            params=params,
            files=files,
            method="POST",
            check_for_errors=check_for_errors,
        )

    def put(
        self, url: str, check_for_errors: bool = True, **kwargs: Any
    ) -> Any:
        """
        Performs a generic PUT request for specified params, returning the response.
        """
        referenced = self._extract_referenced_vars(url)
        url = url.format(**kwargs)
        params = dict(
            [(k, v) for k, v in kwargs.items() if not k in referenced]
        )
        return self._request(
            url, params=params, method="PUT", check_for_errors=check_for_errors
        )

    def delete(
        self, url: str, check_for_errors: bool = True, **kwargs: Any
    ) -> Any:
        """
        Performs a generic DELETE request for specified params, returning the response.
        """
        referenced = self._extract_referenced_vars(url)
        url = url.format(**kwargs)
        params = dict(
            [(k, v) for k, v in kwargs.items() if not k in referenced]
        )
        return self._request(
            url,
            params=params,
            method="DELETE",
            check_for_errors=check_for_errors,
        )
