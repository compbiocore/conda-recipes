# conda-recipes

This is the conda recipe repository for the [Computational Biology Core (CBC)](http://brown.edu/cis/data-science/compbiocore/index.html) at Brown University. At the moment it is a work in progress. In the future all bioinformatics recipes/packages that we support for Brown users on URSA & Stronghold will be hosted on here.

# Build system

The build system for all the recipes is CentOS 6 with conda build 3. A Docker image of our build system is on [Dockerhub](https://hub.docker.com/r/compbiocore/dockerfiles/) if needed.

# Our CI workflow

To maintain package quality and compatibility we keep a `main` conda environment which has recent versions of gcc, zlib and other vital software. For each recipe that is uploaded,

# Contributors

Fernando Gelin, August Guang, Andrew Leith, Ashok Ragavendran.

# To request a package or software // if something is broken

Please contact cbc-help@brown.edu to request software or if something is broken. This is not a guarantee that the software you are requesting will be installed. If we determine that the software does not follow good reproducibility and maintenance practices or is too outdated we reserve the right to refuse to install and support as our goal is to support reproducible research at Brown.