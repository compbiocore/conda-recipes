import os
import sys
import json
import yaml
import glob
import logging
import argparse
import subprocess
from subprocess import PIPE, call, check_call, Popen, check_output
from jinja2 import Environment, FileSystemLoader

from conda_build.config import Config


config = Config()

log = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
handler.setLevel(logging.INFO)
log.addHandler(handler)
log.setLevel(logging.INFO)

def build_recipes(recipes, channel, environment, readme, al, ap):
    '''Build multiple recipes recursively.
    Parameters
    ----------
    recipes : set
        Set of recipes to build.
    channel : str
        Anaconda channel where the packages will be uploaded.
    environment : str
        Path to environment yaml from which to reconstruct files
    '''
    build_error = 0
    build_passed = 0
    failed_recipes = ""

    for p in recipes:
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
                            install(name, version, channel, environment, readme, al, ap)
                        else:
                            log.info("Failed build: {0}".format(root))
                            build_error+=1
                            failed_recipes=failed_recipes+root+"\n"
                        log.info("Cleaning environment.")
                        FNULL = open(os.devnull, 'w')
                        call('conda clean -a -y', shell=True, stdout=FNULL, stderr=subprocess.STDOUT, close_fds=True)
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
    build_cmd = 'conda build -c compbiocore "%s" --perl 5.26.2' % root
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
    return False

def changed_recipes(diff_files):
    recipes = set()
    for file in diff_files.split('\n'):
        if file.startswith('recipes'):
            folder = file.split('/')[1]
            recipes.add('recipes/'+folder)
    return recipes

def install(name, version, channel, environment, readme, al, ap):
    '''Install a built package. If there are dependency conflicts with the main environment,
    output to a log file and add conflict label. Otherwise add main label and add to main env.

    Parameters
    ----------
    name: str
        Package name.
    version : str
        Package version.
    channel : str
        Channel where package will be uploaded.
    environment : str
        YAML conda environment file.
    readme : str
        path to README.md of Github repo
    '''
    env_cmd = 'conda env create -f {0}'.format(environment)
    log.info('Setting up main environment: {0}'.format(env_cmd))
    call(env_cmd, shell=True)

    log.info('Activating environment: source activate main')
    call('source activate main', shell=True)

    install_cmd = 'conda install --use-local %s=%s --yes' % (name, version)
    log.info('Installing: {0}'.format(install_cmd))
    proc = call(install_cmd, shell=True)

    if proc==0:
        log.info('No conflicts with main environment.')
        upload(name, version, channel, al, ap)
    else:
        log.info('%s conflicts with main environment' % name)
        ## TODO: modify readme todo...
        with open(readme,'a') as f:
            f.write(name+'\n')
        if os.environ['TRAVIS_SECURE_ENV_VARS'] == 'true':
            upload(name, version, channel, al, ap, label="conflict")
        else:
            log.info("Uploading not available in Pull Requests")
#        dependency_conflicts.py

def upload(name, version, channel, al, ap, label="main"):
    '''Upload a built package.
    Parameters
    ----------
    name : str
        Package name.
    version : str
        Package version.
    channel : str
        Channel where the package will be uploaded.
    label : str
        Label to be uploaded with. Should generally be main or conflict.
    '''
    built_glob = os.path.join(
        config.bldpkgs_dir,
        '{0}-{1}*.tar.bz2'.format(name, version))
    built = glob.glob(built_glob)[0]
    login_cmd = 'anaconda login --username %s --password %s' % (al, ap)
    upload_cmd = 'anaconda upload -u %s %s --label %s' % (channel, built, label)
    # Do not show decrypted token!
    log.info('Uploading: {0}'.format(upload_cmd))
    try:
        proc_login = check_call(login_cmd, shell=True)
        log.info(proc_login)
        proc_upload = check_call(
            upload_cmd, shell=True)
        log.info(proc_upload)
    except:
        log.info("Uploading failed; did you update the build version? The script will not force upload"+
            "so please manually upload if necessary.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build, upload and install recipes with logs to identify errors.')

    ds = ' [%(default)s]'
    parser.add_argument('range', help='commit range')
    parser.add_argument('-r', '--readme', help='path to README.md')
    parser.add_argument('-c', '--channel', help='channel to build and upload recipes to')
    parser.add_argument('-al', '--anaconda_login', help='anaconda login')
    parser.add_argument('-ap', '--anaconda_password', help='anaconda password')
    parser.add_argument('-e', '--environment', help='conda environment.yml to replicate base env from')
    opts = parser.parse_args()

    channel = opts.channel
    env = opts.environment
    readme = opts.readme
    al = opts.anaconda_login
    ap = opts.anaconda_password


    diff_files_cmd = 'git diff --name-only {0}'.format(opts.range)
    diff_files = check_output(diff_files_cmd, shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
    log.info('Changed files are: {0}'.format(diff_files))
    recipes = changed_recipes(diff_files)
    log.info('Changed recipes are: {0}'.format(recipes))

    build_recipes(recipes, channel, env, readme, al, ap)