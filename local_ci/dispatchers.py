import os
import utils

from packages import sh
from dockerlib import run_docker_containter

class BaseDispatcher(object):

    def __init__(self, path, settings):

        self.repo_path = os.path.abspath(path)
        if not os.path.exists(self.repo_path):
            raise IOError('The repository does not exist, %s' % self.repo_path)

        self.settings = settings


    def get_docker_image(self, alias):
        ''' returns docker image name from settings according to provided alias
        '''
        if alias in self.settings['docker-images']:
            return self.settings['docker-images'].get(alias)
        else:
            return None


    def run(self, image):
        ''' run docker container based on image name
        '''
        local_ci_run_path = utils.renew_local_ci_path(self.repo_path)
        utils.create_run_script(local_ci_run_path, self.script())

        run_docker_containter(image, self.repo_path)


    def docker_images(self):
        ''' returns the list of docker images
        '''
        raise NotImplemented()


    def script(self):
        ''' returns the script for execution in docker container
        '''
        raise NotImplemented()
