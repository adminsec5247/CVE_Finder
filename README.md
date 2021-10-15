# CVE_Finder
基于python3开发的一款CVE监控工具，需要开启网易邮箱SMTP服务获得授权码(方法请自行百度)，需要安装lxml模块
# 使用方法
1.源代码中配置好SMTP服务相关参数
mail_user = "xxxxxxxxx@163.com"   # 用户名
mail_pass = "xxxxxxxxx"           # 授权密码，非登录密码
sender = 'xxxxxxxxx@163.com'      # 发件人邮箱(最好写全, 不然会失败)
receivers = ['xxxxxxxxx@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

2.安装lxml
pip3 install lxml

3.运行
python3 CVE_Finder.py

# Linux添加自动任务
1.打开crontab文件
vim /etc/crontab

2.添加每天23点自动执行脚本
0 3 * * * root python3 CVE_Finder.py # 注意前面可能需要添加任务编号
