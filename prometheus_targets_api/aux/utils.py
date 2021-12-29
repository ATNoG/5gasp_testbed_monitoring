import configparser
import logging
import constants as Constants
import ipaddress
from fastapi.responses import JSONResponse
from http import HTTPStatus
import json
import aux.exceptions as Exceptions

def create_response(status_code=HTTPStatus.OK, data=[], errors=[], success=True, message=""):
    return JSONResponse(status_code=status_code, content={"message": message, "success": success, 
    "data": data, "errors": errors}, headers={"Access-Control-Allow-Origin": "*"})


def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        Constants.AUTH_TOKEN = config['Auth']['Token']

        Constants.PROMETHEUS_DATA["BASE_URL"] = config['Prometheus']['BASE_URL']
        Constants.PROMETHEUS_DATA["RELOAD_ENDPOINT"] = config['Prometheus']['RELOAD_ENDPOINT']
        Constants.PROMETHEUS_DATA["TARGETS_FILEPATH"] = config['Prometheus']['TARGETS_FILEPATH']
        Constants.PROMETHEUS_DATA["METRICS_COLLECTION_PORT"] = int(config['Prometheus']['METRICS_COLLECTION_PORT'])
        logging.info("config.ini loaded with success")
    except:
        logging.error("config.ini does not contain the needed information")
        return False, """The config file should have the folling sections with the following variables: 
        Auth -> Token, Prometheus -> BASE_URL, RELOAD_ENDPOINT, TARGETS_FILEPATH, METRICS_COLLECTION_PORT"""
    return True, ""


def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        return False

