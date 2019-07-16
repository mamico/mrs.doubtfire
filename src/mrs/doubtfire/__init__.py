# -*- coding: utf-8 -*-
"""Init and utils."""
import logging
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('mrs.doubtfire')
logger = logging.getLogger(__name__)


# BBB: usare monkeypatcher
from mrs.doubtfire.meta import metricmethod
from plone.app.viewletmanager.manager import BaseOrderedViewletManager
import functools


def addmetrics(f):
    @functools.wraps(f)
    def wrapper(self, viewlets):
        func_name = f.__name__
        viewlets = f(self, viewlets)
        for name, viewlet in viewlets:
            viewlet.render = metricmethod(threshold=50, info=name)(viewlet.render)
        return viewlets
    return wrapper


BaseOrderedViewletManager.sort = addmetrics(BaseOrderedViewletManager.sort)


# BBB: monkey patch al logger di c.stats
from collective.stats.pubtime import logger as stats_logger
stats_logger_info_orig = stats_logger.info
def stats_logger_info(msg, *args, **kwargs):
    if len(args) == 15:
        (te, ta, tb, tr, lo, to, tc, mo, rm, pa, to, tc, tu, r1, r2) = args
        if int(mo) > 1 and rm not in ('POST', 'PUT', 'DELETE'):
            # objects modified ... 
            logger.warning('write during GET/HEAD request method:%s path:%s object modified:%s', rm, pa, mo)
    else:
        return stats_logger_info_orig(msg, *args, **kwargs)
stats_logger.info = stats_logger_info
