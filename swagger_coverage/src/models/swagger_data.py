from swagger_coverage.src.models.stats import Statistics


class SwaggerData:
    def __init__(
        self, swagger_data: dict = None, summary: Statistics = None, diff=None, url=None
    ):
        self.swagger_data = swagger_data
        self.summary = summary
        self.diff = diff
        self.url = url


class SwaggerResponse:
    def __init__(self, paths: dict, swagger_type: str):
        self.paths = paths
        self.swagger_type = swagger_type
