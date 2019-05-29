# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from mrs.doubtfire.testing import MRS_DOUBTFIRE_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that mrs.doubtfire is properly installed."""

    layer = MRS_DOUBTFIRE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if mrs.doubtfire is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'mrs.doubtfire'))

    def test_browserlayer(self):
        """Test that IMrsDoubtfireLayer is registered."""
        from mrs.doubtfire.interfaces import (
            IMrsDoubtfireLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IMrsDoubtfireLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = MRS_DOUBTFIRE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['mrs.doubtfire'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if mrs.doubtfire is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'mrs.doubtfire'))

    def test_browserlayer_removed(self):
        """Test that IMrsDoubtfireLayer is removed."""
        from mrs.doubtfire.interfaces import \
            IMrsDoubtfireLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IMrsDoubtfireLayer,
            utils.registered_layers())
