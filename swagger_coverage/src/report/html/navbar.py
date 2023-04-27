class Navbar:
    def __init__(self, title: str):
        self.title = title

    def create(self):
        return (
            '<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-2"><div '
            'class="container-fluid"><a '
            f'class="navbar-brand" href="#">Report created at {self.title}</a><button class="navbar-toggler" '
            'type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" '
            'aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation"><span '
            'class="navbar-toggler-icon"></span></button><form class="d-flex"></form></div></nav>'
        )
