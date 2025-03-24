import requests
import time
import json
import subprocess
from datetime import datetime

# 配置信息
ID = ''  # 一卡通号
PASSWORD = ''  # 密码
ipv4_adr = '' #电脑的ipv4地址


def get_client_ip():
    """获取本机IP地址"""
    try:
        response = requests.get('https://w.seu.edu.cn/drcom/chkstatus?callback=dr1003', verify=False)
        json_str = response.text[7:-1]  # 去除包裹的dr1003(...)
        data = json.loads(json_str)
        return data['v46ip']
    except Exception as e:
        log(f"获取IP失败: {str(e)}")
        return ipv4_adr


def login_seu(ip):
    """执行登录操作"""
    try:
        url = f'https://w.seu.edu.cn:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account=%2C0%2C{ID}&user_password={PASSWORD}&wlan_user_ip={ip}'
        response = requests.get(url, verify=False)
        log(f"登录结果: {response.text}")
        return "success" in response.text.lower()
    except Exception as e:
        log(f"登录异常: {str(e)}")
        return False


def check_internet():
    """检测网络连通性（适配Windows）"""
    try:
        result = subprocess.run(
            ['ping', '-n', '1', 'baidu.com'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False


def log(message):
    """日志记录"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('seu_auto_login.log', 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")


if __name__ == "__main__":
    log("自动登录服务启动")

    while True:
        if not check_internet():
            log("网络不可用，尝试登录...")
            client_ip = get_client_ip()
            if client_ip:
                if login_seu(client_ip):
                    log("登录成功")
                else:
                    log("登录失败")
            else:
                log("无法获取IP地址")
            time.sleep(10)
        else:
            log("网络正常")
            time.sleep(600)  # 40分钟检测一次

# 使用说明：
# 1. 安装依赖：pip install requests
# 2. 填写一卡通号和密码
# 3. 设置为开机启动或手动运行
# 4. 日志会保存在同目录的seu_auto_login.log文件中
