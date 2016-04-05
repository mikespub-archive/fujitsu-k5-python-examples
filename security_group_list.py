from os import environ as env
from keystoneclient.v3 import client as kclient
from neutronclient.v2_0 import client as nclient

keystone = kclient.Client(username=env['OS_USERNAME'],
                       password=env['OS_PASSWORD'],
                       user_domain_name=env['OS_DOMAIN_NAME'],
                       project_domain_name=env['OS_DOMAIN_NAME'],
                       project_name=env['OS_PROJECT_NAME'],
                       auth_url=env['OS_AUTH_URL'])

neutron_endpoint_name_text = "network".encode('utf-8')
neutron_endpoint_url_text = "url".encode('utf-8')
neutron_endpoint_url = keystone.service_catalog.get_endpoints()[neutron_endpoint_name_text][0][neutron_endpoint_url_text]

neutron_client = nclient.Client(token=keystone.auth_token,
                                endpoint_url = neutron_endpoint_url)


for group in neutron_client.list_security_groups()["security_groups"]:
    print "-----------"
    print u"ID:          " + group["id"]
    print u"Description: " + group["description"]
    print u"security_group_rules:"

    for security_group_rules in group["security_group_rules"]:
        print " ------"
        print u" ID:                 " + security_group_rules["id"]
        if security_group_rules["protocol"] is not None:
            print u"  protocol:          " + security_group_rules["protocol"]
        else:
            print u"  protocol:          " + "any"                
        print u"  direction:         " + security_group_rules["direction"]
        print u"  ethertype:         " + security_group_rules["ethertype"]
        if security_group_rules["remote_ip_prefix"] is not None:
            print u"  remote_ip_prefix:  " + security_group_rules["remote_ip_prefix"]
        print u"  port_range_min:    " + str(security_group_rules["port_range_min"])
        print u"  port_range_max:    " + str(security_group_rules["port_range_max"])
    print "--"
