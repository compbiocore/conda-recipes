# conda-recipes

This is the conda recipe repository for the [Computational Biology Core (CBC)](http://brown.edu/cis/data-science/compbiocore/index.html) at Brown University. At the moment it is a work in progress. In the future all bioinformatics recipes/packages that we support for Brown users on URSA & Stronghold will be hosted on here.

# Build system

The build system for all the recipes is CentOS 7 with conda build 3 and GCC 8.2.0. A Docker image of our build system is on [Dockerhub](https://hub.docker.com/r/compbiocore/dockerfiles/) if needed.

# Build command

From within the recipe directory, build the package by tying:

```
conda build -c compbiocore . --perl 5.26.2
```

# Our CI workflow

To maintain package quality and compatibility we provide a `main` environment which is a set of up-to-date packages that we maintain and are commonly used by the Brown community for their daily workflows.

We have a continuous integration workflow which is managed with a centOS Docker image that replicates the CCV computing cluster system on Travis. All recipes must be modified and built on their own branches. For each recipe (or recipes) that is pushed, Travis spins up a Docker image and attempt to build the recipe. If the build fails, then the user is informed to go back and fix their recipe.

If the build passes, then Travis replicates the `main` conda environment in Docker with all packages and attempts to install the package. If the package successfully installs, then it will be uploaded to the `compbiocore` channel with the `main` label. If there are installation conflicts (such as between different versions of `samtools` dependencies), then the package will be uploaded to the `compbiocore` channel with the `conflict` label instead. Additionally, this README will be updated with the list of packages that have the `conflict` label.

Packages with the `conflict` label can still be installed, but will not be part of the default `main` environment we provide and support. Instead, the user will need to create their own separate `conda` environment and install the conflicting package there.

# Contributors

Fernando Gelin, August Guang, Andrew Leith, Ashok Ragavendran.

# To request a package or software // if something is broken

Please contact cbc-help@brown.edu to request software or if something is broken. This is not a guarantee that the software you are requesting will be installed. If we determine that the software does not follow good reproducibility and maintenance practices or is too outdated we reserve the right to refuse to install and support as our goal is to support reproducible research at Brown.

# Packages with the conflict label

