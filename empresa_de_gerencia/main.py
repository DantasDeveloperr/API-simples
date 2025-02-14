import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from pydantic import BaseModel, EmailStr
from typing import List
from dotenv import load_dotenv
import alembic.config # type: ignore


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./empresas.db")


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Empresa(Base):
    __tablename__ = "empresas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cnpj = Column(String, unique=True, index=True)
    endereco = Column(String)
    email = Column(String, unique=True, index=True)
    telefone = Column(String)
    obrigacoes = relationship("ObrigacaoAcessoria", back_populates="empresa", cascade="all, delete-orphan")

class ObrigacaoAcessoria(Base):
    __tablename__ = "obrigacoes_acessorias"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    periodicidade = Column(String, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"))
    empresa = relationship("Empresa", back_populates="obrigacoes")


class ObrigacaoAcessoriaBase(BaseModel):
    nome: str
    periodicidade: str

class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    pass

class ObrigacaoAcessoriaResponse(ObrigacaoAcessoriaBase):
    id: int
    class Config:
        orm_mode = True

class EmpresaBase(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: EmailStr
    telefone: str

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaResponse(EmpresaBase):
    id: int
    obrigacoes: List[ObrigacaoAcessoriaResponse] = []
    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.post("/empresas/", response_model=EmpresaResponse)
def criar_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.get("/empresas/", response_model=List[EmpresaResponse])
def listar_empresas(db: Session = Depends(get_db)):
    return db.query(Empresa).all()

@app.get("/empresas/{empresa_id}/", response_model=EmpresaResponse)
def obter_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return db_empresa

@app.put("/empresas/{empresa_id}/", response_model=EmpresaResponse)
def atualizar_empresa(empresa_id: int, empresa: EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    for key, value in empresa.dict().items():
        setattr(db_empresa, key, value)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.delete("/empresas/{empresa_id}/", response_model=dict)
def deletar_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    db.delete(db_empresa)
    db.commit()
    return {"message": "Empresa deletada com sucesso"}


@app.post("/empresas/{empresa_id}/obrigacoes/", response_model=ObrigacaoAcessoriaResponse)
def adicionar_obrigacao(empresa_id: int, obrigacao: ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    db_obrigacao = ObrigacaoAcessoria(**obrigacao.dict(), empresa_id=empresa_id)
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

@app.get("/obrigacoes/{obrigacao_id}/", response_model=ObrigacaoAcessoriaResponse)
def obter_obrigacao(obrigacao_id: int, db: Session = Depends(get_db)):
    db_obrigacao = db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.id == obrigacao_id).first()
    if not db_obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")
    return db_obrigacao

@app.delete("/obrigacoes/{obrigacao_id}/", response_model=dict)
def deletar_obrigacao(obrigacao_id: int, db: Session = Depends(get_db)):
    db_obrigacao = db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.id == obrigacao_id).first()
    if not db_obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")
    db.delete(db_obrigacao)
    db.commit()
    return {"message": "Obrigação deletada com sucesso"}


def run_migrations():
    alembic.config.main(argv=["upgrade", "head"])


