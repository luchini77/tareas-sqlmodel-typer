import typer
from typing_extensions import Annotated
from rich.console import Console
from rich.table import Table

from database import get_tareas, crear_tarea,borrar_tarea,actualizar_tarea,tarea_completada
from model import Tarea

consola = Console()

app = typer.Typer()

@app.command(help='agregar elemento')
def agregar(tarea:str,categoria:str):
    typer.echo(f"agregando {tarea},{categoria}")

    new_tarea = Tarea(tarea=tarea,categoria=categoria)
    crear_tarea(new_tarea)

    listar()

@app.command()
def borrar(id:int):
    typer.echo(f"borrando {id}")

    borrar_tarea(id)

    listar()

@app.command()
def actualizar(id:int,tarea:Annotated[str, typer.Option(prompt=True)],categoria:Annotated[str,typer.Option(prompt=True)]):
    typer.echo(f"actualizando {id}")

    actualizar_tarea(id,tarea,categoria)

    listar()

@app.command()
def terminada(id:int): 
    typer.echo(f"terminada {id}")

    tarea_completada(id)

    listar()

@app.command()
def listar():
    tareas =  get_tareas()

    consola.print("[bold magenta]Tareas[/bold magenta]!", "💻")

    tabla = Table(show_header=True, header_style="bold blue")
    tabla.add_column("#", style="dim", width=6)
    tabla.add_column("Tarea", min_width=20)
    tabla.add_column("Categoria", min_width=12, justify="right")
    tabla.add_column("Terminada", min_width=12, justify="right")

    def get_category_color(categoria):
        COLORS = {'aprender': 'bright_green', 'YouTube': 'bright_red', 'deportes': 'bright_cyan', 'estudiar': 'bright_magenta'}
        if categoria in COLORS:
            return COLORS[categoria]
        return 'white'

    for idx, tarea in enumerate(tareas, start=1):
        c = get_category_color(tarea.categoria)
        is_done_str = '✅' if tarea.estado != False else '❌'
        tabla.add_row(str(idx), tarea.tarea, f'[{c}]{tarea.categoria}[/{c}]', is_done_str)
    consola.print(tabla)



if __name__ == "__main__":
    app()