from enum import Enum
from typing import List

from pydantic import BaseModel


class RecommendKey(str, Enum):
    roadmap_ids = u"roadmap_ids"


class Recommend(BaseModel):
    roadmap_ids: List[str]
