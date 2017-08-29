# -*- coding: utf-8 -*-
from iuem20.portfolio.interfaces import Iportfolio
from iuem20.portfolio.testing import IUEM20_PORTFOLIO_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class portfolioIntegrationTest(unittest.TestCase):

    layer = IUEM20_PORTFOLIO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='portfolio')
        schema = fti.lookupSchema()
        self.assertEqual(Iportfolio, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='portfolio')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='portfolio')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(Iportfolio.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='portfolio',
            id='portfolio',
        )
        self.assertTrue(Iportfolio.providedBy(obj))
