from chainlit_graphql.model.score import Score as ModelScore
from chainlit_graphql.repository.score import ScoreRepository
from chainlit_graphql.api.v1.graphql.schema.score import ScoreType, Score as SchemaScore
from typing import List, Optional


class ScoreService:
    def __init__(self, score_repository: ScoreRepository):
        self.score_repository = score_repository

    async def add_score(
        self,
        name: str,
        type: ScoreType,
        value: float,
        stepId: Optional[str],
        generationId: Optional[str],
        datasetExperimentItemId: Optional[str],
        comment: Optional[str],
        tags: Optional[List[str]],
    ) -> SchemaScore:

        # Create and save the new Score using the model
        score = await self.score_repository.create(
            ModelScore(
                name=name,
                type=type.value,
                value=value,
                step_id=stepId,
                generation_id=generationId,
                dataset_experiment_item_id=datasetExperimentItemId,
                comment=comment,
                tags=tags,
            )
        )

        # Return a schema Score object
        return SchemaScore(
            id=score.id,
            name=score.name,
            type=score.type,
            value=score.value,
            stepId=score.step_id,
            generationId=score.generation_id,
            datasetExperimentItemId=score.dataset_experiment_item_id,
            comment=score.comment,
            tags=score.tags,
        )

    async def update_score(
        self,
        id: str,
        name: Optional[str],
        type: Optional[ScoreType],
        value: Optional[float],
        stepId: Optional[str],
        generationId: Optional[str],
        datasetExperimentItemId: Optional[str],
        comment: Optional[str],
        tags: Optional[List[str]],
    ) -> SchemaScore:

        # Create the score object with the updates using the model
        score_to_update = ModelScore(
            id=id,
            name=name,
            type=type,
            value=value,
            step_id=stepId,
            generation_id=generationId,
            dataset_experiment_item_id=datasetExperimentItemId,
            comment=comment,
            tags=tags,
        )

        updated_score = await self.score_repository.update(id, score_to_update)

        if updated_score:
            # Return a schema Score object
            return SchemaScore(
                id=updated_score.id,
                name=updated_score.name,
                type=updated_score.type,
                value=updated_score.value,
                stepId=updated_score.step_id,
                generationId=updated_score.generation_id,
                datasetExperimentItemId=updated_score.dataset_experiment_item_id,
                comment=updated_score.comment,
                tags=updated_score.tags,
            )
        else:
            raise ValueError(f"Score with id {id} not found")

    async def delete(self, id: str) -> SchemaScore:

        deleted_score = await self.score_repository.delete(id)

        if deleted_score:
            return SchemaScore(
                id=deleted_score.id,
                name=deleted_score.name,
                type=deleted_score.type,
                value=deleted_score.value,
                stepId=deleted_score.step_id,
                generationId=deleted_score.generation_id,
                datasetExperimentItemId=deleted_score.dataset_experiment_item_id,
                comment=deleted_score.comment,
                tags=deleted_score.tags,
            )
        else:
            return None
