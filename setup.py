from setuptools import setup

from local_ci import __version__

setup(
    name='local-ci',
    version=__version__,
    py_modules=['local_ci'],
    entry_points='''
        [console_scripts]
        local-ci=local_ci.main:run
    ''',
)
