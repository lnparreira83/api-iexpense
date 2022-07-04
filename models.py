from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///despesas.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Despesas(Base):
    __tablename__ = 'despesas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(60), index=True)
    data = Column(String(10), index=True)
    tipo = Column(String(10), index=True)
    valor = Column(Float())
    observacao = Column(String(100), index=False)

    def __repr__(self):
        return '<Despesa {}>'.format(self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
