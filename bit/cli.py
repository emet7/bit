# bit/cli.py
import typer
from datetime import datetime

app = typer.Typer()

@app.command()
def heartbeat():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Bit heartbeat at {now}")
@app.command()
def status():
    print("Need status")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        heartbeat()

if __name__ == "__main__":
    app()
