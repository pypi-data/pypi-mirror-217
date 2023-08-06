import pandapower
import time

from rich import print


def open_net(fpath: str) -> pandapower.pandapowerNet:
    print(f"opening [blue]{fpath}")
    tick = time.perf_counter()
    try:
        net = pandapower.from_json(fpath)
    except Exception as e:
        raise e
    ttick = time.perf_counter()

    print(f"--- opened the net in [green]{ttick-tick} [red](s)")

    assert type(net) == pandapower.pandapowerNet
    return net
