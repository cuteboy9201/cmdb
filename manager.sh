#!/bin/bash 
### 
# @Author: Youshumin
# @Date: 2019-11-15 12:01:01
 # @LastEditors: YouShumin
 # @LastEditTime: 2020-06-10 16:38:23
# @Description: 
###

workdir=$(cd $(dirname $0); pwd) 
export PYTHONPATH=$PYTHONPATH:${workdir} 
export RUN_ENV=test
pyenv="${workdir}/.env/bin/python"
echo $PYTHONPATH 
echo $pyenv
start_main(){
    cd $workdir
    ${pyenv} run_server.py
}

rbac_db_init(){
    cd ${workdir}/dblib
    ${pyenv} module.py create
}

rbac_db_del(){
    cd ${workdir}/dblib
    ${pyenv} module.py drop
}
case "$1" in 
    start)
        start_main
        ;;
    dbinit)
        rbac_db_init
        ;;
    dbdel)
        rbac_db_del
        ;;
    *)
        echo "start, dbinit"
        ;;
esac