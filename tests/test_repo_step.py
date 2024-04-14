from chainlit_graphql.api.v1.graphql.schema.step import AttachmentPayloadInput, GenerationPayloadInput
from chainlit_graphql.core.mappers import MapperUtility
import pytest
from chainlit_graphql.db.database import db
from chainlit_graphql.repository.step import step_repo
from chainlit_graphql.model import Thread, Step
from datetime import datetime, timedelta, timezone


@pytest.mark.asyncio
async def test_upsert_step_insert(prepare_db):
    async with db.SessionLocal() as session:
        thread_id = "test-thread-id"
        now = datetime.now(timezone.utc)
        new_thread = Thread(id=thread_id, name="Test Thread", createdAt=now)
        session.add(new_thread)
        await session.commit()

        step_id = "test-step-id"
        start_time = now
        end_time = now + timedelta(hours=1)
        step_type = "Normal"
        error = None
        input_data = {"input_key": "input_value"}
        output_data = {"output_key": "output_value"}
        metadata = {"metadata_key": "metadata_value"}
        tags = ["initial_tag"]
        parent_id = None
        name = "Initial Step"
        
        generation = GenerationPayloadInput(
            type="ExampleType",
            prompt="Example prompt",
            settings={"setting_key": "setting_value"},
            inputs={"input_key": "input_value"}
        )
        
        attachments = [
            AttachmentPayloadInput(
                id="attachment-1",
                metadata={"size": "2MB"},  # Example metadata
                mime="image/jpeg",
                name="example.jpeg",
                objectKey="path/to/example.jpeg",
                url="http://example.com/path/to/example.jpeg"
            )
        ]

        await step_repo.upsert_step(
            id=step_id,
            threadId=thread_id,
            startTime=start_time,
            endTime=end_time,
            type=step_type,
            error=error,
            input=input_data,
            output=output_data,
            metadata=metadata,
            parentId=parent_id,
            name=name,
            tags=tags,
            generation=generation,
            attachments=attachments,
        )

        async with db.SessionLocal() as session:
            inserted_step = await session.get(Step, step_id)
            inserted_step.generation = MapperUtility.deserialize_generation_payload(inserted_step.generation)
            inserted_step.attachments = MapperUtility.deserialize_attachments_payload(inserted_step.attachments, thread_id, step_id)

            assert inserted_step is not None
            assert inserted_step.thread_id == thread_id
            assert inserted_step.start_time == start_time
            assert inserted_step.end_time == end_time
            assert inserted_step.type == step_type
            assert inserted_step.error == error
            assert inserted_step.input == input_data
            assert inserted_step.output == output_data
            assert inserted_step.meta_data == metadata
            assert inserted_step.tags == tags
            assert inserted_step.parent_id == parent_id
            assert inserted_step.name == name
            assert inserted_step.generation.type == "ExampleType"
            assert inserted_step.attachments[0].name == "example.jpeg"

@pytest.mark.asyncio
async def test_upsert_step_update(prepare_db):
    async with db.SessionLocal() as session:
        thread_id = "test-thread-id-update"
        now = datetime.now(timezone.utc)
        new_thread = Thread(id=thread_id, name="Test Thread for Update", createdAt=now)
        session.add(new_thread)

        step_id = "test-step-id-update"
        new_step = Step(
            id=step_id,
            thread_id=thread_id,
            name="Step Before Update",
            meta_data={"key": "value"},
            createdAt=now,
            tags=["old_tag"],
            start_time=now - timedelta(hours=1),
            end_time=now,
            type="Basic",
            input={"old_input_key": "old_input_value"},
            output={"old_output_key": "old_output_value"},
        )
        session.add(new_step)
        await session.commit()

        updated_name = "Step After Update"
        updated_metadata = {"key": "updated"}
        updated_tags = ["new_tag"]
        updated_start_time = now
        updated_end_time = now + timedelta(hours=1)
        updated_type = "Advanced"
        updated_input = {"new_input_key": "new_input_value"}
        updated_output = {"new_output_key": "new_output_value"}

        await step_repo.upsert_step(
            id=step_id,
            threadId=thread_id,
            startTime=updated_start_time,
            endTime=updated_end_time,
            type=updated_type,
            input=updated_input,
            output=updated_output,
            metadata=updated_metadata,
            name=updated_name,
            tags=updated_tags,
        )

        async with db.SessionLocal() as session:
            session.expire_all()
            updated_step = await session.get(Step, step_id)
            assert updated_step is not None
            assert updated_step.name == updated_name
            assert updated_step.meta_data == updated_metadata
            assert updated_step.tags == updated_tags
            assert updated_step.start_time == updated_start_time
            assert updated_step.end_time == updated_end_time
            assert updated_step.type == updated_type
            assert updated_step.input == updated_input
            assert updated_step.output == updated_output
