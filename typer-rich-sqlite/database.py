from sqlmodel import Session, SQLModel, create_engine, select
from typing import List

from datetime import datetime
from pytz import timezone

from model import Tarea

sqlite_file_name = "Tarea.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

SQLModel.metadata.create_all(engine)


def hora_actual():
    hora = datetime.now(timezone('America/Santiago'))
    time = hora.strftime("%H:%M:%S")
    return time


def get_tareas() -> List[Tarea]:
    with Session(engine) as session:
        sta = select(Tarea)
        res = session.exec(sta)

        tareas = []

        for r in res:
            tareas.append(r)

        return tareas

def crear_tarea(tarea:Tarea):
    with Session(engine) as session:
        
        session.add(tarea)
        session.commit()
        session.refresh(tarea)

        return tarea
    
def borrar_tarea(id:int):
    with Session(engine) as session:

        sta = select(Tarea).where(Tarea.id == id)
        res = session.exec(sta)
        tarea = res.first()

        if tarea is None:
            print('No existe tarea con ese id entregado!!!')
            
        else:
            session.delete(tarea)
            session.commit()

def actualizar_tarea(id:int,tarea:str,categoria:str):
    with Session(engine) as session:

        sta = select(Tarea).where(Tarea.id == id)
        res = session.exec(sta)
        up_tarea = res.one()

        up_tarea.tarea = tarea
        up_tarea.categoria = categoria

        session.add(up_tarea)
        session.commit()
        session.refresh(up_tarea)

        return up_tarea
    
def tarea_completada(id:int):
    with Session(engine) as session:

        sta = select(Tarea).where(Tarea.id == id)
        res = session.exec(sta)
        up_tarea = res.one()

        up_tarea.estado = True
        up_tarea.fecha_termino = hora_actual()

        session.add(up_tarea)
        session.commit()
        session.refresh(up_tarea)

        return up_tarea