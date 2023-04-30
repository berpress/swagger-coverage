class H:
    def __init__(self, text: str, level: int):
        self.text = text
        self.level = level

    def create(self, attribute="text-center"):
        return f"<h{self.level} class={attribute}>{self.text}</h{self.level}>"
