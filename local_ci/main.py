# -*- coding: utf-8 -*-

import os
import sys
import optparse

from utils import get_settings
from utils import get_repo_dispatcher

def run():

    parser = optparse.OptionParser()
    parser.add_option('-r', '--repo-path', help="the path to source repository")
    parser.add_option('-s', '--settings', help="the path to local-ci configuration file (.local-ci.yml)")
    opts, args = parser.parse_args()

    if not opts.repo_path or not os.path.exists(opts.repo_path):
        print >> sys.stderr, '[ERROR] The path to source repo is not specified or does not exist'
        sys.exit(1)

    if not opts.settings or not os.path.exists(opts.settings):
        print >> sys.stderr, '[ERROR] The path to configuration file is not specified or does not exist'
        sys.exit(1)

    repo_dispatcher = get_repo_dispatcher(opts.repo_path, get_settings(opts.settings))

    for image in repo_dispatcher.docker_images():
        if not image:
            print >> sys.stderr, "[WARNING] Unknown image, %s" % image
        else:
            print >> sys.stderr, "[INFO] The image, %s" % image
            repo_dispatcher.run(image)
