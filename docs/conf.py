# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

import datetime
import pathlib
import sys

root = pathlib.Path(__file__).parent.parent
sys.path.insert(0, root.as_posix())

project = "aioitertools"
copyright = f"{datetime.date.today().year}, Amethyst Reese"
author = "Amethyst Reese"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx_mdinclude",
]

autodoc_default_options = {
    "show-inheritance": True,
    "members": True,
    "inherited-members": True,
}
autodoc_member_order = "bysource"
autodoc_typehints = "description"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

highlight_language = "python3"
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
master_doc = "index"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"
html_theme_options = {
    "description": "itertools and more for AsyncIO",
    "fixed_sidebar": True,
    "badge_branch": "master",
    "github_button": False,
    "github_user": "omnilib",
    "github_repo": "aioitertools",
    "show_powered_by": False,
    "sidebar_collapse": False,
    "extra_nav_links": {
        "Report Issues": "https://github.com/omnilib/aioitertools/issues",
    },
}

html_sidebars = {
    "**": [
        "about.html",
        "badges.html",
        "navigation.html",
        "relations.html",
        "searchbox.html",
        "omnilib.html",
    ],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
