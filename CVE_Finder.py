"""
Author:adminsec
Date:2021-10-15
Description:用于获取”http://cve.scap.org.cn/vulns/1“最新的漏洞信息
"""
import requests
import smtplib
import datetime
from email.mime.text import MIMEText
from lxml import etree
import os

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61'
}


def send_email():
    with open(get_date() + "-targets.txt", "r", encoding="utf-8") as f:
        data = f.read()
    # 第三方 SMTP 服务
    mail_host = "smtp.163.com"  # SMTP服务器
    mail_user = "xxxxxxxxx@163.com"  # 用户名
    mail_pass = "xxxxxxxxx"  # 授权密码，非登录密码

    sender = 'xxxxxxxxx@163.com'  # 发件人邮箱(最好写全, 不然会失败)
    receivers = ['xxxxxxxxx@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    title = '最新漏洞情报更新'  # 邮件主题

    message = MIMEText(data, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("邮件发送成功！")
    except smtplib.SMTPException:
        print("出错啦!邮件发送失败!")


def get_info():
    date = get_date()
    with open(get_date() + "-targets.txt", "w", encoding="utf-8") as f:
        for i in range(1, 11):
            url = "http://cve.scap.org.cn/vulns/" + str(i)
            response = requests.get(url=url, headers=header).text
            tree = etree.HTML(response)
            tr_list = tree.xpath('//tbody[@class="whiteB"]/tr')
            for tr in tr_list:
                target_cve_date = tr.xpath('./td[2]/text()')[0]
                if target_cve_date == date:
                    target_cve_num = (tr.xpath('./td/a/text()')[0])[29:43]
                    target_cve_des = tr.xpath('./td[4]/text()')[0]
                    vul = "CVE-ID:" + target_cve_num + "  Description:" + target_cve_des + "\n"
                    f.write(vul)
            if target_cve_date != date:
                break


def get_date():
    get_year = datetime.datetime.now().year
    get_month = datetime.datetime.now().month
    get_day = datetime.datetime.now().day
    batch = str(get_year) + "-" + str(get_month) + "-" + str(get_day)
    return batch


def run():
    get_info()
    if not os.path.exists(get_date() + "-targets.txt"):
        exit()
    elif os.path.getsize(get_date() + "-targets.txt") == 0:
        os.remove(get_date() + "-targets.txt")
        exit()
    else:
        send_email()


if __name__ == '__main__':
    run()
