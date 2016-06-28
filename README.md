# local-ci

[![Build Status](https://travis-ci.org/ownport/local-ci.svg?branch=master)](https://travis-ci.org/ownport/local-ci)

Simple CI tool for building and testing projects in different environments. Local-CI is used the approach with docker containers to create new environment, install required for the project dependencies and run tests.

## Installation

No installation is required. Just needed to copy binary file `local-ci` from Releases page  https://github.com/ownport/local-ci/releases to your computer and run from command line:

```sh
$ ./bin/local-ci --help
Usage: local-ci [options]

Options:
  -h, --help            show this help message and exit
  -r REPO_PATH, --repo-path=REPO_PATH
                        the path to source repository
  -s SETTINGS, --settings=SETTINGS
                        the path to local-ci configuration file (.local-
                        ci.yml)
```

## How to use

At the moment local-ci supports [Travis-CI](https://travis-ci.org/) configuration
[YAML file](https://docs.travis-ci.com/user/customizing-the-build/) for building and testing projects in different environments

The repository of local-ci project itself is good example how this project could be used for building and testing
projects locally. [.travis-ci.yml](https://github.com/ownport/local-ci/blob/master/.travis.yml) file is used as for
local testing as for testing project in Travis-CI environment

There is the example of .travis-ci.yml file in the local-ci repository which used by Travis-CI for testing the project:
```yaml
language: python

python:
  - "2.7"
  # - "3.5"

env:
  - PYTHONDONTWRITEBYTECODE=1

install:
  - pip install ${PIP_OPTS} pytest
  - pip install ${PIP_OPTS} pytest-cov

script:
  - pip install --editable .
  - make test-all-with-coverage
````

The result of the execution can be founded on the [Travis-CI dashboard for local-ci project](https://travis-ci.org/ownport/local-ci)

Similar results can be achieved by using local-ci script. In the command line you need to specify the path to local
directory to project and local-ci configuration file:

```sh
$ ./bin/local-ci -r /svc/github/local-ci/ -s /svc/github/local-ci/.local-ci.yml
```

The .local-ci.yml configuration file contains additional information about:
- the environment inside of docker container  
- docker images mapping which will be used based on `language` and `version` fields from .travis-ci.yml file.

The example of .local-ci.yml file:

```yaml
env:
  - LOCAL_REPOS_HOST=172.17.0.2
  - PIP_OPTS="--index-url=http://${LOCAL_REPOS_HOST}/repo/pypi/simple/ --trusted-host=${LOCAL_REPOS_HOST}"

docker-images:
  python:2.7: ownport/python-dev:2.7
  python:3.5: ownport/python-dev:3.5
```

After starting the script above in command line you can see the next result:

```sh
$ make run-local-ci
[INFO] Cleaning directory: /media/data1/svc/github/local-ci/bin
[INFO] Cleaning directory: /media/data1/svc/github/local-ci/.local-ci
[INFO] Cleaning directory: /media/data1/svc/github/local-ci/local-ci.egg-info
[INFO] Cleaning files: *.pyc
[INFO] Cleaning files: .coverage
[INFO] Compiling to binary, local-ci
[INFO] image: ownport/python-dev:2.7, container_name: local-ci-94zpf4, path: /media/data1/svc/github/local-ci
Collecting pytest
  Downloading http://172.17.0.2/repo/pypi/simple/pytest/pytest-2.9.2-py2.py3-none-any.whl (162kB)
Collecting py>=1.4.29 (from pytest)
  Downloading http://172.17.0.2/repo/pypi/simple/py/py-1.4.31-py2.py3-none-any.whl (81kB)
Installing collected packages: py, pytest
Successfully installed py-1.4.31 pytest-2.9.2
Collecting pytest-cov
  Downloading http://172.17.0.2/repo/pypi/simple/pytest-cov/pytest_cov-2.2.1-py2.py3-none-any.whl
Requirement already satisfied (use --upgrade to upgrade): pytest>=2.6.0 in /usr/lib/python2.7/site-packages (from pytest-cov)
Collecting coverage>=3.7.1 (from pytest-cov)
  Downloading http://172.17.0.2/repo/pypi/simple/coverage/coverage-4.1.tar.gz (370kB)
Requirement already satisfied (use --upgrade to upgrade): py>=1.4.29 in /usr/lib/python2.7/site-packages (from pytest>=2.6.0->pytest-cov)
Installing collected packages: coverage, pytest-cov
  Running setup.py install for coverage: started
    Running setup.py install for coverage: finished with status 'done'
Successfully installed coverage-4.1 pytest-cov-2.2.1
Obtaining file:///repo
Installing collected packages: local-ci
  Running setup.py develop for local-ci
Successfully installed local-ci
[INFO] Cleaning directory: /repo/bin
[INFO] Cleaning directory: /repo/.local-ci
[INFO] Cleaning directory: /repo/local-ci.egg-info
[INFO] Cleaning files: *.pyc
[INFO] Cleaning files: .coverage
============================= test session starts ==============================
platform linux2 -- Python 2.7.11, pytest-2.9.2, py-1.4.31, pluggy-0.3.1
rootdir: /repo, inifile:
plugins: cov-2.2.1
collected 1 items

tests/test_utils.py .
--------------- coverage: platform linux2, python 2.7.11-final-0 ---------------
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
local_ci/__init__.py          0      0   100%
local_ci/__main__.py          2      2     0%   1-3
local_ci/dispatchers.py      22     12    45%   11-15, 21-24, 30-33, 39, 45
local_ci/dockerlib.py        22     15    32%   12-13, 19-37, 40-41
local_ci/errors.py            2      0   100%
local_ci/main.py             19     19     0%   3-28
local_ci/travis.py           37     25    32%   31-37, 43-51, 58-74
local_ci/utils.py            40     22    45%   17-19, 24, 30-38, 56-61, 67-71
-------------------------------------------------------
TOTAL                       144     95    34%

=========================== 1 passed in 1.14 seconds ===========================
$
```
