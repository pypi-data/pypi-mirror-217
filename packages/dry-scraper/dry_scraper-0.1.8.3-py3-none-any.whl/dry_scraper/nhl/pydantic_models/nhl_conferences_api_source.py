from typing import List, Optional

from dry_scraper.nhl.pydantic_models.base_model import BaseModelNoException
from pydantic import constr, Field

ConferenceLink = constr(regex=r"^/api/v1/conferences/(\d+|null)$")


class Conference(BaseModelNoException):
    id: int
    name: str
    link: ConferenceLink
    abbreviation: str
    short_name: str = Field(alias="shortName")
    active: bool


class ShortConference(BaseModelNoException):
    id: Optional[int]
    name: Optional[str]
    link: ConferenceLink


class Conferences(BaseModelNoException):
    conferences: List[Conference]
