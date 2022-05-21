from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as Session_

from workshop.config import settings


engine = create_engine(
    settings.db_url,
    connect_args={'check_same_thread': False}
)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False
)


def get_session() -> Session_:
    session: Session_ = Session()
    try:
        yield session
    finally:
        session.close()
    return session
