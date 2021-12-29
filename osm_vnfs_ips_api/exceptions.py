from http import HTTPStatus

class CouldNotLoginOnOSM(Exception):
    def __init__(self, username=None, password=None, project_id=None):
        self.status_code = HTTPStatus.UNAUTHORIZED
        if username and password and project_id:
            self.message = f'Could not login on OSM with username "{username}" and password "{password}" and project_id "{project_id}"'
        else:
            self.message = 'Could not get authentication token from OSM using the provided credentials'
        super().__init__(self.message)

    def __str__(self):
        return self.message


class CouldNotUpdatePrometheusTargets(Exception):
    def __init__(self, prometheus_api_message=None):
        self.status_code = HTTPStatus.BAD_REQUEST
        if prometheus_api_message: 
            self.message = f'Could not update Prometheus targets: {prometheus_api_message}'
        else:
            self.message = 'Could not update Prometheus targets'
        super().__init__(self.message)

    def __str__(self):
        return self.message
