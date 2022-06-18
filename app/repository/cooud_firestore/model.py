from enum import Enum


class ModelName(str, Enum):
    users = u'users'
    roadmaps = u'roadmaps'
    graphs = u'graphs'
    edges = u'edges',
    vertexes = u'vertexes'
    user_favorites = u'user_favorites'
