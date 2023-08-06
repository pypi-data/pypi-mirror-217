from typing import List, Optional, Literal

from base_model import BaseModelNoException
from pydantic import Field, constr

from dry_scraper.nhl.pydantic_models.nhl_conferences_api_source import (
    ShortConference,
)

DivisionLink = constr(regex=r"^/api/v1/divisions/(\d+|null)$")


class ShortDivision(BaseModelNoException):
    id: int
    name: str
    name_short: Optional[str] = Field(alias="nameShort")
    link: DivisionLink
    abbreviation: Optional[str]


class Division(BaseModelNoException):
    id: int
    name: str
    name_short: Optional[str] = Field(alias="nameShort")
    link: DivisionLink
    abbreviation: Optional[str]
    conference: ShortConference
    active: bool


class NullDivision(BaseModelNoException):
    link: Literal["/api/v1/divisions/null"]

    class Config:
        extra = "forbid"


class Divisions(BaseModelNoException):
    divisions: List[NullDivision | Division]
