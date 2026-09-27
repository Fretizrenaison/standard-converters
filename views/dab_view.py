from engine.dab_math import solve_sps_dab

DAB_CONFIG = {
    "id": "dab",
    "name": "DAB Converter",
    "title": "Dual Active Bridge (DAB) — Single Phase Shift (SPS)",
    "specs": [
        {"key": "v_in",     "label": "Vin nom (V1)",    "default": 400.0,  "step": 10.0,  "min": 1.0,  "unit": "V"},
        {"key": "v_out",    "label": "Vout nom (V2)",   "default": 400.0,  "step": 10.0,  "min": 1.0,  "unit": "V"},
        {"key": "n_turns",  "label": "Turns Ratio (n)", "default": 1.0,    "step": 0.1,   "min": 0.01, "unit": "N1/N2"},
        {"key": "power",    "label": "Rated Power",     "default": 2000.0, "step": 100.0, "min": 10.0, "unit": "W"},
        {"key": "f_sw_khz", "label": "Sw. Freq",        "default": 100.0,  "step": 5.0,   "min": 1.0,  "unit": "kHz"},
    ],
    "modulation": [
        {"key": "d_ratio",  "label": "Phase Shift Ratio (D)", "default": 0.25, "min": 0.01, "max": 0.49, "step": 0.01}
    ],
    "design_groups": [
        {
            "group": "Inductor & Transformer",
            "rows": [
                {"label": "Lk Required",  "key": "lk_uH",    "fmt": "{:.2f}", "unit": "µH"},
                {"label": "I_L Peak",     "key": "i_peak_A", "fmt": "{:.2f}", "unit": "A"},
                {"label": "I_L RMS",      "key": "i_rms_A",  "fmt": "{:.2f}", "unit": "A"},
                {"label": "Tx VA Rating", "key": None,       "fmt": "—",      "unit": "kVA"},
            ]
        },
        {
            "group": "Capacitors (Cin / Cout)",
            "rows": [
                {"label": "Cin Bulk",     "key": None,       "fmt": "—",      "unit": "µF"},
                {"label": "Cout Bulk",    "key": None,       "fmt": "—",      "unit": "µF"},
                {"label": "ΔVo Ripple",   "key": None,       "fmt": "—",      "unit": "%"},
            ]
        },
        {
            "group": "Operating Point & Efficiency",
            "rows": [
                {"label": "Phase Shift D","key": "d_ratio",  "fmt": "{:.2f}", "unit": ""},
                {"label": "ZVS Status",   "key": None,       "fmt": "—",      "unit": ""},
                {"label": "Efficiency η", "key": None,       "fmt": "—",      "unit": "%"},
            ]
        }
    ]
}

def compute_dab_view(params: dict) -> dict:
    """Runs the pure math engine and formats values for the CAD shell."""
    v_in = float(params.get("v_in", 400.0))
    v_out = float(params.get("v_out", 400.0))
    n_turns = float(params.get("n_turns", 1.0))
    power = float(params.get("power", 2000.0))
    f_sw_khz = float(params.get("f_sw_khz", 100.0))
    d_ratio = float(params.get("d_ratio", 0.25))

    raw = solve_sps_dab(v_in, v_out, power, f_sw_khz * 1e3, n_turns, d_ratio)
    raw["d_ratio"] = d_ratio

    formatted = {}
    for grp in DAB_CONFIG["design_groups"]:
        for row in grp["rows"]:
            k = row["key"]
            if k and k in raw:
                formatted[k] = row["fmt"].format(raw[k])

    return {
        "raw": raw,
        "formatted": formatted
    }