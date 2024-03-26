#!/usr/bin/env python3
"""Where can I learn Python?"""

from pymongo import MongoClient
from typing import List


def schools_by_topic(mongo_collection: MongoClient, topic: str) -> List[object]:
    """
    Returns the list of school having a specific topic
    """
    return mongo_collection.find({"topics": topic})
    