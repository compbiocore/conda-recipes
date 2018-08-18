#NOTES

After installing the package you need to make sure that the GMAPDB directory is created in the PREFIX of the conda environment the package is installed to. For example if your conda enviroment is located at `/gpfs/runtime/cbc_conda/cbc_conda_v1_root/envs/bioflows` you need to make sure to create the GMAPDB directory under that path. The GMAPDB is always created as `gmapdb_{{$PKG_VERSION}}`, so the final path should be something like `/gpfs/runtime/cbc_conda/cbc_conda_v1_root/envs/bioflows/gmap_{{$PKG_VERSION}}`
