from setuptools import setup

setup(
    name='local-ci',
    version='1.0.0',
    py_modules=['local_ci'],
    # install_requires=[
    #     'pyaml',
    # ],
    entry_points='''
        [console_scripts]
        local-ci=local_ci.main:run
    ''',
)
