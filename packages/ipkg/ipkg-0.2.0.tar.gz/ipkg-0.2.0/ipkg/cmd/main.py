import typer

from ipkg import NAME
from ipkg.pkg.btop.install import main as install_btop
from ipkg.pkg.btop.remove import main as remove_btop
from ipkg.pkg.conda.install import main as install_conda
from ipkg.pkg.conda.remove import main as remove_conda
from ipkg.utils.typer import add_command

install_cmd: typer.Typer = typer.Typer(name="install")
add_command(app=install_cmd, command=install_btop, name="btop")
add_command(app=install_cmd, command=install_conda, name="conda")

remove_cmd: typer.Typer = typer.Typer(name="remove")
add_command(app=remove_cmd, command=remove_btop, name="btop")
add_command(app=remove_cmd, command=remove_conda, name="conda")

app: typer.Typer = typer.Typer(name=NAME)
add_command(app=app, command=install_cmd, name="install")
add_command(app=app, command=remove_cmd, name="remove")
