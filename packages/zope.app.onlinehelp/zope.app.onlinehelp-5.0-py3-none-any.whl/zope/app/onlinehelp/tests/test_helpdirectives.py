##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
"""Test the gts ZCML namespace directives.

"""
import unittest

import zope.app.component
import zope.app.security
import zope.traversing
from zope.component import testing
from zope.component.factory import Factory
from zope.component.interfaces import IFactory
from zope.configuration.xmlconfig import XMLConfig
from zope.interface import Interface
from zope.security.interfaces import IPermission
from zope.security.permission import Permission

import zope.app.onlinehelp
from zope.app.onlinehelp import globalhelp
from zope.app.onlinehelp import tests
from zope.app.onlinehelp.onlinehelptopic import OnlineHelpTopic
from zope.app.onlinehelp.onlinehelptopic import RESTOnlineHelpTopic
from zope.app.onlinehelp.onlinehelptopic import STXOnlineHelpTopic
from zope.app.onlinehelp.onlinehelptopic import ZPTOnlineHelpTopic


ztapi = tests


class I1(Interface):
    pass


class DirectivesTest(testing.PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super().setUp()
        ztapi.provideUtility(IPermission, Permission('zope.View', 'View', ''),
                             'zope.View')
        XMLConfig('meta.zcml', zope.app.security)()
        XMLConfig('meta.zcml', zope.app.component)()
        XMLConfig('meta.zcml', zope.app.onlinehelp)()
        XMLConfig('configure.zcml', zope.traversing)

        default = Factory(OnlineHelpTopic)
        rest = Factory(RESTOnlineHelpTopic)
        stx = Factory(STXOnlineHelpTopic)
        zpt = Factory(ZPTOnlineHelpTopic)
        ztapi.provideUtility(IFactory, default, 'onlinehelp.topic.default')
        ztapi.provideUtility(IFactory, rest, 'onlinehelp.topic.rest')
        ztapi.provideUtility(IFactory, stx, 'onlinehelp.topic.stx')
        ztapi.provideUtility(IFactory, zpt, 'onlinehelp.topic.zpt')

    def test_register(self):
        self.assertEqual(list(globalhelp.keys()), [])
        XMLConfig('help.zcml', tests)()
        res = ['help4', 'help5', 'help2', 'help3', 'help1']
        res.sort()

        helpList = sorted(globalhelp.keys())
        self.assertEqual(helpList, res)
        topic = globalhelp['help1']
        self.assertIn('test1.png', topic.keys())


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
