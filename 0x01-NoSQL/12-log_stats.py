#!/usr/bin/env python3
"""Log stats"""

from pymongo import MongoClient


def log_stats():
    client = MongoClient('localhost', 27017)
    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})
    print("{} logs".format(total_logs))

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method":method})
        print("\tmethod {}: {}".format(method, count))

    count_status_check = collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(count_status_check))

if __name__ == "__main__":
    log_stats()
