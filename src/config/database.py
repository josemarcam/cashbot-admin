from src.config.env import environment
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base


base_entity = declarative_base()

class DB:
    
    engine = create_engine(environment.get_item("DATABASE_URI"))
    session = None
    def get_engine(self):
        return self.engine
    
    def get_scopped_session(self):
        if not self.session:
            Session = orm.sessionmaker(self.engine)
            self.session = Session()
            return self.session
        return self.session
        