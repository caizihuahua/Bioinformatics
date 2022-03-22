import requests
import urllib3
import random

urllib3.disable_warnings()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}


def download(url: str):
    print('正在下载', url)
    try:
        res = requests.get(url, headers=headers, timeout=60, verify=False)
        res.raise_for_status()
        print('下载成功')
        return res
    except Exception as e:
        print('下载出现异常:\n' + str(e))
        return None


def main():
    try:
        with open('data.txt', 'r') as f:
            res = f.readlines()
    except:
        res = download(
            'https://ftp.wwpdb.org/pub/pdb/derived_data/pdb_entry_type.txt')
        if res is None:
            return
        res = res.text.strip().split('\n')
        res = [x + '\n' for x in res if x.find('nuc') == -1]
        with open('data.txt', 'w') as f:
            f.writelines(res)

    res = random.sample(res, 10)
    print('随机抽取的 10 行为:\n' + ''.join(res))


if __name__ == '__main__':
    main()
