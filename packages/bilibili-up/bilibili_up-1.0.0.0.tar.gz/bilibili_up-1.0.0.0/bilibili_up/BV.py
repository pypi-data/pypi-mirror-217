import requests

# 报错信息
class 查询失败(Exception):
    pass

# 获取BV视频信息
def BV_get_File(bv, headers=None, ip=None):
    # 构建API链接
    api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv}"

    try:
        response = requests.get(api_url, headers=headers, proxies={'http': ip, 'https': ip} if ip else None)
        data = response.json()

        if data['code'] == 0:
            video_data = data['data']

            play_count = video_data['stat']['view']  # 播放量
            publish_time = video_data['pubdate']  # 发布时间
            author_name = video_data['owner']['name']  # 作者
            author_uid = video_data['owner']['mid']  # 作者UID
            danmaku_count = video_data['stat']['danmaku']  # 弹幕数量

            return {
                "播放量": play_count,
                "发布时间": publish_time,
                "作者": {
                    "名称": author_name,
                    "UID": author_uid
                },
                "弹幕数量": danmaku_count,
                "bvid": video_data['bvid'],  # 视频BV号
                "援助": video_data['aid'],  # 视频援助号
                "视频tid": video_data['tid'],  # 视频tid
                "tname": video_data['tname'],  # 视频分类名
                "版权": video_data['rights'],  # 版权信息
                "封面图片": video_data['pic'],  # 封面图片链接
                "title": video_data['title']  # 视频标题
            }
        else:
            raise 查询失败("出现错误，请检查连接网络或请求头。")
            pass
    except Exception as e:
        raise 查询失败("出现错误，请检查连接网络或请求头。")
        pass

# 获取BV视频评论区（字典）
def BV_get_comments(BV, PageNumber, headers=None, ip=None):
    try:
        url = f'https://api.bilibili.com/x/v2/reply/main?pn=1&type=1&oid={BV}&sort=0'
        comments_dict = {}
        PageNumber = int(PageNumber)
        PageNumber += 1
        for page in range(1, PageNumber):  # 获取前五页评论
            params = {'pn': page}
            response = requests.get(url, headers=headers, proxies={'http': ip, 'https': ip} if ip else None,
                                    params=params)
            data = response.json()

            for comment_info in data['data']['replies']:
                username = comment_info['member']['uname']
                content = comment_info['content']['message']
                comments_dict[username] = content
        return comments_dict
    except Exception as e:
        raise 查询失败("出现错误，请检查连接网络、请求头或BV号。")
