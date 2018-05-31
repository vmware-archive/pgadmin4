##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import uuid

import pytest
from grappa import should

from pgadmin.utils.base_test_generator import BaseTestGenerator, \
    PostgresVersion
from regression.python_test_utils import test_utils as utils
from . import utils as resource_groups_utils


@pytest.mark.skip_databases(['pg'])
@pytest.mark.skip_if_postgres_version({'below_version': PostgresVersion.v94},
                                      'Resource groups are not supported '
                                      'by PG9.3 '
                                      'and PPAS9.3 and below.')
class TestResourceGroupsDelete(BaseTestGenerator):
    def test_delete_resource_group(self, request, context_of_tests):
        """
        When request to delete a resource group is valid
        It returns success
        """
        request.addfinalizer(self.tearDown)

        self.server = context_of_tests['server']
        server_id = context_of_tests['server_information']['server_id']
        url = '/browser/resource_group/obj/'
        http_client = context_of_tests['test_client']

        self.resource_group = "test_resource_group_delete%s" % \
                              str(uuid.uuid4())[1:8]
        resource_group_id = resource_groups_utils.create_resource_groups(
            self.server, self.resource_group)
        resource_grp_response = resource_groups_utils.verify_resource_group(
            self.server, self.resource_group)
        if not resource_grp_response:
            raise Exception("Could not find the resource group to fetch.")

        response = http_client.delete(
            "{0}{1}/{2}/{3}".format(
                url,
                utils.SERVER_GROUP,
                server_id,
                resource_group_id),
            follow_redirects=True)

        response.status_code | should.be.equal(200)

    def tearDown(self):
        connection = utils.get_db_connection(self.server['db'],
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'],
                                             self.server['sslmode'])
        resource_groups_utils.delete_resource_group(connection,
                                                    self.resource_group)
