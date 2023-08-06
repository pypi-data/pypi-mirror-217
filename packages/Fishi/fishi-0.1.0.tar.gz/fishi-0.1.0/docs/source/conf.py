# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.append(os.path.abspath('../../'))
import Fishi


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Fishi'
copyright = '2022, Jonas Pleyer, Polina Gaindrik'
author = 'Jonas Pleyer, Polina Gaindrik'
release = '0.0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.mathjax',
    'sphinxcontrib.bibtex',
]

autosummary_generate = True
add_module_names = False
autodoc_typehints_format = 'short'

templates_path = ['_templates']
exclude_patterns = ['_build', '_templates', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_theme_options = {
   "logo": {
      "image_light": "logo-light.png",
      "image_dark": "logo-dark.png",
   }
}
html_static_path = ['_static']
bibtex_bibfiles = ['references.bib']
