from swagger_coverage.src.models.stats import (
    EndpointStatistics,
    PercentageEndpointStatistics,
    Statistics,
)


class SwaggerSummary:
    def __init__(self, swagger_data: dict, swagger_diff: dict):
        """
        Get summary for report
        """
        self.swagger_data = swagger_data
        self.swagger_diff = swagger_diff

    def get_summary(self):
        """
        Calculate report summary
        """
        # init stats
        count_checked = 0
        count_not_checked = 0
        count_partially_checked = 0
        count_diff = len(list(self.swagger_diff.items()))

        # data = copy.deepcopy(self.swagger_data)
        for key, value in self.swagger_data.items():
            checked_count_list = [
                list(status.values())[0] for status in value.get("statuses")
            ]
            is_all_checked = all(checked_count_list)
            if is_all_checked:
                count_checked += 1
                value["sw_result"] = "checked"
            else:
                count_zero = checked_count_list.count(0)
                if count_zero == len(checked_count_list):
                    count_not_checked += 1
                    value["sw_result"] = "not_checked"
                else:
                    count_partially_checked += 1
                    value["sw_result"] = "partially_checked"

        total = count_checked + count_not_checked + count_partially_checked + count_diff
        stats_endpoints = EndpointStatistics(
            endpoints=total,
            checked_endpoints=count_checked,
            partially_checked=count_partially_checked,
            not_checked_endpoints=count_not_checked,
            not_added_endpoints=count_diff,
        )
        percentage = self._calculate_percentage(stats_endpoints)
        return Statistics(stat_endpoints=stats_endpoints, stat_percentage=percentage)

    def _calculate_percentage(
        self, stats: EndpointStatistics, format_type=".1f"
    ) -> PercentageEndpointStatistics:
        """
        Calculate percentage of statuses
        """
        whole = stats.endpoints
        percentage_checked = format(
            100 * float(stats.checked_endpoints) / float(whole), format_type
        )
        percentage_not_checked = format(
            100 * float(stats.not_checked_endpoints) / float(whole), format_type
        )
        percentage_partially_checked = format(
            100 * float(stats.partially_checked) / float(whole), format_type
        )
        percentage_diff = format(
            100 * float(stats.not_added_endpoints) / float(whole), format_type
        )
        return PercentageEndpointStatistics(
            p_checked_endpoints=percentage_checked,
            p_partially_checked=percentage_partially_checked,
            p_not_checked_endpoints=percentage_not_checked,
            p_not_added_endpoints=percentage_diff,
        )
