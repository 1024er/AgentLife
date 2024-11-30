import json
import time
import requests
import traceback
from datetime import datetime


class WeiBoTools(object):

    """
    微博发布/回复评论。

    COOKIE 获取 URL: https://weibo.com/u/7962675853
    """
    
    UID = "7962675853"
    XSRF_TOKEN = "K_hAvDA9bPtWbEhrCXZ3yH7D"
    COOKIE = "_s_tentry=github.com; Apache=5752462256458.981.1731302427534; SINAGLOBAL=5752462256458.981.1731302427534; ULV=1731302427539:1:1:1:5752462256458.981.1731302427534:; XSRF-TOKEN=K_hAvDA9bPtWbEhrCXZ3yH7D; SCF=AkIy3krxjuV1jM0aki7llTK9rhTkc-1Egh-YGXscdqsSwLSQorILhL7WruvGI6FWRYcZ3KZHezbN7Nk_XOMHP9I.; UOR=github.com,s.weibo.com,www.google.com.hk; ALF=1735033008; SUB=_2A25KRoPgDeRhGeFH7VAX9yvEzj-IHXVpPZkorDV8PUJbkNANLXL2kW1NetPJwRqAn1neBiTJAAIcEu2mwIyjXFZW; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWHX4OQI281zo7SQL1_Plja5JpX5KMhUgL.FoM4SozcS0-RSKe2dJLoIf2LxK-LB.-L1K5LxKMLBKeL122LxK-L12qLB-2LxKqL1KnLB-qLxKqL1hnL1K2LxKML1-2L1hBLxKnLBKML1KzLxKnL1h.LBozLxK-L1K5L12Bt; WBPSESS=3QQs2tO418lrfhdFTxw_8XCUeQFFHkhyR_ttTAi3ZmEg5FddUwtnmdT67dqmWTTGNZc-iomBMbs1QlwSMpL3h2MoeJjh_hDg-aigAvvb8ZhSVdN3pihUCa2GM6HNa9COxAVNaav3a_BfILl2Y9Vl_Q=="
    
    LAST_POST_TIME = None                           # 上次发布微博的时间，用于控制发布频率
    ALREADY_REPLY_COMMENTS = []                     # 已经回复过的评论，避免重复回复

    @staticmethod
    def post_weibo(
        content: str
    ):
        """
        发布一条微博消息。

        Args:
            content (_type_): 发布的内容。
            
        Returns:
            {
                "data": {
                    "visible": {
                        "type": 0,
                        "list_id": 0
                    },
                    "created_at": "Sun Nov 17 15: 26: 58 +0800 2024",
                    "id": 5101720511972954,
                    "idstr": "5101720511972954",
                    "mid": "5101720511972954",
                    "mblogid": "P0IL18hfQ",
                    "user": {
                        "id": 7962675853,
                        "idstr": "7962675853",
                        "pc_new": 0,
                        "screen_name": "徐磊只是我的角色名",
                        "profile_image_url": "https: //tvax1.sinaimg.cn/crop.0.0.590.590.50/008GSzJHly8hvoij810juj30ge0gemxo.jpg?KID=imgbed,tva&Expires=1731839218&ssig=zX9FZaGmAG",
                        "profile_url": "/u/7962675853",
                        "verified": False,
                        "verified_type": -1,
                        "domain": "",
                        "weihao": "",
                        "status_total_counter": {
                            "total_cnt_format": 2,
                            "comment_cnt": "2",
                            "repost_cnt": "0",
                            "like_cnt": "0",
                            "total_cnt": "2"
                        },
                        "avatar_large": "https://tvax1.sinaimg.cn/crop.0.0.590.590.180/008GSzJHly8hvoij810juj30ge0gemxo.jpg?KID=imgbed,tva&Expires=1731839218&ssig=uVtf6M%2Fntr",
                        "avatar_hd": "https://tvax1.sinaimg.cn/crop.0.0.590.590.1024/008GSzJHly8hvoij810juj30ge0gemxo.jpg?KID=imgbed,tva&Expires=1731839218&ssig=e1B78%2BO2HZ",
                        "follow_me": False,
                        "following": False,
                        "mbrank": 0,
                        "mbtype": 0,
                        "v_plus": None,
                        "planet_video": True,
                        "icon_list": []
                    },
                    "can_edit": False,
                    "textLength": 22,
                    "annotations": [
                        {
                            "shooting": 1
                        },
                        {
                            "source_text": "",
                            "phone_id": ""
                        },
                        {
                            "mapi_request": True
                        }
                    ],
                    "source": "微博网页版",
                    "favorited": False,
                    "reads_count": 1,
                    "pic_ids": [],
                    "pic_num": 0,
                    "is_paid": False,
                    "mblog_vip_type": 0,
                    "reposts_count": 0,
                    "comments_count": 0,
                    "attitudes_count": 0,
                    "attitudes_status": 0,
                    "isLongText": False,
                    "mlevel": 0,
                    "content_auth": 0,
                    "is_show_bulletin": 2,
                    "comment_manage_info": {
                        "comment_manage_button": 1,
                        "comment_permission_type": 0,
                        "approval_comment_type": 0,
                        "comment_sort_type": 0,
                        "ai_play_picture_type": 0
                    },
                    "share_repost_type": 0,
                    "title": {
                        "text": "公开",
                        "base_color": 1,
                        "icon_url": "http://h5.sinaimg.cn/upload/2015/07/14/34/timeline_title_public.png"
                    },
                    "mblogtype": 0,
                    "showFeedRepost": False,
                    "showFeedComment": False,
                    "pictureViewerSign": False,
                    "showPictureViewer": False,
                    "rcList": [],
                    "analysis_extra": "",
                    "readtimetype": "mblog",
                    "mixed_count": 0,
                    "is_show_mixed": False,
                    "isSinglePayAudio": False,
                    "text": "那银翼的魔术师好看不？ ​​​",
                    "text_raw": "那银翼的魔术师好看不？ ​​​",
                    "customIcons": []
                },
                "msg": "发布成功",
                "ok": 1
            }
        """
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': WeiBoTools.COOKIE,
            'Mweibo-Pwa': '1',
            'Origin': 'https://m.weibo.cn',
            'Priority': 'u=1, i',
            'Referer': 'https://m.weibo.cn/compose/',
            'Sec-CH-UA': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'Sec-CH-UA-Mobile': '?0',
            'Sec-CH-UA-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'X-XSRF-TOKEN': WeiBoTools.XSRF_TOKEN
        }
        
        data = {
            'content': content,
            'visible': 0,
            'share_id': '',
            'vote': '',
            'media': ''
        }

        try:
            response = requests.post(
                'https://weibo.com/ajax/statuses/update', 
                headers=headers, 
                data=data
            ).json()
            
            # print(response)
            
            sucess = response.get('ok', False)
            if sucess:
                WeiBoTools.LAST_POST_TIME = time.time()
                    
            return f"https://m.weibo.cn{response['data']['user']['profile_url']}?"
        except:
            print(traceback.format_exc())
            return ''
    
    @staticmethod
    def get_all_comments(
        weibo_id: int
    ):
        """
        获得一条微博下面的所有评论。

        Args:
            weibo_id (int): _description_
            
        Returns:
            list: 评论列表, 每一条评论的格式为 {
                "created_at": "Sat Nov 16 22: 38: 31 +0800 2024",
                "id": 5101466727221344,
                "rootid": 5101466727221344,
                "rootidstr": "5101466727221344",
                "floor_number": 1,
                "text": "微博：你的快乐，我来承包~",
                "disable_reply": 0,
                "restrictOperate": 0,
                "source_allowclick": 0,
                "source_type": 4,
                "source": "来自罗伯特",
                "user": {
                    "id": 5762999670,
                    "idstr": "5762999670",
                    "pc_new": 0,
                    "screen_name": "评论罗伯特",
                    "profile_image_url": "https: //tvax3.sinaimg.cn/crop.0.0.512.512.50/006i0XtAly8htt0v6r8pjj30e80e874t.jpg?KID=imgbed,tva&Expires=1731779801&ssig=%2BQWkFvIcLa",
                    "profile_url": "/u/5762999670",
                    "verified": True,
                    "verified_type": 0,
                    "domain": "",
                    "weihao": "",
                    "verified_type_ext": 2,
                    "status_total_counter": {
                        "total_cnt_format": "102.1万",
                        "comment_cnt": "280,199",
                        "repost_cnt": "43,945",
                        "like_cnt": "697,181",
                        "total_cnt": "1,021,325"
                    },
                    "avatar_large": "https://tvax3.sinaimg.cn/crop.0.0.512.512.180/006i0XtAly8htt0v6r8pjj30e80e874t.jpg?KID=imgbed,tva&Expires=1731779801&ssig=pR79Lk1ayr",
                    "avatar_hd": "https://tvax3.sinaimg.cn/crop.0.0.512.512.1024/006i0XtAly8htt0v6r8pjj30e80e874t.jpg?KID=imgbed,tva&Expires=1731779801&ssig=wQCs1i0kgK",
                    "follow_me": False,
                    "following": False,
                    "mbrank": 1,
                    "mbtype": 12,
                    "v_plus": 0,
                    "fansIcon": {
                        "fans_uid": 5762999670,
                        "val": 0,
                        "member_rank": 1,
                        "svip": 1,
                        "vvip": 1,
                        "lighting": False,
                        "icon_url": "",
                        "uid": 5762999670,
                        "name": ""
                    },
                    "planet_video": True,
                    "verified_reason": "互联网科技博主",
                    "description": "微博官方认证机器人",
                    "location": "海外",
                    "gender": "f",
                    "followers_count": 1395637,
                    "followers_count_str": "139.6万",
                    "friends_count": 18,
                    "statuses_count": 83,
                    "url": "",
                    "svip": 1,
                    "vvip": 1,
                    "cover_image_phone": "https://ww2.sinaimg.cn/crop.0.0.640.640.640/a1d3feabjw1ecasunmkncj20hs0hsq4j.jpg",
                    "icon_list": [
                        {
                            "type": "vip",
                            "data": {
                                "mbrank": 1,
                                "mbtype": 12,
                                "svip": 1,
                                "vvip": 1
                            }
                        }
                    ]
                },
                "mid": "5101466727221344",
                "idstr": "5101466727221344",
                "url_objects": [],
                "liked": False,
                "readtimetype": "comment",
                "analysis_extra": "author_uid:7962675853|mid:5101466549487239|ai_type:2",
                "mark_type": 1,
                "match_ai_play_picture": False,
                "rid": "0_0_0_162526931220760413_0_0_0",
                "allow_follow": False,
                "item_category": "comment",
                "degrade_type": "normal",
                "report_scheme": "sinaweibo://mpdialog?scheme=sinaweibo%3A%2F%2Fwbox%3Fid%3Dt8wto09182%26page%3Dpages%2Fcomplaint%2Fcomplaint%26comment%3D%25E5%25BE%25AE%25E5%258D%259A%25EF%25BC%259A%25E4%25BD%25A0%25E7%259A%2584%25E5%25BF%25AB%25E4%25B9%2590%25EF%25BC%258C%25E6%2588%2591%25E6%259D%25A5%25E6%2589%25BF%25E5%258C%2585%7E%26nickname%3D%25E8%25AF%2584%25E8%25AE%25BA%25E7%25BD%2597%25E4%25BC%25AF%25E7%2589%25B9%26ct_type%3D2%26rid%3D5101466727221344%26ct_time%3D1731769001696%26ct_sign%3D4124257832%26luicode%3D",
                "comments": [],
                "max_id": 0,
                "total_number": 0,
                "isLikedByMblogAuthor": False,
                "hot_icon": {
                    "url": "https://h5.sinaimg.cn/upload/100/1640/2022/08/31/detail_comments_icon_firstcomment.png",
                    "wh_ratio": "1.44"
                },
                "like_counts": 0,
                "text_raw": "微博：你的快乐，我来承包~"
            }
        """
        url = 'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={weiboID}&is_show_bulletin=2&is_mix=0&count=20&type=feed&uid={uid}&fetch_level=0&locale=zh-CN'.format(
            weiboID=weibo_id, 
            uid=WeiBoTools.UID
        )
        
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'client-version': 'v2.46.33',
            'cookie': WeiBoTools.COOKIE,
            'priority': 'u=1, i',
            'referer': 'https://weibo.com/u/7962675853',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'server-version': 'v2024.11.15.2',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-xsrf-token': WeiBoTools.XSRF_TOKEN
        }

        try:        
            response = requests.get(
                url, 
                headers=headers
            )
            return [
                res for res in response.json()['data']
                if res['rootidstr'] not in WeiBoTools.ALREADY_REPLY_COMMENTS
            ]
        except:
            print(response.text)
            return []
    
    @staticmethod
    def reply_comment(
        cid: str,
        mid: str,
        reply_content: str,
    ):
        """
        回复某一条评论。

        Args:
            reply (str): 回复内容
            mid (str): get_all_comments 中返回的 analysis_extra 中的 mid
            cid (str): 评论 ID
        """
        url = 'https://weibo.com/ajax/comments/reply'
        
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'client-version': 'v2.46.33',
            'cookie': WeiBoTools.COOKIE,
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://weibo.com',
            'priority': 'u=1, i',
            'referer': 'https://weibo.com/u/7962675853',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'server-version': 'v2024.11.15.2',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-xsrf-token': WeiBoTools.XSRF_TOKEN
        }

        data = {
            'id': mid,
            'cid': cid,
            'comment': reply_content,
            'pic_id': '',
            'is_repost': 0,
            'comment_ori': 0,
            'is_comment': 0
        }

        response = requests.post(
            url, 
            headers=headers, 
            data=data
        )
        
        # print('================= post reply =================')
        # print(json.dumps(response.json(), ensure_ascii=False, indent=4))

        try:
            success = response.json().get('ok', 0)
            if success:
                WeiBoTools.ALREADY_REPLY_COMMENTS.append(cid)
                WeiBoTools.ALREADY_REPLY_COMMENTS = WeiBoTools.ALREADY_REPLY_COMMENTS[-100:]
            return success
        except:
            return False
            
    @staticmethod
    def get_all_my_post_weibo():
        """
        获取当前发布的所有微博。
        
        Returns: List[dict] -> {
                "visible": {
                    "type": 0,
                    "list_id": 0
                },
                "created_at": "Sat Nov 16 22: 37: 49 +0800 2024",
                "id": 5101466549487239,
                "idstr": "5101466549487239",
                "mid": "5101466549487239",
                "mblogid": "P0C9oDO3Z",
                "user": {
                    "id": 7962675853,
                    "idstr": "7962675853",
                    "pc_new": 0,
                    "screen_name": "用户7962675853",
                    "profile_image_url": "https: //tvax1.sinaimg.cn/default/images/default_avatar_female_50.gif?KID=imgbed,tva&Expires=1731781769&ssig=4uelfYugG1",
                    "profile_url": "/u/7962675853",
                    "verified": False,
                    "verified_type": -1,
                    "domain": "",
                    "weihao": "",
                    "status_total_counter": {
                        "total_cnt_format": 2,
                        "comment_cnt": "2",
                        "repost_cnt": "0",
                        "like_cnt": "0",
                        "total_cnt": "2"
                    },
                    "avatar_large": "https://tvax1.sinaimg.cn/default/images/default_avatar_female_180.gif?KID=imgbed,tva&Expires=1731781769&ssig=b6WpxTuYlk",
                    "avatar_hd": "https://tvax1.sinaimg.cn/default/images/default_avatar_female_180.gif?KID=imgbed,tva&Expires=1731781769&ssig=b6WpxTuYlk",
                    "follow_me": False,
                    "following": False,
                    "mbrank": 0,
                    "mbtype": 0,
                    "v_plus": None,
                    "planet_video": True,
                    "icon_list": []
                },
                "can_edit": False,
                "textLength": 22,
                "source": "微博 HTML5 版",
                "favorited": False,
                "rid": "0_0_50_5058370983808085644_0_0_0",
                "reads_count": 3,
                "pic_ids": [],
                "pic_num": 0,
                "is_paid": False,
                "mblog_vip_type": 0,
                "number_display_strategy": {
                    "apply_scenario_flag": 19,
                    "display_text_min_number": 1000000,
                    "display_text": "100万+"
                },
                "reposts_count": 0,
                "comments_count": 3,
                "attitudes_count": 0,
                "attitudes_status": 0,
                "isLongText": False,
                "mlevel": 0,
                "content_auth": 0,
                "is_show_bulletin": 2,
                "comment_manage_info": {
                    "comment_manage_button": 1,
                    "comment_permission_type": 0,
                    "approval_comment_type": 0,
                    "comment_sort_type": 0
                },
                "share_repost_type": 0,
                "mblogtype": 0,
                "showFeedRepost": False,
                "showFeedComment": False,
                "pictureViewerSign": False,
                "showPictureViewer": False,
                "rcList": [],
                "analysis_extra": "",
                "readtimetype": "mblog",
                "mixed_count": 0,
                "is_show_mixed": False,
                "isSinglePayAudio": False,
                "text": "微博真好用哈哈哈啊哈！ ​​​",
                "text_raw": "微博真好用哈哈哈啊哈！ ​​​",
                "region_name": "发布于 北京",
                "customIcons": []
            }
        """
        url = f'https://weibo.com/ajax/statuses/mymblog?uid={WeiBoTools.UID}&page=1&feature=0'
        
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'client-version': 'v2.46.33',
            'cookie': WeiBoTools.COOKIE,
            'priority': 'u=1, i',
            'referer': 'https://weibo.com/u/7962675853',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'server-version': 'v2024.11.15.2',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-xsrf-token': WeiBoTools.XSRF_TOKEN
        }

        response = requests.get(
            url, 
            headers=headers
        )

        try:
            return response.json()['data']['list']
        except:
            return []
        
    @staticmethod
    def test_get_all_my_post_weibo():
        """
        测试 get_all_my_post_weibo 方法。
        """
        res = WeiBoTools.get_all_my_post_weibo()
        return res != []
    
    @staticmethod
    def convert_weibo_datetime(
        weibo_date_str: str
    ):
        """将微博返回内容中的时间字符串转换为 年-月-日 时:分:秒 的形式

        Args:
            weibo_date_str (str): _Sat Nov 16 22: 38: 31 +0800 2024
        """
        date_obj = datetime.strptime(weibo_date_str, "%a %b %d %H:%M:%S %z %Y")
        return date_obj.strftime("%Y-%m-%d %H:%M:%S")
    
    
if __name__ == '__main__':
    res = WeiBoTools.post_weibo(
        "名侦探柯南哪个剧场版最好看？ 只能推荐一个。"
    )
    print(res)
    
    # print(
    #     WeiBoTools.get_all_my_post_weibo()
    # )
    
    # print(WeiBoTools.get_all_comments(5101486305972210))