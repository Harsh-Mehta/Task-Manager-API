from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_PATH / "db"

# SQLite database URL
PROD_DATABASE_URL = f"sqlite:///{DATABASE_PATH}/task_manager.db"
TEST_DATABASE_URL = f"sqlite:///{DATABASE_PATH}/task_manager_test.db"
