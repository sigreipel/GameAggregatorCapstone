import os
from django.apps import AppConfig
from pathlib import Path

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        try:
            from RecommendationEngine import placeholder_db  # import from project-level
        except ImportError as e:
            print(f"Placeholder DB import failed: {e}")
            return

        BASE_DIR = Path(__file__).resolve().parent.parent
        DB_PATH = BASE_DIR / "placeholder.db"

        if not DB_PATH.exists():
            print("Running placeholder_db setup...")
            con, cur = placeholder_db.makeConnection(str(DB_PATH))
            placeholder_db.createDB(cur)
            placeholder_db.populateDB(cur, con)
            con.close()
            print("Database created and populated.")
        else:
            print("Database already exists. Skipping creation.")
