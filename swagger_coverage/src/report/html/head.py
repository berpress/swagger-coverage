from swagger_coverage.src.report.html.constants import BOOTSTRAP_URL


class Head:
    def __init__(self, title: str, bootstrap_url: str = BOOTSTRAP_URL):
        self.title = title
        self.bootstrap_url = bootstrap_url

    def create(self):
        return (
            '<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, '
            f'initial-scale=1"><title>{self.title}</title><link '
            f'href="{self.bootstrap_url}" '
            'rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" '  # noqa
            'crossorigin="anonymous"><script src="https://cdn.jsdelivr.net/npm/chart.js"></script></head>'
        )
