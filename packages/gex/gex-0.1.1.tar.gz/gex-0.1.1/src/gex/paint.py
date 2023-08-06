from dataclasses import dataclass

import matplotlib.pyplot as plt

from rich import print, inspect
from rich.traceback import install

install()

from pandapower.auxiliary import pandapowerNet as ppNet


@dataclass
class GEdge:
    entity: str
    idx: int
    bfrom: int
    bto: int


_color_count = 0


def get_color() -> str:
    global _color_count
    c = ["k", "r", "b", "g"]
    result = c[_color_count]
    _color_count = (_color_count + 1) % len(c)
    return result


def setup_net_plot_config(net: ppNet) -> None:
    """Initiates plot options into ppNet data frames."""

    net.line[["plot_color", "plot_style"]] = "grey", "-"
    net.trafo[["plot_color", "plot_style"]] = "orange", "-."

    for key, df in net.bus.groupby("vn_kv"):
        net.bus.loc[df.index, ["plot_color", "plot_marker", "plot_label"]] = (
            get_color(),
            "o",
            key,
        )

    net.switch.loc[net.switch.et == "b", ["plot_color", "plot_style", "plot_label"]] = (
        "red",
        ":",
        "switch_b-b",
    )

    sw = net.switch
    for i in sw.index:
        row = sw.loc[i]

        entity = row["et"]
        tag = "line" if entity == "l" else "trafo" if entity == "t" else "bus"
        if tag == "bus":
            continue  # draw special lines for these

        idx = row["element"]
        net[tag].loc[idx, "plot_color"] = "blue"

    net._plot_options_initialized = True


def plot_pp_network(net: ppNet, ax: plt.Axes | None = None) -> None:
    """Draws the network using properties inserted into the net dataframes.
    If missing, it initializes them to defaults.
    """
    is_ax_owner = False
    if ax is None:
        plt.figure()
        ax = plt.gca()
        is_ax_owner = True
    assert type(ax) == plt.Axes

    try:
        _ = net._plot_options_initialized
    except AttributeError:
        setup_net_plot_config(net)

    ## buses
    bids = sorted(net.bus.index)
    bus_coo = net.bus_geodata.loc[bids, ["x", "y"]]
    # print(bus_coo)

    ## plot each group
    ## buses:
    marker_groups = net.bus.groupby("plot_label")
    for key, df in marker_groups:
        bids = sorted(df.index)
        ax.scatter(
            bus_coo.loc[bids, "x"],
            bus_coo.loc[bids, "y"],
            color=df.plot_color,
            marker=df.plot_marker.iloc[0],
            label=f"Un:{int(key):d}kV",
        )

    ## lines
    line_groups = net.line.groupby(["plot_color", "plot_style"])
    for keys, df in line_groups:
        color, style = keys
        edges = {"x": [], "y": []}
        lids = sorted(df.index)
        for i in lids:
            line = df.loc[i]
            x1, y1 = bus_coo.loc[line.from_bus]
            x2, y2 = bus_coo.loc[line.to_bus]
            edges["x"] += [x1, x2, None]
            edges["y"] += [y1, y2, None]

        ax.plot(
            edges["x"],
            edges["y"],
            color=color,
            linestyle=style,
            label=f"l{color}{style}",
        )

    ## trafos
    trafo_groups = net.trafo.groupby(["plot_color", "plot_style"])
    for keys, df in trafo_groups:
        color, style = keys
        edges = {"x": [], "y": []}
        tids = sorted(df.index)
        for i in tids:
            trafo = df.loc[i]
            x1, y1 = bus_coo.loc[trafo.lv_bus]
            x2, y2 = bus_coo.loc[trafo.hv_bus]
            edges["x"] += [x1, x2, None]
            edges["y"] += [y1, y2, None]

        ax.plot(
            edges["x"],
            edges["y"],
            color=color,
            linestyle=style,
            label=f"t{color}{style}",
        )

    ## switch - just show busbus
    swdf = net.switch[net.switch.et == "b"]
    if len(swdf) > 0:
        sids = sorted(swdf.index)
        color, style, label = swdf.loc[
            sids[0], ["plot_color", "plot_style", "plot_label"]
        ]
        edges = {"x": [], "y": []}
        for i in sids:
            switch = swdf.loc[i]
            x1, y1 = bus_coo.loc[switch.bus]
            x2, y2 = bus_coo.loc[switch.element]
            edges["x"] += [x1, x2, None]
            edges["y"] += [y1, y2, None]

        ax.plot(
            edges["x"],
            edges["y"],
            color=color,
            linestyle=style,
            label=label,
        )

    if is_ax_owner:
        plt.legend()
        plt.show()


def plot_pp_network_plain(net: ppNet, ax=None):
    is_ax_owner = False
    if ax is None:
        plt.figure()
        ax = plt.gca()
        is_ax_owner = True

    ## buses
    bids = sorted(net.bus.index)
    bus_coo = net.bus_geodata.loc[bids, ["x", "y"]]
    # print(bus_coo)

    ax.scatter(bus_coo.x, bus_coo.y)

    ## lines
    lids = sorted(net.line.index)
    edges = {"x": [], "y": []}
    for i in lids:
        line = net.line.loc[i]
        tag = GEdge("line", i, line.from_bus, line.to_bus)

        x1, y1 = bus_coo.loc[line.from_bus]
        x2, y2 = bus_coo.loc[line.to_bus]
        edges["x"] += [x1, x2, None]
        edges["y"] += [y1, y2, None]

    ax.plot(edges["x"], edges["y"], color="grey")

    ## trafo
    tids = sorted(net.trafo.index)
    edges = {"x": [], "y": []}
    for i in tids:
        trafo = net.trafo.loc[i]
        tag = GEdge("trafo", i, trafo.hv_bus, trafo.lv_bus)

        x1, y1 = bus_coo.loc[trafo.lv_bus]
        x2, y2 = bus_coo.loc[trafo.hv_bus]
        edges["x"] += [x1, x2, None]
        edges["y"] += [y1, y2, None]

    ax.plot(edges["x"], edges["y"], color="orange")


if __name__ == "__main__":
    from gex.extra.NetworkList import network_index

    net = network_index["case118"]()
    plot_pp_network(net)
