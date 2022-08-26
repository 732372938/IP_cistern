# 此文档仅仅用于学术交流，请勿用于商业用途
# 青龙使用代理池来避免黑IP问题
## TG群 https://t.me/InteIJ 
## 此文档默认为最新文档，同步脚本更新此文档
#### 本脚本可能有一些其他问题存在，出现问题请反馈，容器版本会尽快发布
## 运行脚本
### 容器安装
```shell
docker run -dit \
  -p 5001:5001 \
  --name http \
  --restart unless-stopped \
  xgzk/httpproxy:latest
```
挂载目录会报错，就没有挂载目录

### 之前拉取旧版本容器的卸载
```shell
docker kill http
docker rm -f http
docker rmi -f xgzk/httpproxy:2.1.0 #2.0.1是版本号,
```

### 接口
```shell
# 免费代理池接口
http://IP:端口/http
# 付费代理池接口，付费池无法提取会自动降级为免费池
http://IP:端口/nofreehttp
# 日志接口
http://IP:端口/log
# 暂停和恢复分配代理接口
http://IP:端口/
# 获取当前IP池所有IP的接口
http://IP:端口/getall
# 定时不使用代理(后面会修改)
http://IP:端口/ti
```
## 星空代理注册

[点我去注册账号](http://www.xkdaili.com/?ic=4deqad9q)
邀请码: `4deqad9q`
*开发过程中吞了我不少IP，让开发者回回血吧QAQ*
**生成单个IP且为TXT格式的api才能使用**

## 自己搭建教程
安装所需库
```pip3
pip3 install -r requirements.txt
```
测试脚本是否正常
```shell
python3 ip.py
```
先运行上面命令查看脚本是否有问题，没有问题运行下面命令进行，ip_broker.py只是检测脚本是否设置正确
运行脚本并添加守护进程

没有nodejs的使用这个
```shell
python3 kill.py # 开启守护进程
# 杀死守护进程
yum install lsof-y # 使用yum指令的
apt install lsof-y # 使用apt指令的
lsof -i:5001
kill -9 进程号 # 进程号就是一串数字
```
有nodejs的使用这个
```shell
pm2 start ip.yml --env productionpid # 开启守护进程
pm2 list # 查看脚本ID HTTPProxy就是
pm2 delete ID # 杀死守护进程
pm2 restart ID # 重启获取输入的ID pm2 restart 3
```

脚本自动添加守护进程，只需python3 kill.py即可，请勿再添加守护进程，使用python3 kill.py可以杀死原来全部ip_broker.py的所有守护进程，而后创建新的
运行后请查看ql.log日志是否有异常信息


##### 文件配置conn.yml

```text
第2行占用端口号
第4行日志文件路径
第6行数据库位置
```
**如果使用nodejs的pm2执行将ip.yml 并且修改PORT和conn.yml第二行端口一致**

## 接口配置
### [青龙代理视频演示和使用教程](https://www.youtube.com/playlist?list=PLH5cFwS6-yF-yDy-eGA3nVVa-2Nl43ZKk)
### 青龙面板添加依赖

依赖管理-->nodejs-->新建依赖
```text
global-agent
```
依赖管理-->python-->新建依赖
```text
requests
pysocks
ping3
proxynova-scraper
```

### 使用报错

如果运行提示图片 import ****** 报错 请安装 pip install ******，或者百度搜索 import ******,
根据需代码提示缺少依赖添加

<img src="./img/cw.jpg" alt="错误提示缺少依赖库">

### 查看是否添加成功
#### python3 检测代理是否添加成功
在青龙脚本管理-->新建脚本-->ip.py
把下内容进去，然后调试，脚本选择python,然后运行，如果显示代理IP表示添加成功

```python3
import requests
aas = requests.get("https://ip.tool.lu/")
print("检测到的IP", aas.text)
```

#### nodejs 检测代理是否添加成功
在青龙脚本管理-->新建脚本-->ip.js
```javascript
htt = process.env.GLOBAL_AGENT_HTTP_PROXY
    ? process.env.GLOBAL_AGENT_HTTP_PROXY
    : '';
// 判断activityUrl中是否有http://127.0.0.1 和长度大于16
if (null == htt.match('127\.0\.0\.1') && htt.length > 16) {
    const {bootstrap, globalTunnel} = require("global-agent");
    bootstrap();
}
const https = require("https");
https.get('https://ip.tool.lu/' , function (res) {
    console.log('statusCode:', res.statusCode);
    console.log('headers:', res.headers);
    res.on('data', function (d) {
        process.stdout.write(d);
    });
})
```
###  让接口对接青龙教程

配置文件中添加的
```shell
urls="http://ip:端口/http"
url=$(curl -m 30 $urls)
substr=${url%%p*}
if [ $substr = "htt" ]; then
    export GLOBAL_AGENT_HTTP_PROXY=$url
    export ALL_PROXY=$url
    echo $url
else
    echo "请求代理池接口失败"
    export GLOBAL_AGENT_HTTP_PROXY=http://青龙IP和端口
    export ALL_PROXY=http://青龙IP和端口
fi
```

js里面添加的内容
```javascript
htt = process.env.GLOBAL_AGENT_HTTP_PROXY
    ? process.env.GLOBAL_AGENT_HTTP_PROXY
    : '';
// 判断activityUrl中是否有http://127.0.0.1 和长度大于16
if (null == htt.match('127\.0\.0\.1') && htt.length > 16) {
    const {bootstrap, globalTunnel} = require("global-agent");
    bootstrap();
}
```
```text
所有js脚本都会调用jdCookie.js的内容获取青龙的CK
所以修改jdCookie.js的内容,这样就不用把所有的脚本都改了
既然修改这个脚本就不能把这个脚本拉下来
把jdCookie.js加入到黑名单中，拉取脚本确认jdCookie.js没有被拉下来，如果拉下来修改后也会被覆盖，因为这个问题头疼了一天
这里以脚本为例，重点观察^jd[^_] jdCookie
原本脚本 ql repo 库地址 "jd_|jx_|jdCookie" "activity|backUp" "^jd[^_]|USER|utils|function|sign|sendNotify|ql|JDJR"
修改后的 ql repo 库地址 "jd_|jx_" "jdCookie.js|activity|backUp" "USER|utils|function|sign|sendNotify|ql|JDJR"
在库那新建一个jdCookie.js去仓库把脚本内容并且把 **js里面添加的内容** 添加任意位置
每拉取一个库就修改一个使用代理的情况下，不修改会不走代理
然后就成了
```

#### 星空代理自动签到
拉库 ql repo  https://github.com/XgzK/JD_annex.git "qd_" "" "notify"
青龙配置文件填写 export xingkong ="账户1:密码&账户2:密码"
如果你青龙添加了消息通知，签到后将会收到通知

## 有想捐赠的可以捐赠下

<img src="./img/wx.jpg" alt="微信收款码" height="300px" width="300px">
<img src="./img/zfb.jpg" alt="支付宝收款码" height="300px" width="300px">

<details>
  <summary>不可用的代理池</summary>
  <pre><code> 
http://ip.yqie.com/ipproxy.htm 确认不可用
http://www.xsdaili.cn/ 没看到更新，放弃
http://www.taiyanghttp.com/free 放弃没有可用的
https://www.toolbaba.cn/ip 不可用
https://www.atomintersoft.com/high_anonymity_elite_proxy_list 不可用
https://ab57.ru/downloads/proxyold.txt 不可用
http://www.proxylists.net/http_highanon.txt 不可用
https://www.my-proxy.com/free-proxy-list-2.html 不可用
https://www.cnproxy.com/proxy1.html 不可用
https://www.89ip.cn/ 不可用
http://emailtry.com/index/1 不可用
https://pzzqz.com/ 不可用
http://nntime.com/ 不可用
https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1 不可用
https://openproxy.space/ 不可用
https://www.tyhttp.com/free/ 不可用
https://proxy11.com/ 不可用
http://www.nimadaili.com/ 服务器垃圾
http://www.ip3366.net/
  </code></pre>
</details>

<details>
  <summary>检测可用代理池</summary>
  <pre><code> 
https://premproxy.com/socks-list/
https://api.proxyscrape.com/?request=displayproxies&proxytype=all
https://www.proxyscan.io/
https://pzzqz.com/
http://proxylist.fatezero.org/  可用率高
https://proxy.mimvp.com/freesecret 抓起来麻烦，端口是图片
https://freeproxylists.net/zh/ 1/10
http://www.kxdaili.com/dailiip.html 1/5
http://pubproxy.com/api/proxy 不可用，偶尔可用
https://www.cool-proxy.net/ 九个出一个
https://proxy-list.org/english/index.php bs4加密，可能有反爬，国内不能直接访问，待测试可用时长
https://regex101.com/
https://ip.jiangxianli.com/ 13个出两个
https://www.freeproxylists.net/zh/ 1/20
https://www.proxy-list.download/HTTP 26出一个
http://www.cybersyndrome.net/pla6.html 1/20可用
https://spys.one/en/ 两个
https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt 1/1000
https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt 可用率高
https://github.com/mertguvencli/http-proxy-list
https://github.com/monosans/proxy-scraper-checker
https://ip.ihuan.me/ 一个可用
https://hidemy.name/en/proxy-list/ 一个可用
https://www.us-proxy.org/ 5个
https://proxy.seofangfa.com/ 可以使用就一个检测成功的
https://proxy.ip3366.net/
https://www.proxy-list.download/api/v1
https://www.juliangip.com/api?ref=proxy_pool
https://www.66ip.cn/ 1~2个可用
https://www.proxydb.net/ 3~6个可用
https://www.proxynova.com/ 3个可用
http://httpbin.org/ip 显示IP的
  </code></pre>
</details>
<details>
  <summary>版本更新</summary>
  <pre><code> 
1.0版本
    > 修复运行多个线程守护而对配置文件照成合并乱码删除的BUG
1.1版本
    > 添加日志输出，输出位置为当前目录下的ql_acting.log
    > ql_acting.log > 10M 会清空日志
1.2版本
    > 换肉不换皮，基本能封闭的都分离的
    > 添加了sqlite3数据库，支持节点筛选
    > 添加国外代理
    > 优化代理检测速度，由原来单线程变成同时检测多个代理，极大减少了未来多节点的检测时间
    > 第一次运行会提示异常，第二次就没有问题了
1.2.1版本
    > 修复了sqlite3数据库获取上次数据问题，无法获取本次代理问题
    > 增加了代理检测，在添加到配置文件的时候又进行了一次检测，但是会导致脚本运行时间延长
1.2.2版本
    > 添加定时任务取消代理
1.2.3版本
    > 添加支持多个容器代理
2.0版本
    > 修复了不能Js不走代理的问题
    > 耗费资源问题，由原来每次都爬取变成少于6次再爬取
    > 为了防止一些代理存活时间过长，四个小时后自动强制爬取一次
    > 添加了接口，由脚本执行调用一次切换一次代理
2.0.1版本
    > 使用了两个表，一个存储代理，一个存储检测结果
2.0.2版本
    > 增加了一些代理池
2.1.0版本
    > 增加了一些代理池
    > 检测服务器位置，根据位置决定是否执行部分代理爬取
    > 第一次会优先出随机国内代理，第二次按照代理池顺序出代理
2.2.0版本
    > 增加并修复了一些代理池
    > 现在启动程序不会卡住，get代理秒回应
    > 增加了线程池+双监听线程，获取iplist更快而且存活率也得到了保证
    > 国内IP大于4个才会返回国内代理，否则获取随机代理，主要预防很多人用一个IP导致黑IP和黑号
    > 添加日志显示
    > js改成http, 添加log日志接口
2.3.0版本
    > 增加并修复了一些代理池
    > 筛选池改为内存缓冲，数据库改为队列数据库
    > 响应速度更快
    > 支持付费代理池API
2.3.1版本
    > 优化代理池
2.3.2版本
    > 添加自动更新
    > 修复上版本添加星空代理需要重启容器BUG
    > 支持添加多个星空代理API
  </code></pre>
</details>


<details>
  <summary>问题</summary>
  <pre><code> 
代理添加上不能用
    > 青龙2.10版本支持代理版本未知，2.11支持，2.12支持，2.13支持
    > 不确定抓取代理池多了是否会被封IP
    > 代理池抓取的IP安全性方面无法保证，请自行选择是否使用
    > 如果因为抓取过多，而被网址封IP，可反馈，有解决方案，但是怕被某些人攻击服务器，只能当备用方案
其他问题
    > 所有反馈都会尽量解决，但是因个人技术问题，不能保证解决所有问题
    > 以后反馈问题会在晚上十点左右回复，白天有时回复，但是不保证
    > 此脚本可能存在其他问题，请自行测试，并且反馈问题
    > 本人只能保证本人仓库的代码的没有任何偷取信息行为，如果有信息泄露，一切与本人无关
    > 此脚本仅限用于学习交流，代码在使用过程中，出现任何不法行为，本人将不承担任何责任
  </code></pre>
</details>
