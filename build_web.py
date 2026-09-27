from stlitepack import pack, setup_github_pages

pack(
    "app.py",
    requirements=["numpy", "pandas"],
    extra_files_to_embed=[
        "engine/__init__.py",
        "engine/dab_math.py",
        "views/__init__.py",
        "views/dab_view.py"
    ],
    title="Standard Converters"
)

setup_github_pages(mode="gh-actions")