import logging
import os

def install(name, version, channel, environment, readme):
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

    install_cmd = 'conda install --use-local %s=%s' % (name, version)
    log.info('Installing: {0}'.format(install_cmd))
    proc = call(install_cmd, shell=True)

    if proc==0:
        log.info('No conflicts with main environment.')
        if os.environ['TRAVIS_SECURE_ENV_VARS'] == 'true':
            upload(name, version, channel)
        else:
            log.info("Uploading not available in Pull Requests")
    else:
        log.info('%s conflicts with main environment' % name)
        ## TODO: modify readme todo...
        with open(readme,'a') as f:
            f.write(name+'\n')
        if os.environ['TRAVIS_SECURE_ENV_VARS'] == 'true':
            upload(name, version, channel, label="conflict")
        else:
            log.info("Uploading not available in Pull Requests")
#        dependency_conflicts.py

def upload(name, version, channel, label="main"):
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
    upload_cmd = 'anaconda -t {token} upload -u %s %s --label %s' % (channel, built, label)
    # Do not show decrypted token!
    log.info('Uploading: {0}'.format(upload_cmd))
    try:
        proc = check_call(
            upload_cmd.format(token=os.environ['ANACONDA_TOKEN']),
            shell=True)
        log.info(proc)
    except:
        log.info("Uploading failed; did you update the build version? The script will not force upload"+
            "so please manually upload if necessary.")