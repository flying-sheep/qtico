QtICO |cov|_
============

This package provides tools to manage PyQt icon themes.

The |QIcon.fromTheme|_ API works with icon themes following the `freedesktop icon theme spec`_,
which is great for Linux systems with installed and enabled themes, but not for Windows or OS X, which lack them.

To benefit, you just have to create a theme directory with the right structure and use this package’s functions::

    icons (The default directory name)
    ├hicolor
    │├16x16/apps/myapp.png
    │├32x32/apps/myapp.png
    │┆
    │└scalable/apps/myapp.svg
    └mypackage-builtin
     ├16x16
     │├actions
     ││├document-open.png
     ││┆
     │├mimetypes
     ││├application-x-mymime.png
     ┆┆┆

This package provides the following functions to ease bundling an in-memory icon theme for those systems:

``write_theme_indices``
    Creates ``.index.theme`` files from the ``.png`` and ``.svg`` files.

``write_resources``
    Create a ``.qrc`` and ``_rc.py`` file to import the icon data from. (Needs the ``.index.theme`` files)

``write_iconset``
    Creates a iconset folder for OSX apps, e.g. via py2app_, using the ``hicolor/<s>x<s>/apps/myapp.png`` files.

``install_icon_theme``
    To be used in a running application to make the builtin icons available.

The ``hicolor/<s>x<s>/apps/myapp.png`` files can be

#. installed to the system by packagers (``/usr/share/icons/hicolor/…``)
#. subsequently used in a .desktop file (``Icon=myapp``)
#. used as window icon (``self.setWindowIcon(QIcon.fromTheme('myapp'))``)

.. |cov| image:: https://codecov.io/gh/flying-sheep/qtico/graph/badge.svg?token=wyxb6gH2I3
.. _cov: https://codecov.io/gh/flying-sheep/qtico
.. |QIcon.fromTheme| replace:: ``QIcon.fromTheme``
.. _QIcon.fromTheme: http://doc.qt.io/qt-5/qicon.html#fromTheme
.. _freedesktop icon theme spec: http://standards.freedesktop.org/icon-theme-spec/icon-theme-spec-latest.html
.. _py2app: https://py2app.readthedocs.io
