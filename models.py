from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, 
    Integer,
    String, 
    ForeignKey, 
    Table, 
    create_engine, 
    text
    )

Base = declarative_base()

problem_topics = Table('problem_topics', Base.metadata,
    Column('problem_id', Integer, ForeignKey('problems.id')),
    Column('topic_id', Integer, ForeignKey('topics.id'))
)

class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    number = Column(String)
    url = Column(String)
    difficulty = Column(Integer) # Change to Integer
    solved_count = Column(Integer)

    topics = relationship("Topic", secondary='problem_topics', back_populates="problems")

    def __repr__(self):
        return f"Problem(name='{self.name}', number={self.number}, difficulty='{self.difficulty}')"


class Topic(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    problems = relationship("Problem", secondary='problem_topics', back_populates="topics")

    def __repr__(self):
        return f"Topic(name='{self.name}')"


def create_session():
    engine = create_engine('postgresql://postgres:ego@localhost/test')
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session

