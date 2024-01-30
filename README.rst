.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

=============
mrs.doubtfire
=============

"Upstairs, my little nose miners! Go! Flee before me! Onward and upward! Go pump some neurons! Expand your craniums!"
Euphegenia Doubtfire


Features
--------

☐ reporting on the use of slow methods

☐ write during navigation

☐ browserview call during tal rendering

☑ profiling slow browserview call, viewlet, portlet, subrequest, catalog

☑ extensible

☑ (collective.stats)


Documentation
-------------

Add metric using zcml ::

  <configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:doubtfire="http://namespaces.plone.org/doubtfire"
    i18n_domain="mrs.doubtfire">

    <doubtfire:metrics
        module="collective.my.module"
        method="my_function"
        threshold="50"
        level="debug"
        />

  </configure>

Or wrapping/monkeypatching the function ::
 
   from mrs.doubtfire.meta import metricmethod
   from my.package import MyClass

   MyClass.my_function = metricmethod(MyClass.my_function)

Installation
------------

Install mrs.doubtfire by adding it to your buildout::

    [buildout]

    ...

    eggs +=
        mrs.doubtfire


and then running ``bin/buildout``

Battery included::

    zcml +=
        mrs.doubtfire-metrics
        mrs.doubtfire-catalog

Monitoring `pas.plugins.ldap`::

    zcml +=
        mrs.doubtfire-ldap

Contribute
----------

- Issue Tracker: https://github.com/collective/mrs.doubtfire/issues
- Source Code: https://github.com/collective/mrs.doubtfire


License
-------

The project is licensed under the GPLv2.
