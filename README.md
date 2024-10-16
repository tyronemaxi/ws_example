# api_infra_base
基础 WEB 框架
## 说明
本项目是基础 WEB 框架，基于 python 语言开发，采用 flask && flask restful web 框架。

各位开发者请遵循以下规则：
1. restful api 风格
2. MVC 架构风格
3. 遵循 Python 代码风格，详见 PythonCookbook.md
4. 遵守项目目录结构
5. 遵守项目命名规范, 采用蛇形命名法，变量名请简洁&&见名知义
6. 遵守项目注释规范，请使用中文注释
待补充...
当前版本：v0.1.0

Python: 3.10.13

## 风格说明
见 PythonCookbook.md

架构风格为 MVC 架构


## 目录介绍
```
.
├── app                          # 项目入口
│         ├── client             # 其他服务客户端
│         ├── controller         # controller 曾
│         ├── core               # 底层核心模块
│             └── errors         # 异常处理
│             └── exception      # 项目标准 API Exception
│             └── flask_config   # flask 相关配置
│             └── http_code      # 项目标准 API 返回状态码
│             └── json_encoder   # json 转换配置
│             └── log            # 日志记录配置
│             └── middleware     # 中间件
│             └── request        # 请求处理模块
│             └── response       # 响应处理模块
│         ├── dao                # dao 层
│         ├── engine             # 数据库/缓存/队列/日志等
│         ├── extension          # 扩展
│         ├── model              # model 层
│         └── routes             # 路由层（view 层）
│             └── api            # api 接口
├── conf                         # 配置文件 
├── db                           # 数据库脚本文件和 schemal 文件，用于项目迭代升级留存
├── docker                       # 镜像构建文件
├── log                          # 日志
├── scripts                      # 项目脚本
├── tests                        # 单元测试
└── utils                        # 通用组件
```
## 配置项一览
### 基本配置
| 配置项                              | 描述                            | 默认值             |
|----------------------------------|-------------------------------|-----------------|
| `ENV`                            | 环境配置：dev, test, prod,         | `dev`           |
| `TZ`                             | 时区                            | `Asia/Shanghai` |
| `LOGGING_LEVEL`                  | 日志级别                          | `INFO`          |
| `SERVER_PORT`                    | 服务端口                          | `8080`          |
| `SQL_PRINT`                      | SQL 日志打印, 生产环境：False; 开发&&测试：True | True            |
| `GUNICORN_ERROR_LOG`                      | gunicorn 异常日志记录               | -               |
| `SECRET_KEY`                      | 服务生产密钥                        | -               |
| `GUNICORN_WORKER_NUM`                      | gunicorn worker 数量            | 2               |
| `DB_HOST`                      | 数据库 HOST                      | 127.0.0.1       |
| `DB_DATABASE`                      | 数据库 database                  | -               |
| `DB_PORT`                      | 数据库 PORT 端口                   | -               |
| `DB_USER`                      | 数据库用户                         | -               |
| `DB_PASSWORD`                      | 数据库 password                  | -               |
| `POOL_RECYCLE`                      | 数据库连接池回收策略                    | 300             |
| `POOL_SIZE`                      | 数据库连接池大小                      | -               |
| `MAX_OVERFLOW`                      | 数据库连接池 overflow               | 10              |
| `POOL_TIMEOUT`                      | 数据库连接池 timeout                | 30              |
| `REDIS_HOST`                      | redis host                    | -               |
| `REDIS_PORT`                      | redis port                    | -               |
| `REDIS_PASSWORD`                      | redis password                | -               |
| `REDIS_CACHE_DB`                      | redis db                      | -               |
| `MINIO_IP`                      | minio IP                      | -               |
| `MINIO_AK`                      | minio ak                      | -               |
| `MINIO_SK`                      | minio sk                      | -               |
| `DATA_DIR`                      | 项目数据目录                        | -               |
