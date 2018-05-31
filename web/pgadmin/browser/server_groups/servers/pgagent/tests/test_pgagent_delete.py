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

from regression.python_test_utils import test_utils as utils
from . import utils as pgagent_utils


class TestPgAgentDelete:
    def test_pg_agent_delete(self, request, context_of_tests):
        """
        When the PG Agent delete request is sent to the backend
        it returns 200 status
        """

        request.addfinalizer(self.tearDown)

        self.tester = context_of_tests['test_client']
        self.server = context_of_tests['server']

        flag, message = pgagent_utils.is_valid_server_to_run_pgagent(self)
        if not flag:
            pytest.skip(message)

        flag, message = pgagent_utils.is_pgagent_installed_on_server(self)
        if not flag:
            pytest.skip(message)

        url = '/browser/pga_job/obj/'

        name = "test_job_delete%s" % str(uuid.uuid4())[1:8]
        self.job_id = pgagent_utils.create_pgagent_job(self, name)

        response = self.tester.delete(
            '{0}{1}/{2}/{3}'.format(
                url, str(utils.SERVER_GROUP), str(self.server_id),
                str(self.job_id)
            ),
            content_type='html/json'
        )

        response.status_code | should.be.equal.to(200)
        pgagent_utils.verify_pgagent_job(self) | \
            should.be.equal.to(False,
                               msg='pgAgent job was not deleted successfully')

    def tearDown(self):
        pgagent_utils.delete_pgagent_job(self)
