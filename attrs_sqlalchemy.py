import attr
from sqlalchemy import inspect


def attrs_sqlalchemy(maybe_cls=None):
    """
    A class decorator that adds ``__repr__``, ``__eq__``, ``__cmp__``, and
    ``__hash__`` methods according to the fields defined on the SQLAlchemy
    model class.
    """
    def wrap(cls):
        these = {
            name: attr.ib()
            # `__mapper__.columns` is a dictionary mapping field names on the
            # model class to table columns. SQLAlchemy provides many ways to
            # access the fields/columns, but this works at the time the class
            # decorator is called:
            #
            # - We can't use `cls.__table__.columns` because that directly maps
            #   the column names rather than the field names on the model. For
            #   example, given `_my_field = Column('field', ...)`,
            #   `__table__.columns` will contain 'field' rather than '_my_field'.
            #
            # - We can't use `cls.__dict__`, where values are
            #   `InstrumentedAttribute`s, because that includes relationships,
            #   synonyms, and other features.
            #
            # - We can't use `cls.__mapper__.column_attrs`
            #   (or `sqlalchemy.inspect`) because they will attempt to
            #   initialize mappers for all of the classes in the registry,
            #   which won't be ready yet.
            for name in inspect(cls).columns.keys()
        }
        return attr.s(cls, these=these, init=False)

    # `maybe_cls` depends on the usage of the decorator. It's a class if it's
    # used as `@attrs_sqlalchemy` but `None` if it's used as
    # `@attrs_sqlalchemy()`
    # ref: https://github.com/hynek/attrs/blob/15.2.0/src/attr/_make.py#L195
    if maybe_cls is None:
        return wrap
    else:
        return wrap(maybe_cls)
