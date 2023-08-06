##############################################################################
#
# Copyright (c) 2002, 2003 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Test OnlineHelp

"""
import os
import re
import unittest
from doctest import DocTestSuite

import zope.traversing
from zope.component import testing
from zope.configuration import xmlconfig
from zope.interface import Interface
from zope.interface import implementer
from zope.testing import renormalizing

from zope.app.onlinehelp import onlinehelp
from zope.app.onlinehelp import onlinehelptopic


class I1(Interface):
    pass


@implementer(I1)
class Dummy1:
    pass


class Dummy2:
    pass


class TestOnlineHelpResource(unittest.TestCase):

    def test_size(self):
        r = onlinehelptopic.OnlineHelpResource(
            os.path.join(testdir(), 'help.html'))
        self.assertEqual(20, r.getSize())


class TestBaseOnlineHelpTopic(unittest.TestCase):

    def test_bad_path(self):
        from zope.configuration.exceptions import ConfigurationError

        self.assertRaises(
            ConfigurationError,
            onlinehelptopic.BaseOnlineHelpTopic,
            'id', 'title', 'path that does not exist',
            'parentpath')


class TestOnlineHelp(unittest.TestCase):

    def test_bad_path(self):
        from zope.configuration.exceptions import ConfigurationError
        the_help = onlinehelp.OnlineHelp('title', testdir())

        self.assertRaises(
            ConfigurationError,
            the_help.registerHelpTopic,
            'parentpath', 'id', 'title',
            'path that does not exist')


class TestOnlineHelpNamespace(unittest.TestCase):

    def test_context(self):
        from zope.app.onlinehelp import globalhelp
        from zope.app.onlinehelp import helpNamespace

        traversed = helpNamespace(self).traverse(None, None)
        self.assertIs(traversed.context, self)
        self.assertIsNone(getattr(globalhelp, 'context', None))

    def test_cannot_pickle(self):
        import pickle

        from zope.app.onlinehelp import helpNamespace

        traversed = helpNamespace(self).traverse(None, None)
        self.assertRaises(TypeError,
                          pickle.dumps, traversed)


def testdir():
    return os.path.dirname(__file__)


def setUp(tests):
    testing.setUp()
    xmlconfig.file('configure.zcml', zope.traversing)


def test_suite():
    checker = renormalizing.RENormalizing((
        (re.compile(r"u('.*')"), r'\1'),
    ))

    return unittest.TestSuite((
        DocTestSuite('zope.app.onlinehelp',
                     setUp=setUp, tearDown=testing.tearDown,
                     checker=checker),
        DocTestSuite('zope.app.onlinehelp.onlinehelptopic',
                     setUp=setUp, tearDown=testing.tearDown,
                     checker=checker),
        DocTestSuite('zope.app.onlinehelp.onlinehelp',
                     setUp=setUp, tearDown=testing.tearDown,
                     checker=checker),
        unittest.defaultTestLoader.loadTestsFromName(__name__),
    ))
