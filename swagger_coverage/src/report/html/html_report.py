import os
from datetime import datetime

from swagger_coverage.src.report.html.accordion import Accordion
from swagger_coverage.src.report.html.body import Body
from swagger_coverage.src.report.html.btn_group import BtnGroups
from swagger_coverage.src.report.html.constants import HTML_TEMPLATE
from swagger_coverage.src.report.html.h2 import H
from swagger_coverage.src.report.html.head import Head
from swagger_coverage.src.report.html.href import Href
from swagger_coverage.src.report.html.models import (
    BodyModel,
    ButtonsGroup,
    ProgressGroup,
)
from swagger_coverage.src.report.html.navbar import Navbar
from swagger_coverage.src.report.html.prepare_data import PrepareDataToHtml
from swagger_coverage.src.report.html.progress import Progress
from swagger_coverage.src.report.html.scripts import JS_SCRIPT
from swagger_coverage.src.report.html.table import Table


class HtmlReport:
    def __init__(self, results):
        self.results = results

    def _save_html(self, html: str, path: str, file_name: str = "index.html"):
        """
        Save html with swagger check diff
        """
        with open(os.path.join(path, file_name), "w") as outfile:
            outfile.write(html)

    def create(self, path):
        # script
        script = JS_SCRIPT
        # head
        head = Head(title="Swagger Report")
        head_html = head.create()
        # navbar
        date_now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        navbar = Navbar(title=date_now)
        navbar_html = navbar.create()
        # title
        title = "Swagger API report"
        h2 = H(text=title, level=2)
        h2_html = h2.create()
        # api url
        api_url = self.results.url
        href = Href(api_url)
        href_html = href.create()
        # buttons group
        endpoints = self.results.summary.stat_endpoints.endpoints
        checked_endpoints = self.results.summary.stat_endpoints.checked_endpoints
        partially_checked = self.results.summary.stat_endpoints.partially_checked
        not_checked_endpoints = (
            self.results.summary.stat_endpoints.not_checked_endpoints
        )
        not_added_endpoints = self.results.summary.stat_endpoints.not_added_endpoints
        buttons_list = [
            ButtonsGroup(color="primary", value=endpoints, text="All"),
            ButtonsGroup(color="success", value=checked_endpoints, text="Checked"),
            ButtonsGroup(
                color="danger", value=not_checked_endpoints, text="Not checked"
            ),
            ButtonsGroup(
                color="warning", value=partially_checked, text="Partial checked"
            ),
            ButtonsGroup(color="info", value=not_added_endpoints, text="Not added"),
        ]
        buttons = BtnGroups(buttons_list)
        buttons_html = buttons.create()
        # progress
        p_checked_endpoints = self.results.summary.stat_percentage.p_checked_endpoints
        p_not_added_endpoints = (
            self.results.summary.stat_percentage.p_not_added_endpoints
        )
        p_not_checked_endpoints = (
            self.results.summary.stat_percentage.p_not_checked_endpoints
        )
        p_partially_checked = self.results.summary.stat_percentage.p_partially_checked
        progress_list = [
            ProgressGroup(color="success", value=p_checked_endpoints),
            ProgressGroup(color="info", value=p_not_added_endpoints),
            ProgressGroup(color="danger", value=p_not_checked_endpoints),
            ProgressGroup(color="warning", value=p_partially_checked),
        ]
        progress = Progress(progress_list)
        progress_html = progress.create()
        # accordion
        prepare_data = PrepareDataToHtml(self.results.swagger_data)
        data = prepare_data.prepare_data()
        accordion = Accordion(data=data, diff=self.results.diff)
        accordion_html = accordion.create()
        # table
        table = Table(self.results.swagger_data)
        table_html = table.create()
        # title time avg
        title_time_avg_h2 = H(text="Request average time", level=2)
        title_time_avg_html = title_time_avg_h2.create()
        # body
        body_model = BodyModel(
            script=script,
            head=head_html,
            navbar=navbar_html,
            title=h2_html,
            api_url=href_html,
            btn_groups=buttons_html,
            progress_bar=progress_html,
            accordions=accordion_html,
            table=table_html,
            title_avg=title_time_avg_html,
        )
        body = Body(data=body_model)
        body_html = body.create()
        html = HTML_TEMPLATE.format(body_html)
        self._save_html(html=html, path=path)
