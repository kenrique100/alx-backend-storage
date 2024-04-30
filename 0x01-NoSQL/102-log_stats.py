#!/usr/bin/env python3
"""Log stats"""
from pymongo import MongoClient


def print_logs(logs):
    """
    Print logs
    """
    print(f"{logs.count()} logs")
    print("Methods:")
    print(f"    method GET: {logs.count_documents({'method': 'GET'})}")
    print(f"    method POST: {logs.count_documents({'method': 'POST'})}")
    print(f"    method PUT: {logs.count_documents({'method': 'PUT'})}")
    print(f"    method PATCH: {logs.count_documents({'method': 'PATCH'})}")
    print(f"    method DELETE: {logs.count_documents({'method': 'DELETE'})}")
    print(f"{logs.count_documents({'path': '/status'})} status check")
    print("IPs:")
    ip_counts = logs.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    for ip_count in ip_counts:
        print(f"    {ip_count['_id']}: {ip_count['count']}")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs = client.logs.nginx
    print_logs(logs)
    client.close()
