#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#

# def pytest_generate_tests(metafunc):
#     print('\n\n\npytest_generate_tests\n\n\n')
#     idlist = []
#     argvalues = []
#     for scenario in metafunc.cls.scenarios:
#         idlist.append(scenario[0])
#         items = scenario[1].items()
#         argnames = [x[0] for x in items]
#         argvalues.append(([x[1] for x in items]))
#     metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")
import sys


def pytest_generate_tests(metafunc):
    print('Generation next')
    idlist = []
    argvalues = []
    argnames = []
    print('output', file=sys.stderr)
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [x[0] for x in items]
        argvalues.append(([x[1] for x in items]))
        print('bamm', file=sys.stderr)
    print('shebang', file=sys.stderr)
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class",
                         indirect=False)
