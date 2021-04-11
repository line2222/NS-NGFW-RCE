# 网康NS-NGFW防火墙远程漏洞批量检测
网康NS-NGFW防火墙远程漏洞（本脚本只做检测使用，仅作为防守方自查使用）利用fofa搜索还是有很多漏洞的。

## 使用
新建url.txt，直接将待检测的url地址（fofa爬一下）放在url.txt，运行
```
python3 poc.py
```
即可，结果将保存在loophole.txt中
