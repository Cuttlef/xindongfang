import re
import asyncio
import aiohttp
from tqdm import tqdm
import requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '__jsluid_s=44c1afa389b836e423829a4cf6c53864; KUID=cysocs1686205650154; gr_user_id=186b5ef7-690b-46ea-ba9b-a68e0f3058e8; 9dee9d3e36a527e1_gr_last_sent_cs1=ec2285550d4f44a56e18112d3bbd179eaaad67cccc9954dc244d64b557ed2a340310f0d8b1e87f203549a22f9a489351; koolearn_netalliance_cookie=c0e7ac6d355d11eba6dfdcf401e66ca1#8ac8b344a7c248228ab19d6c8eb0a0eb; koolearn_netalliance_cookie_exp=1688797773; koolearn_netalliance_criteo=a6d8d8ec44f5484bab86151b7304a1b2#9e2c68b49b7142988f885e05b5e2a387; mp_ec424f4c03f8701f7226f5a009d90586_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A18899b29f831150-008c20fffab952-26031a51-144000-18899b29f831150%22%2C%22%24device_id%22%3A%20%2218899b29f831150-008c20fffab952-26031a51-144000-18899b29f831150%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; _ga_MYF8GNFSSR=GS1.1.1686216066.2.0.1686216066.0.0.0; JSESSIONID=E2B14822CF0020100066CAE07A2555E9; koo-shark-live-webapp=15b8144d9a173f8fe05968fe4b5178f9; log.session=a73d7db9f4a741df8756deffaba3b609; Hm_lvt_5023f5fc98cfb5712c364bb50b12e50e=1688082014; Hm_lpvt_5023f5fc98cfb5712c364bb50b12e50e=1688082014; _ga=GA1.2.1529090770.1686205798; _gid=GA1.2.520477409.1688082014; _ga_8RBHSP5JM6=GS1.2.1688082014.1.0.1688082014.60.0.0; Qs_lvt_143225=1686205651%2C1688082014; Qs_pv_143225=3536466425530541600%2C2354307777715217400; sso-message-image-code=ae15d8ad137944469e56cfd3fba5f4bf; sso.ssoId=ec2285550d4f44a56e18112d3bbd179eaaad67cccc9954dc244d64b557ed2a340310f0d8b1e87f203549a22f9a489351; ssoSessionID=781F0CC9C9A10128B3A328F25ACB1222-n1; login_token=login_token_v2_781F0CC9C9A10128B3A328F25ACB1222-n1; koo.line=study; Hm_lvt_e89735d560e89742be5242cc4268949e=1688082041; sharks-webapp-study-common-nginx=fc745d3bb5866287dd116985f3fbfc0b; prelogid=02b5dc9a3a7f1bc2019a644eada815e0; Hm_lpvt_e89735d560e89742be5242cc4268949e=1688082082; 9dee9d3e36a527e1_gr_cs1=ec2285550d4f44a56e18112d3bbd179eaaad67cccc9954dc244d64b557ed2a340310f0d8b1e87f203549a22f9a489351',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}

newList = []
getMpUrl = []


def index(baseUrl):
    baseResponse = requests.get(url=baseUrl, headers=headers)
    baseJson = baseResponse.json()
    lives = baseJson['data']['lives']
    for i in range(len(lives)):
        newJson = {}
        # liveTeachers = lives[i]['liveTeachers']
        newJson['liveName'] = lives[i]['liveName']
        newJson['liveUrl'] = lives[i]['liveUrl']
        newList.append(newJson)


def getVideoUrl(url):
    vidoeResponse = requests.get(url, headers=headers)
    return vidoeResponse.url


def realVidoeUrl(url):
    # 使用正则表达式提取mainId和token
    main_id = re.search(r'mainId=([^&]+)', url).group(1)
    token = re.search(r'token=([^&]+)', url).group(1)
    realUrl = f'https://api.roombox.xdf.cn/api/schedule/get-classroom?classroomId={main_id}&token={token}'
    realVidoe = requests.get(realUrl)
    realJson = realVidoe.json()
    return realJson['data']['playback']['urls'][0]


async def download_mp4(url, save_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            print('---正在开始下载-' + newList[i]['liveName'] + '.mp4' + '    url:' + url)
            total_size = int(response.headers.get('content-length', 0))
            with open(save_path, 'wb') as file:
                progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
                while True:
                    chunk = await response.content.read(8192)
                    if not chunk:
                        break
                    file.write(chunk)
                    progress_bar.update(len(chunk))
                progress_bar.close()


if __name__ == '__main__':
    # 输入要抓取的页码
    num = 3
    # 主页面找到各个视频地址
    baseUrl = f'https://study.koolearn.com/live/search-live?isWap=true&moduleId=2&pageno={num}'
    # 保存路径
    path = 'E:\\xindongfang1\\'
    if not os.path.exists(path):
        os.mkdir(path)
    index(baseUrl)
    for i in newList:
        getMpUrl.append(realVidoeUrl(getVideoUrl(i['liveUrl'])))

    for i in range(len(getMpUrl)):
        save_path = path + newList[i]['liveName'] + '.mp4'
        url = getMpUrl[i]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_mp4(url, save_path))
