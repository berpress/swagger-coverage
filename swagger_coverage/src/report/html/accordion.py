from swagger_coverage.src.report.html.colors import COLOR_METHOD, Coloros


class Accordion:
    def __init__(self, data: dict, diff: dict):
        self.data = data
        self.diff = diff

    def create(self):
        diff_accordion = self._create_diff_accordion_html()
        res = ['<div id="accordions">']
        res.append('<div class="accordion accordion-flush" id="accordionFlushExample">')
        for key, value in self.data.items():
            res.append(f"<h3>{key.capitalize()}</h3>")
            for route in value:
                res.append(self._accordion_item(route))
        res.append(diff_accordion)
        res.append("</div>")
        res.append("</div>")
        return "".join(res)

    def _accordion_item(self, value):
        color = COLOR_METHOD.get(value.get("method"))
        if color is None:
            color = COLOR_METHOD.get("default")
        status_check = self._check_status_html(value.get("sw_result"))
        res = [
            '<div class="accordion-item">',
            f'<h2 class="accordion-header id="{value.get("key")}">',
        ]
        according_button = (
            f'<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-status='
            f'"{value.get("sw_result")}"'
            f'data-bs-target="#flush-collapseTwo" aria-expanded="false" '
            f'aria-controls="flush-collapseTwo"><p style="color:{color}">{value.get("method")}</p> '
            f'<p>&nbsp{value.get("path")}</p>&nbsp&nbsp{status_check}</button>'
        )
        res.append(according_button)
        res.append("</h2>")

        desc = value.get("description", "-")

        avg_execution = value.get("time_executions")
        if avg_execution is None:
            summery_time_exc = "-"
        else:
            summery_time_exc = sum(avg_execution) / len(avg_execution)

        table_rows = []
        for count, row in enumerate(value.get("statuses")):
            res_table = self._create_table_body(count + 1, row)
            table_rows.append(res_table)

        according_body = (
            f'<div class="accordion-collapse collapse" '
            f'data-bs-parent="#accordionFlushExample" style=""><div class="accordion-body"> '
            f"<section><b>Description:</b> {desc}<br><b>Average execution:</b> "
            f'{str(summery_time_exc)[:5]} seconds <br>{self._create_table("".join(table_rows))}'
            f"</section></div></div>"
        )
        res.append(according_body)
        res.append("</button>")
        res.append("</div>")

        return "".join(res)

    def _create_table(self, rows):
        """
        Create table in accordion
        """
        return f""" <table class="table">
                      <thead>
                        <tr>
                          <th scope="col">#</th>
                          <th scope="col">Status code</th>
                          <th scope="col">Number of calls</th>
                        </tr>
                      </thead>
                      {rows}
                    </table>
        """

    def _create_table_body(self, count: int, status: dict) -> str:
        st, result = list(status.items())[0]
        color = "green" if result else "red"
        return f"""<tbody>
                        <tr>
                          <th scope="row">{count}</th>
                          <td><p style="color:{color};">{st}</p></td>
                          <td>{result}</td>
                        </tr>
                      </tbody>
                      """

    def _check_status_html(self, status: str) -> str:
        color = {
            "checked": "#064D1A",
            "not_checked": "#EA150E",
            "partially_checked": "#ffc107",
        }
        p = f'<p style="color: {color.get(status, "#050200")}">{status.replace("_", " ")}</p>'
        return p

    def _create_diff_accordion_html(self):
        """
        create diff html
        """
        diff_text = self._create_diff_text(self.diff)
        return self._create_accordion_diff(
            endpoint="endpoint", color=Coloros.BLUE, value=self._area(diff_text)
        )

    def _create_diff_text(self, diff: dict) -> str:
        """
        Create diff text for data_swagger.yaml
        """
        text = []
        spaces = "  "
        for key, values in diff.items():
            desc = values.get("description", "-")
            if desc is None:
                desc = "-"
            text.append(f"{key}:\n")
            text.append(f"{spaces}description: {desc}\n")
            text.append(f'{spaces}method: {values.get("method")}\n')
            text.append(f'{spaces}path: {values.get("path")}\n')
            text.append(f"{spaces}statuses:\n")
            text.append(f"{spaces}- 200\n")
            text.append(f"{spaces}- 400\n")
            text.append(f'{spaces}tag: {values.get("tag")} \n')
        return "".join(text)

    def _create_accordion_diff(self, endpoint, value, color: str = None):
        """
        id, color, description, sections
        """
        description = "Missing endpoints (copy to setting file)"

        return f"""
        <div class="accordion-item">
            <h2 class="accordion-header" id="{endpoint}">
                    <button class="accordion-button collapsed" type="button" data-status="not_added"
                        data-bs-toggle="collapse" data-bs-target="#flush-collapseOne"
                        aria-expanded="false" aria-controls="flush-collapseOne"
                        style="background-color: {color};">
                        {description}
                    </button>
            </h2>
        <div class="accordion-collapse collapse" aria-labelledby="flush-headingOne"
            data-bs-parent="#accordionFlushExample" data-state="collapse">
                <div class="accordion-body"> <section>
                    {value} </section>
        </div>
            </div>
                </div>
                """  # noqa

    def _area(self, text: str):
        return f"""
                <textarea class="form-control" rows="3">{text}</textarea>
                """
