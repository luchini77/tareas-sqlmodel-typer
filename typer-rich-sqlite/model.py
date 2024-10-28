from typing import Optional
from sqlmodel import Field, SQLModel

from datetime import datetime
from pytz import timezone

def hora_actual():
    hora = datetime.now(timezone('America/Santiago'))
    time = hora.strftime("%H:%M:%S")
    return time

class Tarea(SQLModel, table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    tarea:str
    categoria:str
    fecha_inicio: str | None = Field(default=hora_actual())
    fecha_termino:Optional[str]=None
    estado:bool | None = Field(default=False)