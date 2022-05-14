class EndpointStatisticsHtml:
    def __init__(
        self,
        endpoints: int,
        checked_endpoints: int,
        not_checked_endpoints: int,
        not_added_endpoints: int,
    ):
        self.endpoints = endpoints
        self.checked_endpoints = checked_endpoints
        self.not_checked_endpoints = not_checked_endpoints
        self.not_added_endpoints = not_added_endpoints


class PercentStatistic:
    def __init__(self, success: str, failed: str):
        self.success = success
        self.failed = failed


class DescriptionHtml:
    def __init__(self, api_url: str, swagger_url: str):
        self.api_url = api_url
        self.swagger_url = swagger_url


class SwaggerData:
    def __init__(
        self, swagger_data: dict = None, diff: dict = None, summary: dict = None
    ):
        self.swagger_data = swagger_data
        self.diff = diff
        self.summary = summary
