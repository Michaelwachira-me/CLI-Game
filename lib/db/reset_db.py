#!/usr/bin/env python3

import os
import subprocess
import sys

DB_FILE = "gaia.db"

def remove_old_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Removed old database: {DB_FILE}")
    else:
        print(f"No existing database found.")

def run_migrations():
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Alembic migrations applied.")
    except subprocess.CalledProcessError:
        print("Failed to apply migrations.")
        sys.exit(1)

def seed_database():
    try:
        # Set PYTHONPATH so imports like `lib.models` work
        subprocess.run(["python3", "lib/db/seed.py"], check=True, env={**os.environ, "PYTHONPATH": "."})
        print("Database seeded successfully.")
    except subprocess.CalledProcessError:
        print("Failed to seed the database.")
        sys.exit(1)

if __name__ == "__main__":
    remove_old_db()
    run_migrations()
    seed_database()
