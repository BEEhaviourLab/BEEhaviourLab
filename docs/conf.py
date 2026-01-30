project = "BEEhaviourLab"
author = "BEEhaviourLab"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
]
autosummary_generate = True
exclude_patterns = []
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "show_prev_next": False,
}
