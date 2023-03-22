from MultiFlowSim.voguel import *
import pytest



def test_sim():


    assert plot_riemann_sum(f, 0, 2, 10, method="left") == None
    assert plot_riemann_sum(f, 0, 2, 20, method="right") == None
    assert plot_riemann_sum(f, 0, 2, 30, method="middle") == None

test_plot_riemann_sum()