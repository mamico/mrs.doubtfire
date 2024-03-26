# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import mrs.doubtfire


class MrsDoubtfireLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=mrs.doubtfire)


MRS_DOUBTFIRE_FIXTURE = MrsDoubtfireLayer()


MRS_DOUBTFIRE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MRS_DOUBTFIRE_FIXTURE,),
    name="MrsDoubtfireLayer:IntegrationTesting",
)


MRS_DOUBTFIRE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MRS_DOUBTFIRE_FIXTURE,),
    name="MrsDoubtfireLayer:FunctionalTesting",
)
