# GridExplorer APP

from rich import print
from rich.panel import Panel
from importlib import resources


def ppanel(s: str):
    print(Panel.fit(s))


def run_cli_demo():
    """opens network in pandapower.json format"""

    import sys

    argv = sys.argv

    if len(argv) > 1 and argv[1] == "gex":
        # import webbrowser

        with resources.open_text("gex.extra", "gex.svg") as imfile:
            txt = imfile.read()
            print(txt)

        return

    ppanel("Hello, this is [purple]GridExplorer!")
    if len(argv) == 1:
        print(
            """---
No arguments found.
This is just a demo app, but you can try it out on a [blue]pandapower .json[/blue] file."""
        )

        return

    cmd: str = argv[1]

    if cmd == "this":
        # import this

        with resources.open_text("gex.extra", "this.txt") as t:
            txt = t.read()
            print("\n", txt)

        ppanel("gex finished!")
        return

    elif cmd == "help":
        print(
            "-- help:\nusage: [purple]gex[/purple] this | gex | [cyan]<pandapowernet.json>"
        )

    ## DEFAULT: open as ppnet

    if not cmd.endswith(".json"):
        print(
            """
The provided argument is [red]not a json file."""
        )

        return

    import pandapower

    print(f"opening [blue]{cmd}")
    try:
        net = pandapower.from_json(cmd)
    except Exception:
        print(Exception)

    from rich import inspect

    inspect(net)

    ppanel(f"[red]Summaries:")
    inspect_tags = ["line", "bus", "trafo", "trafo3f", "load", "switch", "gen", "sgen"]
    for tag in inspect_tags:
        if tag not in net:
            ppanel(tag + " [red]not found")
            continue
        ppanel(f"table [blue]{tag}")
        print(net[tag].dropna().describe())

    ppanel(f"[red]Power Flow Reuslts")
    for tag in inspect_tags:
        if tag not in net:
            ppanel(tag + " [red]not found")
            continue
        ppanel(f"table [blue] res_{tag}")
        print(net["res_" + tag].describe())

    ppanel("\n\n\t[green]Thats ALL from [purple]gex[green] !!!")


if __name__ == "__main__":
    run_cli_demo()
