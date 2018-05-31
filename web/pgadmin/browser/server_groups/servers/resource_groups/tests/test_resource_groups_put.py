##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import json
import uuid

import pytest
from grappa import should

from pgadmin.utils.base_test_generator import PostgresVersion
from regression.python_test_utils import test_utils as utils
from . import utils as resource_groups_utils


@pytest.mark.skip_databases(['pg'])
@pytest.mark.skip_if_postgres_version({'below_version': PostgresVersion.v94},
                                      'Resource groups are not supported '
                                      'by PG9.3 '
                                      'and PPAS9.3 and below.')
class TestResourceGroupsPut:
    def test_delete_resource_group(self, request, context_of_tests):
        """
        When request to update a resource group is valid
        It returns success
        """
        request.addfinalizer(self.tearDown)

        url = '/browser/resource_group/obj/'
        http_client = context_of_tests['test_client']

        self.server = context_of_tests['server']
        self.server_id = context_of_tests['server_information']['server_id']

        initial_resource_group_name = "test_resource_group_put%s" % \
                                      str(uuid.uuid4())[1:8]
        self.resource_group_id = resource_groups_utils.create_resource_groups(
            self.server,
            initial_resource_group_name)
        resource_grp_response = resource_groups_utils.verify_resource_group(
            self.server,
            initial_resource_group_name)
        if not resource_grp_response:
            raise Exception("Could not find the resource group to fetch.")

        self.updated_resource_group_name = "test_resource_group_put%s" % \
                                           str(uuid.uuid4())[1:8]

        data = {"id": self.resource_group_id,
                "name": self.updated_resource_group_name}
        response = http_client.put('{0}{1}/{2}/{3}'.format(
            url,
            utils.SERVER_GROUP,
            self.server_id,
            self.resource_group_id), data=json.dumps(data),
            follow_redirects=True)

        response.status_code | should.be.equal(200)

    def tearDown(self):
        connection = utils.get_db_connection(self.server['db'],
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'],
                                             self.server['sslmode'])
        resource_groups_utils.delete_resource_group(
            connection,
            self.updated_resource_group_name)
