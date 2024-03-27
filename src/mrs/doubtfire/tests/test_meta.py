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
            self.assertEqual(
                [
                    "INFO:mrs.doubtfire:Request URL: http://nohost",
                    "INFO:mrs.doubtfire:func=mrs.doubtfire.tests.test_meta.fun "
                    "info=None args=() kwargs={'foo': 'bar', 'baz': 'qux', 'password': '***'} "
                    "elapsed=1000ms threshold=-1ms 💩",
                ],
                log.output,
            )

    def test_metrics(self):
        with self.assertLogs("mrs.doubtfire", "INFO") as log:
            self.browser.open(self.portal.absolute_url())
            self.assertEqual(
                [
                    "INFO:mrs.doubtfire:Request URL: http://nohost/plone/document_view",
                    "INFO:mrs.doubtfire:func=plone.portlets.manager.render "
                    "info=plone.footerportlets "
                    "args=(<plone.app.portlets.manager.ColumnPortletManagerRenderer ...>,) "
                    "kwargs={} elapsed=... threshold=... ...",
                    "INFO:mrs.doubtfire:func=plone.app.layout.viewlets.common.render "
                    "info=plone.footer elapsed=... threshold=... ...",
                ],
                [
                    re.sub(r"(object at 0x[0-9a-f]+|[0-9]+ms|s[😎🤔💩])", "...", row)
                    for row in log.output
                ],
            )

    def test_emoji(self):
        self.assertEqual("😎", emoji_by_elapsed(10))
        self.assertEqual("🤔", emoji_by_elapsed(99))
        self.assertEqual("💩", emoji_by_elapsed(999))
