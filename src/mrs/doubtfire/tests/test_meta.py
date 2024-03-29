# -*- coding: utf-8 -*-
from mrs.doubtfire.meta import emoji_by_elapsed
from mrs.doubtfire.meta import logger
from mrs.doubtfire.meta import metricmethod
from mrs.doubtfire.meta import sanitize_kwargs
from mrs.doubtfire.testing import MRS_DOUBTFIRE_INTEGRATION_TESTING  # noqa
from plone.testing.z2 import Browser

import logging
import re
import time
import unittest


class TestMeta(unittest.TestCase):

    layer = MRS_DOUBTFIRE_INTEGRATION_TESTING
    maxDiff = None

    def setUp(self):
        self.portal = self.layer["portal"]
        self.browser = Browser(self.layer["app"])
        logger.setLevel(logging.INFO)

    def test_sanitize_kwargs(self):
        kwargs = {
            "foo": "bar",
            "baz": "qux",
            "password": "corge",
        }
        expected = {"foo": "bar", "baz": "qux", "password": "***"}
        self.assertEqual(sanitize_kwargs(kwargs), expected)

    def test_sanitize_kwargs_log(self):
        with self.assertLogs("mrs.doubtfire", "INFO") as log:
            kwargs = {
                "foo": "bar",
                "baz": "qux",
                "password": "corge",
            }

            @metricmethod(level="debug")
            def fun(**kw):
                time.sleep(1)
                return kw

            res = fun(**kwargs)
            self.assertEqual(res, kwargs)
            logs = [re.sub(r"[0-9]{4}ms", "...", row) for row in log.output]
            self.assertEqual(
                [
                    "INFO:mrs.doubtfire:Request URL: http://nohost",
                    "INFO:mrs.doubtfire:func=mrs.doubtfire.tests.test_meta.fun "
                    "info=None args=() kwargs={'foo': 'bar', 'baz': 'qux', 'password': '***'} "
                    "elapsed=... threshold=-1ms 💩",
                ],
                logs,
            )

    def test_metrics(self):
        with self.assertLogs("mrs.doubtfire", "INFO") as log:
            self.browser.open(self.portal.absolute_url())
            logs = [
                re.sub(r"(object at 0x[0-9a-f]+|[0-9]+ms|[😎🤔💩])", "...", row)
                for row in log.output
            ]
            expecteds = [
                # 'INFO:mrs.doubtfire:func=zope.browserpage.simpleviewclass.__call__ '
                # 'info=plone.app.i18n.locales.languageselector elapsed=... threshold=... ...',
                # 'INFO:mrs.doubtfire:func=plone.app.layout.viewlets.common.render '
                # 'info=plone.documentbyline elapsed=... threshold=... ...',
                # 'INFO:mrs.doubtfire:func=plone.app.layout.viewlets.common.render '
                # 'info=plone.relateditems elapsed=... threshold=... ...',
                "INFO:mrs.doubtfire:Request URL: http://nohost/plone/document_view",
                "INFO:mrs.doubtfire:func=plone.portlets.manager.render "
                "info=plone.footerportlets "
                "args=(<plone.app.portlets.manager.ColumnPortletManagerRenderer ...>,) "
                "kwargs={} elapsed=... threshold=... ...",
                "INFO:mrs.doubtfire:func=plone.app.layout.viewlets.common.render "
                "info=plone.footer elapsed=... threshold=... ...",
            ]
            # XXX: This test is flaky, the order of the logs is not guaranteed
            for expected in expecteds:
                self.assertIn(expected, logs)

    def test_emoji(self):
        self.assertEqual("😎", emoji_by_elapsed(10))
        self.assertEqual("🤔", emoji_by_elapsed(99))
        self.assertEqual("💩", emoji_by_elapsed(999))
