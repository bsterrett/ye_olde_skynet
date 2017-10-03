from .base import Base
from sqlalchemy import Column, Integer, String

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    tribe = Column(String)
    alliance = Column(String)

    def __repr__(self):
       return "<User(username='%s', tribe='%s', alliance='%s')>" % (
                            self.username, self.tribe, self.alliance)
