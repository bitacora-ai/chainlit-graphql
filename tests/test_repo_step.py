import pytest
from chainlit_graphql.db.database import db
from chainlit_graphql.repository.step import step_repo
from chainlit_graphql.model import Thread, Step
from datetime import datetime, timezone


@pytest.mark.asyncio
async def test_upsert_step_integrity_error(prepare_db):
    # Setup: Ensure the test database and session are prepared
    async with db.SessionLocal() as session:
        thread_id = "test-thread-integrity"
        step_id = "test-step-integrity"
        step_name = "Step Name"

        # Create and insert a Thread first to satisfy the foreign key constraint
        new_thread = Thread(
            id=thread_id,
            name="Test Thread for Integrity",
            createdAt=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        session.add(new_thread)
        await session.commit()

        # Directly insert a Step with the same id to simulate a race condition
        new_step = Step(
            id=step_id,
            thread_id=thread_id,
            name="Existing Step",
            createdAt=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        session.add(new_step)
        await session.commit()

    # Now, attempt to upsert the same Step, simulating a concurrent operation that isn't aware of the existing record
    async def upsert_attempt(step_id, thread_id, name):
        try:
            await step_repo.upsert_step(id=step_id, threadId=thread_id, name=name)
        except Exception as e:
            print(f"Exception caught during upsert: {e}")

    await upsert_attempt(step_id, thread_id, step_name)

    # Verify the outcome - In this case, the upsert_attempt should either succeed in updating the existing step or raise an IntegrityError
    async with db.SessionLocal() as session:
        session.expire_all()  # Refresh session view
        updated_step = await session.get(Step, step_id)
        assert updated_step is not None
        assert (
            updated_step.name == step_name
        )  # Assuming the upsert successfully updated the existing record


@pytest.mark.asyncio
async def test_upsert_step_insert(prepare_db):
    # Setup: Ensure the test database and session are prepared
    async with db.SessionLocal() as session:
        # Create and insert a Thread first to satisfy the foreign key constraint
        thread_id = "test-thread-id"
        new_thread = Thread(
            id=thread_id,
            name="Test Thread",
            createdAt=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        session.add(new_thread)
        await session.commit()

        # Now attempt to insert a new Step with the existing thread_id
        step_id = "test-step-id"
        # Adjust the call to match the method signature
        await step_repo.upsert_step(id=step_id, threadId=thread_id, name="Initial Step")

        # Verify the Step was inserted
        inserted_step = await session.get(Step, step_id)
        assert inserted_step is not None
        assert inserted_step.thread_id == thread_id


@pytest.mark.asyncio
async def test_upsert_step_update(prepare_db):
    # Similar setup as the insert test, ensure a Step exists first
    async with db.SessionLocal() as session:
        thread_id = "test-thread-id-update"
        new_thread = Thread(
            id=thread_id,
            name="Test Thread for Update",
            createdAt=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        session.add(new_thread)
        step_id = "test-step-id-update"
        new_step = Step(
            id=step_id,
            thread_id=thread_id,
            name="Step Before Update",
            meta_data={"key": "value"},
            createdAt=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        session.add(new_step)
        await session.commit()

        # Now attempt to update the existing Step
        updated_name = "Step After Update"
        # Adjust the call to match the method signature
        await step_repo.upsert_step(
            id=step_id, threadId=thread_id, name=updated_name, metadata={"key": "value"}
        )
        session.expire_all()
        # Verify the Step was updated
        updated_step = await session.get(Step, step_id)
        assert updated_step is not None
        assert updated_step.name == updated_name
