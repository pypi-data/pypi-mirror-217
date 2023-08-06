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
"""Schemas for the ``help`` ZCML namespace
"""
__docformat__ = 'restructuredtext'

from zope.configuration.fields import GlobalInterface
from zope.configuration.fields import GlobalObject
from zope.configuration.fields import MessageID
from zope.configuration.fields import Path
from zope.configuration.fields import Tokens
from zope.interface import Interface
from zope.schema import NativeStringLine
from zope.schema import TextLine


class IOnlineHelpTopicDirective(Interface):
    """Register an online topic.

    Optionally you can register a topic for a component and view.
    """

    id = NativeStringLine(
        title="Topic Id",
        description="Id of the topic as it will appear in the URL.",
        required=True)

    title = MessageID(
        title="Title",
        description="Provides a title for the online Help Topic.",
        required=True)

    parent = NativeStringLine(
        title="Parent Topic",
        description="Id of the parent topic.",
        default="",
        required=False)

    for_ = GlobalInterface(
        title="Object Interface",
        description="Interface for which this Help Topic is registered.",
        default=None,
        required=False)

    view = NativeStringLine(
        title="View Name",
        description="The view name for which this Help Topic is registered.",
        default="",
        required=False)

    doc_path = Path(
        title="Path to File",
        description="Path to the file that contains the Help Topic content.",
        required=True)

    class_ = GlobalObject(
        title="Factory",
        description="""
        The factory is the topic class used for initializeing the topic""",
        required=False,
    )

    resources = Tokens(
        title="A list of resources.",
        description="""
        A list of resources which shall be used for the Help Topic.
        The resources must be located in the same directory as
        the Help Topic definition.
        """,
        value_type=TextLine(),
        required=False
    )
