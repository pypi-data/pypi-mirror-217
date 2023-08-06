##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
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
"""OnlineHelp Interfaces

These are the interfaces designed for the `OnlineHelp` system.

"""
__docformat__ = 'restructuredtext'

import zope.i18nmessageid
from zope.app.file.interfaces import IFile
from zope.app.publication.interfaces import IFileContent
from zope.configuration.fields import GlobalInterface
from zope.container.interfaces import IContainer
from zope.schema import Choice
from zope.schema import SourceText
from zope.schema import TextLine


_ = zope.i18nmessageid.MessageFactory("zope")


class IOnlineHelpTopic(IContainer):
    """A Topic is a single help page that you can view. Topics are able to
    contain other Topics and so on.

    You can also associate a Topic with a particular view.

    The Topic's content can be in the following four formats:

     - Plain Text,
     - HTML,
     - Structured Text (STX) and
     - Restructured Text (ReST).

    The Content is stored in a file and not the Topic itself.
    The file is only read when required.

    Note that all the Sub-Topic management is done via the utility service.
    The topic itself is stored in the IContainer implementation after add
    the right parent topic of a child. This mechanism ensures that we don't
    have to take care on the registration order.
    The topic resources are stored in the
    :class:`zope.container.interfaces.IContainer` implementation of the topic,
    too.
    """

    id = TextLine(
        title=_("Id"),
        description=_("The Id of this Help Topic"),
        default="",
        required=True)

    parentPath = TextLine(
        title=_("Parent Path"),
        description=_("The Path to the Parent of this Help Topic"),
        default="",
        required=False)

    title = TextLine(
        title=_("Help Topic Title"),
        description=_("The Title of a Help Topic"),
        default=_("Help Topic"),
        required=True)

    path = TextLine(
        title=_("Path to the Topic"),
        description=_("The Path to the Definition of a Help Topic"),
        default="./README.TXT",
        required=True)

    interface = GlobalInterface(
        title=_("Object Interface"),
        description=_("Interface for which this Help Topic is registered."),
        default=None,
        required=False)

    view = TextLine(
        title=_("View Name"),
        description=_("The View Name for which this Help Topic"
                      " is registered"),
        default=_(""),
        required=True)

    def addResources(resources):
        """Add resources to this Help Topic.

        The resources must be located in the same directory
        as the Help Topic itself.
        """

    def getTopicPath():
        """Return the presumed path to the topic, even the topic is not
        traversable from the onlinehelp."""

    def getSubTopics():
        """Returns IOnlineHelpTopic provided childs."""


class ISourceTextOnlineHelpTopic(IOnlineHelpTopic):
    """REstructed text based online help topic."""

    source = SourceText(
        title=_("Source Text"),
        description=_("Renderable source text of the topic."),
        default="",
        required=True,
        readonly=True)

    type = Choice(
        title=_("Source Type"),
        description=_("Type of the source text, e.g. structured text"),
        default="zope.source.rest",
        required=True,
        vocabulary="SourceTypes")


class IRESTOnlineHelpTopic(ISourceTextOnlineHelpTopic):
    """REstructed text based online help topic."""


class ISTXOnlineHelpTopic(ISourceTextOnlineHelpTopic):
    """Structed text based online help topic."""


class IZPTOnlineHelpTopic(IOnlineHelpTopic):
    """Page template based online help topic."""


class IOnlineHelp(ISourceTextOnlineHelpTopic):
    """The root of an onlinehelp hierarchy.

    Manages the registration of new topics.
    """

    def registerHelpTopic(parent_path, id, title, doc_path,
                          interface=None, view=None, resources=None):
        """This method registers a topic at the correct place.

        :param parent_path: Location of this topic's parent in the OnlineHelp
            tree. Need not to exist at time of creation.

        :param id: Specifies the id of the topic

        :param title: Specifies title of the topic. This title will be used in
            the tree as Identification.

        :param doc_path: -- Specifies where the file that contains the topic
            content is located.

        :keyword interface: Name of the interface for which the help topic is
            being registered. This can be optional, since not all topics must
            be bound to a particular interface.

        :keyword view: This attribute specifies the name of the view for which
            this topic is registered. Note that this attribute is also
            optional.

        :keyword resources: Specifies a list of resources for the topic, for
            example images that are included by the rendered topic content.
            Optional.
        """


class IOnlineHelpResource(IFile, IFileContent):
    """A resource, which can be used in a help topic """

    path = TextLine(
        title=_("Path to the Resource"),
        description=_("The Path to the Resource, assumed to be "
                      "in the same directory as the Help Topic"),
        default="",
        required=True)
