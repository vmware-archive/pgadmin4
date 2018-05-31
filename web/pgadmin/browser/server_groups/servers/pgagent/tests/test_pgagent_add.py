##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
import pytest
import simplejson as json
import uuid

from grappa import should

from regression.python_test_utils import test_utils as utils
from . import utils as pgagent_utils


class TestPgAgentAdd:
    def test_pg_agent_add(self, request, context_of_tests):
        """
        When the PG Agent add request is sent to the backend
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

        server_id = context_of_tests['server_information']['server_id']
        http_client = context_of_tests['test_client']
        pgagent_job = "test_job_add%s" % str(uuid.uuid4())[1:8]

        data = {
            'jobname': pgagent_job,
            'jobenabled': True,
            'jobhostagent': '',
            'jobjclid': 1,
            'jobdesc': '',
            'jsteps': [{
                'jstid': None,
                'jstjobid': None,
                'jstname': 'test_step',
                'jstdesc': '',
                'jstenabled': True,
                'jstkind': True,
                'jstconntype': True,
                'jstcode': 'SELECT 1;',
                'jstconnstr': None,
                'jstdbname': 'postgres',
                'jstonerror': 'f',
                'jstnextrun': '',
            }],
            'jschedules': [{
                'jscid': None,
                'jscjobid': None,
                'jscname': 'test_sch',
                'jscdesc': '',
                'jscenabled': True,
                'jscstart': '2050-01-01 12:14:21 +05:30',
                'jscend': None,
                'jscweekdays': [False] * 7,
                'jscmonthdays': [False] * 32,
                'jscmonths': [False] * 12,
                'jschours': [False] * 24,
                'jscminutes': [False] * 60,
                'jscexceptions': [],
            }],
        }

        response = http_client.post(
            '{0}{1}/{2}/'.format(
                url, utils.SERVER_GROUP, server_id
            ),
            data=json.dumps(data),
            content_type='html/json'
        )

        response.status_code | should.be.equal.to(200)

        response_data = json.loads(response.data)

        self.job_id = response_data['node']['_id']
        pgagent_utils.verify_pgagent_job(self) | \
            should.be.equal.to(True,
                               msg='pgAgent job was not created successfully')

    def tearDown(self):
        pgagent_utils.delete_pgagent_job(self)
