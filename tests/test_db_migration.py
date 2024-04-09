import pytest
from sqlalchemy import text
from chainlit_graphql.db.base import drop_all
from chainlit_graphql.db.database import db


@pytest.mark.asyncio
async def test_create_all_and_drop_all():
    # Ensure tables were created (setup by prepare_db)
    async with db.engine.connect() as conn:
        result = await conn.execute(
            text(
                """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """
            )
        )
        tables = {row["table_name"] for row in result.mappings().all()}
        assert "participants" in tables, "Table 'participants' was not created"
        assert "threads" in tables, "Table 'threads' was not created"
        assert "steps" in tables, "Table 'steps' was not created"
        assert "scores" in tables, "Table 'scores' was not created"

    # Now explicitly drop all tables to test the drop_all functionality
    await drop_all()

    # Verify tables were dropped
    async with db.engine.connect() as conn:
        result = await conn.execute(
            text(
                """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """
            )
        )
        tables = {row["table_name"] for row in result.fetchall()}
        assert "participants" not in tables, "Table 'participants' was not dropped"
        assert "threads" not in tables, "Table 'participants' was not dropped"
        assert "steps" not in tables, "Table 'participants' was not dropped"
        assert "scores" not in tables, "Table 'participants' was not dropped"
