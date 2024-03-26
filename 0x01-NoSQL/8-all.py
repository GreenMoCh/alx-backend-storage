#!/usr/bin/env python3
"""List all documents in Python"""

from pymongo import MongoClient
from typing import Iterator


def list_all(mongo_collection: MongoClient) -> Iterator:
    """
    Lists all documents in a collection
    """
    if mongo_collection.count() == 0:
        return []

    return mongo_collection.find()
