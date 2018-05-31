#############################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##############################################################

import sys
import traceback
from abc import ABCMeta
from importlib import import_module

from werkzeug.utils import find_modules


class TestsGeneratorRegistry(ABCMeta):
    """
    class TestsGeneratorRegistry(object)
        Every module will be registered automatically by its module name.

    Class-level Methods:
    ----------- -------
    * __init__(...)
      - This is used to register test modules. You don't need to
      call this function explicitly. This will be automatically executed,
      whenever we create a class and inherit from BaseTestGenerator -
      it will register it as an available module in TestsGeneratorRegistry.
      By setting the __metaclass__ for BaseTestGenerator to
      TestsGeneratorRegistry it will create new instance of this
      TestsGeneratorRegistry per class.

    * load_generators():
      - This function will load all the modules from __init__()
      present in registry.
    """

    registry = dict()

    def __init__(cls, name, bases, d):

        # Register this type of module, based on the module name
        # Avoid registering the BaseDriver itself

        if name != 'BaseTestGenerator' and name != 'BaseFeatureTest':
            TestsGeneratorRegistry.registry[d['__module__']] = cls

        ABCMeta.__init__(cls, name, bases, d)

    @classmethod
    def load_generators(cls, pkg_root, exclude_pkgs):

        cls.registry = dict()

        all_modules = []

        all_modules += find_modules(pkg_root, False, True)

        # Check for SERVER mode
        for module_name in all_modules:
            try:
                if "tests." in str(module_name) and not any(
                    str(module_name).startswith(
                        'pgadmin.' + str(exclude_pkg)
                    ) for exclude_pkg in exclude_pkgs
                ):
                    import_module(module_name)
            except ImportError:
                traceback.print_exc(file=sys.stderr)
