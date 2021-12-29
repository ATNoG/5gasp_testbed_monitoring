from http import HTTPStatus

class CouldNotLoadTargetsFileException(Exception):
    def __init__(self, filepath=None):
        self.status_code = HTTPStatus.BAD_REQUEST
        if filepath:
            self.filepath = filepath
            self.message = f'Could not load the targets file "{filepath}"'
        else:
           self.message = 'Could not load the targets file'
        super().__init__(self.message)

    def __str__(self):
        return self.message


class CouldNotUpdateTargets(Exception):
    def __init__(self):
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = 'Could not update the targets'
        super().__init__(self.message)

    def __str__(self):
        return self.message


class CouldNotReloadPrometheusConfig(Exception):
    def __init__(self):
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = 'Could not reload Prometheus config'
        super().__init__(self.message)

    def __str__(self):
        return self.message
