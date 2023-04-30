class BodyModel:
    def __init__(
        self,
        script: str,
        head: str,
        navbar: str,
        title: str,
        api_url: str,
        btn_groups: str,
        progress_bar: str,
        accordions: str,
        table: str,
        title_avg: str,
    ):
        self.head = head
        self.navbar = navbar
        self.title = title
        self.api_url = api_url
        self.btn_groups = btn_groups
        self.progress_bar = progress_bar
        self.accordions = accordions
        self.title_avg = title_avg
        self.table = table
        self.script = script


class ButtonsGroup:
    def __init__(self, text: str, color: str, value: str):
        self.text = text
        self.color = color
        self.value = value


class ProgressGroup:
    def __init__(self, value: str, color: str):
        self.color = color
        self.value = value
