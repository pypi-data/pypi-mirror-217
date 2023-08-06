import pandas as pd
import matplotlib.pyplot as plt

import pandapower as pp
import pandapower.networks as pn

# from pandapower.plotting.plotly import simple_plotly
# from pandapower.plotting.plotly import pf_res_plotly
# from pandapower.plotting import simple_plot

network_bundle = {
    "example": [pn.example_simple, pn.example_multivoltage],
    "simple": [
        pn.panda_four_load_branch,
        pn.four_loads_with_branches_out,
        pn.simple_four_bus_system,
        pn.simple_mv_open_ring_net,
    ],
    "cirge": [
        pn.create_cigre_network_hv,
        pn.create_cigre_network_mv,
        pn.create_cigre_network_mv,
        pn.create_cigre_network_mv,
        pn.create_cigre_network_lv,
    ],
    "mv_oberrhein": [pn.mv_oberrhein],
    "test_cases": [
        pn.case4gs,
        pn.case5,
        pn.case6ww,
        pn.case9,
        pn.case14,
        pn.case24_ieee_rts,
        pn.case30,
        pn.case_ieee30,
        pn.case33bw,
        pn.case39,
        pn.case57,
        pn.case89pegase,
        pn.case118,
        pn.case145,
        pn.case_illinois200,
        pn.case300,
        pn.case1354pegase,
        pn.case1888rte,
        pn.case2848rte,
        pn.case2869pegase,
        pn.case3120sp,
        pn.case6470rte,
        pn.case6495rte,
        pn.case6515rte,
        pn.case9241pegase,
        pn.GBnetwork,
        pn.GBreducednetwork,
        pn.iceland,
    ],
    "kerben": [
        pn.create_kerber_landnetz_freileitung_1,
        pn.create_kerber_landnetz_freileitung_2,
        pn.create_kerber_landnetz_kabel_1,
        pn.create_kerber_landnetz_kabel_2,
        pn.create_kerber_dorfnetz,
        pn.create_kerber_vorstadtnetz_kabel_1,
        pn.create_kerber_vorstadtnetz_kabel_2,
    ],
    "kerbenextreme": [
        pn.kb_extrem_landnetz_freileitung,
        pn.kb_extrem_landnetz_kabel,
        pn.kb_extrem_landnetz_freileitung_trafo,
        pn.kb_extrem_landnetz_kabel_trafo,
        pn.kb_extrem_dorfnetz,
        pn.kb_extrem_dorfnetz_trafo,
        pn.kb_extrem_vorstadtnetz_1,
        pn.kb_extrem_vorstadtnetz_2,
        pn.kb_extrem_vorstadtnetz_trafo_1,
        pn.kb_extrem_vorstadtnetz_trafo_2,
    ],
}


_db = []
for x in ["short", "middle", "long"]:
    for y in ["good", "average", "bad"]:
        foox = x
        fooy = y
        _db += [
            lambda: pn.create_dickert_lv_network(
                feeders_range=foox, linetype="cable", customer="multiple", case=fooy
            )
        ]
network_bundle["direktLV"] = _db


_db = []
for x in ["rural_1", "rural_2", "village_1", "village_2", "suburb_1"]:
    foox = x
    _db += [lambda: pn.create_synthetic_voltage_control_lv_network(network_class=foox)]
network_bundle["synthetic_control"] = _db


network_list = []
for tag in network_bundle:
    for x in network_bundle[tag]:
        name = str(x.__name__)
        network_list += [(name, x)]

dick = {}
for i in range(len(network_list)):
    name, new = network_list[i]

    if name in dick:
        dick[name] += 1
        network_list[i] = (name + f"_{dick[name]}", new)
    else:
        dick[name] = -1


if __name__ == "__main__":
    for name, new in network_list:
        net = net()
