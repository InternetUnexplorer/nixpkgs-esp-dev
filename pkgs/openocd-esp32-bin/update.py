#! /usr/bin/env python3

import json
from subprocess import DEVNULL, PIPE, run
from sys import argv
from typing import Dict, List

PLATFORMS = {
    "aarch64-linux": "linux-arm64",
    "x86_64-linux": "linux-amd64",
}


def get_stdout(command: List[str], **kwargs) -> str:
    """Run `command` and return the output."""
    process = run(command, stdout=PIPE, check=True, **kwargs)
    return process.stdout.decode("utf-8")


def get_url_hash(url: str) -> str:
    """Get the SRI hash of `url` using nix-prefetch-url."""
    sha256 = get_stdout(["nix-prefetch-url", url], stderr=DEVNULL).strip()
    return get_stdout(["nix", "hash", "to-sri", "--type", "sha256", sha256]).strip()


def get_artifact(version: str, platform: str) -> Dict[str, str]:
    """Get the URL and SRI hash of a specific release artifact."""
    url = "https://github.com/espressif/openocd-esp32/releases/download"
    url += f"/v{version}"
    url += f"/openocd-esp32-{PLATFORMS[platform]}-{version}.tar.gz"
    print(f"downloading {url}...")
    return {"url": url, "hash": get_url_hash(url)}


def get_all_artifacts(version: str) -> Dict[str, Dict[str, str]]:
    """Run `get_artifact` for every platform."""
    return {platform: get_artifact(version, platform) for platform in PLATFORMS.keys()}


if __name__ == "__main__":
    if len(argv) != 2:
        print(f"Usage: {argv[0]} VERSION")
        print(f"  e.g. {argv[0]} 0.11.0-esp32-20221026")
        exit(1)
    version = argv[1]
    sources = {
        "version": version,
        "artifacts": get_all_artifacts(version),
    }
    with open("sources.json", "w") as file:
        json.dump(sources, file, indent=2)
