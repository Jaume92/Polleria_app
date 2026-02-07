import sys
import os

# Add parent directory to path so we can import polleria_app package
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from polleria_app.database.db import init_db

if __name__ == "__main__":
    print("Resetting database...")
    init_db()
    print("Database reset complete.")
