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

from logging import LoggerAdapter

from fastapi import APIRouter, Depends, HTTPException, Query, status
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.post(
    "",
    response_model=schemas.RSUQuery,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new RSU Query.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.RSUQuery, "description": "Created"},
        status.HTTP_400_BAD_REQUEST: {"model": schemas.ErrorMessage, "description": "Bad Request"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def create(
    rsu_query_in: schemas.RSUQueryCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSUQuery:
    for rsu_id in rsu_query_in.rsus:
        rus_in_db = crud.rsu.get(db, id=rsu_id)
        if not rus_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"RSU [id: {rsu_id}] not found",
            )

    rsu_query_in_db = crud.rsu_query.create(db, obj_in=rsu_query_in)
    for rsu_id in rsu_query_in.rsus:
        crud.rsu_query_result.create(
            db, obj_in=schemas.RSUQueryResultCreate(query_id=rsu_query_in_db.id, rsu_id=rsu_id)
        )
    return rsu_query_in_db.to_dict()


@router.get(
    "/{rsu_query_id}",
    response_model=schemas.RSUQueryDetail,
    status_code=status.HTTP_200_OK,
    description="""
Get a RSU Query.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSUQueryDetail, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get(
    rsu_query_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSUQueryDetail:
    rsu_query_in_db = crud.rsu_query.get(db, id=rsu_query_id)
    if not rsu_query_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RSU Query [id: {rsu_query_id}] not found",
        )
    return schemas.RSUQueryDetail(**{"data": [v.to_all_dict() for v in rsu_query_in_db.results]})


@router.get(
    "",
    response_model=schemas.RSUQueries,
    status_code=status.HTTP_200_OK,
    description="""
Get all RSUQueries.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSUQueries, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def list(
    page_num: int = Query(1, alias="pageNum", gt=0, description="Page number"),
    page_size: int = Query(10, alias="pageSize", gt=0, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSUQueries:
    skip = page_size * (page_num - 1)
    total, data = crud.rsu_query.get_multi_with_total(db, skip=skip, limit=page_size)
    return schemas.RSUQueries(total=total, data=[rsu_query.to_dict() for rsu_query in data])
