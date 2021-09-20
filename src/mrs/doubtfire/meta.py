# -*- coding: utf-8 -*-
"""ZCML handling"""
from time import time
import functools
from zope.configuration.exceptions import ConfigurationError
from zope.configuration.fields import GlobalObject, PythonIdentifier
from zope.event import notify
from zope.interface import Interface, implementer
from zope.schema import Int, Bool, TextLine

import pkg_resources
import re
from six.moves import map

from . import interfaces
from . import logger


class IMetricsDirective(Interface):
    """ZCML directive
    """

    class_ = GlobalObject(
        title=u"The class being patched",
        required=False)
    module = GlobalObject(
        title=u"The module being patched",
        required=False)
    method = PythonIdentifier(title=u"Method or function to measure")
    info = GlobalObject(
        title=u"A function to get info.",
        description=(u"Must take same parameters as method, or function, to measure"),
        required=False)
    threshold = Int(
        title=u"Min execution time for logging (ms)",
        required=False,
        default=-1)
    level = TextLine(
        title=u"Logging level",
        required=False,
        default=u'info')


def metrics(
        _context,
        method,
        class_=None,
        module=None,
        info=None,
        threshold=-1,
        level='info'):
    """ZCML directive handler"""
    if class_ is None and module is None:
        raise ConfigurationError(u"You must specify 'class' or 'module'")
    if class_ is not None and module is not None:
        raise ConfigurationError(
            u"You must specify one of 'class' or 'module', but not both.")

    scope = class_ or module

    to_be_measured = getattr(scope, method, None)

    if to_be_measured is None:
        raise ConfigurationError(
            "Original %s in %s not found" % (method, str(scope)))

    _context.action(
        discriminator=None,
        callable=_do_perfmetrics,
        args=(scope, method, threshold, level, info))
    return


def _do_perfmetrics(scope, method, threshold=-1, level='info', info=None):
    logger.info(u"👵 monitoring %s.%s threshold=%s, level=%s, info=%s", scope.__name__, method, threshold, level, info)
    setattr(scope, method, metricmethod(threshold=threshold, level=level, info=info)(getattr(scope, method)))


def emoji_by_elapsed(elapsed):
    if elapsed < 20:
        return u'\U0001F60E'  # GOOD
    elif elapsed < 100:
        return u'\U0001F914'  # MUMBLE
    else:
        return u'\U0001F4A9'  # SHIT


# http://stackoverflow.com/questions/3931627/how-to-build-a-python-decorator-with-optional-parameters
def metricmethod(*args, **kwargs):
    info = None
    def _metricmethod(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                func_name = f.__name__
                func_full_name = '%s.%s' % (f.__module__, func_name)
            except AttributeError:
                func_full_name = f.__self__.__name__
            start = time()
            try:
                return f(*args, **kwargs)
            finally:
                elapsed = int((time() - start) * 1000.0)
                if elapsed > threshold:
                    if level == 'debug':
                        logger.info(u'func=%s info=%s args=%s kwargs=%s elapsed=%sms threshold=%sms %s',
                                    func_full_name,
                                    info(*args, **kwargs) if callable(info) else info,
                                    args,
                                    kwargs,
                                    elapsed,
                                    threshold,
                                    emoji_by_elapsed(elapsed))
                    else:
                        logger.info(u'func=%s info=%s elapsed=%sms threshold=%sms %s',
                                    func_full_name, info, elapsed, threshold, emoji_by_elapsed(elapsed))
        return wrapper
    if 'threshold' not in kwargs and 'level' not in kwargs and 'info' not in kwargs and callable(args[0]):
        # No arguments, this is the decorator
        # Set default values for the arguments
        threshold = -1
        level = 'info'
        info = None
        return _metricmethod(args[0])
    else:
        # This is just returning the decorator
        threshold = kwargs.get('threshold', -1)
        level = kwargs.get('level', 'info')
        info = kwargs.get('info', None)
        return _metricmethod
