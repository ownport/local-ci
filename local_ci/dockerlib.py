
import random
import string

from packages import sh

DOCKER_RUN_TEMPLATE="docker run -ti --rm --name {container_name} -v {volume_path}:/data/ {docker_image} {script}"

def get_container_name(prefix=None, n=6):
    '''returns random container name as "local-ci-<random>
    '''
    rand = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))
    if prefix:
        return '-'.join([prefix,rand])
    else:
        return '-'.join(['local-ci',rand])


def run_docker_containter(image, repo_path, opts={}):
    ''' run docker container
    '''
    def process_stdout(line):
        print line,

    def process_stderr(line):
        print line,

    if 'name' in opts and opts.get('name', None):
        opts['name'] = get_container_name(opts['name'])
    else:
        opts['name'] = get_container_name()

    if 'hostname' in opts and opts.get('hostname', None):
        opts['hostname'] = opts['name']

    print "[INFO] image: %s, container_name: %s, path: %s" % (image, opts['name'], repo_path)
    try:
        docker_opts = ['run', '-i', '--rm',]
        docker_opts.extend(['--%s=%s' % (k,v) for k,v in opts.items() ])
        docker_opts.extend(['-v', "%s:/repo/" % repo_path, image, '/repo/.local-ci/run.sh',])
        print "[INFO] docker options: %s" % docker_opts

        process = sh.docker(*docker_opts, _iter=True, _out=process_stdout, _err=process_stderr)
        process.wait()

    except sh.ErrorReturnCode, err:
        print err

# def t1():
#     bash_script = []
#     bash_script.extend([DOCKER_RUN_TEMPLATE.format(
#                             container_name="???",
#                             docker_image=di,
#                             volume_path=os.path.dirname(self._travel_yml_path),
#                             script='/data/run/script')
#                             for di in self._docker_images])
