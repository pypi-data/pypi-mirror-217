import numpy as np
import pytest
import importlib.util
import lekkersim as lk


A = np.array(
    [
        [
            0.00000000e00 + 0.0j,
            0.00000000e00 + 0.0j,
            4.32978028e-17 + 0.70710678j,
            7.07106781e-01 + 0.0j,
        ],
        [
            0.00000000e00 + 0.0j,
            0.00000000e00 + 0.0j,
            -7.07106781e-01 + 0.0j,
            4.32978028e-17 - 0.70710678j,
        ],
        [
            4.32978028e-17 - 0.70710678j,
            7.07106781e-01 + 0.0j,
            0.00000000e00 + 0.0j,
            0.00000000e00 + 0.0j,
        ],
        [
            -7.07106781e-01 + 0.0j,
            4.32978028e-17 + 0.70710678j,
            0.00000000e00 + 0.0j,
            0.00000000e00 + 0.0j,
        ],
    ]
)

A = np.array(
    [
        [0.0 + 0.0j, 0.0 + 0.0j, 0.70710678 + 0.0j, 0.0 + 0.70710678j],
        [0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.70710678j, 0.70710678 + 0.0j],
        [0.70710678 + 0.0j, 0.0 + 0.70710678j, 0.0 + 0.0j, 0.0 + 0.0j],
        [0.0 + 0.70710678j, 0.70710678 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j],
    ]
)


def test_simple_model():
    BS = lk.BeamSplitter()
    S = BS.create_S()
    assert np.allclose(S, A)
    S = BS.create_S()
    assert np.allclose(S, A)
    S = BS.solve().S
    assert np.allclose(S, A)
    S = BS.solve(wl=[1.5, 1.55, 1.6]).S
    assert np.allclose(S, np.array(3 * [A]))
    S = BS.solve(wl=np.linspace(1.5, 1.6, 3)).S
    assert np.allclose(S, np.array(3 * [A]))


def test_parametric_block():
    PS = lk.PhaseShifter()
    assert PS.solve().get_PH("a0", "b0") == pytest.approx(0.0, 1e-8)
    assert PS.solve(PS=1.0).get_PH("a0", "b0") == pytest.approx(np.pi, 1e-8)
    assert np.allclose(
        PS.solve(PS=np.linspace(0.0, 1.0, 101))
        .get_data("a0", "b0")["Phase"]
        .to_numpy(),
        np.linspace(0.0, np.pi, 101),
    )


def test_MZM():
    with lk.Solver(name="MZM_BB") as MZM_BB_sol:
        BM = lk.BeamSplitter()
        WG = lk.Waveguide(L=500, n=2.5)
        PS = lk.PhaseShifter()
        AT = lk.Attenuator(loss=0.0)

        bm1 = BM.put()
        t_ = WG.put("a0", bm1.pin["b0"])
        t_ = PS.put("a0", t_.pin["b0"], param_mapping={"PS": "PS1"})
        t_ = PS.put("a0", t_.pin["b0"], param_mapping={"PS": "DP"})
        t_ = AT.put("a0", t_.pin["b0"])
        bm2 = BM.put("a0", t_.pin["b0"])
        t_ = WG.put("a0", bm1.pin["b1"])
        t_ = PS.put("a0", t_.pin["b0"], param_mapping={"PS": "PS2"})
        t_ = AT.put("a0", t_.pin["b0"])
        lk.connect(t_.pin["b0"], bm2.pin["a1"])

        lk.Pin("a0").put(bm1.pin["a0"])
        lk.Pin("a1").put(bm1.pin["a1"])
        lk.Pin("b0").put(bm2.pin["b0"])
        lk.Pin("b1").put(bm2.pin["b1"])

        lk.set_default_params({"PS1": 0.0, "PS2": 0.5, "DP": 0.0})

    psl = np.linspace(0.0, 1.0, 5)
    assert np.allclose(
        MZM_BB_sol.solve(wl=1.55, DP=psl, PS1=0.0, PS2=0.0)
        .get_data("a0", "b0")["T"]
        .to_numpy(),
        np.sin(0.5 * np.pi * psl) ** 2.0,
    )
    assert np.allclose(
        MZM_BB_sol.solve(wl=1.55, DP=psl, PS1=0.0, PS2=0.5)
        .get_data("a0", "b0")["T"]
        .to_numpy(),
        np.sin((0.5 * psl - 0.25) * np.pi) ** 2.0,
    )
    assert np.allclose(
        MZM_BB_sol.solve(wl=1.55, DP=psl, PS1=0.5, PS2=0.0)
        .get_data("a0", "b0")["T"]
        .to_numpy(),
        np.sin((0.5 * psl + 0.25) * np.pi) ** 2.0,
    )
    assert np.allclose(
        MZM_BB_sol.solve(wl=1.55, DP=psl, PS1=0.5).get_data("a0", "b0")["T"].to_numpy(),
        np.sin((0.5 * psl) * np.pi) ** 2.0,
    )

    # assert np.allclose(MZM_BB_sol.solve(wl=1.55, DP=psl, PS1=0.5, PS2=0.0).get_data('a0','b0')['T'].to_numpy(), np.cos(0.5*np.pi*psl+0.25)**2.0)


if __name__ == "__main__":
    # PS=lk.PhaseShifter()
    # a=PS.solve(PS=np.linspace(0.0,1.0,101)).get_data('a0','b0')['Phase']
    # print(a.to_numpy())
    pytest.main([__file__, "-s", "-v"])  # -s: show print output
