# Network Load Balancer

## Example Syntax

```yaml
    - name: Create Network Load Balancer
      ionoscloudsdk.ionoscloud.network_load_balancer:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        name: "{{ name }}"
        ips:
          - "10.12.118.224"
        listener_lan: "{{ listener_lan.lan.id }}"
        target_lan: "{{ target_lan.lan.id }}"
        wait: true
      register: nlb_response

    - name: Update Network Load Balancer
      ionoscloudsdk.ionoscloud.network_load_balancer:
        datacenter_id: "{{ datacenter_response.datacenter.id }}"
        network_load_balancer_id: "{{ nlb_response.network_load_balancer.id }}"
        name: "{{ name }} - UPDATE"
        listener_lan: "{{ listener_lan.lan.id }}"
        target_lan: "{{ target_lan.lan.id }}"
        wait: true
        state: update
      register: nlb_response_update

    - name: Remove Network Load Balancer
      ionoscloudsdk.ionoscloud.network_load_balancer:
       network_load_balancer_id: "{{ nlb_response.network_load_balancer.id }}"
       datacenter_id: "{{ datacenter_response.datacenter.id }}"
       wait: true
       state: absent
    
```

## Parameter Reference

The following parameters are supported:

| Name | Required | Type | Default | Description |
| :--- | :---: | :--- | :--- | :--- |
| name | **yes**/no | string |  | The name of the Network Load Balancer. Required only for state = 'present'.|
| listener_lan | **yes**/no | string |  | Id of the listening LAN. (inbound) Required only for state = 'present'. |
| ips | no | string |  | Collection of IP addresses of the Network Load Balancer. (inbound and outbound) IP of the listenerLan must be a customer reserved IP for the public load balancer and private IP for the private load balancer. |
| target_lan | **yes**/no | string |  | Id of the balanced private target LAN. (outbound) Required only for state = 'present'. |
| lb_private_ips | no | string |  | Collection of private IP addresses with subnet mask of the Network Load Balancer. IPs must contain valid subnet mask. If user will not provide any IP then the system will generate one IP with /24 subnet. |
| datacenter_id | **yes** | string |  | The ID of the datacenter. |
| network_load_balancer_id | **yes**/no | string |  | The ID of the Network Load Balancer. Required when state = 'update' or state = 'absent'. |
| api\_url | no | string |  | The Ionos API base URL. |
| username | no | string |  | The Ionos username. Overrides the IONOS\_USERNAME environement variable. |
| password | no | string |  | The Ionos password. Overrides the IONOS\_PASSWORD environement variable. |
| wait | no | boolean | true | Wait for the operation to complete before continuing. |
| wait\_timeout | no | integer | 600 | The number of seconds until the wait ends. |
| state | no | string | present | Indicate desired state of the resource: **present**, absent, update |

