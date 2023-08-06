# Copyright (C) 2023 Bootloader.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Bootloader or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Bootloader.
#
# BOOTLOADER MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
# SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR
# A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  BOOTLOADER SHALL NOT BE
# LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF
# USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

import json
from pathlib import Path

import unreal

from bootloader.ue.model.uasset import UAsset


UNREAL_ENGINE_PROJECT_CONTENT_PATH = '/Game/'


def build_asset(asset_data: unreal.AssetData) -> UAsset:
    """
    Return an instance {@link UAsset} from the asset data.


    :param asset_data: The data of the asset returned by the Unreal Engine
        Python API's Asset Registry.


    :return: An instance {@link UAsset}.
    """
    asset_name = asset_data.asset_name
    package_name = asset_data.package_name

    # @note: The property `asset_class` has been deprecated.  The asset
    #     class name must be converted to full asset pathname.
    asset_class = f'{asset_data.asset_class_path.package_name}/{asset_data.asset_class_path.asset_name}'

    # Find the package names of the assets that this asset depends on.
    dependencies = find_asset_dependencies(asset_data)

    # Build the asset instance.
    asset = UAsset(
        str(asset_name),
        str(asset_class),
        str(package_name),
        dependencies
    )

    return asset


def dump_assets(root_path: str or Path) -> str:
    """
    Serialize the assets found in the specified path to JSON formatted
    string.


    :param root_path: The path to the assets.


    :return: A JSON string representing the list of assets.
    """
    assets = find_assets(root_path)
    json_string = json.dumps([asset.to_json() for asset in assets], indent=2)
    return json_string


def find_asset_dependencies(asset_data: unreal.DataAsset):
    """
    Return the list of the package names of assets that the specified
    asset depends on.

    The function excludes any Unreal Engine's assets.  The function only
    includes assets from the game itself.


    :param asset_data: The data of the asset returned by the Unreal Engine
        Python API's Asset Registry.


    :return: A list of the package names of assets.
    """
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    dependency_options = unreal.AssetRegistryDependencyOptions(
        # include_soft_package_references=True,
        # include_hard_package_references=True,
        # include_searchable_names=True,
        # include_soft_management_references=True,
        # include_hard_management_references=True,
    )

    asset_dependencies_package_name = asset_registry.get_dependencies(asset_data.package_name, dependency_options)

    return [
        str(package_name)
        for package_name in asset_dependencies_package_name
        if str(package_name).startswith(UNREAL_ENGINE_PROJECT_CONTENT_PATH)
    ]


def find_assets(content_path: str or Path) -> list[UAsset]:
    """
    Return the list of the assets found recursively in the specified path.


    :param content_path: The path to the assets.


    :return: The list of the assets found in the specified path.
    """
    # Retrieve the list of the paths of the assets found recursively in the
    # specified path.
    asset_paths: list = unreal.EditorAssetLibrary.list_assets(str(content_path), True, False)

    # Build the list of assets.
    #
    # @note: Using list comprehension if faster than `loop` (indeed!):
    #
    #     ```python
    #     assets = []
    #     assets_append = assets.append
    #     for asset_path in asset_paths:
    #         asset_data = unreal.EditorAssetLibrary.find_asset_data(asset_path)
    #         if asset_data.is_valid() and asset_data.is_u_asset():  # @note: Usually always true, but who knows?...
    #             assets_append(build_asset(asset_data))
    #     ```
    #
    #     And faster than `map` when not using a `lambda`:
    #
    #     ```python
    #     assets = list(
    #         filter(
    #             lambda asset: asset is not None,
    #             map(get_asset, asset_paths)
    #         )
    #     )
    #     ```
    #
    #   Result with 1k assets:
    #
    #   - Loop --> 0.6712107429998468
    #   - List comprehension --> 0.05552284200030044
    #   - Map --> 0.20423201099993094
    assets = [
        build_asset(asset_data)
        for asset_data in [
            unreal.EditorAssetLibrary.find_asset_data(asset_path)
            for asset_path in asset_paths
        ]
        if asset_data.is_valid() and asset_data.is_u_asset()
    ]

    return assets


def get_asset(asset_path):
    """
    Return the data of the specified asset.


    :param asset_path: The Unreal Engine path of the asset.


    :return: The asset's data if the asset is valid and is an Unreal
        Engine asset; ``None`` otherwise.
    """
    asset_data = unreal.EditorAssetLibrary.find_asset_data(asset_path)
    if asset_data.is_valid() and asset_data.is_u_asset():
        return build_asset(asset_data)
