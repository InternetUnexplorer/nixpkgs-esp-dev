#! /usr/bin/env python3

import json
from subprocess import DEVNULL, PIPE, run
from sys import argv
from typing import Dict, List

TARGETS = [
    "riscv32-esp-elf",
    "xtensa-esp32-elf",
    "xtensa-esp32s2-elf",
    "xtensa-esp32s3-elf",
]

PLATFORMS = {
    "aarch64-linux": "linux-arm64",
    "i686-linux": "linux-i686",
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


def get_artifact(
    version: str, gcc_version: str, target: str, platform: str
) -> Dict[str, str]:
    """Get the URL and SRI hash of a specific release artifact."""
    gcc_version = gcc_version.replace(".", "_")
    url = "https://github.com/espressif/crosstool-NG/releases/download"
    url += f"/esp-{version}"
    url += f"/{target}-gcc{gcc_version}-esp-{version}-{PLATFORMS[platform]}.tar.xz"
    print(f"downloading {url}...")
    return {"url": url, "hash": get_url_hash(url)}


def get_target_artifacts(
    version: str, gcc_version: str, target: str
) -> Dict[str, Dict[str, str]]:
    """Run `get_artifact` for every platform with a specific target."""
    return {
        platform: get_artifact(version, gcc_version, target, platform)
        for platform in PLATFORMS.keys()
    }


def get_all_artifacts(
    version: str, gcc_version: str
) -> Dict[str, Dict[str, Dict[str, str]]]:
    """Run `get_target_artifact` for every target."""
    return {
        target: get_target_artifacts(version, gcc_version, target) for target in TARGETS
    }


if __name__ == "__main__":
    if len(argv) != 3:
        print(f"Usage: {argv[0]} VERSION GCC-VERSION")
        print(f"  e.g. {argv[0]} 2022r1 11.2.0")
        exit(1)
    version, gcc_version = argv[1], argv[2]
    sources = {
        "version": version,
        "gcc_version": gcc_version,
        "artifacts": get_all_artifacts(version, gcc_version),
    }
    with open("sources.json", "w") as file:
        json.dump(sources, file, indent=2)
