class Href:
    def __init__(self, url: str):
        self.url = url

    def create(self):
        return f'<p class="text-center">API url: <a href={self.url}>{self.url}</a></p>'
