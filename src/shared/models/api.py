from typing import Mapping
from http import HTTPMethod, HTTPStatus
from pydantic import BaseModel, Field
from fastapi import Request, Response
from shared.models.constants import ActorNames
from shared.models.policy import DTO_CONFIG, DTO_EDGE_CONFIG


class API(BaseModel):
    model_config = DTO_CONFIG
    app_version: str


class APIEvent(BaseModel):
    """DTO - For API Event Log Output"""

    model_config = DTO_CONFIG
    Method: HTTPMethod
    RoutePathTemplate: str
    RouteName: str
    RequestPath: str
    PathParams: Mapping[str, str]
    Status: HTTPStatus
    DurationMs: int = Field(ge=0)
    RequestSize: int = Field(ge=0, le=2_097_152)
    ResponseSize: int = Field(ge=0, le=10_485_760)


# Support dynamic ASGI DTOs. ASGI objects are "frozen" at the edge as logging events
class ASGIEvent(BaseModel):
    """DTO - for API Log Event Input"""

    model_config = DTO_EDGE_CONFIG
    Request: Request
    Response: Response
    DurationMS: int = Field(ge=0)


class InfoResponse(BaseModel):
    """DTO for api output /info"""

    model_config = DTO_CONFIG
    FastApiVersion: str
    PSSVersion: str


# @dto(schema_extra=lambda cls: {"Title": "Immutable DTO for the /ready"})
class ReadyResponse(BaseModel):
    """DTO for api output /ready"""

    model_config = DTO_CONFIG
    API: bool
    Mailbox: bool
    Handler: bool


class RootResponse(BaseModel):
    """DTO for api output /"""

    model_config = DTO_CONFIG
    Message: str


class Routes(BaseModel):
    """Internal DTO for for helper.log"""

    model_config = DTO_CONFIG
    RoutePathTemplate: str
    RouteName: str
    RequestPath: str


class AddressInput(BaseModel):
    """Input for address client"""

    model_config = DTO_CONFIG

    actor: ActorNames
    behavior: str
