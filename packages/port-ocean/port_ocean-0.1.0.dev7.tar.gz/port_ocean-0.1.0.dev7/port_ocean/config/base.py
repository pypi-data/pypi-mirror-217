import os
import re
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseSettings

PROVIDER_WRAPPER_PATTERN = r"\{\{ from (.*) \}\}"
PROVIDER_CONFIG_PATTERN = r"^[a-zA-Z0-9]+ .*$"


def read_yaml_config_settings_source(
    settings: "BaseOceanSettings", base_path: str
) -> str:
    """Loads settings from a YAML file at `Config.yaml_file`

    "<file:xxxx>" patterns are replaced with the contents of file xxxx. The root path
    were to find the files is configured with `secrets_dir`.
    """
    yaml_file = getattr(settings.__config__, "yaml_file", "")

    assert yaml_file, "Settings.yaml_file not properly configured"

    path = Path(base_path) / yaml_file

    if not path.exists():
        raise FileNotFoundError(f"Could not open yaml settings file at: {path}")

    return path.read_text("utf-8")


def validate_config_provider_pattern(value: str) -> tuple[str, str]:
    match = re.match(PROVIDER_CONFIG_PATTERN, value)
    if not match:
        raise ValueError(
            f"Invalid pattern: {value}. Pattern should match: {PROVIDER_CONFIG_PATTERN}"
        )

    index = value.find(" ")
    provider_type, provider_value = value[:index], value[index + 1 :]

    return provider_type, provider_value


def load_from_config_provider(provider_type: str, value: str) -> Any:
    if provider_type == "env":
        result = os.environ.get(value)
        if result is None:
            raise ValueError(f"Environment variable not found: {value}")
        return result
    else:
        raise ValueError(f"Invalid provider type: {provider_type}")


def load_providers(settings: "BaseOceanSettings", base_path: str) -> dict[str, Any]:
    value = read_yaml_config_settings_source(settings, base_path)
    matches = re.finditer(PROVIDER_WRAPPER_PATTERN, value)
    for match in matches:
        provider_type, provider_value = validate_config_provider_pattern(match.group(1))
        data = load_from_config_provider(provider_type, provider_value)
        value = re.sub(re.escape(match.group()), data, value, count=1)

    return yaml.safe_load(value)


class BaseOceanSettings(BaseSettings):
    base_path: str

    class Config:
        yaml_file = "./config.yaml"

        @classmethod
        def customise_sources(cls, init_settings, *_, **__):  # type: ignore
            return (
                init_settings,
                lambda s: load_providers(s, init_settings.init_kwargs["base_path"]),
            )
