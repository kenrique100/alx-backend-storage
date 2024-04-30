#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """
from pymongo import MongoClient

def get_total_logs(collection):
    """Returns the total number of logs"""
    return collection.count_documents({})

def get_method_counts(collection, methods):
    """Returns the count of each HTTP method"""
    method_counts = {}
    for method in methods:
        count = collection.count_documents({"method": method})
        method_counts[method] = count
    return method_counts

def get_status_check_count(collection):
    """Returns the count of status checks"""
    return collection.count_documents({"method": "GET", "path": "/status"})

def get_top_ips(collection, limit=10):
    """Returns the top IPs along with their counts"""
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ])
    return [(ip['_id'], ip['count']) for ip in top_ips]

def print_logs_stats(collection):
    """Prints statistics about Nginx logs"""
    print(f"{get_total_logs(collection)} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    method_counts = get_method_counts(collection, methods)
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")

    status_check_count = get_status_check_count(collection)
    print(f"{status_check_count} status check")

    print("IPs:")
    top_ips = get_top_ips(collection)
    for ip, count in top_ips:
        print(f"\t{ip}: {count}")

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    print_logs_stats(nginx_collection)
    client.close()
