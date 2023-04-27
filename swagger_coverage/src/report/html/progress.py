from typing import List

from swagger_coverage.src.report.html.models import ProgressGroup


class Progress:
    def __init__(self, progress_list: List[ProgressGroup]):
        self.progress_list = progress_list

    def create(self):
        result = []
        for progress in self.progress_list:
            if progress.color == "":
                color = ""
            else:
                color = f"bg-{progress.color}"
            result.append(
                f'<div class="progress" role="progressbar" aria-label="Segment one" aria-valuenow="15" '
                f'aria-valuemin="0" aria-valuemax="100" style="width: {progress.value}%"><div '
                f'class="progress-bar {color}">{progress.value} %</div></div>'
            )

        return f'<p></p><div class="progress-stacked">{"".join(result)}</div>'
