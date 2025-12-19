#!/usr/bin/env python3
"""
Initialize Database Script
Creates all necessary database tables
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import init_db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


if __name__ == "__main__":
    print("🗄️  Initializing database...")
    init_db()
    print("✅ Database initialization complete!")
