#!/usr/bin/env python3
"""Insert a document in Python"""

from pymongo import MongoClient
from typing import Mapping


def insert_school(mongo_collection: MongoClient, **kwargs: Mapping[str, str]) -> str:
    """
    Inserts a new document in a collection based on kwargs
    """
    return mongo_collection.insert_one(kwargs).insert_id
    