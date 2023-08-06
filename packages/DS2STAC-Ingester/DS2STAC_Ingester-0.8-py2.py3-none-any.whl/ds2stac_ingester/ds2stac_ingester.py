"""Main module."""


import json
import os

from pypgstac.db import PgstacDB
from pypgstac.load import Loader, Methods

from . import config_pgstac


class Ingester(object):
    def __init__(self, stac_dir, API_posting):
        if API_posting is False:
            """With enabling 'stac_catalog_dynamic' STAC catalogs
            , collections and items ingest into the 'pgSTAC'"""

            config_pgstac.run_all()  # This enables the confiduration of pgSTAC
            # First of all catalog should be opened
            f = open(os.path.join(stac_dir, "stac/catalog.json"))
            catalog_json = json.load(f)
            # pgSTAC database will be loaded here
            loader = Loader(db=PgstacDB(dsn=""))
            # Each collection and item that are linked to the catalog through 'links' is extracted.
            for dc in catalog_json["links"]:
                # if dc["rel"] == "item":
                #     try:
                #         loader.load_items(
                #             str(
                #                 os.path.join(
                #                     stac_dir,
                #                     "stac/" + dc["href"].replace("./", ""),
                #                 )
                #             ),
                #             Methods.insert,
                #         )
                #     except:
                #         continue
                #     print("|____", dc["href"])

                # 'child' means Collection in Catalog json file
                if dc["rel"] == "child":
                    self.ingest(
                        loader,
                        dc["href"],
                        stac_dir,
                        "stac/" + dc["href"].replace("./", ""),
                    )

    def ingest(self, loaderx, param, stac_dirx, address_coll):
        """This is a function for ingesting collections
        into pgSTAC specifically for nested datasets"""

        f = open(os.path.join(stac_dirx, address_coll))
        collection_josn_path = os.path.join(stac_dirx, address_coll)
        collection_josn_data = json.load(f)

        item_collection_list = [
            ci["rel"] for ci in collection_josn_data["links"]
        ]

        if (
            "child" in item_collection_list
        ):  # To ensure collection exists in 'links'
            item_collection_list = []  # Considered empty to prevent recursion

            for ci in collection_josn_data["links"]:
                if ci["rel"] == "child":
                    try:
                        self.dynamic_ingester(
                            loaderx,
                            ci["href"],
                            stac_dirx,
                            collection_josn_path.replace(
                                "collection.json", "/"
                            )
                            + ci["href"].replace("./", ""),
                        )
                    except Exception as e:
                        print(e)
                        continue
        else:
            item_collection_list = []  # Considered empty to prevent recursion
            loaderx.load_collections(
                str(os.path.join(stac_dirx, collection_josn_path)),
                Methods.insert,
            )
            print(param)
            for ci in collection_josn_data["links"]:
                if ci["rel"] == "item":
                    try:
                        loaderx.load_items(
                            str(
                                os.path.join(
                                    stac_dirx,
                                    collection_josn_path.replace(
                                        "collection.json", "/"
                                    )
                                    + ci["href"].replace("./", ""),
                                )
                            ),
                            Methods.insert,
                        )
                        print("|____", ci["href"])
                    except Exception as e:
                        print(e)
                        continue
