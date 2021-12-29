import time
import logging
import requests
import yaml
import exceptions as Exceptions
import constants as Constants


class OSM_Wrapper:
    auth_token = ""
    expires_at = ""

    def __init__(self, ip, username, password, project_id):
        self.ip = ip
        self.username = username
        self.password = password
        self.project_id = project_id
        self.authenticate()


    # DECORATORS
    # Auth Decorator
    def requires_auth(func, *args, **kwargs):
        def wrapper(self, *args, **kwargs):
            try:
                self.update_auth_token()
                return func(self, *args, **kwargs)
            except Exception as e:
                logging.error("Auth Required: To call this function you need to be authenticated in OSM! - " + str(e))
        return wrapper

    
    def authenticate(self):
        try:
            response = requests.post(
                f"http://{self.ip}/osm/admin/v1/tokens",
                data = {
                    "username": self.username,
                    "password": self.password, 
                    "project_id": self.project_id
                },
                timeout=5)
            # check status
            response.raise_for_status()
            # get data 
            response_data = yaml.safe_load(response.text)
            self.auth_token = response_data["id"]
            self.expires_at = response_data["expires"]
        except:
            raise Exceptions.CouldNotLoginOnOSM(self.username, self.password, self.project_id)


    def update_auth_token(self):
        if self.auth_token == "" or self.expires_at < time.time():
            self.authenticate()


    @requires_auth
    def get_vdus_ip(self):
        try:
            response = requests.get(
                f"http://{self.ip}/osm/nslcm/v1/vnf_instances",
                headers={"Authorization": f"Bearer {self.auth_token}"},
                timeout=5)
            # check status
            response.raise_for_status()
            response_data = yaml.safe_load(response.text)
            # get active vdus ips
            vdus_ip = [vdu["ip-address"]for vnf_data in response_data for vdu in vnf_data['vdur'] if vdu["status"] == "ACTIVE"]
            return vdus_ip
        except:
            raise Exceptions.CouldNotLoginOnOSM(self.username, self.password, self.project_id)