#!/usr/bin/bash

scp -r  kddev@192.168.5.102:/data2/model/sign-retina-mask/$1 /tmp/
echo $?;
#if [ $? == 0 ];then
#echo "step 1 success"
#else
#echo "step 1 failed"
#fi
#ansible 10.11.5.121 -m copy -a 'src=/tmp/$1 dest=/data2/model/lane-resnet/ owner=hadoop group=hadoop' -b -K -f 20
ansible-playbook model-release.yaml -e dir=$1
echo $?;
