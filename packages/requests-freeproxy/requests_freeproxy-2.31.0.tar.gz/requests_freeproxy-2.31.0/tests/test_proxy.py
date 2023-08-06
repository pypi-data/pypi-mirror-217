# import requests

import requests_freeproxy as requests

def uc_unicom(ip):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36 Edg/111.0.1661.41'
        }
        proxies = {
            'http': f'http://{ip}',
            'https': f'http://{ip}',
            'headers': {
                'Proxy-Authorization': 'Basic dXNlcjpwd2Q='
            }
        }
        response = requests.get('https://api.ip.sb/ip', headers=headers, proxies=proxies)
        print(response.text)
    except Exception as e:
        print(e)

def baidu_telecom(ip):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36 Edg/111.0.1661.41'
        }
        proxies = {
            'http': f'http://{ip}',
            'https': f'http://{ip}',
            'headers': {
                'Host': '153.3.236.22:443',
                'X-T5-Auth': '683556433',
                'User-Agent': 'baiduboxapp'
            }
        }
        # session = requests.session()
        # print(session.get('https://api.ip.sb/ip', headers=headers, proxies=proxies).text)
        # print(session.get('https://api.ip.sb/ip', headers=headers, proxies=proxies).text)
        # print(session.get('https://searchplugin.csdn.net/api/v1/ip/get', headers=headers, proxies=proxies).text)
        # print(session.get('https://api.ip.sb/ip', headers=headers, proxies=proxies).text)
        # response = session.get('https://searchplugin.csdn.net/api/v1/ip/get', headers=headers, proxies=proxies)
        response = requests.get('https://api.ip.sb/ip', headers=headers, proxies=proxies)
        # response = requests.get('https://searchplugin.csdn.net/api/v1/ip/get', headers=headers, proxies=proxies)
        # print(response.status_code)
        print(response.text)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    # uc_unicom('127.0.0.1:8080')
    baidu_telecom('14.215.179.244:443')
