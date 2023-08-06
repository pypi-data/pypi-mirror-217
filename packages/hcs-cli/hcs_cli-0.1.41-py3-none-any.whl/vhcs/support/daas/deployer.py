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

import subprocess
from vhcs.common.ctxp import context
from vhcs.plan.provider.azure import _az_facade as az
from . import helper
from vhcs.service import auth, admin

runtime = None
tenant_request = None

label_creating = '[Creating]'
label_skipped  = '[Skipped ]'
label_ok       = '[OK      ]'
label_error    = '[Error   ]'

def deploy(req: dict):
    
    global tenant_request, runtime
    tenant_request = req
    
    ctx_name = 'daas-runtime-' + tenant_request['deploymentId']
    runtime = context.get(ctx_name, default={})

    try:
        helper.prep_az_cli(tenant_request)
        _identify_location()
        _calculate_cidr()
        _create_resource_group()
        _create_nsg()
        _create_subnet()
        _register_subnet_to_provider()
        _get_idp_config()
        _create_azure_ad_users()
        _create_pool_template()
        _create_pool_group()
        _create_entitlement()
        _create_launch_items()
    except subprocess.CalledProcessError as e:
        return e
    except:
        raise
    finally:
        context.set('daas-runtime-' + tenant_request['deploymentId'], runtime)

def _res_name():
    return 'titan-lite-' + tenant_request['deploymentId']

def _create(type_name, name, impl):
    label = type_name + ": " + name
    print(label_creating, label)
    try:
        id = impl()
    except:
        print(label_error, label)
        raise
    if not id:
        id = name
    print(label_ok, type_name + ": " + id)
    
def _prep_az_cli():
    providerInstanceId = tenant_request['provider']['providerInstanceId']
    print('Provider:', providerInstanceId)
    providerInstance = admin.provider.get('azure', providerInstanceId)
    subscriptionId = providerInstance['providerDetails']['data']['subscriptionId']
    print('Subscription:', subscriptionId)
    az.set_subscription(subscriptionId)

def _identify_location():
    vnet = az.get_vnet(tenant_request['network']['vNetId'])
    runtime.vnet = vnet
    runtime.location = vnet['location']
    print('Region:', runtime.location)

def _calculate_cidr():
    #TODO
    cidr = "10.200.1.0/24"
    runtime.cidr = cidr
    print('Calculated CIDR: ' + cidr)

def _create_resource_group():
    rg_name = _res_name()
    def impl():
        rg = az.create_resource_group(location=runtime.location, name=rg_name)
        runtime.resource_group = rg
        return rg['id']
    _create('resource group', rg_name, impl)

def _create_nsg():
    if runtime.nsg:
        print(label_skipped, "nsg: " + runtime.nsg['id'])
        return
    
    name = _res_name()
    def impl():
        rg_name = runtime.vnet['resourceGroup']
        nsg_result = az.create_nsg(rg_name, name, runtime.location)
        nsg = nsg_result['NewNSG']
        runtime.nsg = nsg
        return nsg['id']
    _create("NSG", name, impl)

def _create_subnet():
    if runtime.subnet:
        print(label_skipped, "subnet: " + runtime.subnet['id'])
    name = _res_name()
    rg_name = runtime.vnet['resourceGroup']
    vnet_name = runtime.vnet['name']
    def impl():
        nsg_name = runtime.nsg['name']
        runtime.subnet = az.create_subnet(rg_name, vnet_name, name, runtime.cidr, nsg_name)
        return runtime.subnet['id']
    _create("subnet", rg_name + "/" + vnet_name + "/" + name, impl)

def _register_subnet_to_provider():
    pass
    # print("[+      ] register subnet to provider")
    # print("[created] register subnet to provider")

def _get_idp_config():
    runtime.idp_config = auth.admin.get_org_idp_map()
    print("[created] IDP config")

def _create_azure_ad_users():
    print("[TODO  ] Create AD users")


