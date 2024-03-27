# -*- coding: utf-8 -*-
"""Init and utils."""
from collective.stats.pubtime import logger as stats_logger
from plone.app.viewletmanager.manager import BaseOrderedViewletManager

import functools
import logging


logger = logging.getLogger(__name__)


# TODO: move to zcml with info/handler (see c.monkeypatcher)
def addmetrics(f):
    from mrs.doubtfire.meta import metricmethod

    @functools.wraps(f)
    def wrapper(self, viewlets):
        # func_name = f.__name__
        viewlets = f(self, viewlets)
        for name, viewlet in viewlets:
            viewlet.render = metricmethod(threshold=50, info=name)(
                viewlet.render
            )  # noqa E501
        return viewlets

    return wrapper


# TODO: move to zcml with info/handler (see c.monkeypatcher)
BaseOrderedViewletManager.sort = addmetrics(BaseOrderedViewletManager.sort)


def portletmanager_info(self, *args, **kwargs):
    return self.manager.__name__


stats_logger_info_orig = stats_logger.info


def stats_logger_info(msg, *args, **kwargs):
    if len(args) == 15:
        (te, ta, tb, tr, lo, to, tc, mo, rm, pa, to, tc, tu, r1, r2) = args
        if int(mo) > 1 and rm not in ("POST", "PUT", "DELETE"):
            # objects modified ...
            logger.warning(
                "write during GET/HEAD request method:%s path:%s object modified:%s",  # noqa E501
                rm,
                pa,
                mo,
            )
    else:
        return stats_logger_info_orig(msg, *args, **kwargs)


stats_logger.info = stats_logger_info
