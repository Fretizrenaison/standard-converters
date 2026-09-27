import numpy as np

def solve_sps_dab(v_in: float, v_out: float, p_req: float, 
                  f_sw: float, n_turns: float = 1.0, d_ratio: float = 0.25) -> dict:
    """
    Pure mathematical solver for Dual Active Bridge (Single Phase Shift).
    """
    v_out_ref = v_out / n_turns
    t_sw = 1.0 / f_sw

    # Required Leakage Inductance (Lk)
    l_k = (v_in * v_out_ref * d_ratio * (1.0 - d_ratio)) / (2.0 * f_sw * p_req)

    # Switching instant currents (i1 at t=0, i2 at t=D*T_sw/2)
    i_1 = (v_out_ref * (1.0 - 2.0 * d_ratio) - v_in) / (4.0 * f_sw * l_k)
    i_2 = (v_in * (2.0 * d_ratio - 1.0) + v_out_ref) / (4.0 * f_sw * l_k)

    # Piecewise linear waveform coordinates over one full cycle
    t_points = np.array([
        0.0, 
        d_ratio * t_sw / 2.0, 
        t_sw / 2.0, 
        (1.0 + d_ratio) * t_sw / 2.0, 
        t_sw
    ])
    i_points = np.array([i_1, i_2, -i_1, -i_2, i_1])

    # RMS Current calculation for piecewise trapezoidal waveform
    i_rms = np.sqrt((i_1**2 + i_1 * i_2 + i_2**2) / 3.0)

    return {
        "lk_uH": float(l_k * 1e6),
        "i_peak_A": float(max(abs(i_1), abs(i_2))),
        "i_rms_A": float(i_rms),
        "time_us": (t_points * 1e6).tolist(),
        "current_A": i_points.tolist()
    }
    