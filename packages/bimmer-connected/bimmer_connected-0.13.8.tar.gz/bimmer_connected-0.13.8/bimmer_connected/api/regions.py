"""Get the right url for the different countries."""
from base64 import b64decode
from typing import List

from bimmer_connected.const import APP_VERSIONS, OCP_APIM_KEYS, SERVER_URLS_MYBMW, Regions


def valid_regions() -> List[str]:
    """Get list of valid regions as strings."""
    return [region.name.lower() for region in Regions]


def get_region_from_name(name: str) -> Regions:
    """Get a region for a string.

    This function is not case-sensitive.
    """
    for region in Regions:
        if name.lower() == region.name.lower():
            return region
    raise ValueError(f"Unknown region {name}. Valid regions are: {','.join(valid_regions())}")


def get_server_url(region: Regions) -> str:
    """Get the url of the server for the region."""
    return f"https://{SERVER_URLS_MYBMW[region]}"


def get_app_version(region: Regions) -> str:
    """Get the app version & build number for the region."""
    return APP_VERSIONS[region]


def get_ocp_apim_key(region: Regions) -> str:
    """Get the authorization for OAuth settings."""
    return b64decode(OCP_APIM_KEYS[region]).decode()
