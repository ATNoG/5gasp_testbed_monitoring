import logging
import constants as Constants
import json
import aux.exceptions as Exceptions
import requests

def load_targets_file_content():
    print(Constants.PROMETHEUS_DATA["TARGETS_FILEPATH"])
    try:
        with open(Constants.PROMETHEUS_DATA["TARGETS_FILEPATH"], "r") as targets_file:
            Constants.TARGETS_FILE_CONTENT = json.load(targets_file)
            return Constants.TARGETS_FILE_CONTENT
    except:
        raise Exceptions.CouldNotLoadTargetsFileException()


def update_targets_on_targets_file(new_targets):
    load_targets_file_content()
    try:
        # Get current targets
        current_targets = Constants.TARGETS_FILE_CONTENT[0]["targets"]
        # new targets with ports
        new_targets = [
            f"{t}:{Constants.PROMETHEUS_DATA['METRICS_COLLECTION_PORT']}" for t in new_targets]
        # update the targets
        new_targets = list(set(new_targets + current_targets))
        # write to the targets file
        Constants.TARGETS_FILE_CONTENT[0]["targets"] = new_targets
        with open(Constants.PROMETHEUS_DATA["TARGETS_FILEPATH"], "w") as targets_file:
            json.dump(Constants.TARGETS_FILE_CONTENT, targets_file)
        return new_targets
    except:
        raise Exceptions.CouldNotUpdateTargets()


def delete_targets_on_targets_file(targets_to_delete):
    load_targets_file_content()
    try:
        # Get current targets
        current_targets = Constants.TARGETS_FILE_CONTENT[0]["targets"]
        # remove some targets
        new_targets = [ t for t in current_targets if t.split(":")[0] not in targets_to_delete]
        # write to the targets file
        Constants.TARGETS_FILE_CONTENT[0]["targets"] = new_targets
        with open(Constants.PROMETHEUS_DATA["TARGETS_FILEPATH"], "w") as targets_file:
            json.dump(Constants.TARGETS_FILE_CONTENT, targets_file)
        return new_targets
    except:
        raise Exceptions.CouldNotUpdateTargets()


def reload_prometheus_config():
    try:
        logging.info("Reloading Prometheus config...")
        response = requests.post(f"{Constants.PROMETHEUS_DATA['BASE_URL']}{Constants.PROMETHEUS_DATA['RELOAD_ENDPOINT']}", timeout=5)
        if response.status_code != 200:
            logging.error(f"Prometheus reload failed with status code {response.status_code}") 
            raise Exceptions.CouldNotReloadPrometheusConfig()
    except:
        logging.error(f"Prometheus reload failed.") 
        raise Exceptions.CouldNotReloadPrometheusConfig()
    logging.info("Reloaded Prometheus config")
