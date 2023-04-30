from typing import List

from swagger_coverage.src.report.html.models import ButtonsGroup


class BtnGroups:
    def __init__(self, buttons: List[ButtonsGroup]):
        self.buttons = buttons

    def create(self):
        result = []
        for button in self.buttons:
            result.append(
                f'<button type="button" id="{button.text.lower().replace(" ", "_")}" ,="" class="btn btn-{button.color}">{button.text} <span class="badge '
                f'bg-secondary"> {button.value}</span></button>'
            )

        res = (
            f'<div class="btn-group" role="group" aria-label="Basic mixed styles example">'
            f'{"".join(result)}</div>'
        )
        return f'<div class="d-flex justify-content-center" {res} </div>'
