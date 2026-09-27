import streamlit as st
import pandas as pd
from engine.dab_math import solve_sps_dab

def render_dab_subsection():
    st.header("Dual Active Bridge (DAB) Converter")
    st.caption("Isolated Bidirectional DC-DC Topology — Single Phase Shift (SPS) Synthesis")

    # Sidebar inputs specific to the DAB subsection
    st.sidebar.subheader("DAB Specifications")
    v_in = st.sidebar.number_input("Input Voltage V1 (V)", value=400.0, step=10.0, min_value=1.0)
    v_out = st.sidebar.number_input("Output Voltage V2 (V)", value=400.0, step=10.0, min_value=1.0)
    n_turns = st.sidebar.number_input("Turns Ratio (n = N1/N2)", value=1.0, step=0.1, min_value=0.01)
    power = st.sidebar.number_input("Rated Power (W)", value=2000.0, step=100.0, min_value=10.0)
    f_sw_khz = st.sidebar.number_input("Switching Frequency (kHz)", value=100.0, step=5.0, min_value=1.0)
    d_ratio = st.sidebar.slider("Phase Shift Ratio (D)", min_value=0.01, max_value=0.49, value=0.25, step=0.01)

    # Call the isolated math engine
    results = solve_sps_dab(v_in, v_out, power, f_sw_khz * 1e3, n_turns, d_ratio)

    # Display calculated parameters in a 3-column metric row
    col1, col2, col3 = st.columns(3)
    col1.metric("Required Inductance (Lk)", f"{results['lk_uH']:.2f} µH")
    col2.metric("Peak Inductor Current", f"{results['i_peak_A']:.2f} A")
    col3.metric("RMS Inductor Current", f"{results['i_rms_A']:.2f} A")

    st.divider()

    # Plot waveform
    st.subheader("Steady-State Inductor Current Waveform i_L(t)")
    df = pd.DataFrame({
        "Time (µs)": results["time_us"],
        "Inductor Current (A)": results["current_A"]
    }).set_index("Time (µs)")

    st.line_chart(df, use_container_width=True)