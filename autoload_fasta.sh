#/bin/bash

function return_all_fasta() {
cd ./Fasta
ALL_FASTA=()
for file in *.fasta
do
ALL_FASTA+=($file)
done
cd ..
}

return_all_fasta
echo ${ALL_FASTA[*]}
