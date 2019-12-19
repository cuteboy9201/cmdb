<!--
 * @Author: Youshumin
 * @Date: 2019-11-12 15:58:29
 * @LastEditors  : Please set LastEditors
 * @LastEditTime : 2019-12-19 15:18:43
 * @Description: 
 -->
## CMDB设计 
* 资产列表
    * 添加删除主机, 展示主机基本信息【后期添加主机监控】
    * 登陆主机按钮[webssh]
* 管理账号 
    * 获取主机基本信息一般使用管理账号认证,
* 用户账号
    * dev账号, 只读账号给开发人员登陆主机使用,没有sudu权限。
    * super账号, 用来运行开发应用账号...[非php应用的时候]
    * www账号 php应用应用账号,包含php,nginx 
    * 其他系统应用的时候 暂时也是使用super账号运行 具有sudo权限
    * 账号都由管理账号创建/修改,都有密码和密钥文件,并设置访问控制权限[指定IP],每90天更换一次

    用户表设计
    id user password sshKey updateTime cretaeTime desc
* 授权列表
    * 主要是授权给用户登陆 比如 主机 ---> 用户[角色(将角色当成用户组)] ---> 认证用户[dev/super]
    
    表设计
    id hostInfo userInfo roleInfo authInfo status createTime updateTime 

## 通信以及运行
* 和前端通信时候使用restful接口形式
* 应用之间使用rabbitmq进行通信[为了方便省事,应用都是使用tornado==5.1单线程模式运行]
* 大部分接口都会验证是否登陆以及异步验证是不是有接口访问权限
* 使用supervisor或者pm2管理,更加趋向于pm2管理(个人喜好)

## 代码说明
*  **代码严重依赖手动安装oslo https://github.com/cuteboy9201/oslo.git**
```
├── README.md        
├── app.py                          # 应用启动内容
├── configs                         # 配置相关
│   ├── __init__.py
│   ├── cfg.py                      #  生产配置文件 
│   ├── dev_cfg.py                  #  开发配置文件
│   └── setting.py                  #  根据当前环境选择倒入配置文件 run_env[环境变量]
├── dblib
│   ├── __init__.py                 
│   ├── crud.py                     #  操作数据库接口  
│   └── module.py                   #  数据库module
├── forms
│   ├── __init__.py
│   ├── adminuser.py                #  管理用户表单验证
│   └── property.py                 #  资产列表表单验证
├── handlers                        ## 接受web请求
│   ├── __init__.py
│   ├── adminuser.py                #  接受requeest请求 管理用户相关
│   ├── property.py                 #  资产列表相关
│   └── sysuser.py                  #  系统用户相关
├── manager.sh                      #  sh启动脚本 调用 run_server.py
├── requirements.txt                #  项目依赖包
├── run_server.py                   #  调用app.py 启动应用
└── utils
    ├── __init__.py
    ├── auth.py                     #  检测用户登陆/用户权限相关
    ├── mq.py                       #  rabbitmq 初始化以及发送数据和回复数据处理
    └── sshkey.py                   #  验证是不是合格密钥
```