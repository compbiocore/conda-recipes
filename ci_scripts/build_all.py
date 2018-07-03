import os
import sys
import json
import yaml
import glob
import logging
import argparse
from subprocess import PIPE, call, check_call, Popen, check_output
from jinja2 import Environment, FileSystemLoader
import install

from conda_build.config import Config


config = Config()

log = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
handler.setLevel(logging.INFO)
log.addHandler(handler)
log.setLevel(logging.INFO)

def build_upload_recipes(p, channel):
    '''Build & upload recipes recursively in a directory.
    Parameters
    ----------
    p : str
        Path to the recipes.
    channel : str
        Anaconda channel where the packages will be uploaded.
    '''
    build_error = 0
    build_passed = 0
    failed_recipes = ""

    for root, dirs, files in os.walk(p):
        has_recipe = 'meta.yaml' in files
        if not dirs and has_recipe:
            with open(os.path.join(root, 'meta.yaml')) as f:
                log.info("Checking {}".format(root))

                # for Jinja
                env = Environment(loader=FileSystemLoader(root))
                template = env.get_template('meta.yaml')
                meta = yaml.load(template.render())
                
                name = meta['package']['name']
                version = meta['package']['version']
                try:
                    build_number = meta['build']['number']
                except: # Should be a KeyError but possible a TypeError or others as well
                    # Build number is 0 if not specified
                    build_number = 0
                if is_not_uploaded(name, version, build_number, channel):
                    build_call = build(root)
                    if build_call==0:
                        build_passed+=1
                    else:
                        log.info("Failed build: {0}".format(root))
                        build_error+=1
                        failed_recipes=failed_recipes+root+"\n"
                    log.info("Cleaning environment.")
                    FNULL = open(os.devnull, 'w')
                    call('conda clean -a -y', shell=True, stdout=FNULL, stderr=subprocess.STDOUT, close_fds=True)
                    #if os.environ['TRAVIS_SECURE_ENV_VARS'] == 'true':
                    #    upload(name, version, channel)
                    #else:
                    #    log.info("Uploading not available in Pull Requests")
                    log.info("Not uploading at the moment...")
                else:
                    # Only new packages (either version or build_number)
                    log.info("Skipping package: {0}-{1}-{2}".format(
                        name, version, build_number))
    log.info("Number of successfully built packages: {0}".format(build_passed))
    log.info("Number of errored packages while building: {0}".format(build_error))
    if build_error > 0:
        log.error("Have failed recipes: {0}".format(failed_recipes))
        raise ValueError("Have failed recipes. Please check log.")


def build(root):
    '''Build a recipe.
    Parameters
    ----------
    root : str
        the directory path for the recipe.
    '''
    # Quote is need in case the root path has spaces in it.
    #build_cmd = 'conda build --dirty "%s"' % root
    build_cmd = 'conda build -c compbiocore "%s"' % root
    log.info('Building: {0}'.format(build_cmd))
    FNULL = open(os.devnull, 'w')
    proc = call(build_cmd, shell=True, stdout=FNULL, stderr=subprocess.STDOUT, close_fds=True)
    return(proc)
    #    proc = Popen(build_cmd, shell=True, stdout=PIPE, stderr=subprocess.STDOUT)
#        proc.terminate()
#        return True
#    except (OSError, subprocess.CalledProcessError) as exception:
#        log.info("Exception occured: " + str(exception))
#        proc.terminate()
#        log.info("Build failed.")
#        with open("failed_recipes.txt",'a') as f:
#            f.write(root+"\n")
# need to figure out how docker permissions work...
#        return False
    # install()


def is_not_uploaded(name, version, build_number, channel):
    '''Check if we want to build & upload a package.
    It checks package name, version and build number
    sequentially to decide whether to build and upload it or not.
    Parameters
    ----------
    name : str
        Package name.
    version : str
        Package version.
    build_number : int
        Build number
    channel : str
        Anaconda channel to check the previous build.
    Returns
    -------
    Bool
        If a package in the channel has the same name, the same
        version, and an equal or higher build number, then return
        False; otherwise, return True.
    '''
    # if the package has never been uploaded so far, conda search throws an
    # error and check_call() would result in an exit status != 0, causing the Python
    # program to exit with an error. By adding ; true to the system call, we
    # ensure that Python does not break
    check_cmd = ('conda search --json --override-channels '
                 '-c {0} {1}; true').format(
                     channel, name)
    log.info('Checking: {0}'.format(check_cmd))
    proc = Popen(check_cmd, shell=True, stdout=PIPE)
    #proc = check_call(check_cmd, shell=True, stdout=PIPE)
    log.info(proc)
    res = json.loads(proc.communicate()[0].decode('utf-8'))

    # if the resulting object reports that package has never been uploaded,
    # we find and 'exception_name' with value 'PackageNotFoundError'
    if 'exception_name' in res:
        if res['exception_name'] == 'PackageNotFoundError':
            return True

    if name not in res:
        return True
    pkg = res[name]
    if version not in [i['version'] for i in pkg]:
        return True
    if build_number > max(
            i['build_number'] for i in pkg if i['version'] == version):
        return True
    return True

def changed_recipes(diff_files):
    recipes = []
    for file in diff_files:
        if file.startswith('recipes'):
            recipes.append(file)
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build, upload and install recipes with logs to identify errors.')

    ds = ' [%(default)s]'
    parser.add_argument('-r', '--readme', help='path to README.md')
    parser.add_argument('-d', '--dir', help='directory with recipes')
    parser.add_argument('-c', '--channel', help='channel to build and upload recipes to')
    parser.add_argument('-e', '--environment', help='conda environment.yml to replicate base env from')
    opts = parser.parse_args()

    recipes = opts.dir
    channel = opts.channel
    env = opts.environment

    build_upload_recipes(recipes, channel)