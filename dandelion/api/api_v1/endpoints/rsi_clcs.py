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

from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps

router = APIRouter()


@router.get(
    "",
    response_model=schemas.RSICLCs,
    status_code=status.HTTP_200_OK,
    description="""
Get all RSI CLCs.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSICLCs, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def list_rsi_clcs(
    info: Optional[int] = Query(None, alias="info", description="UseCase type"),
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSICLCs:
    skip = page_size * (page_num - 1)
    total, data = crud.rsi_clc.get_multi_with_total(
        db,
        skip=skip,
        limit=page_size,
        info=info,
    )
    return schemas.RSICLCs(total=total, data=[clc.to_all_dict() for clc in data])
