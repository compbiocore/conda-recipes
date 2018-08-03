echo "Running the build.sh Script"
echo "Adding perl scripts"
pwd
#cpanm -i Math::BaseCalc
mkdir -p $PREFIX/bin/
mkdir -p $PREFIX/jar/
mkdir -p $PREFIX/share/
mkdir -p $PREFIX/share/strelka
mkdir -p $PREFIX/scripts/
mkdir -p $PREFIX/data/
echo "Adding picard jar files"
cp $RECIPE_DIR/picard/* $PREFIX/jar/
echo "Adding polysolver data"
#cp -r $SRC_DIR/data/ $PREFIX/share/polysolver_data
cp -R $SRC_DIR/data/* $PREFIX/data
echo "Rebuilding novoalign index"
#novoindex $PREFIX/share/polysolver_data/abc_complete.nix $PREFIX/share/polysolver_data/abc_complete.fasta
novoindex $PREFIX/data/abc_complete.nix $PREFIX/data/abc_complete.fasta
echo "Put scripts into the polysolver build"
cp $SRC_DIR/scripts/* $PREFIX/scripts/

echo "Build strelka"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib
#echo "start building vcftools"
cd $RECIPE_DIR/include/ && \
  tar -xzf strelka-upstream-v1.0.11.tar.gz && \
  cd strelka-upstream-v1.0.11 && \
  ./configure --prefix=$PREFIX/share/strelka && \
  make
#  cd $SRC_DIR/include/strelka-upstream-v1.0.11/redist/vcftools-r837 && \
#  make
#echo "build main part"
#cp -r $SRC_DIR/include/strelka-upstream-v1.0.11/redist/vcftools-r837/bin $PREFIX/share/strelka/opt/vcftools/bin
#cp -r $SRC_DIR/include/strelka-upstream-v1.0.11/redist/vcftools-r837/lib $PREFIX/share/strelka/opt/vcftools/lib
#echo "Trying to finish the vcftools install"
#cd $PREFIX/share/strelka/opt/vcftools && make
#mydisp=$(ls -l $PREFIX/share/strelka/opt/vcftools)
#echo "${mydisp}"

echo "Set envs"

echo "export PSHOME=$PREFIX" > $PREFIX/config.sh
echo "export SAMTOOLS_DIR=$CONDA_PREFIX/bin" >> $PREFIX/config.sh
echo "export JAVA_DIR=$CONDA_PREFIX/bin" >> $PREFIX/config.sh
echo "export NOVOALIGN_DIR=$CONDA_PREFIX/bin" >> $PREFIX/config.sh
echo "export GATK_DIR=$CONDA_PREFIX/jar" >> $PREFIX/config.sh
echo "export MUTECT_DIR=$CONDA_PREFIX/share/mutect-1.1.6-1" >> $PREFIX/config.sh
echo "export STRELKA_DIR=$CONDA_PREFIX/share/strelka" >> $PREFIX/config.sh
echo "export NUM_THREADS=8" >> $PREFIX/config.sh
#echo "export DATA_DIR=$CONDA_PREFIX/share/polysolver_data" >> $PREFIX/config.sh
#echo "export TMP_DIR=/tmp" >> $PREFIX/config.sh
cat $PREFIX/config.sh

cat $PREFIX/config.sh > $PREFIX/bin/shell_annotate_hla_mutations
cat $PREFIX/config.sh > $PREFIX/bin/shell_call_hla_mutations_from_type
cat $PREFIX/config.sh > $PREFIX/bin/shell_call_hla_type

cat $PREFIX/bin/shell_call_hla_type

chmod 755 $PREFIX/bin/shell_annotate_hla_mutations
chmod 755 $PREFIX/bin/shell_call_hla_mutations_from_type
chmod 755 $PREFIX/bin/shell_call_hla_type
cat $SRC_DIR/scripts/shell_annotate_hla_mutations >> $PREFIX/bin/shell_annotate_hla_mutations
cat $SRC_DIR/scripts/shell_call_hla_mutations_from_type >> $PREFIX/bin/shell_call_hla_mutations_from_type
cat $SRC_DIR/scripts/shell_call_hla_type >> $PREFIX/bin/shell_call_hla_type
