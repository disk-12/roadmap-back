from typing import List

from algoliasearch.search_client import SearchClient

from app.model.roadmap import Roadmap, RoadmapKey
from app.repository.algolia.indexes import IndexKey
from app.repository.roadmap_search import IRoadmapSearchRepository, SearchRoadmap


class RoadmapSearchRepository(IRoadmapSearchRepository):
    client: SearchClient

    def __init__(self, client: SearchClient):
        self.client = client

    def search(self, arg: SearchRoadmap) -> List[Roadmap]:
        index = self.client.init_index(IndexKey.roadmaps)
        result = index.search(arg.keyword)

        hits = result['hits']

        ary = []
        for hit in hits:
            ary.append(
                Roadmap.from_dict({
                    **hit,
                    RoadmapKey.favorited: False,
                    RoadmapKey.edges: [],
                    RoadmapKey.vertexes: [],
                    RoadmapKey.achievement: None,
                })
            )

        return ary
