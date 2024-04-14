from chainlit_graphql.api.v1.graphql.schema.score import Score
from chainlit_graphql.api.v1.graphql.schema.step import (
    AttachmentType,
    GenerationType,
    StepsType,
)
from tenacity import retry, stop_after_attempt, wait_fixed

from typing import Optional, List

import boto3


class MapperUtility:

    @staticmethod
    async def map_scores_to_scoretypes(scores_models) -> List[Score]:

        return [
            Score(
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
            for score in scores_models
        ]

    @staticmethod
    async def map_attachment_to_attachmenttype(attachment_model) -> AttachmentType:
        return AttachmentType(
            id=attachment_model.id,
            threadId=attachment_model.thread_id,
            stepId=attachment_model.step_id,
            metadata=attachment_model.metadata,
            mime=attachment_model.mime,
            name=attachment_model.name,
            objectKey=attachment_model.object_key,
            url=attachment_model.url,
        )

    @staticmethod
    def serialize_generation_payload(generation_payload):
        if generation_payload is None:
            return None
        return {
            "type": generation_payload.type,
            "prompt": generation_payload.prompt,  # Added
            "provider": generation_payload.provider,
            "settings": generation_payload.settings,
            "variables": generation_payload.variables,  # Added
            "stepId": generation_payload.stepId,  # Added
            "inputs": generation_payload.inputs,
            "duration": generation_payload.duration,  # Added
            "model": generation_payload.model,  # Added
            "ttFirstToken": generation_payload.ttFirstToken,  # Added
            "completion": generation_payload.completion,
            "tokenThroughputInSeconds": generation_payload.tokenThroughputInSeconds,  # Added
            "tags": generation_payload.tags,  # Added
            "error": generation_payload.error,  # Added
            "tools": generation_payload.tools,  # Added
            "inputTokenCount": generation_payload.inputTokenCount,  # Added
            "outputTokenCount": generation_payload.outputTokenCount,  # Added
            "messageCompletion": generation_payload.messageCompletion,  # Added
            "templateFormat": generation_payload.templateFormat,
            "template": generation_payload.template,
            "formatted": generation_payload.formatted,
            "messages": generation_payload.messages,
            "tokenCount": generation_payload.tokenCount,
        }

    @staticmethod
    def serialize_attachments_payload(attachments_payload_list):
        if attachments_payload_list is None:
            return None

        serialized_list = []
        for attachments_payload in attachments_payload_list:
            serialized_list.append(
                {
                    "id": attachments_payload.id,
                    "name": attachments_payload.name,
                    "metadata": attachments_payload.metadata,
                    "mime": attachments_payload.mime,
                    "url": attachments_payload.url,
                    "objectKey": attachments_payload.objectKey,
                }
            )

        return serialized_list

    @staticmethod
    def deserialize_generation_payload(json_data) -> Optional[GenerationType]:
        if json_data is None:
            return None
        data = json_data
        return GenerationType(
            type=data.get("type"),
            prompt=data.get("prompt"),  # Added
            provider=data.get("provider"),
            settings=data.get("settings"),
            variables=data.get("variables"),  # Added
            stepId=data.get("stepId"),  # Added
            inputs=data.get("inputs"),
            duration=data.get("duration"),  # Added
            model=data.get("model"),  # Added
            ttFirstToken=data.get("ttFirstToken"),  # Added
            completion=data.get("completion"),
            tokenThroughputInSeconds=data.get("tokenThroughputInSeconds"),  # Added
            tags=data.get("tags"),  # Added
            error=data.get("error"),  # Added
            tools=data.get("tools"),  # Added
            inputTokenCount=data.get("inputTokenCount"),  # Added
            outputTokenCount=data.get("outputTokenCount"),  # Added
            messageCompletion=None, #data.get("messageCompletion"),  # Added
            templateFormat=data.get("templateFormat"),
            template=data.get("template"),
            formatted=data.get("formatted"),
            messages=data.get("messages"),
            tokenCount=data.get("tokenCount"),
        )

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def get_attachment_url(object_key):
        bucket_name = "chatdata-998197354163"
        s3_client = boto3.client("s3", region_name="us-east-2")
        signed_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=3600,
        )
        return signed_url

    @staticmethod
    def deserialize_attachments_payload(
        json_data_list, thread_id, step_id
    ) -> Optional[List[AttachmentType]]:
        if json_data_list is None:
            return None

        attachments = []
        for data in json_data_list:

            object_key = data.get("objectKey")
            url = data.get("url")

            if object_key is not None and url is None:
                url = MapperUtility.get_attachment_url(object_key)

            attachment = AttachmentType(
                id=data.get("id"),
                threadId=thread_id,
                stepId=step_id,
                metadata=data.get("metadata"),
                mime=data.get("mime"),
                name=data.get("name"),
                objectKey=data.get("objectKey"),
                url=url,
            )
            attachments.append(attachment)

        return attachments

    @staticmethod
    async def map_step_to_stepstype(step_model) -> StepsType:
        # Fetch and convert score for the step
        score_type = None
        if step_model.scores:
            score_type = await MapperUtility.map_scores_to_scoretypes(step_model.scores)

        generation_payload = MapperUtility.deserialize_generation_payload(
            step_model.generation
        )

        attachments_payload = MapperUtility.deserialize_attachments_payload(
            step_model.attachments, step_model.thread_id, step_model.id
        )

        # Convert the Step model to StepsType
        return StepsType(
            id=step_model.id,
            thread_id=step_model.thread_id,
            parent_id=step_model.parent_id,
            start_time=step_model.start_time,
            end_time=step_model.end_time,
            createdAt=step_model.createdAt,
            type=step_model.type,
            error=step_model.error,
            input=step_model.input,
            tags=step_model.tags,
            output=step_model.output,
            metadata=step_model.meta_data,
            name=step_model.name,
            scores=score_type,
            generation=generation_payload,
            attachments=attachments_payload,
            ok=True,
            message="Step added successfully",
        )
