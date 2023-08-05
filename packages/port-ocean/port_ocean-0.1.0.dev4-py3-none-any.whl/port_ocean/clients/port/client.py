from datetime import datetime
from typing import Any

import httpx as httpx
from loguru import logger
from pydantic import BaseModel, Field, PrivateAttr

from port_ocean.clients.port.types import (
    KafkaCreds,
    RequestOptions,
    UserAgentType,
)
from port_ocean.core.models import Entity, Blueprint
from port_ocean.exceptions.clients import KafkaCredentialsNotFound


class TokenResponse(BaseModel):
    access_token: str = Field(alias="accessToken")
    expires_in: int = Field(alias="expiresIn")
    token_type: str = Field(alias="tokenType")
    _retrieved_time: datetime = PrivateAttr(datetime.now())

    @property
    def expired(self) -> bool:
        return (
            self._retrieved_time.timestamp() + self.expires_in
            < datetime.now().timestamp()
        )

    @property
    def full_token(self) -> str:
        return f"{self.token_type} {self.access_token}"


class PortClient:
    def __init__(
        self, base_url: str, client_id: str, client_secret: str, user_agent_id: str
    ):
        self.api_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent_id = user_agent_id
        self._last_token_object: TokenResponse | None = None

    async def _get_token(self, client_id: str, client_secret: str) -> TokenResponse:
        async with httpx.AsyncClient() as client:
            logger.info(f"Fetching access token for clientId: {client_id}")

            credentials = {"clientId": client_id, "clientSecret": client_secret}
            token_response = await client.post(
                f"{self.api_url}/auth/access_token", json=credentials
            )
            token_response.raise_for_status()
            return TokenResponse(**token_response.json())

    def _user_agent(self, user_agent_type: UserAgentType | None = None) -> str:
        user_agent = f"port-ocean/{self.user_agent_id}"
        if user_agent_type:
            user_agent += f"/{user_agent_type.value or UserAgentType.exporter.value}"

        return user_agent

    async def _headers(
        self, user_agent_type: UserAgentType | None = None
    ) -> dict[Any, Any]:
        return {
            "Authorization": await self.token,
            "User-Agent": self._user_agent(user_agent_type),
        }

    @property
    async def token(self) -> str:
        logger.info("Fetching access token")
        if not self._last_token_object or self._last_token_object.expired:
            self._last_token_object = await self._get_token(
                self.client_id, self.client_secret
            )
        else:
            logger.info("Access token found in cache")

        return self._last_token_object.full_token

    async def upsert_entity(
        self,
        entity: Entity,
        request_options: RequestOptions,
        user_agent_type: UserAgentType | None = None,
    ) -> None:
        validation_only = request_options.get("validation_only", False)
        logger.info(
            f"{'Validating' if validation_only else 'Upserting'} entity: {entity.identifier} of blueprint: {entity.blueprint}"
        )
        headers = await self._headers(user_agent_type)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/blueprints/{entity.blueprint}/entities",
                json=entity.dict(exclude_unset=True),
                headers=headers,
                params={
                    "upsert": "true",
                    "merge": str(request_options.get("merge", False)).lower(),
                    "create_missing_related_entities": str(
                        request_options.get("create_missing_related_entities", False)
                    ).lower(),
                    "validation_only": str(validation_only).lower(),
                },
            )

        if not response.status_code < 400:
            logger.error(
                f"Error upserting "
                f"entity: {entity.identifier} of "
                f"blueprint: {entity.blueprint}, "
                f"error: {response.text}"
            )
        response.raise_for_status()

    async def delete_entity(
        self,
        entity: Entity,
        request_options: RequestOptions,
        user_agent_type: UserAgentType | None = None,
    ) -> None:
        logger.info(
            f"Delete entity: {entity.identifier} of blueprint: {entity.blueprint}"
        )
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.api_url}/blueprints/{entity.blueprint}/entities/{entity.identifier}",
                headers=await self._headers(user_agent_type),
                params={
                    "delete_dependents": request_options["delete_dependent_entities"]
                    or False
                },
            )

        if not response.status_code < 400:
            logger.error(
                f"Error deleting "
                f"entity: {entity.identifier} of "
                f"blueprint: {entity.blueprint}, "
                f"error: {response.text}"
            )
            response.raise_for_status()

    async def get_kafka_creds(self) -> KafkaCreds:
        logger.info("Fetching organization kafka credentials")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/kafka-credentials", headers=await self._headers()
            )
        if not response.status_code < 400:
            logger.error(f"Error getting kafka credentials, error: {response.text}")
            response.raise_for_status()

        credentials = response.json()["credentials"]

        if credentials is None:
            raise KafkaCredentialsNotFound("No kafka credentials found")

        return credentials

    async def get_org_id(self) -> str:
        logger.info("Fetching organization id")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/organization", headers=await self._headers()
            )
        if not response.status_code < 400:
            logger.error(f"Error getting organization id, error: {response.text}")
            response.raise_for_status()

        return response.json()["organization"]["id"]

    async def validate_entity_exist(self, identifier: str, blueprint: str) -> None:
        logger.info(f"Validating entity {identifier} of blueprint {blueprint} exists")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/blueprints/{blueprint}/entities/{identifier}",
                headers=await self._headers(),
            )
        if response.status_code >= 400:
            logger.error(
                f"Error validating "
                f"entity: {identifier} of "
                f"blueprint: {blueprint}, "
                f"error: {response.text}"
            )
        response.raise_for_status()

    async def search_entities(self, user_agent_type: UserAgentType) -> list[Entity]:
        query = {
            "combinator": "and",
            "rules": [
                {
                    "property": "$datasource",
                    "operator": "=",
                    "value": self._user_agent(user_agent_type),
                },
            ],
        }

        logger.info(f"Searching entities with query {query}")
        async with httpx.AsyncClient() as client:
            search_req = await client.post(
                f"{self.api_url}/entities/search",
                json=query,
                headers=await self._headers(),
                params={
                    "exclude_calculated_properties": "true",
                    "include": ["blueprint", "identifier"],
                },
            )
        search_req.raise_for_status()
        return [Entity.parse_obj(result) for result in search_req.json()["entities"]]

    async def search_dependent_entities(self, entity: Entity) -> list[Entity]:
        body = {
            "combinator": "and",
            "rules": [
                {
                    "operator": "relatedTo",
                    "blueprint": entity.blueprint,
                    "value": entity.identifier,
                    "direction": "downstream",
                }
            ],
        }

        logger.info(f"Searching dependent entity with body {body}")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/entities/search",
                headers=await self._headers(),
                json=body,
            )
        response.raise_for_status()

        return [Entity.parse_obj(result) for result in response.json()["entities"]]

    async def validate_entity_payload(
        self, entity: Entity, options: RequestOptions
    ) -> None:
        logger.info(f"Validating entity {entity.identifier}")
        await self.upsert_entity(
            entity,
            {
                "merge": options.get("merge", False),
                "create_missing_related_entities": options.get(
                    "create_missing_related_entities", False
                ),
                "validation_only": True,
            },
        )

    async def get_integration(self, identifier: str) -> dict[str, Any]:
        logger.info(f"Fetching integration with id: {identifier}")
        async with httpx.AsyncClient() as client:
            integration = await client.get(
                f"{self.api_url}/integration/{identifier}",
                headers=await self._headers(),
            )
        integration.raise_for_status()
        return integration.json()["integration"]

    async def initiate_integration(
        self, _id: str, _type: str, changelog_destination: dict[str, Any]
    ) -> None:
        logger.info(f"Initiating integration with id: {_id}")
        headers = await self._headers()
        json = {
            "installationId": _id,
            "installationAppType": _type,
            "changelogDestination": changelog_destination,
        }
        async with httpx.AsyncClient() as client:
            installation = await client.patch(
                f"{self.api_url}/integration/{_id}",
                headers=headers,
                json=json,
            )
            if installation.status_code == 404:
                logger.info(f"Integration with id: {_id} not found, creating it")
                installation = await client.post(
                    f"{self.api_url}/integration", headers=headers, json=json
                )

        if installation.status_code >= 400:
            logger.error(
                f"Error initiating integration with id: {_id}, error: {installation.text}"
            )

        installation.raise_for_status()
        logger.info(f"Integration with id: {_id} successfully registered")

    async def get_blueprint(self, identifier: str) -> Blueprint:
        logger.info(f"Fetching blueprint with id: {identifier}")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/blueprints/{identifier}", headers=await self._headers()
            )
        response.raise_for_status()
        return Blueprint.parse_obj(response.json()["blueprint"])
