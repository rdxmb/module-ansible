#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

HAS_SDK = True

try:
    import ionoscloud
    from ionoscloud import __version__ as sdk_version
    from ionoscloud.models import NetworkLoadBalancer, NetworkLoadBalancerProperties
    from ionoscloud.rest import ApiException
    from ionoscloud import ApiClient
except ImportError:
    HAS_SDK = False

from ansible import __version__
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils._text import to_native

uuid_match = re.compile(
    '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', re.I)


def _get_resource(resource_list, identity):
    """
    Fetch and return a resource regardless of whether the name or
    UUID is passed. Returns None error otherwise.
    """

    for resource in resource_list.items:
        if identity in (resource.properties.name, resource.id):
            return resource.id

    return None


def _update_nlb(module, client, nlb_server, datacenter_id, network_load_balancer_id, nlb_properties):
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    response = nlb_server.datacenters_networkloadbalancers_patch_with_http_info(datacenter_id, network_load_balancer_id,
                                                                                nlb_properties)
    (nlb_response, _, headers) = response

    if wait:
        request_id = _get_request_id(headers['Location'])
        client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    return nlb_response


def _get_request_id(headers):
    match = re.search('/requests/([-A-Fa-f0-9]+)/', headers)
    if match:
        return match.group(1)
    else:
        raise Exception("Failed to extract request ID from response "
                        "header 'location': '{location}'".format(location=headers['location']))


