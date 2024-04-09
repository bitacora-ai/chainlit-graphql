from datetime import datetime, timedelta, timezone
from chainlit_graphql.api.v1.graphql.schema.score import ScoreType
from chainlit_graphql.model.score import Score
from chainlit_graphql.model.step import Step
import pytest
from chainlit_graphql.db.database import db
from chainlit_graphql.repository.score import score_repo


@pytest.mark.asyncio
async def test_create_score(prepare_db):
    async with db.SessionLocal():
        score_data = Score(
            id="score-1",
            name="Test Score",
            type=ScoreType.AI.value,
            value=5.0,
            comment="Excellent performance",
        )
        created_score = await score_repo.create(score_data)
        assert created_score.id == score_data.id
        assert created_score.name == score_data.name
        assert created_score.type == ScoreType.AI.value
        assert created_score.value == score_data.value
        assert created_score.comment == score_data.comment


@pytest.mark.asyncio
async def test_update_score(prepare_db):
    async with db.SessionLocal() as session:
        score_data = Score(
            id="score-2",
            name="Initial Test Score",
            type=ScoreType.HUMAN.value,
            value=3.0,
            comment="Good performance",
        )
        session.add(score_data)
        await session.commit()

        updated_model = Score(
            id="score-2",
            name="Updated Test Score",
            comment="Updated excellent performance",
            value=4.5,
            type=ScoreType.AI.value,
        )
        updated_score = await score_repo.update("score-2", updated_model)
        assert updated_score.id == updated_model.id
        assert updated_score.name == updated_model.name
        assert updated_score.type == ScoreType.AI.value
        assert updated_score.value == updated_model.value
        assert updated_score.comment == updated_model.comment


@pytest.mark.asyncio
async def test_create_and_fetch_score(prepare_db):
    # Establish a database session and insert test data
    async with db.SessionLocal() as session:
        utc_now = datetime.now(timezone.utc).replace(tzinfo=None)

        # Setup test Step
        step = Step(
            id="step-123",
            start_time=utc_now - timedelta(hours=1),
            end_time=utc_now,
            name="Test Step",
            createdAt=utc_now,
        )

        # Setup test Score associated with the Step
        score = Score(
            id="score-1",
            name="Test Score",
            type="Test Type",
            value=88.5,
            comment="Well done",
            step_id="step-123",  # Linking to the Step created above
            createdAt=utc_now,
        )

        session.add_all([step, score])
        await session.commit()

        # Fetch the inserted Score by ID using the repository method
        fetched_score = await score_repo.get_by_id("score-1", session)

        # Assertions to verify that the fetched data matches the inserted data
        assert fetched_score is not None, "Score not found by ID"
        assert fetched_score.id == "score-1", "Fetched Score ID mismatch"
        assert fetched_score.step_id == "step-123", "Score's Step ID mismatch"
        assert fetched_score.value == 88.5, "Score value mismatch"


@pytest.mark.asyncio
async def test_delete_score(prepare_db):
    # Setup the environment
    async with db.SessionLocal() as session:
        utc_now = datetime.now(timezone.utc).replace(tzinfo=None)

        # Setup test Step and Score
        step = Step(
            id="step-123",
            start_time=utc_now - timedelta(hours=1),
            end_time=utc_now,
            name="Test Step",
            createdAt=utc_now,
        )
        score = Score(
            id="score-3",
            name="Test Score",
            type="Test Type",
            value=88.5,
            comment="Well done",
            step_id="step-123",  # Linking to the Step created above
            createdAt=utc_now,
        )
        session.add_all([step, score])
        await session.commit()

        # Ensure the score is created
        created_score = await session.get(Score, "score-3")
        assert created_score is not None, "Score should exist before deletion"

        # Perform the delete operation
        deleted_score = await score_repo.delete("score-3")

        # Check the result of the delete operation
        assert (
            deleted_score is not None
        ), "Delete operation should return the deleted Score object"
        assert (
            deleted_score.id == "score-3"
        ), "Deleted Score ID should match the requested ID"

        # Manually evict the deleted object from the session to ensure fresh retrieval from the DB
        session.expire_all()

        # Ensure the score is actually deleted
        deleted_score_check = await session.get(Score, "score-3")
        assert deleted_score_check is None, "Score should not exist after deletion"
