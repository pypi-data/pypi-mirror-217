"""Sphinx configuration."""  # noqa: INP001

project = 'SQLs'
copyright = '2023, Marko Durkovic'  # noqa: A001
author = 'Marko Durkovic'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
]

html_theme = 'furo'
