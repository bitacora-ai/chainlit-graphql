from chainlit_graphql.model.score import Score
from chainlit_graphql.db.database import db
from sqlalchemy.sql import select
from typing import Optional
import base64


class ScoreRepository:

    @staticmethod
    async def create(score_data: Score) -> Score:
        async with db as session:
            async with session.begin():
                session.add(score_data)
            await session.commit()

            result = await session.execute(
                select(Score).where(Score.id == score_data.id)
            )
            score = result.scalars().one()

            return score

    @staticmethod
    async def update(id: str, model: Score) -> Optional[Score]:
        async with db as session:
            stmt = select(Score).where(Score.id == id)
            result = await session.execute(stmt)
            existing_model = result.scalars().first()

            if existing_model:
                # Update the fields based on the provided model
                existing_model.name = model.name
                existing_model.type = model.type
                existing_model.value = model.value
                existing_model.comment = model.comment
                existing_model.step_id = model.step_id
                existing_model.generation_id = model.generation_id
                existing_model.dataset_experiment_item_id = (
                    model.dataset_experiment_item_id
                )

                await session.commit()
                return existing_model
            else:
                return None

    async def get_by_id(self, id: str, session) -> Optional[Score]:
        try:
            stmt = select(Score).where(Score.id == id)
            result = await session.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            print(f"An error occurred while retrieving the score: {e}")
            await session.rollback()
            raise e

    async def delete(self, score_id: str) -> Optional[str]:
        async for session in db.get_db():
            try:
                # Attempt to decode as base64, assuming encoded format might be 'Score:id'
                try:
                    decoded_id = base64.b64decode(score_id).decode()
                    if ":" in decoded_id:
                        score_id = decoded_id.split(":")[1]
                except (base64.binascii.Error, UnicodeDecodeError):
                    pass  # If decoding fails, assume it's a regular UUID and do nothing

                # Fetch the score to be deleted using a straightforward query
                score_to_delete = await self.get_by_id(score_id, session)

                # If the score exists, delete it
                if score_to_delete:
                    await session.delete(score_to_delete)
                    await session.commit()

                    return score_to_delete  # Return ID of the deleted score
                else:
                    return None  # Or handle the case where the score does not exist

            except Exception as e:
                await session.rollback()
                print(f"An error occurred during deletion: {e}")
                raise e


score_repo = ScoreRepository()
