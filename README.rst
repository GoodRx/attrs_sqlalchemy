================
attrs_sqlalchemy
================

Use `attrs <https://attrs.readthedocs.io>`_ to add ``__repr__``, ``__eq__``,
``__cmp__``, and ``__hash__`` methods according to the fields on a SQLAlchemy
model class.

.. code-block:: python

   from attrs_sqlalchemy import attrs_sqlalchemy

   @attrs_sqlalchemy
   class MyModel(Base):
       __tablename__ = 'mymodel'

       id = sa.Column(Integer, primary_key=True)
       text = sa.Column(sa.String)

   instance = MyModel(id=1, text='hello')
   same_data = MyModel(id=1, text='hello')
   same_pk = MyModel(id=1, text='world')

   assert instance == same_data
   assert instance != same_pk
   assert repr(instance) == "MyModel(id=1, text='hello')"
