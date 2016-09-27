import pytest
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from attrs_sqlalchemy import attrs_sqlalchemy


class TestAttrsSqlalchemy:

    @pytest.mark.parametrize('decorator', [attrs_sqlalchemy, attrs_sqlalchemy()])
    def test_attrs_sqlalchemy(self, decorator):
        """
        Decorating a class with ``@attrs_sqlalchemy`` or
        ``@attrs_sqlalchemy()`` should add ``__repr__``, ``__eq__``, and
        ``__hash__`` methods based on the fields on the model.
        """
        TestBase = declarative_base()

        @attrs_sqlalchemy
        class MyModel(TestBase):
            __tablename__ = 'mymodel'

            id = sa.Column(sa.Integer, primary_key=True)
            text = sa.Column(sa.String)

        instance = MyModel(id=1, text='hello')
        same_data = MyModel(id=1, text='hello')
        same_pk = MyModel(id=1, text='world')

        # All fields are the same
        assert instance == same_data

        # Primary key is not enough for equality
        assert instance != same_pk

        # Instances should have a repr containing their keys and type
        assert repr(instance) == "MyModel(id=1, text='hello')"

        # Instances should be hashable by their fields and used in a dict
        d = {instance: True}
        assert d.get(same_data) == d[instance]
        assert d.get(same_pk) is None

    def test_field_name_not_column_name(self):
        """
        ``@attrs_sqlalchemy`` should use attribute/field names, not column names.
        """
        @attrs_sqlalchemy
        class MyModel(declarative_base()):
            __tablename__ = 'mymodel'

            _id = sa.Column('id', sa.Integer, primary_key=True)
            text = sa.Column(sa.String)

        assert {attr.name for attr in MyModel.__attrs_attrs__} == {'_id', 'text'}

    def test_subclass(self):
        """
        When used on a subclass, ``@attrs_sqalchemy`` should also include the
        attributes from the parent class(es), even if a parent class is also
        decorated with ``@attrs_sqlalchemy``.
        """
        @attrs_sqlalchemy
        class ParentModel(declarative_base()):
            __tablename__ = 'parent'

            id = sa.Column(sa.Integer, primary_key=True)
            type = sa.Column(sa.String)

            __mapper_args__ = {
                'polymorphic_identity': 'parent',
                'polymorphic_on': type,
            }

        @attrs_sqlalchemy
        class ChildModel(ParentModel):
            __tablename__ = 'child'

            id = sa.Column(sa.Integer, sa.ForeignKey('parent.id'), primary_key=True)
            child_field = sa.Column(sa.Integer)

            __mapper_args__ = {
                'polymorphic_identity': 'child',
            }

        @attrs_sqlalchemy
        class ChildChildModel(ChildModel):
            __tablename__ = 'very_child'

            id = sa.Column(sa.Integer, sa.ForeignKey('child.id'), primary_key=True)
            very_child_field = sa.Column(sa.String)

            __mapper_args__ = {
                'polymorphic_identity': 'childchild',
            }

        assert {attr.name for attr in ChildModel.__attrs_attrs__} == {
            'id', 'type', 'child_field',
        }

        assert {attr.name for attr in ChildChildModel.__attrs_attrs__} == {
            'id', 'type', 'child_field', 'very_child_field',
        }

    def test_hybrid_property(self):
        """
        Hybrid properties should not be included in the attributes used by
        ``@attrs_sqlalchemy``.
        """
        @attrs_sqlalchemy
        class MyModel(declarative_base()):
            __tablename__ = 'mymodel'

            id = sa.Column(sa.Integer, primary_key=True)
            text = sa.Column(sa.String)

            @hybrid_property
            def tiny_text(self):  # pragma: no cover
                return self.text[:10]

        assert {attr.name for attr in MyModel.__attrs_attrs__} == {'id', 'text'}
