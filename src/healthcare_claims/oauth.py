from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from http.server import (
    BaseHTTPRequestHandler,
    HTTPServer,
)
from urllib.error import (
    HTTPError,
    URLError,
)
from urllib.parse import (
    parse_qs,
    urlencode,
    urlparse,
)
from urllib.request import (
    Request,
    urlopen,
)

import base64
import json
import secrets
import time
import webbrowser

from .config import Settings


class OAuthError(RuntimeError):
    pass


@dataclass(frozen=True)
class TokenSet:

    access_token: str = field(
        repr=False
    )

    refresh_token: str | None = field(
        default=None,
        repr=False,
    )

    token_type: str = "Bearer"
    expires_in: int | None = None
    scope: str = ""
    patient: str | None = None

    @property
    def granted_scopes(
        self,
    ) -> set[str]:

        return set(
            self.scope.split()
        )


def _pkce_pair(
) -> tuple[str, str]:

    verifier = (
        secrets.token_urlsafe(64)
    )

    digest = sha256(
        verifier.encode("ascii")
    ).digest()

    challenge = (
        base64.urlsafe_b64encode(
            digest
        )
        .decode("ascii")
        .rstrip("=")
    )

    return verifier, challenge


def authorize_interactively(
    settings: Settings,
    scopes: list[str],
    timeout_seconds: int = 300,
) -> TokenSet:

    verifier, challenge = (
        _pkce_pair()
    )

    state = (
        secrets.token_urlsafe(32)
    )

    authorization_url = (
        settings.authorize_endpoint
        + "?"
        + urlencode(
            {
                "client_id":
                    settings.client_id,

                "redirect_uri":
                    settings.redirect_uri,

                "response_type":
                    "code",

                "scope":
                    " ".join(scopes),

                "state":
                    state,

                "code_challenge":
                    challenge,

                "code_challenge_method":
                    "S256",
            }
        )
    )

    redirect = urlparse(
        settings.redirect_uri
    )

    port = (
        redirect.port
        or 80
    )

    callback_path = (
        redirect.path
        or "/"
    )

    callback: dict[
        str,
        str | None,
    ] = {}

    class Handler(
        BaseHTTPRequestHandler
    ):

        def log_message(
            self,
            format: str,
            *args,
        ) -> None:
            return

        def do_GET(
            self,
        ) -> None:

            parsed = urlparse(
                self.path
            )

            if (
                parsed.path
                != callback_path
            ):
                self.send_response(
                    404
                )
                self.end_headers()
                return

            query = parse_qs(
                parsed.query
            )

            callback["code"] = (
                query.get(
                    "code",
                    [None],
                )[0]
            )

            callback["state"] = (
                query.get(
                    "state",
                    [None],
                )[0]
            )

            callback["error"] = (
                query.get(
                    "error",
                    [None],
                )[0]
            )

            callback[
                "error_description"
            ] = (
                query.get(
                    "error_description",
                    [None],
                )[0]
            )

            body = (
                "<html><body>"
                "<h2>"
                "CMS Blue Button "
                "authorization received."
                "</h2>"
                "<p>"
                "You may return to "
                "VS Code."
                "</p>"
                "</body></html>"
            ).encode("utf-8")

            self.send_response(
                200
            )

            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8",
            )

            self.send_header(
                "Content-Length",
                str(len(body)),
            )

            self.end_headers()

            self.wfile.write(
                body
            )

    try:
        server = HTTPServer(
            (
                redirect.hostname
                or "localhost",
                port,
            ),
            Handler,
        )

    except OSError as exc:
        raise OAuthError(
            "Cannot start OAuth "
            "callback listener on "
            f"port {port}: {exc}"
        ) from exc

    server.timeout = 1

    webbrowser.open(
        authorization_url,
        new=1,
    )

    deadline = (
        time.time()
        + timeout_seconds
    )

    try:

        while (
            "code" not in callback
            and "error"
                not in callback
            and time.time()
                < deadline
        ):
            server.handle_request()

    finally:
        server.server_close()

    if callback.get("error"):

        description = (
            callback.get(
                "error_description"
            )
            or
            "No description provided"
        )

        raise OAuthError(
            "Authorization failed: "
            f"{callback['error']} "
            f"({description})"
        )

    code = callback.get(
        "code"
    )

    if not code:
        raise OAuthError(
            "Authorization code "
            "was not received "
            "before timeout."
        )

    if (
        callback.get("state")
        != state
    ):
        raise OAuthError(
            "OAuth state "
            "validation failed."
        )

    form = urlencode(
        {
            "code":
                code,

            "grant_type":
                "authorization_code",

            "redirect_uri":
                settings.redirect_uri,

            "code_verifier":
                verifier,
        }
    ).encode("utf-8")

    basic = (
        base64.b64encode(
            (
                f"{settings.client_id}:"
                f"{settings.client_secret}"
            ).encode("utf-8")
        )
        .decode("ascii")
    )

    request = Request(
        settings.token_endpoint,
        data=form,
        method="POST",
        headers={
            "Authorization":
                f"Basic {basic}",

            "Content-Type":
                "application/"
                "x-www-form-urlencoded",

            "Accept":
                "application/json",
        },
    )

    try:

        with urlopen(
            request,
            timeout=60,
        ) as response:

            payload = json.loads(
                response.read()
                .decode("utf-8")
            )

    except HTTPError as exc:
        raise OAuthError(
            "Token exchange failed "
            f"with HTTP {exc.code}."
        ) from exc

    except URLError as exc:
        raise OAuthError(
            "Token endpoint "
            "connection failed: "
            f"{exc.reason}"
        ) from exc

    except json.JSONDecodeError as exc:
        raise OAuthError(
            "Token endpoint "
            "returned invalid JSON."
        ) from exc

    access_token = (
        payload.get(
            "access_token"
        )
    )

    if not access_token:
        raise OAuthError(
            "Token response did "
            "not contain an "
            "access token."
        )

    token = TokenSet(
        access_token=
            access_token,

        refresh_token=
            payload.get(
                "refresh_token"
            ),

        token_type=
            payload.get(
                "token_type",
                "Bearer",
            ),

        expires_in=
            payload.get(
                "expires_in"
            ),

        scope=
            payload.get(
                "scope",
                "",
            ),

        patient=
            payload.get(
                "patient"
            ),
    )

    missing = [
        scope
        for scope in scopes
        if scope
        not in token.granted_scopes
    ]

    if missing:
        raise OAuthError(
            "Required scopes were "
            "not granted: "
            + ", ".join(missing)
        )

    return token
