from setuptools import setup

setup(
    name = "raptor",
    version = "0.1",
    packages = ['src', 'src.hooks', 'src.jobs'],
    entry_points = {
        'console_scripts': [
            'raptor = src.main:main'
        ]
    }
)
