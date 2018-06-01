#!/usr/bin/env python
import sys,os,  subprocess as sp

def real_dirname(path):
    	"""Return the symlink-resolved, canonicalized directory-portion of path."""
    	return os.path.dirname(os.path.realpath(path))

def main():
	args=' '.join(sys.argv[1:])
	jar_dir = real_dirname(sys.argv[0])
	if args.find("Xmx") > 0:
    		args=sys.argv[1] + " " + ' '.join(sys.argv[3:])
    		cmd = "java " + ' '.join(sys.argv[2:3], "-jar ",os.path.join(jar_dir,"picard.jar"), args)
	else:
    		cmd = "java -Xmx1000M  -jar " + os.path.join(jar_dir,"picard.jar") + " " + args
		print cmd
	sp.call(cmd, shell=True)

if __name__ == '__main__':
    main()
