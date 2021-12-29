from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import aux.utils as Utils
import aux.prometheus as Prometheus
from http import HTTPStatus
import schemas as Schemas
# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)

fast_api_tags_metadata = [
    {
        "name": "targets",
        "description": "Operations related with the target VMs to monitor.",
    },
]

fast_api_description = "Prometheus Targets Update API"

# Start Fast API
app = FastAPI(
    title="Prometheus Targets Update API",
    description=fast_api_description,
    version="0.0.1",
    contact={
        "name": "Rafael Direito",
        "email": "rdireito@av.it.pt",
    },
    openapi_tags=fast_api_tags_metadata
)


app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="http(s)?://ci-cd-manager\.5gasp\.eu.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()
Utils.load_config()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.put(
    "/targets",
    tags=["targets"],
    summary="Update the Prometheus targets",
    description="Update the Prometheus target VMs"
)
def put_targets(targets_info: Schemas.Targets):
    # validate the auth_token
    #if not Aux.is_auth_token_valid(targets_info.auth_token):
    #    return Aux.create_response(status_code=HTTPStatus.FORBIDDEN, errors=["Invalid auth token"])

    # validate the targets
    valid_targets = [target for target in targets_info.targets if Utils.validate_ip(target)]
    if len(valid_targets) == 0:
        return Utils.create_response(status_code=HTTPStatus.NOT_MODIFIED, errors=["No valid targets found"])

    # update the targets file and reload the targets
    try:
        new_targets = Prometheus.update_targets_on_targets_file(valid_targets)
        Prometheus.reload_prometheus_config()
    except Exception as e:
        return Utils.create_response(success=False, status_code=e.status_code, message=e.message)
    
    return Utils.create_response(status_code=HTTPStatus.OK, data={"new_targets":new_targets}, message="Targets updated")


@app.delete(
    "/targets",
    tags=["targets"],
    summary="Delete some Prometheus targets",
    description="Delete some Prometheus targets"
)
def delete_targets(targets_info: Schemas.Targets):
    # validate the auth_token
    #if not Aux.is_auth_token_valid(targets_info.auth_token):
    #    return Aux.create_response(status_code=HTTPStatus.FORBIDDEN, errors=["Invalid auth token"])

    # validate the targets
    valid_targets = [
        target for target in targets_info.targets if Utils.validate_ip(target)]
    if len(valid_targets) == 0:
        return Utils.create_response(success=False, status_code=HTTPStatus.NOT_MODIFIED, message="No valid targets found")

    # update the targets file and reload the targets
    try:
        new_targets = Prometheus.delete_targets_on_targets_file(valid_targets)
        Prometheus.reload_prometheus_config()
    except Exception as e:
        print(e)
        return Utils.create_response(success=False, status_code=e.status_code, message=e.message)

    return Utils.create_response(status_code=HTTPStatus.OK, data={"targets_deleted": valid_targets, "current_targets": new_targets}, message="Targets deleted")
