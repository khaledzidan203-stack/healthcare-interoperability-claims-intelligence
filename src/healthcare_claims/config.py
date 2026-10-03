from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse


class ConfigError(ValueError):
    pass


def _read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}

    for raw in path.read_text(
        encoding="utf-8-sig"
    ).splitlines():

        line = raw.strip()

        if (
            not line
            or line.startswith("#")
            or "=" not in line
        ):
            continue

        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()

    return values


@dataclass(frozen=True)
class Settings:
    client_id: str

    client_secret: str = field(
        repr=False
    )

    redirect_uri: str
    api_version: str
    base_url: str

    @property
    def authorize_endpoint(self) -> str:
        return (
            f"{self.base_url}/"
            f"{self.api_version}/o/authorize/"
        )

    @property
    def token_endpoint(self) -> str:
        return (
            f"{self.base_url}/"
            f"{self.api_version}/o/token/"
        )

    @property
    def fhir_base_url(self) -> str:
        return (
            f"{self.base_url}/"
            f"{self.api_version}/fhir"
        )

    def validate(self) -> None:

        if not self.client_id:
            raise ConfigError(
                "CMS Blue Button Client ID is missing."
            )

        if not self.client_secret:
            raise ConfigError(
                "CMS Blue Button Client Secret is missing."
            )

        if self.api_version != "v3":
            raise ConfigError(
                "This implementation is validated "
                "for CMS Blue Button v3."
            )

        base = urlparse(self.base_url)

        if (
            base.scheme != "https"
            or not base.netloc
        ):
            raise ConfigError(
                "Sandbox base URL must be an "
                "absolute HTTPS URL."
            )

        redirect = urlparse(
            self.redirect_uri
        )

        if (
            redirect.scheme != "http"
            or redirect.hostname
            not in {
                "localhost",
                "127.0.0.1",
            }
        ):
            raise ConfigError(
                "Redirect URI must use local "
                "HTTP localhost/127.0.0.1."
            )

        if (
            redirect.query
            or redirect.fragment
        ):
            raise ConfigError(
                "Redirect URI must not contain "
                "query parameters or fragments."
            )


def load_settings(
    project_root: Path,
) -> Settings:

    env_path = project_root / ".env"

    if not env_path.exists():
        raise ConfigError(
            f"Missing local credential file: "
            f"{env_path}"
        )

    values = _read_env_file(
        env_path
    )

    required = [
        "CMS_BLUEBUTTON_CLIENT_ID",
        "CMS_BLUEBUTTON_CLIENT_SECRET",
        "CMS_BLUEBUTTON_REDIRECT_URI",
        "CMS_BLUEBUTTON_API_VERSION",
        "CMS_BLUEBUTTON_SANDBOX_BASE_URL",
    ]

    missing = [
        key
        for key in required
        if not values.get(key)
    ]

    if missing:
        raise ConfigError(
            "Missing required .env values: "
            + ", ".join(missing)
        )

    settings = Settings(
        client_id=
            values[
                "CMS_BLUEBUTTON_CLIENT_ID"
            ],

        client_secret=
            values[
                "CMS_BLUEBUTTON_CLIENT_SECRET"
            ],

        redirect_uri=
            values[
                "CMS_BLUEBUTTON_REDIRECT_URI"
            ],

        api_version=
            values[
                "CMS_BLUEBUTTON_API_VERSION"
            ],

        base_url=
            values[
                "CMS_BLUEBUTTON_SANDBOX_BASE_URL"
            ].rstrip("/"),
    )

    settings.validate()

    return settings
