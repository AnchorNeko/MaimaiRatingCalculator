from io import BytesIO
import re
import math
import requests
import urllib3
import json
from bs4 import BeautifulSoup
from ..music_data.music_model import MaiMusicDB
from ..music_data.music_model import Song

def computeRa(ds: float, score: float) -> int:
    if score == None:
        score = 0
    if score < 50:
        baseRa = 7.0
    elif score < 60:
        baseRa = 8.0
    elif score < 70:
        baseRa = 9.6
    elif score < 75:
        baseRa = 11.2
    elif score < 80:
        baseRa = 12.0
    elif score < 90:
        baseRa = 13.6
    elif score < 94:
        baseRa = 15.2
    elif score < 97:
        baseRa = 16.8
    elif score < 98:
        baseRa = 20.0
    elif score < 99:
        baseRa = 20.3
    elif score < 99.5:
        baseRa = 20.8
    elif score < 100:
        baseRa = 21.1
    elif score < 100.5:
        baseRa = 21.6
    else:
        baseRa = 22.4
    data = math.floor(ds * (min(100.5, score) / 100) * baseRa)
    return data

def str_to_float(text):
    pattern = re.compile(r'\d+\.\d+')
    match = pattern.search(text)
    if match:
        return float(match.group())
    else:
        return None

class song_score:
    def __init__(self, song_name: str, user_score: float, song_kind: str, song_difficulty: str, song_data: Song, tag_list: [str]):
        self.song_name = song_name
        self.user_score = user_score
        self.song_kind = song_kind
        self.song_difficulty = song_difficulty
        self.song_data = song_data
        self.tag_list = tag_list
        #
        self.version = self.song_data.version
        for sheet in self.song_data.sheets:
            if sheet.type == self.song_kind and sheet.difficulty == song_difficulty:
                self.internalLevelValue = sheet.internal_level_value
                self.rating =  computeRa(sheet.internal_level_value, self.user_score)
        
