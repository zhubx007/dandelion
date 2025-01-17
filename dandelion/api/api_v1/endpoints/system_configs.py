# Copyright 2022 99Cloud, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps
from dandelion.mqtt import cloud_server as mqtt_cloud_server

router = APIRouter()


@router.post(
    "",
    response_model=schemas.SystemConfig,
    status_code=status.HTTP_200_OK,
    description="""
Get detailed info of System Config.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.SystemConfig, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def create(
    user_in: schemas.SystemConfigCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.SystemConfig:
    """
    Set system configuration.
    """
    # System configuration is global, So use ID=1.
    system_config = crud.system_config.get(db, id=1)
    if system_config:
        system_config = crud.system_config.update(db, db_obj=system_config, obj_in=user_in)
        if mqtt_cloud_server.MQTT_CLIENT:
            mqtt_cloud_server.MQTT_CLIENT.disconnect()
        mqtt_cloud_server.connect()
    else:
        system_config = crud.system_config.create(db, obj_in=user_in)
        mqtt_cloud_server.connect()

    return system_config


@router.get(
    "/{system_config_id}",
    response_model=schemas.SystemConfig,
    status_code=status.HTTP_200_OK,
    description="""
Get detailed info of System Config.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.SystemConfig, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get(
    system_config_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.SystemConfig:
    system_config = crud.system_config.get(db, id=system_config_id)
    if not system_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"System config [id: {system_config_id}] not found.",
        )
    return system_config
