import strawberry
from strawberry.fastapi import GraphQLRouter
from .resolver.query import Query
from .resolver.mutation import Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)
router = GraphQLRouter(schema)
