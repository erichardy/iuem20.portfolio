# -*- coding: utf-8 -*-
"""
Nous auront besoin des references :
http://docs.plone.org/external/plone.app.dexterity/docs/advanced/references.html
pour associer un projet a des missions et des portraits.
"""

from iuem20.portfolio import _
from iuem20.portfolio.interfaces import IPortfolio
from plone import api
from plone.dexterity.browser import add
from plone.dexterity.content import Container
from plonetheme.iuem20.utils import isPublished
from plonetheme.iuem20.utils import sort_by_position
from z3c.form import button
from zope.interface import implementer
from zope.publisher.browser import BrowserView

import logging


logger = logging.getLogger('iuem20.portfolio')


class PortfolioView(BrowserView):
    pass


@implementer(IPortfolio)
class portfolio(Container):

    def getPorfolioBG(self):
        try:
            bg = self.bg_css_class
            if len(bg) > 0:
                return bg
            else:
                return 'bg-dark'
        except Exception:
            return 'bg-dark'

    def getImgAuthor(self):
        """
        :return: L'auteur de l'image principale de la mission.
           Ou ``False`` si pas d'auteur
        """
        if not self.img_author:
            return False
        return self.img_author

    def getPortfolioAuthors(self):
        # c = self.context
        authors_folder = self.authors_pict_folder
        if len(authors_folder) > 0:
            try:
                f = self[authors_folder]
                founds = api.content.find(portal_type='Image',
                                          path='/'.join(f.getPhysicalPath()),
                                          depth=1,
                                          )
                # logger.info(founds)
                if len(founds) == 0:
                    return False
                objs = [i.getObject() for i in founds
                        if api.content.get_state(i.getObject()) == 'published']
                return sorted(objs, sort_by_position)
            except Exception:
                return False
        else:
            return False

    def getPortfolioImages(self):
        # c = self.context
        images = api.content.find(portal_type='Image',
                                  path='/'.join(self.getPhysicalPath()),
                                  depth=1,
                                  )
        # import pdb;pdb.set_trace()
        founds = images
        if len(founds) == 0:
            return False
        objs = [i.getObject() for i in founds if isPublished(i)]
        return sorted(objs, sort_by_position)

    def getImageSRC(self, image):
        """
        pour utiliser avec l'attribut src de <img src="....
        """
        if image.portal_type == 'Image':
            src = image.absolute_url() + '/@@download/image/'
            src += image.image.filename
            return src
        else:
            return image.absolute_url()

    def getPortfolioImagesSRC(self):
        founds = self.getPortfolioImages()
        # import pdb;pdb.set_trace()
        return [self.getImageSRC(i) for i in founds]

    def getPorfolioText(self):
        try:
            return self.presentation.output
        except Exception:
            return False


class AddForm(add.DefaultAddForm):
    portal_type = 'iuem20.portfolio'
    ignoreContext = True
    label = _(u'Add a new portfolio !')

    def update(self):
        super(add.DefaultAddForm, self).update()
        # logger.info('portfolio addForm : in update()')
        # logger.info(self.context)

    def updateWidgets(self):
        super(add.DefaultAddForm, self).updateWidgets()
        # logger.info(self.context)

    @button.buttonAndHandler(
        _(u'Save this portfolio'),
        name='save_this_portfolio')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = _('Please correct errors')
            return
        try:
            obj = self.createAndAdd(data)
            # logger.info(obj)
            # logger.info(u'=-=-=-=-=')
            context = self.context
            objId = obj.getId()
            url = context[objId].absolute_url()
            self.request.response.redirect(url)
        except Exception:
            raise

    @button.buttonAndHandler(_(u'Cancel this portfolio'))
    def handleCancel(self, action):
        data, errors = self.extractData()
        # context is the thesis repo
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)


class AddView(add.DefaultAddView):
    form = AddForm


"""
class editForm(edit.DefaultEditForm):
    pass
"""
