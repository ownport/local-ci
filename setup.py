from setuptools import setup

setup(
    name='local-ci',
    version='1.0.2',
    py_modules=['local_ci'],
    entry_points='''
        [console_scripts]
        local-ci=local_ci.main:run
    ''',
)
