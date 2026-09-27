"""
Build script for The Standard Converters Project.
Bundles pure Python modules (engine/ & views/) into web/template.html
to produce the static WebAssembly application at docs/index.html.
"""
import json
from pathlib import Path

PYTHON_MODULES = [
    "engine/__init__.py",
    "engine/dab_math.py",
    "views/__init__.py",
    "views/dab_view.py",
    "app.py",
]

TEMPLATE_PATH = Path("web/template.html")
OUTPUT_PATH = Path("docs/index.html")


def build():
    bundle = {}
    for path in PYTHON_MODULES:
        code = Path(path).read_text(encoding="utf-8")
        if "import streamlit" in code:
            raise RuntimeError(f"❌ '{path}' still imports streamlit. Save the updated file first!")
        bundle[path] = code

    # Smoke-test app.py locally so any Python bug is caught immediately in the terminal
    import app
    schema_test = json.loads(app.get_app_schema_json())
    calc_test = json.loads(app.run_converter_json("dab", "{}"))
    assert "converters" in schema_test and "raw" in calc_test, "App output check failed!"

    template_html = TEMPLATE_PATH.read_text(encoding="utf-8")
    compiled_html = template_html.replace("__PYTHON_BUNDLE__", json.dumps(bundle))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(compiled_html, encoding="utf-8")
    print(f"✅ Build verified & written to {OUTPUT_PATH} (Lk = {calc_test['raw']['lk_uH']:.2f} uH)")


if __name__ == "__main__":
    build()