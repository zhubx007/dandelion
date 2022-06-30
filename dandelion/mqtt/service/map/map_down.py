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

import logging
from typing import Any, Dict, Optional

from dandelion.mqtt import send_msg
from dandelion.mqtt.topic.map import v2x_rsu_map_down, v2x_rsu_map_down_all

logger = logging.getLogger(__name__)


def map_down(
    map_slice: str, map_: Dict[str, Any], e_tag: str, rsu_esn: Optional[str] = None
) -> None:
    data = dict(mapSlice=map_slice, map=map_, eTag=e_tag, ack=False)
    topic = v2x_rsu_map_down_all()
    if rsu_esn is not None:
        topic = v2x_rsu_map_down(rsu_esn)
    send_msg(topic, data)
