"""Functions for finding FAST-HEP software"""
from __future__ import annotations

from typing import Callable, Iterator

import pkg_resources


def __find_package_versions(
    filter_function: Callable[[str], bool]
) -> Iterator[tuple[str, str]]:
    """
    Find the versions of a list of packages
    """
    installed_packages = list(pkg_resources.working_set)
    for installed_package in installed_packages:
        if filter_function(installed_package.key):
            yield installed_package.key, installed_package.version


def _find_package_versions(package_names: list[str]) -> list[tuple[str, str]]:
    """
    Find the versions of a list of packages
    """
    return sorted(list(__find_package_versions(lambda x: x in package_names)))


def _is_fasthep_package(package_name: str) -> bool:
    """
    Check if a package is a FAST-HEP package
    """
    fast_hep_prefixes = ["fasthep-", "fast-", "scikit-validate"]
    for prefix in fast_hep_prefixes:
        if package_name.startswith(prefix):
            return True
    return False


def _find_fast_hep_packages() -> list[tuple[str, str]]:
    """
    Find all FAST-HEP packages
    """
    return list(__find_package_versions(_is_fasthep_package))
