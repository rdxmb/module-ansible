# Changelog

## 5.0.1 \(21 December, 2020\)

### Features:

* **IPFailover** now supports dynamically generated IPs
* On **server creation** it is possible to specify an IP for the server's included NIC
* Added an option to **rename network interfaces** \(Update NIC operation\)

### Bug fixes:

* Fixed the return value of start/stop machine

### Enhancements:

* Changed the return values for the tasks. [Here](./usage/returnvalues.md) you can find the more details about the new templates.

### Misc:

* Rebranded the module from **profitbricks** to **ionos-cloud**
* Changed the python package to **ionoscloud** instead of **profitbricks**
* The **datacenter** and **nic** modules now have both _name_ and _id_ parameters, instead of just _name_

## Migration steps from [Profitbricks Module](https://github.com/ionos-enterprise/profitbricks-module-ansible) to [Ionos Cloud Module](https://github.com/ionos-cloud/sdk-ansible):

* install [ionoscloud python package](https://pypi.org/project/ionoscloud) using `pip install ionoscloud`
* set the `IONOS_USERNAME` and `IONOS_PASSWORD` environment variables \(instead of `PROFITBRICKS_USERNAME` and `PROFITBRICKS_PASSWORD`\)
* adapt the playbooks by:
  * using the return values decribed [here](./usage/returnvalues.md)
  * changing the module names in playbooks \(using find and replace\), eliminating the `profitbricks_` prefix:

    | profitbricks module | ionos-cloud module |
    | :--- | :--- |
    | profitbricks\_backupunit | backupunit |
    | profitbricks\_datacenter | datacenter |
    | profitbricks\_firewall\_rule | firewall\_rule |
    | profitbricks\_group | group |
    | profitbricks\_ipblock | ipblock |
    | profitbricks\_k8s\_cluster | k8s\_cluster |
    | profitbricks\_k8s\_config | k8s\_config |
    | profitbricks\_k8s\_nodepool | k8s\_nodepool |
    | profitbricks\_lan | lan |
    | profitbricks\_nic | nic |
    | profitbricks\_pcc | pcc |
    | profitbricks\_s3key | s3key |
    | profitbricks\_share | share |
    | profitbricks\_snapshot | snapshot |
    | profitbricks\_user | user |
    | profitbricks\_volume | volume |
    | profitbricks | server |

## 6.0.0-beta.1 \(May, 2021\)

### Features:

* Added the following modules:
    * cube_server
    * template
    * nat_gateway
    * nat_gateway_rule
    * nat_gateway_rule
    * network_load_balancer
    * network_load_balancer_flowlog
    * network_load_balancer_rule
    
### Misc:
* Removed `nat` parameter from **nic** and **server** module
* Added `user_password` parameter on **user** module


## 6.0.0-beta.2 (June, 2021)

### Features:
* Added a new module (`image`).  [Here](api/compute-engine/image.md) you can find the more details about this feature.
* New parameters on `volume` module:
    * image_alias
    * backupunit_id
    * user_data
    * cpu_hot_plug
    * ram_hot_plug
    * nic_hot_plug
    * nic_hot_unplug
    * disc_virtio_hot_plug
    * disc_virtio_hot_unplug
* New parameters on `server` module:
    * type
    * template_uuid
    * boot_volume
    * boot_cdrom
* Removed the `cube_server` module. Now the users can create **CUBE servers** using the `server` module.


## 6.0.0-beta.3 (September, 2021)

### Bug fixes:

* fixed issue: `Volume Module: HTTP 304 "Failed to parse request body" when attaching a volume to a server`

### Improvements:

* Added support for using image aliases when creating a volume. The modules now support _image ID, snapshot ID or 
  image alias_ values for the `image` parameter. If the image alias is provided, the module will resolve the image alias and
  use the correspondent image ID.
* new parameter for the `volume` module: `location` - used for identifying the image when image alias is used

## 6.0.0-beta.4 \(23 October, 2021\)

### Bug fixes:

* Remove the default value of `dhcp` parameter for `nic` module. The default value was `False`, which was not aligned with the CloudAPI swagger file.


## 6.0.0 (11 January, 2022)

### Bug fixes:

* fix #31 - group deletion
* fix create volume response -> it will return the entire list of created volumes, not an empty list anymore

### Enhancements:

* improved deletion on all resources -> when trying to delete a resource that does not exist, the module will not fail anymore and it will succeed with `changed: False`
* allow name updates for volumes
* fix #28 - added new group permissions according to the Cloud API
* user resource now supports password updates

### Misc:

* docs: updated the name of the module in examples


## 6.0.1

### Bug fixes:

* fix create volume bug that forced disk_type to be always `HDD` 

### Enhancements:

* add support for SSD storage _(new options for volume storage type: SSD Standard, SSD Premium)_ - **SSD Premium is the default** if disk_type=SSD


## 6.1.0

### Enhancements:

* add support for Dbaas Postgres: 3 new modules were added (postgres_cluster, postgres_cluster_info, postgres_backup_info)


## 6.1.1

### Enhancements:
* new parameters on *k8s_cluster* module: `public`, `api_subnet_allow_list` and `s3_buckets`
* new parameters on *k8s_nodepool* module: `gateway_ip`
* documentation updates related to Ansible Galaxy installation and usage


