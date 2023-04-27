class PrepareDataToHtml:
    """
    Prepare data by group
    """

    def __init__(self, data: dict):
        self.data = data

    def prepare_data(self) -> dict:
        res = {}
        for key, value in self.data.items():
            value["key"] = key
            if res.get(value.get("tag")) is None:
                res[value.get("tag")] = [value]
            else:
                res[value.get("tag")].append(value)
        return res
