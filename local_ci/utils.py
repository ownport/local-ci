import os
import re
import sys
import stat
import shutil
import unicodedata

import travis

from packages import yaml
from errors import IncorrectFileFormat


def get_repo_dispatcher(repo_path, settings):
    ''' returns repository dispatcher
    '''
    for config in os.listdir(repo_path):
        if config == '.travis.yml':
            return travis.TravisRepoDispatcher(repo_path, settings)

def get_settings(path):
    ''' retunrs settings from file
    '''
    return read_yaml(path)


def read_yaml(path):
    ''' returns content of yaml file as dict or list
    '''
    path = os.path.abspath(path)
    if not os.path.exists(path):
        raise IOError("The file does not exist, %s" % path)
    try:
        content = yaml.load(open(path, 'r').read())
    except yaml.scanner.ScannerError, err:
        raise IncorrectFileFormat("%s: %s" % (path,err))

    return content


def slugify(value):
    ''' Convert to ASCII. Convert spaces to hyphens. Remove characters that aren't
    alphanumerics, underscores, or hyphens. Convert to lowercase. Also strip
    leading and trailing whitespace.

    https://github.com/django/django/blob/master/django/utils/text.py
    '''
    value = unicodedata.normalize('NFKC', unicode(value))
    value = re.sub('[^\w\s-]', '-', value, flags=re.U).strip().lower()
    return re.sub('[-\s]+', '-', value, flags=re.U)


def renew_local_ci_path(repo_path):
    ''' re-new local-ci path
    '''
    local_ci_run_path = os.path.join(repo_path, '.local-ci/')
    if os.path.exists(local_ci_run_path):
        shutil.rmtree(local_ci_run_path)
    os.mkdir(local_ci_run_path)

    return local_ci_run_path


def create_run_script(path, script):
    ''' create run script
    '''
    script_path = os.path.join(path, 'run.sh')
    with open(script_path, 'w+') as run_sh:
        run_sh.write(script)
    st = os.stat(script_path)
    os.chmod(script_path, st.st_mode | stat.S_IEXEC)
