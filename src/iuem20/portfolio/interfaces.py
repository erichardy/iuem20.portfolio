# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective import dexteritytextindexer
from iuem20.portfolio import _
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope.interface import alsoProvides
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import Choice
from zope.schema import TextLine


class IIuem20PortfolioLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPortfolio(model.Schema):

    model.fieldset('general',
                   label=_(u'general'),
                   fields=['title',
                           'image',
                           'img_author',
                           'thumbnail',
                           'authors_pict_folder',
                           ])
    dexteritytextindexer.searchable('title')
    title = TextLine(title=_(u'portfolio title'),)

    image = NamedBlobImage(
        title=_(u'main photo'),
        required=False
        )
    img_author = TextLine(
        title=_(u'picture author'),
        required=False,
        )
    thumbnail = NamedBlobImage(
        title=_(u'small photo'),
        required=False
        )
    authors_pict_folder = TextLine(
        title=_(u'authors pictures'),
        description=_(u'folder of authors pictures, images only !'),
        required=False,
        default=u'authors',
        )
    #
    model.fieldset('presentation',
                   label=_(u'presentation'),
                   fields=['presentation', ])
    dexteritytextindexer.searchable('presentation')
    presentation = RichText(title=_(u'main presentation'),
                            description=_(u'presentation'),
                            required=False
                            )
    model.fieldset('configuration',
                   label=_(u'configuration'),
                   fields=['bg_css_class',
                           ])
    bg_css_class = Choice(
        title=_(u'CSS class for background'),
        required=True,
        vocabulary='iuem20.bg_classes',
        default=u'bg-dark',
        )
    #


alsoProvides(IPortfolio, IFormFieldProvider)
