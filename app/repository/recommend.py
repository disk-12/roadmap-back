import abc

from app.model.reccomend import Recommend


class IRecommendRepository(abc.ABC):
    @abc.abstractmethod
    def get_recommends(self) -> Recommend:
        raise NotImplementedError()
