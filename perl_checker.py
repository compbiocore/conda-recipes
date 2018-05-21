#!/usr/bin/env python
from tempfile import mkstemp
from shutil import move
import os
import glob
import yaml
from jinja2 import Environment, FileSystemLoader

# common issues with the perl recipes for our build system
# CentOS6, conda-build/2.1.10, python/2.7

# this script is written for python/3.6 however
# Usage: python perl_checker.py -d $CONDA-RECIPES

# checks for perl-threaded and modifies to just perl
# if finds, returns 1
def perl_threaded(meta):
	flag = 0

	build_reqs = meta['requirements']['build']
	if 'perl-threaded' in build_reqs:
		build_reqs.remove('perl-threaded')
		build_reqs.append('perl')
		meta['requirements']['build'] = build_reqs
		flag = 1

	run_reqs = meta['requirements']['run']
	if 'perl-threaded' in run_reqs:
		run_reqs.remove('perl-threaded')
		run_reqs.append('perl')
		meta['requirements']['run'] = run_reqs
		flag = 1

	return flag

# checks for imports and modifies to commands
def imports(meta):
	has_imports = meta['test'].get('imports')
	if has_imports:
		commands = []
		for i in has_imports:
			if 'use' in i: # check if use statements are already there
				break
				commands.append(i)
			use = 'perl -e "use ' + i + '"'
			commands.append(use)
		meta['test']['commands'] = commands
		del meta['test']['imports']
		return 1
	else:
		return 0

# increments build number if anything has been modified
def build_number(meta,v):
	b = meta.get('build')
	if b:
		n = b.get('number')
		if n:
			meta['build']['number']+=1
			if v:
				print("build number is now " + str(meta['build']['number']))
		elif v:
			print("no build number...")
	elif v:
		print("no build key...")

# checks for test_run.pl and removes
def test_run(root, files, v):
	if 'run_test.pl' in files:
		os.remove(os.path.join(root, 'run_test.pl'))
		if v:
			print("found run_test.pl and removed")

# checks build.sh for ./Build and changes to perl ./Build
def check_build(build_file, v):
	flag = 0
	fh, abs_path = mkstemp()
	with os.fdopen(fh, 'w') as new_build:
		with open(build_file) as old_build:
			for line in old_build:
				if line.lstrip().startswith('./Build'):
					new_build.write(line.replace('./Build', 'perl ./Build'))
					flag = 1
				else:
					new_build.write(line)
	os.remove(build_file)
	move(abs_path, build_file)
	if v and flag == 1:
		print("found ./Build instead of perl ./Build and modified")


# run all checks
def checks(directory, v):
#	perl_recipes = glob.glob(os.path.join(directory,'perl-*'))
#for testing in recipe directory:
	perl_recipes = glob.glob(directory)
	for recipe in perl_recipes:
		if opts.verbose: print("------checking " + recipe + "------")
		for root, dirs, files in os.walk(recipe): # get meta.yaml from every level
			has_recipe = 'meta.yaml' in files
			if has_recipe:
				with open(os.path.join(root,"meta.yaml")) as f:
					# for Jinja
					env = Environment(loader=FileSystemLoader(root))
					template = env.get_template('meta.yaml')
					meta = yaml.load(template.render())

				if v:
					print("### version/" + str(meta["package"]["version"]) + " ###")

				threaded = perl_threaded(meta)
				if v and threaded:
					print("found perl-threaded")

				if meta.get('test'): # check if there's tests
					imported = imports(meta)
				else:
					imported = 0
				if v and imported:
					print("found import statements")

				if threaded or imported: build_number(meta, v)
				with open(os.path.join(root,"meta.yaml"),"w") as f:
					yaml.add_representer(type(None), represent_none)
					yaml.dump(meta, f, default_flow_style=False)

				test_run(root, files, v)
				check_build(os.path.join(root,"build.sh"),v)

				if v:
					print("") # for a new line

# from https://stackoverflow.com/questions/37200150/can-i-dump-blank-instead-of-null-in-yaml-pyyaml
def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='go through perl recipes and modify to fit our build system')

    ds = ' [%(default)s]'
    parser.add_argument('-d', '--dir', help='directory with recipes')
    parser.add_argument('-v', '--verbose', help='verbose')
    opts = parser.parse_args()

    directory = opts.dir
    if opts.verbose:
    	checks(directory, 1)
    else:
    	checks(directory, 0)