def _create_pool_template():
    template_name = _res_name()
    def impl():
        template_type = tenant_request['desktop']['templateType']
        number_of_users = len(tenant_request['userEmails'])
        is_multi_session = "MULTI_SESSION" == template_type
        total_vms = 1 if is_multi_session else number_of_users
        provider_id = tenant_request['provider']['providerInstanceId']

        uag_deployments = admin.helper.list_resources_by_provider('uag-deployments', provider_id, limit=1)
        if not uag_deployments:
            raise Exception("No UAG deployment found.")
        uag_deployment_id = uag_deployments[0]['id']

        edge_deployments = admin.helper.list_resources_by_provider('edge-deployments', provider_id, limit=1)
        if not edge_deployments:
            raise Exception("No UAG deployment found.")
        edge_deployment_id = edge_deployments[0]['id']

        search = f"name $eq {tenant_request['desktop']['vmSkuName']}"
        vm_skus = admin.azure_infra.get_compute_vm_skus(provider_instance_id=provider_id, search=search, limit=1)
        if not vm_skus:
            raise Exception("No VM SKUs found.")
        
        runtime.template = {
            "providerInstanceId": tenant_request['provider']["providerInstanceId"],
            "uagDeploymentId": uag_deployment_id,
            "edgeDeploymentId": edge_deployment_id,
            "orgId": tenant_request['orgId'],
            "name": template_name,
            "vmNamePattern": "d-",
            "templateType": template_type,
            "applicationProperties": {
                "azureActiveDirectoryJoined": "true"
            },
            "networks": [
                {
                    "kind": "subnets",
                    "id": runtime.subnet['id'],
                    "data": {
                        "parent": runtime.vnet['id'],
                        "name": runtime.subnet['name'],
                        "availableIpAddresses": 250,
                        "cidr": runtime.cidr
                    }
                }
            ],
            "imageReference": {
                "streamId": tenant_request['desktop']["streamId"],
                "markerId": tenant_request['desktop']["markerId"]
            },
            "licenseProvided": True,
            "desktopAdminUsername": "hcs-admin",
            "desktopAdminPassword": _generate_password(),
            "diskEncryption": {
                "enabled": False
            },
            "sparePolicy": {
                "limit": total_vms,
                "max": total_vms,
                "min": total_vms
            },
            "sessionsPerVm": number_of_users if is_multi_session else 1,
            "vmLicenseType": "WINDOWS_CLIENT",
            "diskSizeInGB": 127,
            "infrastructure": {
                "vmSkus": [vm_skus[0]]
            }
        }

        ret = admin.template.deploy(runtime.template)
        runtime.template_ret = ret
        return ret['id']
    _create("template", template_name, impl)

def _generate_password():
    from random import choice
    upper_chars = "ABCDEFGHJKLMNPQRSTUVWXY"
    readable_chars = "abcdefghjklmnpqrstuvwxy3456789"
    special_chars = "!@#$%_"
    return '' + choice(upper_chars) + ''.join(choice(readable_chars) for i in range(12)) + choice(special_chars)

def _create_pool_group():
    # pool_group_payload = {
    #     "orgId": request.getOrgId(),
    #     "name": request.getDesktopName() + "-" + RandomStringUtils.randomNumeric(5),
    #     "type": "DESKTOP",
    #     "templateType": request.getTemplateType(),
    #     "connectionAffinity": "NEAREST_SITE",
    #     "scope": "ALL_SITES",
    #     "enableSSO": False,
    #     "preferredClientType": "HORIZON_CLIENT",
    #     "protocols": [{
    #         "name": "BLAST",
    #         "defaultProtocol": True
    #     }],
    #     "templates": [{
    #         "id": template_id
    #     }]
    # }

    # return restTemplate.postForObject(String.format("%s/portal/v2/pools",
    #                 stackUrl),
    #         getHttpEntity("Bearer " + cspToken, poolGroupPayload), JsonNode.class);
    pass

def _create_entitlement():
    pass

def _create_launch_items():
    pass

