# -*- coding: utf-8 -*-

import os
import re

import utils

from dispatchers import BaseDispatcher


BASH_SCRIPT_TEMPLATE='''#!/bin/bash'''
RE_ENV_PATTERN=re.compile(r'^.+?=.+?$')
CI_STAGES = [
    'before_install', 'install',
    'before_script', 'script',
    'after_success', 'after_failure',
    'before_deploy', 'deploy', 'after_deploy',
    'after_script',
]

SUPPORTED_CI_STAGES = [
    'install',
    'script',
]


class TravisRepoDispatcher(BaseDispatcher):

    def __init__(self, path, settings):

        super(TravisRepoDispatcher, self).__init__(path, settings)

        self._travisyml_path = os.path.join(self.repo_path, '.travis.yml')
        if not os.path.exists(self._travisyml_path):
            raise IOError('The file .travis.yml does not exist in the directory %s' % self.repo_path)

        self._travisyml = utils.read_yaml(self._travisyml_path)


    def docker_images(self):
        ''' returns the list of docker images
        '''
        language = self._travisyml.get('language', None)
        if not language:
            raise RuntimeError("The language variable is missed in configuration files")

        versions = self._travisyml.get(language, None)
        if not versions:
            raise RuntimeError("The variable is missed in configuration file,  %s" % language)

        return [self.get_docker_image(':'.join((language, str(ver))))
                    for ver in versions]


    def script(self):
        ''' returns the script for execution in docker container
        '''
        script = ['#!/bin/sh',]

        env_vars = list(self._travisyml.get('env', []))
        env_vars.extend(list(self.settings.get('env', [])))

        script.extend(['\n# Environment variables'])
        script.extend([ "export %s" % e for e in env_vars if RE_ENV_PATTERN.match(e) ])

        for stage in SUPPORTED_CI_STAGES:
            stage_actions = self._travisyml.get(stage, None)
            if stage == 'install':
                stage_actions.append('cd /repo')
            if stage_actions:
                script.extend(['\n# Stage: %s' % stage,])
                script.extend(stage_actions)

        return '\n'.join(script)
