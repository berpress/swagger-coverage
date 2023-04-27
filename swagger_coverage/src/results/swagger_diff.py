class SwaggerDiff:
    def __init__(self, local_swagger: dict, actual_swagger: dict):
        """
        Get difference between current local swagger and current actual swagger
        :param local_swagger: local swagger
        :param actual_swagger: actual swagger
        """
        self.local_swagger = local_swagger
        self.actual_swagger = actual_swagger

    def get_diff(self):
        diff = {
            k: self.actual_swagger[k]
            for k in set(self.actual_swagger) - set(self.local_swagger)
        }
        return diff
