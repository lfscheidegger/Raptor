# Raptor - smart hooks for git
# Copyright (C) 2012 Luiz Scheidegger

"""
setup.py
Setup script to install raptor.
"""

from setuptools import setup

setup(
  name = "raptor",
  version = "0.2",
  packages = ['raptor', 'raptor.src', 'raptor.src.hooks', 'raptor.src.jobs'],
  entry_points = {
    'console_scripts': [
      'raptor = raptor.src.main:main'
    ]
  }
)
