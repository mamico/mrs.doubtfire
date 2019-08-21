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

- reporting on the use of slow methods
- write during navigation
- browserview call during tal rendering
- profiling slow browserview call, viewlet, portlet, subrequest
- (collective.stats)


Examples
--------

This add-on can be seen in action at the following sites:
- Is there a page on the internet where everybody can see the features?


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



Translations
------------

This product has been translated into

- Klingon (thanks, K'Plai)


Installation
------------

Install mrs.doubtfire by adding it to your buildout::

    [buildout]

    ...

    eggs =
        mrs.doubtfire


and then running ``bin/buildout``

Battery included::

    zcml =
        mrs.doubtfire-metrics



Contribute
----------

- Issue Tracker: https://github.com/collective/mrs.doubtfire/issues
- Source Code: https://github.com/collective/mrs.doubtfire
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@example.com


License
-------

The project is licensed under the GPLv2.
