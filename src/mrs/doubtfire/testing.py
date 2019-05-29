# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import mrs.doubtfire


class MrsDoubtfireLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=mrs.doubtfire)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'mrs.doubtfire:default')


MRS_DOUBTFIRE_FIXTURE = MrsDoubtfireLayer()


MRS_DOUBTFIRE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MRS_DOUBTFIRE_FIXTURE,),
    name='MrsDoubtfireLayer:IntegrationTesting',
)


MRS_DOUBTFIRE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MRS_DOUBTFIRE_FIXTURE,),
    name='MrsDoubtfireLayer:FunctionalTesting',
)


MRS_DOUBTFIRE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        MRS_DOUBTFIRE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='MrsDoubtfireLayer:AcceptanceTesting',
)
