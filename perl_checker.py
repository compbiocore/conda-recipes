#!/usr/bin/env python
import os
import glob
import yaml

# common issues with the perl recipes for our build system
# CentOS6, conda-build/2.1.10, python/2.7

# this script is written for python/3.6 however

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
	has_tests = meta['test'].get('imports')
	if has_imports:
		commands = []
		for i in has_imports:
			use = 'perl -e "use ' + i + '"'
			commands.append(use)
		meta['test']['commands'] = commands
		del meta['test']['imports']
		return 1
	else:
		return 0


# increments build number if anything has been modified
def build_number(meta):
	meta['build']['number']+=1

# checks for test_run.pl and removes
def test_run(root, files):
	if 'run_test.pl' in files:
		os.remove(os.path.join(root, 'run_test.pl'))

# run all checks
def checks(directory):
	perl_recipes = glob.glob(os.path.join(directory,'perl-*'))
#	perl_recipes = glob.glob(directory)
	for recipe in perl_recipes:
		print("checking " + recipe)
		for root, dirs, files in os.walk(recipe): # get meta.yaml from every level
			print(root)
			print(dirs)
			print(files)
			has_recipe = 'meta.yaml' in files
			if not dirs and has_recipe:
				with open(os.path.join(recipe,"meta.yaml")) as f:
					meta = yaml.load(f)
				print(meta)

				threaded = perl_threaded(meta)
				if meta.get('test'): # check if there's tests
					imported = imports(meta)
				else:
					imported = 0
				if threaded or imported: build_number(meta)
				with open(os.path.join(recipe,"meta.yaml"),"w") as f:
					yaml.add_representer(type(None), represent_none)
					yaml.dump(meta, f, default_flow_style=False)

				test_run(root, files)

# from https://stackoverflow.com/questions/37200150/can-i-dump-blank-instead-of-null-in-yaml-pyyaml
def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='go through perl recipes and modify to fit our build system')

    ds = ' [%(default)s]'
    parser.add_argument('-d', '--dir', help='directory with recipes')
    opts = parser.parse_args()

    directory = opts.dir
    checks(directory)