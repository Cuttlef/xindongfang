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
    'Cookie': '请填写Cookie',
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
