================
attrs_sqlalchemy
================

.. image:: https://img.shields.io/pypi/v/attrs_sqlalchemy.svg
   :target: https://pypi.python.org/pypi/attrs_sqlalchemy

.. image:: https://travis-ci.org/GoodRx/attrs_sqlalchemy.svg?branch=master
   :target: https://travis-ci.org/GoodRx/attrs_sqlalchemy
   :alt: CI status

Use the amazing `attrs <https://attrs.readthedocs.io>`_ library to add
``__repr__``, ``__eq__``, and ``__cmp__`` methods according to the fields on a
SQLAlchemy model class.

``__hash__`` will always fall back to id-based hashing from ``object``.


Example
-------

.. code-block:: python

   from attrs_sqlalchemy import attrs_sqlalchemy
   import sqlalchemy as sa
   from sqlalchemy.ext.declarative import declarative_base

   Base = declarative_base()

   @attrs_sqlalchemy
   class MyModel(Base):
       __tablename__ = 'mymodel'

       id = sa.Column(sa.Integer, primary_key=True)
       text = sa.Column(sa.String)

   instance = MyModel(id=1, text='hello')
   same_data = MyModel(id=1, text='hello')
   same_pk = MyModel(id=1, text='world')

   assert instance == same_data
   assert instance != same_pk
   assert repr(instance) == "MyModel(id=1, text='hello')"

Installation
------------

.. code-block:: bash

   $ pip install attrs_sqlalchemy

Changelog
=========

0.2.0 (UNRELEASED)
------------------

- **Backward-incompatible**: Apply ``attr.s`` with ``hash=False``, using
  id-based hashing instead of value-based hashing.

  attrs 17.1.0 changed the default for ``hash`` to ``None``, which makes
  objects unhashable. We set ``hash=False`` so that we can continue to use
  objects as keys in dictionaries, but without attempting to hash by value.

  http://www.attrs.org/en/stable/changelog.html

0.1.0 (2016-09-24)
------------------

- Initial release

Project Information
===================

``attrs_sqlalchemy`` is released under the `MIT
<http://choosealicense.com/licenses/mit/>`_ license, its code lives on `GitHub
<https://github.com/GoodRx/attrs_sqlalchemy>`_, and the latest release on `PyPI
<https://pypi.org/project/attrs_sqlalchemy/>`_.