class user_score_list:
    def __init__(self) -> None:
        pass        

    async def download_user_cover(self, session, img_url: str) -> BytesIO:
        req = session.get(url=img_url, verify=False)
        return BytesIO(req.content)

    async def get_user_score_list(self, config) -> list[song_score]:
        with open(config, "r", encoding="utf-8") as f:
            content = json.load(f)
        score_list = []
        print("""
        ==========开始模拟登陆流程==========
        """)
        urllib3.disable_warnings()
        session = requests.session()
        session.get(url="https://maimaidx.jp/maimai-mobile/", verify=False)

        session.post(url="https://maimaidx.jp/maimai-mobile/submit/", verify=False, data={
            "segaId" : content["user_name"],
            "password" : content["password"],
            "save_cookie" : "on",
            "token" : session.cookies["_t"]
        })

        session.get(url="https://maimaidx.jp/maimai-mobile/aimeList/submit/?idx=0", verify=False)

        session.get(url="https://maimaidx.jp/maimai-mobile/friend/", verify=False)
        
        session.get(url=f"https://maimaidx.jp/maimai-mobile/friend/friendGenreVs/", verify=False, params={
            "idx": content["friend_code"]
        })
        print("""
        ==========开始登陆流程完毕==========
        """)

        print("""
        ==========开始获取好友信息==========
        """)

        friendBaseInfo = session.get(url=f"https://maimaidx.jp/maimai-mobile/friend/friendDetail/", verify=False, params={
            "idx": content["friend_code"]
        })
        # 获取基本数据
        soup = BeautifulSoup(friendBaseInfo.text, features="html.parser")
        original_friend_data = soup.body.find(class_="wrapper main_wrapper t_c").find(class_="see_through_block m_15 m_t_5 p_10 t_l f_0 p_r").find(class_="basic_block p_10 f_0")
        self.user_name = original_friend_data.find(class_="p_l_10 f_l").find(class_="m_b_5").find(class_="name_block f_l f_16").text
        self.user_cover = await self.download_user_cover(session, original_friend_data.find(class_="w_112 f_l")["src"])
        self.cource_rank = original_friend_data.find(class_="p_l_10 f_l").find(class_="h_35 f_l")["src"].split("_")[-1][:2]
        self.class_rank = original_friend_data.find(class_="p_l_10 f_l").find(class_="p_l_10 h_35 f_l")["src"].split("_")[-1][:2]
        print("""
        ==========获取好友信息结束==========
        """)

        # 绿，黄，红，紫，白
        for diff in [0,1,2,3,4]:
            print(f"""
            ==========开始处理难度{MaiMusicDB.get_diff_name(diff)}歌曲数据==========
             """)
            res = session.get(url="https://maimaidx.jp/maimai-mobile/friend/friendGenreVs/battleStart/", verify=False, params={
                "scoreType": "2",
                "genre": "99",
                "diff": diff,
                "idx": content["friend_code"]
            })
            soup = BeautifulSoup(res.text, features="html.parser")
            original_html_data = soup.body.find(class_="wrapper main_wrapper t_c").find_all(class_=re.compile("_score_back w_450 m_15 p_3 f_0"))
            for song_original_data in original_html_data:
                song_name = song_original_data.find(class_="music_name_block t_l f_13 break").text
                user_score = str_to_float(song_original_data.find(attrs={"class" : "f_14 t_c"}).find_all(class_=re.compile("_score_label w_120 f_b"))[-1].text)
                if user_score == None:
                    continue
                song_kind = "std"
                if song_original_data.find(attrs={"src" : "https://maimaidx.jp/maimai-mobile/img/music_dx.png"}):
                    song_kind = "dx"

                song_tag_list = []
                for tagInfo in song_original_data.find_all(class_="t_r f_0")[-1].find_all(class_="h_30 f_r"):
                    song_tag_list.append(tagInfo["src"].split("icon_")[-1].split(".png")[0].upper())

                song_difficulty = str(song_original_data.find(attrs={"class" : "h_20 f_l"})["src"]).split("diff_")[1].split(".png")[0]
                original_song_data = MaiMusicDB.find_music(song_name)
                score_list.append(song_score(song_name = song_name, 
                                    user_score = user_score, 
                                    song_kind = song_kind, 
                                    song_difficulty = song_difficulty, 
                                    song_data = original_song_data,
                                    tag_list = song_tag_list))
            print(f"""
            ==========难度{MaiMusicDB.get_diff_name(diff)}歌曲数据处理完毕==========
             """)
        self.total_song_score = score_list
        return self.total_song_score
    
    def get_b50_data(self) -> dict:
        b35_list = []
        b15_list = []
        for song_score in self.total_song_score:
            if song_score.version == MaiMusicDB.get_newest_version():
                b15_list.append(song_score)
            else :
                b35_list.append(song_score)
        b35_list = sorted(b35_list, key=lambda song_score: song_score.rating, reverse=True)[:35]
        b15_list = sorted(b15_list, key=lambda song_score: song_score.rating, reverse=True)[:15]
        return {"b35":b35_list, "b15":b15_list}

    def get_total_rating(self) -> int:
        b50_data = self.get_b50_data()
        b50_data['user_name'] = self.user_name
        b50_data['user_cover'] = self.user_cover
        b50_data['cource_rank'] = self.cource_rank
        b50_data['class_rank'] = self.class_rank
        total_rating = 0
        print("======================================")
        print("旧曲B35成绩:")
        for song_score in b50_data["b35"]:
            print(f"{song_score.rating:<4} {song_score.internalLevelValue:<4} {song_score.user_score:<9} {song_score.song_name}")
            total_rating += song_score.rating
        print("======================================")
        print("新曲B15成绩:")
        for song_score in b50_data["b15"]:
            print(f"{song_score.rating:<4} {song_score.internalLevelValue:<4} {song_score.user_score:<9} {song_score.song_name}")
            total_rating += song_score.rating
        b50_data['total_rating'] = total_rating
        print("======================================")
        print(f"total_rating:{total_rating}")
        print("======================================")
        return b50_data

UserScoreList = user_score_list()