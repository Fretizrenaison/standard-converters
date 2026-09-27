import json
from views.dab_view import DAB_CONFIG, compute_dab_view

CONVERTER_REGISTRY = [
    {"id": "dab",     "name": "DAB Converter",                   "active": True},
    {"id": "buck",    "name": "BUCK Converter (Coming Soon)",    "active": False},
    {"id": "flyback", "name": "FLYBACK Converter (Coming Soon)", "active": False},
]


def _json_serializer(obj):
    """Standard serializer for NumPy arrays and floating-point scalars."""
    if hasattr(obj, "tolist"):
        return obj.tolist()
    if hasattr(obj, "item"):
        return obj.item()
    raise TypeError(f"Type {type(obj)} is not JSON serializable")


def get_app_schema_json() -> str:
    return json.dumps({
        "converters": CONVERTER_REGISTRY,
        "configs": {
            "dab": DAB_CONFIG
        }
    }, default=_json_serializer)


def run_converter_json(converter_id: str, params_json: str) -> str:
    params = json.loads(params_json)
    if converter_id == "dab":
        return json.dumps(compute_dab_view(params), default=_json_serializer)
    return json.dumps({"error": f"{converter_id} is under development."})