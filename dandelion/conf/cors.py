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

from oslo_config import cfg

cors_group = cfg.OptGroup(
    name="cors",
    title="CORS Options",
    help="""
CORS related options.
""",
)

cors_opts = [
    cfg.ListOpt(
        "origins",
        default=[],
        help="""
CORS origins.
""",
    ),
]


def register_opts(conf):
    conf.register_group(cors_group)
    conf.register_opts(cors_opts, group=cors_group)


def list_opts():
    return {cors_group: cors_opts}
