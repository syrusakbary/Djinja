"""
Djinja
~~~~~~

`Djinja <http://github.com/syrusakbary/djinja>` tries to integrate `Jinja2
<http://jinja.pocoo.org/2/>` in `Django <http://www.djangoproject.com/>`. The aim is to replace
completely the Django's template system, including administration.

:copyright: 2011 by Syrus Akbary Nieto
:license: BSD, see LICENSE for more details.
"""

#Taked majoritarily from Coffin's <http://www.github.com/dcramer/coffin> __init__.py

__all__ = ('__version__', '__build__', '__docformat__', 'get_revision')
__version__ = (0, 7)
__author__ = 'Syrus Akbary Nieto'
__docformat__ = 'restructuredtext en'

import os

def _get_git_revision(path):
    revision_file = os.path.join(path, 'refs', 'heads', 'master')
    if not os.path.exists(revision_file):
        return None
    fh = open(revision_file, 'r')
    try:
        return fh.read()
    finally:
        fh.close()

def get_revision():
    """
    :returns: Revision number of this branch/checkout, if available. None if
        no revision number can be determined.
    """
    package_dir = os.path.dirname(__file__)
    checkout_dir = os.path.normpath(os.path.join(package_dir, '..'))
    path = os.path.join(checkout_dir, '.git')
    if os.path.exists(path):
        return _get_git_revision(path)
    return None

__build__ = get_revision()