def create_nlb(module, client):
    """
    Creates a Network Load Balancer

    This will create a new Network Load Balancer in the specified Datacenter.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        The Network Load Balancer ID if a new Network Load Balancer was created.
    """
    datacenter_id = module.params.get('datacenter_id')
    name = module.params.get('name')
    ips = module.params.get('ips')
    listener_lan = module.params.get('listener_lan')
    target_lan = module.params.get('target_lan')
    lb_private_ips = module.params.get('lb_private_ips')

    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))

    nlb_server = ionoscloud.NetworkLoadBalancersApi(client)
    nlb_list = nlb_server.datacenters_networkloadbalancers_get(datacenter_id=datacenter_id, depth=2)
    nlb_response = None

    for nlb in nlb_list.items:
        if name == nlb.properties.name:
            return {
                'changed': False,
                'failed': False,
                'action': 'create',
                'network_load_balancer': nlb.to_dict()
            }

    nlb_properties = NetworkLoadBalancerProperties(name=name, listener_lan=listener_lan, ips=ips, target_lan=target_lan,
                                                   lb_private_ips=lb_private_ips)
    network_load_balancer = NetworkLoadBalancer(properties=nlb_properties)

    try:
        response = nlb_server.datacenters_networkloadbalancers_post_with_http_info(datacenter_id, network_load_balancer)
        (nlb_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

    except ApiException as e:
        module.fail_json(msg="failed to create the new Network Load Balancer: %s" % to_native(e))

    return {
        'changed': True,
        'failed': False,
        'action': 'create',
        'network_load_balancer': nlb_response.to_dict()
    }


def update_nlb(module, client):
    """
    Updates a Network Load Balancer.

    This will update a Network Load Balancer.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Network Load Balancer was updated, false otherwise
    """
    datacenter_id = module.params.get('datacenter_id')
    name = module.params.get('name')
    ips = module.params.get('ips')
    listener_lan = module.params.get('listener_lan')
    target_lan = module.params.get('target_lan')
    lb_private_ips = module.params.get('lb_private_ips')
    network_load_balancer_id = module.params.get('network_load_balancer_id')

    nlb_server = ionoscloud.NetworkLoadBalancersApi(client)
    nlb_response = None
    changed = False

    if network_load_balancer_id:
        nlb_properties = NetworkLoadBalancerProperties(name=name, listener_lan=listener_lan, ips=ips,
                                                       target_lan=target_lan,
                                                       lb_private_ips=lb_private_ips)
        nlb_response = _update_nlb(module, client, nlb_server, datacenter_id, network_load_balancer_id,
                                   nlb_properties)
        changed = True

    else:
        nlb_list = nlb_server.datacenters_networkloadbalancers_get(datacenter_id=datacenter_id, depth=2)
        for nlb in nlb_list.items:
            if name == nlb.properties.name:
                nlb_properties = NetworkLoadBalancerProperties(name=name, listener_lan=listener_lan, ips=ips,
                                                               target_lan=target_lan,
                                                               lb_private_ips=lb_private_ips)
                nlb_response = _update_nlb(module, client, nlb_server, datacenter_id, nlb.id,
                                           nlb_properties)
                changed = True

    if not changed:
        module.fail_json(msg="failed to update the Network Load Balancer: The resource does not exist")

    return {
        'changed': changed,
        'action': 'update',
        'failed': False,
        'network_load_balancer': nlb_response.to_dict()
    }


def remove_nlb(module, client):
    """
    Removes a Network Load Balancer.

    This will remove a Network Load Balancer.

    module : AnsibleModule object
    client: authenticated ionoscloud object.

    Returns:
        True if the Network Load Balancer was deleted, false otherwise
    """
    name = module.params.get('name')
    datacenter_id = module.params.get('datacenter_id')
    network_load_balancer_id = module.params.get('network_load_balancer_id')

    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')

    nlb_server = ionoscloud.NetworkLoadBalancersApi(client)
    changed = False

    try:

        network_load_balancer_list = nlb_server.datacenters_networkloadbalancers_get(datacenter_id=datacenter_id, depth=5)
        if network_load_balancer_id:
            network_load_balancer = _get_resource(network_load_balancer_list, network_load_balancer_id)
        else:
            network_load_balancer = _get_resource(network_load_balancer_list, name)

        if not network_load_balancer:
            module.exit_json(changed=False)

        response = nlb_server.datacenters_networkloadbalancers_delete_with_http_info(datacenter_id, network_load_balancer)
        (nlb_response, _, headers) = response

        if wait:
            request_id = _get_request_id(headers['Location'])
            client.wait_for_completion(request_id=request_id, timeout=wait_timeout)

        changed = True

    except Exception as e:
        module.fail_json(
            msg="failed to delete the Network Load Balancer: %s" % to_native(e))

    return {
        'action': 'delete',
        'changed': changed,
        'id': network_load_balancer_id
    }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            listener_lan=dict(type='str'),
            ips=dict(type='list', default=None),
            target_lan=dict(type='str'),
            lb_private_ips=dict(type='list', default=None),
            datacenter_id=dict(type='str'),
            network_load_balancer_id=dict(type='str'),
            api_url=dict(type='str', default=None, fallback=(env_fallback, ['IONOS_API_URL'])),
            username=dict(
                type='str',
                required=True,
                aliases=['subscription_user'],
                fallback=(env_fallback, ['IONOS_USERNAME'])
            ),
            password=dict(
                type='str',
                required=True,
                aliases=['subscription_password'],
                fallback=(env_fallback, ['IONOS_PASSWORD']),
                no_log=True
            ),
            wait=dict(type='bool', default=True),
            wait_timeout=dict(type='int', default=600),
            state=dict(type='str', default='present'),
        ),
        supports_check_mode=True
    )
    if not HAS_SDK:
        module.fail_json(msg='ionoscloud is required for this module, run `pip install ionoscloud`')

    username = module.params.get('username')
    password = module.params.get('password')
    api_url = module.params.get('api_url')
    user_agent = 'ansible-module/%s_ionos-cloud-sdk-python/%s' % ( __version__, sdk_version)

    state = module.params.get('state')

    conf = {
        'username': username,
        'password': password,
    }

    if api_url is not None:
        conf['host'] = api_url
        conf['server_index'] = None

    configuration = ionoscloud.Configuration(**conf)


    with ApiClient(configuration) as api_client:
        api_client.user_agent = user_agent
        if state == 'absent':
            if not (module.params.get('name') or module.params.get('network_load_balancer_id')):
                module.fail_json(
                    msg='name parameter or network_load_balancer_id parameter are required for deleting a Network Load Balancer.')
            try:
                (result) = remove_nlb(module, api_client)
                module.exit_json(**result)

            except Exception as e:
                module.fail_json(msg='failed to set Network Load Balancer state: %s' % to_native(e))

        elif state == 'present':
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for a new Network Load Balancer')
            if not module.params.get('listener_lan'):
                module.fail_json(msg='listener_lan parameter is required for a new Network Load Balancer')
            if not module.params.get('target_lan'):
                module.fail_json(msg='target_lan parameter is required for a new Network Load Balancer')

            try:
                (nlb_dict) = create_nlb(module, api_client)
                module.exit_json(**nlb_dict)
            except Exception as e:
                module.fail_json(msg='failed to set Network Load Balancer state: %s' % to_native(e))

        elif state == 'update':
            if not module.params.get('datacenter_id'):
                module.fail_json(msg='datacenter_id parameter is required for updating a Network Load Balancer')
            if not module.params.get('name'):
                module.fail_json(msg='name parameter is required for updating a Network Load Balancer')
            if not module.params.get('listener_lan'):
                module.fail_json(msg='listener_lan parameter is required for updating a Network Load Balancer')
            if not module.params.get('target_lan'):
                module.fail_json(msg='target_lan parameter is required for updating a Network Load Balancer')
            if not (module.params.get('name') or module.params.get('network_load_balancer_id')):
                module.fail_json(
                    msg='name parameter or network_load_balancer_id parameter are required updating a Network Load Balancer.')
            try:
                (nlb_dict) = update_nlb(module, api_client)
                module.exit_json(**nlb_dict)
            except Exception as e:
                module.fail_json(msg='failed to update the Network Load Balancer: %s' % to_native(e))


if __name__ == '__main__':
    main()
