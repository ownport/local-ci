from setuptools import setup

setup(
    name='local-ci',
    version='0.1',
    py_modules=['local_ci'],
    # install_requires=[
    #     'pyaml',
    # ],
    entry_points='''
        [console_scripts]
        local-ci=local_ci.main:run
    ''',
)
