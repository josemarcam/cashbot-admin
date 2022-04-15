from src.config.database import DB
from sqlalchemy import orm

class BaseRepository():

    def __init__(self, db: DB):
        
        self._db = db
        self.model = None
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._db.get_engine(),
            ),
        )
        self.session: orm.Session = self._session_factory()
        
    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, model):
        self._model = model

    def save(self):
        with self.session as session:
            session.add(self.model)
            session.flush()
            session.expunge_all()
            session.commit()
