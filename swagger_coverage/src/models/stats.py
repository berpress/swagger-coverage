class EndpointStatistics:
    def __init__(
        self,
        endpoints: int,
        checked_endpoints: int,
        partially_checked: int,
        not_checked_endpoints: int,
        not_added_endpoints: int,
    ):
        self.endpoints = endpoints
        self.checked_endpoints = checked_endpoints
        self.partially_checked = partially_checked
        self.not_checked_endpoints = not_checked_endpoints
        self.not_added_endpoints = not_added_endpoints


class PercentageEndpointStatistics:
    def __init__(
        self,
        p_checked_endpoints: str,
        p_partially_checked: str,
        p_not_checked_endpoints: str,
        p_not_added_endpoints: str,
    ):
        self.p_checked_endpoints = p_checked_endpoints
        self.p_partially_checked = p_partially_checked
        self.p_not_checked_endpoints = p_not_checked_endpoints
        self.p_not_added_endpoints = p_not_added_endpoints


class Statistics:
    def __init__(
        self,
        stat_endpoints: EndpointStatistics,
        stat_percentage: PercentageEndpointStatistics,
    ):
        self.stat_endpoints = stat_endpoints
        self.stat_percentage = stat_percentage
