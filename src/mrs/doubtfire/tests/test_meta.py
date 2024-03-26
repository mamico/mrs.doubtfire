# -*- coding: utf-8 -*-
from mrs.doubtfire.meta import logger
from mrs.doubtfire.meta import metricmethod
from mrs.doubtfire.meta import sanitize_kwargs
from mrs.doubtfire.testing import MRS_DOUBTFIRE_INTEGRATION_TESTING  # noqa

import logging
import time
import unittest


class TestMeta(unittest.TestCase):

    layer = MRS_DOUBTFIRE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
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
