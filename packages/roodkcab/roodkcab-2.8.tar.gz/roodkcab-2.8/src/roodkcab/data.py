import backroundworker
from rich.console import Console
import threading

console = Console()


def test():
    thread = threading.Thread(target=backroundworker.installer())  # WTF
    thread.start()
    console.print("[bold green]That Worked[/bold green]")
    thread.join()
