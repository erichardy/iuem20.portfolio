# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from iuem20.portfolio.testing import IUEM20_PORTFOLIO_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that iuem20.portfolio is properly installed."""

    layer = IUEM20_PORTFOLIO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if iuem20.portfolio is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'iuem20.portfolio'))

    def test_browserlayer(self):
        """Test that IIuem20PortfolioLayer is registered."""
        from iuem20.portfolio.interfaces import (
            IIuem20PortfolioLayer)
        from plone.browserlayer import utils
        self.assertIn(IIuem20PortfolioLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = IUEM20_PORTFOLIO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['iuem20.portfolio'])

    def test_product_uninstalled(self):
        """Test if iuem20.portfolio is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'iuem20.portfolio'))

    def test_browserlayer_removed(self):
        """Test that IIuem20PortfolioLayer is removed."""
        from iuem20.portfolio.interfaces import \
            IIuem20PortfolioLayer
        from plone.browserlayer import utils
        self.assertNotIn(IIuem20PortfolioLayer, utils.registered_layers())
