================
attrs_sqlalchemy
================

Deprecation
-----------

**This project is deprecated!** SQLAlchemy already manages ``__eq__`` and
``__hash__`` based on identity within the session. This project is incompatible
with attrs 17.1.0+ or recent versions of SQLAlchemy.

If you're just looking for a nice ``__repr__`` for your SQLAlchemy models,
consider `sqlalchemy-repr <https://pypi.org/project/sqlalchemy-repr/>`_, `repr
<https://pypi.org/project/repr/>`_, or other packages.

Legacy documentation
--------------------

.. image:: https://img.shields.io/pypi/v/attrs_sqlalchemy.svg
   :target: https://pypi.python.org/pypi/attrs_sqlalchemy

.. image:: https://travis-ci.org/GoodRx/attrs_sqlalchemy.svg?branch=master
   :target: https://travis-ci.org/GoodRx/attrs_sqlalchemy
   :alt: CI status

Use the amazing `attrs <https://attrs.readthedocs.io>`_ library to add
``__repr__``, ``__eq__``, ``__cmp__``, and ``__hash__`` methods according to
the fields on a SQLAlchemy model class.


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

Project Information
===================

``attrs_sqlalchemy`` is released under the `MIT
<http://choosealicense.com/licenses/mit/>`_ license, its code lives on `GitHub
<https://github.com/GoodRx/attrs_sqlalchemy>`_, and the latest release on `PyPI
<https://pypi.org/project/attrs_sqlalchemy/>`_.
