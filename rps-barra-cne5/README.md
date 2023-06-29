```
flask+grpc
线程共享
```



信用研究python
配置：
环境变量 FLASK_CONFIG=dev/prod/sit/test
默认test


参数

```
url: {url}/predict/mod/{id}
请求方法：get
参数格式json :
	{
    "interest_rate_indicator": "maturity_treasury_10",
    "start": "20230101",
    "end": "20230101",
    "rollback": 6,
    "indicators": ["ind1_code"]
 }
```

参数说明：

```
:param interest_rate_indicator: String， 利率指标代码: 1. 10年国债到期收益率 2. 10年国开到期收益率
:param start: String 区间开始时间: 20220101
:param end: String 区间结束时间: 20220131
:param rollback: integer 回滚时间: 默认36
:param indicators: list<String, string> 指标列表

java将json存入到Python状态表，通过ID去状态表取对应json数据计算, 都是必传参数
```

响应

成功

```
{
  "message": "success",
  "data": [],
  "code": "1"
}

```

失败

```
{
"message": "参数校验错误:\"请求参数异常'indexList'\"",
"data": [],
"code": "0"
}
```

启动

```
开发环境:
	python app.py
测试环境:
    构建docker:
    1. 构建项目镜像前，先到deploy下执行 build.sh 构建基础环境镜像, 
    2. 修改.flaskenv:FLASK_CONFIG=testing
    3. 最后切换到项目根目录执行./deploy/run.sh，构建项目镜像并运行. 需要修改端口, 在run.sh 29行 -p
sit环境:
1. 修改.flaskenv:FLASK_CONFIG=sit
2. 修改配置文件，修改数据库账号密码，先到application/common/utils/encrypt.py把账号密码加密，再修改./etc/sit.yaml内username/password ，把sit.yaml文件上传到/app/appdata/care_modle/etc/
生产环境prod:
1. 修改.flaskenv:FLASK_CONFIG=prod
2. 修改配置文件，先到application/common/utils/encrypt.py把账号密码加密，如果有乱码，在37行replace掉，再修改./etc/sit.yaml内username/password ,把prod.yaml文件上传到/app/appdata/care_modle/etc/

```

其他说明

```
1. deploy下是构建基础环境镜像的脚本，docker目录下是构建项目镜像的脚本
```
