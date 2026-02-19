import os
import sys
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, BulkWriteError
from dotenv import load_dotenv


def get_mongo_client(uri: str) -> MongoClient:
    """
    Create and return a MongoDB client.
    """
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # Trigger connection check
        client.admin.command("ping")
        print("✅ Successfully connected to MongoDB.")
        return client
    except ConnectionFailure as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        sys.exit(1)


def read_csv_file(file_path: str) -> pd.DataFrame:
    """
    Read CSV file into a pandas DataFrame.
    """
    if not os.path.exists(file_path):
        print(f"❌ CSV file not found: {file_path}")
        sys.exit(1)

    try:
        df = pd.read_csv(file_path)
        print(f"📄 CSV loaded successfully. Rows: {len(df)}")
        return df
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        sys.exit(1)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning:
    - Replace NaN with None (MongoDB compatible)
    """
    df = df.where(pd.notnull(df), None)
    return df


def insert_into_mongo(client: MongoClient, db_name: str, collection_name: str, df: pd.DataFrame):
    """
    Insert DataFrame into MongoDB collection.
    """
    db = client[db_name]
    collection = db[collection_name]

    records = df.to_dict(orient="records")

    if not records:
        print("⚠️ No records to insert.")
        return

    try:
        result = collection.insert_many(records)
        print(f"🚀 Inserted {len(result.inserted_ids)} documents into '{collection_name}'.")
    except BulkWriteError as bwe:
        print(f"❌ Bulk write error: {bwe.details}")
    except Exception as e:
        print(f"❌ Unexpected error during insert: {e}")


def main():
    """
    Main execution function.
    Usage:
        python csv_to_mongo.py <csv_path> <database_name> <collection_name>
    """
    if len(sys.argv) != 4:
        print("Usage: python csv_to_mongo.py <csv_path> <database_name> <collection_name>")
        sys.exit(1)

    csv_path = sys.argv[1]
    db_name = sys.argv[2]
    collection_name = sys.argv[3]

    # Load environment variables
    load_dotenv()

    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        print("❌ MONGO_URI not found in environment variables.")
        sys.exit(1)

    client = get_mongo_client(mongo_uri)
    df = read_csv_file(csv_path)
    df = clean_dataframe(df)

    insert_into_mongo(client, db_name, collection_name, df)


if __name__ == "__main__":
    main()