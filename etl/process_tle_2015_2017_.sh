#!/bin/bash
#!/bin/bash
SRC_DIR=$1
TGT_HDFS=$2
ZIP_FILE=$3
FILE=$4
LPF=$5
FILTER=$6

cd ${SRC_DIR}_tmp

echo ${FILE}
unzip -p ${SRC_DIR}/${ZIP_FILE} ${FILE} | python ${FILTER} | split --lines=$LPF - ${FILE}

