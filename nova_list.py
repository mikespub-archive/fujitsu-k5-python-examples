from os import environ as env
from keystoneclient.v3 import client as kclient
from novaclient import client as nclient

keystone = kclient.Client(username=env['OS_USERNAME'],
                       password=env['OS_PASSWORD'],
                       user_domain_name=env['OS_DOMAIN_NAME'],
                       project_domain_name=env['OS_DOMAIN_NAME'],
                       project_name=env['OS_PROJECT_NAME'],
                       auth_url=env['OS_AUTH_URL'])

nova_endpoint_name_text = "compute".encode('utf-8')
nova_endpoint_url_text = "url".encode('utf-8')
nova_endpoint_url = keystone.service_catalog.get_endpoints()[nova_endpoint_name_text][0][nova_endpoint_url_text]

nova_client = nclient.Client("2.0",
                             auth_token=keystone.auth_token)
nova_client.set_management_url(nova_endpoint_url)

print nova_client.servers.list(detailed=True)
