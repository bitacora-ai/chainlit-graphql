import pytest
from unittest.mock import patch
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from chainlit_graphql.db.base import create_all, drop_all
from chainlit_graphql.db.database import DatabaseSession, db
import subprocess
import time

TEST_DB_URL = "postgresql+asyncpg://postgres:admin@localhost:5433/test_db"


@pytest.fixture(autouse=True)
async def prepare_db():
    # Patch the __init__ method of DatabaseSession to use the TEST_DB_URL
    with patch.object(DatabaseSession, "__init__", lambda self, url=TEST_DB_URL: None):
        # Manually initialize the engine within the patched __init__
        db.engine = create_async_engine(TEST_DB_URL, echo=False)
        db.SessionLocal = sessionmaker(
            bind=db.engine, class_=AsyncSession, expire_on_commit=False
        )

        # Ensure the database is in a clean state before each test
        await drop_all()
        await create_all()

        yield

        # Cleanup database after each test
        await drop_all()


@pytest.fixture(scope="session", autouse=True)
def docker_db():
    try:
        subprocess.run(["docker-compose", "up", "-d"], check=True)

        max_attempts = 10
        attempt = 0
        container_ready = False
        container_name = "tests-db-1"

        while attempt < max_attempts and not container_ready:
            print(
                f"Checking if the container is ready (Attempt {attempt + 1}/{max_attempts})..."
            )
            result = subprocess.run(
                [
                    "docker",
                    "ps",
                    "--filter",
                    "status=running",
                    "--format",
                    "{{.Names}}",
                ],
                capture_output=True,
                text=True,
            )
            print(result.stdout)  # Print the output for debugging
            if container_name in result.stdout:
                print("Container is running. Verifying database readiness...")
                db_check_result = subprocess.run(
                    ["docker", "exec", container_name, "pg_isready", "-h", "db"],
                    capture_output=True,
                    text=True,
                )
                print(db_check_result.stdout)  # Print the output for debugging
                if "accepting connections" in db_check_result.stdout:
                    container_ready = True
                    print("Database is ready.")
                else:
                    print("Database is not ready yet.")
            else:
                print("Container is not up yet.")

            if not container_ready:
                time.sleep(3)
                attempt += 1

        if not container_ready:
            raise Exception("Container did not become ready in time")

    except Exception as e:
        print(f"An error occurred while setting up the Docker database: {e}")
        raise

    yield

    subprocess.run(["docker-compose", "down"], check=True)
