import os
import re
import shutil

import logging
from datetime import datetime
from os.path import exists

from swagger_coverage.src.models import SwaggerData, EndpointStatisticsHtml
from swagger_coverage.src.utils import sort_requests_results

logger = logging.getLogger("swagger")


class ReportHtml:
    """
    Create html swagger report

    Structure:
    body:
        navbar
        links
        result_table:
            endpoints count result
            progress_bar
            accordions
                diff accordion
    """

    def __init__(
        self, path: str, api_url: str = None, swagger_url: str = None, data=None
    ):
        self.api_url = api_url
        self.swagger_url = swagger_url
        self.data: SwaggerData = data
        self.path: str = path

    _COLOR_RED = "#f59993"
    _COLOR_GREEN = "#d6facf"
    _COLOR_ORANGE = "#f2b85a"

    @staticmethod
    def html(title: str, body: str):
        """
        Create html tags
        """
        return f"""
        <html lang="en"> <head> <meta charset="UTF-8">
            <title>{title}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" # noqa
            rel="stylesheet" integrity="sha384 -1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
                </head>
                    <body>
                        {body}
                    </body>
                    <script src="./src/script.js"></script>
        </html> """  # noqa

    @staticmethod
    def _navbar():
        date_now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        return f"""
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-2">
                <div class="container-fluid">
                    <a class="navbar-brand" href="#">Report created at {date_now}</a>
                        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                    <form class="d-flex">
                        <input id="search" class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                        <button id="search-button" class="btn btn-outline-success" type="submit">Search</button>
                    </form>
                </div>
            </nav>
        """  # noqa

    def _body(self):
        """
        Create html body
        :return:
        """
        test_statistic, percent_statistic = self.data.summary
        navbar = self._navbar()
        endpoints = self._endpoints_statistics(test_statistic)
        links = self._links()
        progress_bar = self._progress_bar_container(percent_statistic)
        accordion = []
        for endpoint, value in self.data.swagger_data.items():
            res = self._create_accordion(endpoint, value)
            accordion.append(res)
        accordions = "".join(accordion)
        diff_accordion = self._create_diff_accordion_html()
        result_time_request_table = self._result_time_request_table()
        result_request_header = self._request_buttons_colors()
        result_table = self._result_table(
            endpoints_statistics=endpoints,
            progress_bar=progress_bar,
            accordions=accordions,
            diff_accordion=diff_accordion,
            description_request_button=result_request_header,
            request_time_results=result_time_request_table,
        )
        html = [navbar, links, result_table]
        return "".join(html)

    @staticmethod
    def _div(class_: str, text: str = ""):
        """
        Create div tag
        """
        return f'<div class="{class_}">{text}</div>'

    @staticmethod
    def _button(id_: str, class_: str, text: str, count: int):
        """
        Create button
        """
        return f'<button type="button" id="{id_}", class="{class_}">{text} <span class="badge bg-secondary">{count}</span></button>'  # noqa

    @staticmethod
    def _button_group(buttons: str):
        return f'<div class="btn-group" role="group" aria-label="Basic mixed styles example">{buttons}</div>'  # noqa

    @staticmethod
    def _link(text: str, link: str) -> str:
        return f'<p class="text-center"">{text}<a href={link}>{link}</a></p>'

    def _links(self):
        api_url = self._link("API url: ", self.api_url)
        swagger_url = self._link("Swagger url: ", self.swagger_url)
        return "".join([api_url, swagger_url])

    def _endpoints_statistics(self, data: EndpointStatisticsHtml):
        """
        Create file description, like url and other.
        """
        button_endpoints = self._button(
            id_="all", class_="btn btn-primary", text="All", count=data.endpoints
        )
        button_checked_endpoints = self._button(
            id_="success",
            class_="btn btn-success",
            text="Checked",
            count=data.checked_endpoints,
        )
        button_not_checked_endpoints = self._button(
            id_="not-checked",
            class_="btn btn-danger",
            text="Not checked",
            count=data.not_checked_endpoints,
        )
        button_not_added_endpoints = self._button(
            id_="not-added",
            class_="btn btn-warning",
            text="Not added",
            count=data.not_added_endpoints,
        )
        buttons = "".join(
            [
                button_endpoints,
                button_checked_endpoints,
                button_not_checked_endpoints,
                button_not_added_endpoints,
            ]
        )
        data = self._button_group(buttons)
        content = self._div(class_="d-flex justify-content-center", text=data)
        return content

    def _request_buttons_colors(self):
        """
        Create file description, like url and other.
        """
        button_checked_endpoints = self._button(
            id_="success",
            class_="btn btn-light",
            text="< 1 sec",
            count="",
        )
        button_not_checked_endpoints = self._button(
            id_="not-checked",
            class_="btn btn-warning",
            text="1-3 sec",
            count="",
        )
        button_not_added_endpoints = self._button(
            id_="not-added",
            class_="btn btn-danger",
            text="> 3 sec",
            count="",
        )
        buttons = "".join(
            [
                button_checked_endpoints,
                button_not_checked_endpoints,
                button_not_added_endpoints,
            ]
        )
        data = self._button_group(buttons)
        content = self._div(class_="d-flex justify-content-center", text=data)
        return content

    def _progress_bar_container(self, data):
        success = self._progress_bar(result_class="success", percent=data.success)
        failed = self._progress_bar(result_class="danger", percent=data.failed)
        result = "".join([success, failed])
        return f"""
            <div class="container px-4 py-1">
                <div class="row gx-5">
                    <div class="progress gx-0">
                    {result}
                    </div>
                </div>
            </div>"""
        pass

    @staticmethod
    def _progress_bar(result_class: str, percent: float) -> str:
        return f"""
            <div class="progress-bar bg-{result_class} px-5"
                role="progressbar" style="width: {percent}%" aria-valuenow=20 aria-valuemin="0" aria-valuemax="100">{percent}%
            </div>
            """  # noqa

    @staticmethod
    def _result_table(
        progress_bar: str,
        accordions: str,
        endpoints_statistics: str,
        diff_accordion: str,
        description_request_button: str,
        request_time_results: str,
    ):
        return f"""
        <div class="container px-5">
            <div class="row gx-0">
            <p class="text-center fs-2" >
            Swagger API report
            </p>
            {endpoints_statistics}
            {progress_bar}
            <div id=accordions>
                {accordions}
                {diff_accordion}
            </div>
            </div>
            <p class="text-center fs-2" >
            Request average time
            </p>
            {description_request_button}
            {request_time_results}
        </div>
        """

    def _result_time_request_table(self):
        return f"""
          <table class="table">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">Name</th>
      <th scope="col">Result(seconds)</th>
    </tr>
  </thead>
  <tbody>
    {self._create_request_data_table()}
  </tbody>
</table>
           """

    def _create_request_data_table(self) -> str:
        results = sort_requests_results(self.data.swagger_data)
        table_body = []
        for count, res in enumerate(results):
            table_body.append('<thead style="font-style: normal">\n')
            table_body.append(
                f'<tr class="table-{res.get("color")}" style="font-style: normal">\n'
            )
            table_body.append(f'<th scope="col">{count + 1}</th>\n')
            table_body.append(f'<th scope="col">{res.get("name")}</th>\n')
            table_body.append(f'<th scope="col">{res.get("results")}</th>\n')
            table_body.append("</tr>\n")
            table_body.append("</thead>\n")
        return "".join(table_body)

    @staticmethod
    def _create_section(status: dict) -> str:
        st, result = list(status.items())[0]
        color = "green" if result else "red"
        return f"""
                <section>
                    <p style="color:{color};">{st}</p>
                </section>
            """

    def _create_accordion(self, endpoint, value, color: str = None):
        """
        id, color, description, sections
        """
        text_description = self._camel_terms_to_str(endpoint)
        description = (
            f"<b>{text_description}</b> " f'({value.get("method")} {value.get("path")})'
        )
        is_checked_list = [list(status.values())[0] for status in value.get("statuses")]
        if color is None:
            color = self._COLOR_RED if False in is_checked_list else self._COLOR_GREEN

        table_rows = []
        for count, row in enumerate(value.get("statuses")):
            res = self._create_table_body(count + 1, row)
            table_rows.append(res)

        desc = value.get("description", "-")
        if desc is None:
            desc = "-"

        avg_execution = value.get("time_executions")
        if avg_execution is None:
            summery_time_exc = "-"
        else:
            summery_time_exc = sum(avg_execution) / len(avg_execution)
        return f"""
        <div class="accordion-item">
            <h2 class="accordion-header" id="{endpoint}">
                    <button class="accordion-button collapsed" type="button"
                        data-bs-toggle="collapse" data-bs-target="#flush-collapseOne"
                        aria-expanded="false" aria-controls="flush-collapseOne"
                        style="background-color: {color};">
                        {description}
                    </button>
            </h2>
        <div class="accordion-collapse collapse" aria-labelledby="flush-headingOne"
            data-bs-parent="#accordionFlushExample" data-state="collapse">
                <div class="accordion-body">
                    <section>
                        <b>Description:</b> {desc}<br>
                        <b>Average execution:</b> {str(summery_time_exc)[:5]} seconds <br>
                        {self._create_table(''.join(table_rows))}
                    </section>
                </div>
            </div>
        </div>
                """  # noqa

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

    @staticmethod
    def _create_accordion_diff(endpoint, value, color: str = None):
        """
        id, color, description, sections
        """
        description = "Missing endpoints"

        return f"""
        <div class="accordion-item">
            <h2 class="accordion-header" id="{endpoint}">
                    <button class="accordion-button collapsed" type="button"
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

    @staticmethod
    def _area(text: str):
        return f"""
                <textarea class="form-control" rows="3">{text}</textarea>
                """

    def _create_diff_accordion_html(self):
        """
        create diff html
        """
        diff_text = self._create_diff_text(self.data.diff)
        return self._create_accordion_diff(
            endpoint="endpoint", color=self._COLOR_ORANGE, value=self._area(diff_text)
        )

    @staticmethod
    def _create_diff_text(diff: dict) -> str:
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

    @staticmethod
    def _create_dir(dir_path):
        if not exists(dir_path):
            os.mkdir(dir_path)

    def _copy_src_folder(self):
        """
        Copy folder with css and js files
        :return:
        """
        # create path from library
        src_dir = os.path.dirname(os.path.abspath(__file__))
        src_library_path = os.path.join(src_dir, "files", "script.js")
        # create dir in project
        src_path_js = os.path.join(self.path, "src", "script.js")
        self._create_dir(os.path.join(self.path, "src"))
        shutil.copyfile(src_library_path, src_path_js)

    @staticmethod
    def _camel_terms_to_str(value: str):
        """
        From CamelCase to String
        """
        result = re.findall(
            "[A-Z][a-z]+|[0-9A-Z]+(?=[A-Z][a-z])|[0-9A-Z]{2,}|[a-z0-9]{2,}|[a-zA-Z0-9]",
            value,
        )  # noqa
        result[0] = result[0].capitalize()
        return " ".join(result)

    def save_html(self, file_name: str = "index.html", is_copy=True):
        """
        Save html with swagger check diff
        """
        body = self._body()
        html = self.html("Swagger coverage API", body)
        with open(os.path.join(self.path, file_name), "w") as outfile:
            outfile.write(html)
        if is_copy:
            self._copy_src_folder()
        logger.info(
            f"The swagger report was successfully saved to the folder: " f"{self.path}"
        )
