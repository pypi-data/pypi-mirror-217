# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../../"))

# -- Project information -----------------------------------------------------

project = "cascade-config"
author = "RalfG"
github_project_url = "https://github.com/ralfg/cascade-config/"
github_doc_root = "https://github.com/ralfg/cascade-config/tree/main/docs/"


def get_version(path):
    with open(path, "rt") as f:
        for line in f:
            if line.startswith("__version__ = "):
                return line.strip().split(" = ")[1].strip("\"'")


# The full version, including alpha/beta/rc tags
release = get_version("../../cascade_config.py")

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
    "sphinx_mdinclude",
]
source_suffix = [".rst", ".md"]
master_doc = "index"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]


# -- Autodoc options --------------------------------------------------------
autodoc_default_options = {"members": True, "show-inheritance": True}
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autoclass_content = "init"


# https://github.com/rtfd/recommonmark/blob/master/docs/conf.py
def setup(app):
    config = {
        # 'url_resolver': lambda url: github_doc_root + url,
        "auto_toc_tree_section": "Contents",
        "enable_eval_rst": True,
    }
