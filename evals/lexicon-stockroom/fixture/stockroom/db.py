"""Database access.

Every stock change runs inside ``uow()``, which opens the ORM session and
commits on success. The unit of work and the ORM session are defined in
GLOSSARY.md.
"""

from contextlib import contextmanager

from sqlalchemy.orm import Session

_engine = None


def configure(engine):
    global _engine
    _engine = engine


@contextmanager
def uow():
    """Yield an ORM session; commit on success, roll back on error."""
    db = Session(_engine)
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
