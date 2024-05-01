from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import pymongo

# Conecta ao banco de dados SQLite
engine = create_engine('sqlite:///banco.db', echo=True)

# Base para as classes do SQLAlchemy
Base = declarative_base()

# Definição da classe Cliente
class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    endereco = Column(String)
    contas = relationship("Conta", back_populates="cliente")

# Definição da classe Conta
class Conta(Base):
    __tablename__ = 'conta'
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    numero = Column(String)
    saldo = Column(Float)
    id_cliente = Column(Integer, ForeignKey('cliente.id'))
    cliente = relationship("Cliente", back_populates="contas")

# Cria a engine de banco de dados MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
mongo_db = mongo_client["banco"]
mongo_collection = mongo_db["bank"]

# Cria uma sessão para interagir com o banco de dados SQLite
Session = sessionmaker(bind=engine)
session = Session()

# Recupera todos os clientes do banco de dados SQLite
clientes_sqlalchemy = session.query(Cliente).all()

# Itera sobre os clientes e insere os documentos correspondentes no MongoDB
for cliente_sqlalchemy in clientes_sqlalchemy:
    cliente_mongodb = {
        "nome": cliente_sqlalchemy.nome,
        "cpf": cliente_sqlalchemy.cpf,
        "endereco": cliente_sqlalchemy.endereco,
        "contas": []
    }
    for conta_sqlalchemy in cliente_sqlalchemy.contas:
        conta_mongodb = {
            "tipo": conta_sqlalchemy.tipo,
            "agencia": conta_sqlalchemy.agencia,
            "numero": conta_sqlalchemy.numero,
            "saldo": conta_sqlalchemy.saldo
        }
        cliente_mongodb["contas"].append(conta_mongodb)
    mongo_collection.insert_one(cliente_mongodb)
