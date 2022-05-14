import copy

from swagger_coverage.src.models import (
    PercentStatistic,
    EndpointStatisticsHtml,
    SwaggerData,
)


class DataDiff:
    def result_diff(self, data: SwaggerData, paths, prepare_data):
        """
        Get swagger check result, need for build html report
        """
        data.diff = self._swagger_diff(paths, prepare_data)
        data.summary = self._get_summary(data.diff, data)
        return data

    @staticmethod
    def _swagger_diff(paths, prepare_data):
        """
        Get swagger diff
        """
        diff = {k: prepare_data[k] for k in set(prepare_data) - set(paths)}
        return diff

    def _get_summary(
        self, diff: dict, data
    ) -> [EndpointStatisticsHtml, PercentStatistic]:
        """
        Calculate report summary
        """
        count_success = 0
        count_of_unverified = 0
        data = copy.deepcopy(data.swagger_data)
        for key, value in data.items():
            is_checked_list = [
                list(status.values())[0] for status in value.get("statuses")
            ]
            count_success += len([status for status in is_checked_list if status > 0])
            count_of_unverified += len(
                [status for status in is_checked_list if status == 0]
            )
        count_diff = len(list(diff.items()))
        count_total = count_success + count_of_unverified
        # get percent
        percentage_success = self._percentage(count_success, count_total)
        percentage_unverified = self._percentage(count_of_unverified, count_total)
        return (
            EndpointStatisticsHtml(
                count_total, count_success, count_of_unverified, count_diff
            ),
            PercentStatistic(percentage_success, percentage_unverified),
        )

    @staticmethod
    def _percentage(part, whole) -> str:
        """
        Calculate percentage of verified statuses
        """
        res = 100 * float(part) / float(whole)
        return format(res, ".1f")
