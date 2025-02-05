from .v1.hosts import HostsApi, HostDetailsApi, HostHistoryApi, IsROSConfiguredApi
from .v1.recommendation_ratings import RecommendationRatingsApi
from .v1.recommendations import RecommendationsApi
from .v1.openapi_spec import OpenAPISpec
from .v1.status import Status


# Initialize Routes
def initialize_routes(api):
    api.add_resource(Status, '/api/ros/v1/status')
    api.add_resource(IsROSConfiguredApi, '/api/ros/v1/is_configured')
    api.add_resource(HostsApi, '/api/ros/v1/systems')
    api.add_resource(HostHistoryApi, '/api/ros/v1/systems/<host_id>/history')
    api.add_resource(RecommendationsApi, '/api/ros/v1/systems/<host_id>/suggestions')
    api.add_resource(HostDetailsApi, '/api/ros/v1/systems/<host_id>')
    api.add_resource(RecommendationRatingsApi, '/api/ros/v1/rating')
    api.add_resource(OpenAPISpec, '/api/ros/v1/openapi.json')
