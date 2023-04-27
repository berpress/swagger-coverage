from swagger_coverage.src.report.html.models import BodyModel


class Body:
    def __init__(self, data: BodyModel):
        self.data = data

    def create(self):
        res = "".join(
            [
                self.data.head,
                self.data.navbar,
                self.data.title,
                self.data.api_url,
                '<div class="container px-5">',
                '<div class="row gx-0">',
                '<div class="d-flex justify-content-center">',
                self.data.btn_groups,
                self.data.progress_bar,
                self.data.accordions,
                "<p></p>",
                self.data.title_avg,
                self.data.table,
                "</div>",
                "</div>",
                "</div>",
                self.data.script,
            ]
        )
        return f"<body>" f"{res}" f"</body>"
