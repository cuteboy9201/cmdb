#!/bin/bash 
### 
# @Author: Youshumin
# @Date: 2019-11-15 12:01:01
 # @LastEditors: Youshumin
 # @LastEditTime: 2019-11-22 17:28:23
# @Description: 
###

workdir=$(cd $(dirname $0); pwd) 
export PYTHONPATH=$PYTHONPATH:${workdir} 

pyenv="/Users/youshumin/Desktop/cuteboy9201/cmdb/.env/bin/python3.7"

start_main(){
    cd $workdir
    ${pyenv} run_server.py
}

rbac_db_init(){
    cd ${workdir}/dblib
    ${pyenv} module.py create
    # ${pyenv} init_data.py
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