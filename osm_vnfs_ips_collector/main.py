import logging
import configparser
import time
from osm_wrapper import OSM_Wrapper
import constants as Constants
import requests
import yaml
import exceptions as Exceptions


logging.basicConfig(
    format="[%(asctime)s]%(module)+10s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)

# load config
config = configparser.ConfigParser()
config.read('config.ini')
try:
    Constants.OSM_IP = config['OSM']['IP']
    Constants.OSM_USERNAME = config['OSM']['USERNAME']
    Constants.OSM_PASSWORD = config['OSM']['PASSWORD']
    Constants.OSM_PROJECT_NAME = config['OSM']['PROJECT_NAME']
    Constants.PROMETHEUS_UPDATE_TARGETS_ENDPOINT = config['Prometheus']['UPDATE_TARGETS_ENDPOINT']
    Constants.PROMETHEUS_API_AUTH_TOKEN = config['Prometheus']['API_AUTH_TOKEN']
    logging.info("config.ini loaded with success")
except:
    logging.error("""config.ini does not contain the needed information\n
        The config file should have the folling sections with the following variables: 
        OSM -> IP, USERNAME, PASSWORD, PROJECT_NAME""")
    exit(1)

# create osm wrapper
osm_wrapper = OSM_Wrapper(Constants.OSM_IP, Constants.OSM_USERNAME, Constants.OSM_PASSWORD, Constants.OSM_PROJECT_NAME)
vdus_ips = None
while True:
    new_vdus_ips = osm_wrapper.get_vdus_ip()
    prometheus_targets = new_vdus_ips if not vdus_ips else [vdu_ip for vdu_ip in new_vdus_ips if vdu_ip not in vdus_ips]
    
    # call prometheus api
    try:
        response = requests.put(
            Constants.PROMETHEUS_UPDATE_TARGETS_ENDPOINT,
            json= {
                "targets": prometheus_targets,
                "auth_token": Constants.PROMETHEUS_API_AUTH_TOKEN
            },
            timeout=5)
        # check status
        response.raise_for_status()
        logging.info(f"Prometheus API called with success. Updated the following targets: {prometheus_targets}")
    except Exception as e:
        print("Exception:", str(e))

    vdus_ips = new_vdus_ips

    time.sleep(10)
