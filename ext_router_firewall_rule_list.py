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

firewalls = neutron_client.list_firewalls()["firewalls"]
firewall_rules = neutron_client.list_firewall_rules()["firewall_rules"]
firewall_policys = neutron_client.list_firewall_policies()["firewall_policies"]

routers = neutron_client.list_routers()["routers"]

for policy in firewall_policys:
    for firewall in firewalls:
        for router in routers:
            if router["id"] == firewall["router_id"]:
                print "----"
                print "Router:"
                print "  name:   " + router["name"]
                if policy["id"] == firewall["firewall_policy_id"]:
                    print " firewall_rules: " + policy["name"]
                    for firewall_rule in firewall_rules:
                        print u"  description:              " + firewall_rule["description"]
                        if firewall_rule["protocol"] is not None:
                            print u"    protocol:               " + firewall_rule["protocol"]
                        else:
                            print u"    protocol:               " + "any"
                        print u"    source_ip_address:      " + firewall_rule["source_ip_address"]
                        print u"    source_port:            " + firewall_rule["source_port"]
                        print u"    destination_ip_address: " + firewall_rule["destination_ip_address"]
                        print u"    destination_port:       " + firewall_rule["destination_port"]
print "-----"
