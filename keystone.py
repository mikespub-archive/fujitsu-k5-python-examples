from os import environ as env
from keystoneclient.v3 import client

keystone = client.Client(username=env['OS_USERNAME'],
                       password=env['OS_PASSWORD'],
                       user_domain_name=env['OS_DOMAIN_NAME'],
                       project_domain_name=env['OS_DOMAIN_NAME'],
                       project_name=env['OS_PROJECT_NAME'],
                       auth_url=env['OS_AUTH_URL'])
print  keystone.auth_token
