"""Stream type classes for tap-zoho-inventory."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_zoho_inventory.client import ZohoInventoryStream


class ItemsStream(ZohoInventoryStream):
    """Define custom stream."""

    name = "items"
    path = "/items"
    primary_keys = ["item_id"]
    replication_key = "last_modified_time"
    schema = th.PropertiesList(
        th.Property("item_id", th.StringType, description="The item's system ID"),
        th.Property("name", th.StringType, description="The item's name"),
        th.Property("item_name", th.StringType, description="The item's name"),
        th.Property("unit", th.StringType, description="The unit of measurement for the item"),
        th.Property("status", th.StringType, description="The status of the item"),
        th.Property("source", th.StringType, description="The source of the item"),
        th.Property("is_combo_product", th.BooleanType, description="Indicates if the item is a combo product"),
        th.Property("is_linked_with_zohocrm", th.BooleanType, description="Indicates if the item is linked with Zoho CRM"),
        th.Property("zcrm_product_id", th.StringType, description="The Zoho CRM product ID"),
        th.Property("description", th.StringType, description="The description of the item"),
        th.Property("brand", th.StringType, description="The brand of the item"),
        th.Property("manufacturer", th.StringType, description="The manufacturer of the item"),
        th.Property("rate", th.NumberType, description="The rate of the item"),
        th.Property("tax_id", th.StringType, description="The tax ID of the item"),
        th.Property("tax_name", th.StringType, description="The tax name of the item"),
        th.Property("tax_percentage", th.NumberType, description="The tax percentage applied to the item"),
        th.Property("purchase_account_id", th.StringType, description="The purchase account ID of the item"),
        th.Property("purchase_account_name", th.StringType, description="The purchase account name of the item"),
        th.Property("account_id", th.StringType, description="The account ID of the item"),
        th.Property("account_name", th.StringType, description="The account name of the item"),
        th.Property("purchase_description", th.StringType, description="The purchase description of the item"),
        th.Property("purchase_rate", th.NumberType, description="The purchase rate of the item"),
        th.Property("item_type", th.StringType, description="The type of the item"),
        th.Property("product_type", th.StringType, description="The type of product"),
        th.Property("is_taxable", th.BooleanType, description="Indicates if the item is taxable"),
        th.Property("tax_exemption_id", th.StringType, description="The tax exemption ID of the item"),
        th.Property("tax_exemption_code", th.StringType, description="The tax exemption code of the item"),
        th.Property("has_attachment", th.BooleanType, description="Indicates if the item has an attachment"),
        th.Property("is_returnable", th.BooleanType, description="Indicates if the item is returnable"),
        th.Property("sku", th.StringType, description="The SKU (stock keeping unit) of the item"),
        th.Property("upc", th.StringType, description="The UPC (universal product code) of the item"),
        th.Property("ean", th.StringType, description="The EAN (European article number) of the item"),
        th.Property("isbn", th.StringType, description="The ISBN (International Standard Book Number) of the item"),
        th.Property("part_number", th.StringType, description="The part number of the item"),
        th.Property("image_name", th.StringType, description="The name of the item's image"),
        th.Property("image_type", th.StringType, description="The type of the item's image"),
        th.Property("image_document_id", th.StringType, description="The document ID of the item's image"),
        th.Property("created_time", th.StringType, description="The timestamp when the item was created"),
        th.Property("last_modified_time", th.StringType, description="The timestamp when the item was last modified"),
        th.Property("show_in_storefront", th.BooleanType, description="Indicates if the item should be shown in the storefront"),
        th.Property("length", th.StringType, description="The length of the item"),
        th.Property("width", th.StringType, description="The width of the item"),
        th.Property("height", th.StringType, description="The height of the item"),
        th.Property("weight", th.StringType, description="The weight of the item"),
        th.Property("weight_unit", th.StringType, description="The unit of measurement for weight"),
        th.Property("dimension_unit", th.StringType, description="The unit of measurement for dimensions"),
    ).to_dict()
