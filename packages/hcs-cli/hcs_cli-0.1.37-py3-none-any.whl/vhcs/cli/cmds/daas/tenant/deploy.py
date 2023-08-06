"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import json
import os
import random
import time
import yaml
import click
from vhcs.support.daas import deployer

@click.command()
@click.option("--file", "-f", type=str, required=True)
def deploy(file: str):
    """Deploy a tenant"""

    with open(file, "r") as file:
        payload = file.read()
    tenant_request = yaml.safe_load(payload)

    print('Deploying tenant:', tenant_request['tenantId'])

    ret = deployer.deploy(tenant_request)
    