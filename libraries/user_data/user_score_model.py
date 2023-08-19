
import re
import math
from bs4 import BeautifulSoup
from ..music_data.music_model import MaiMusicDB
from ..music_data.music_model import Song
from typing import Union

def computeRa(ds: float, score: float) -> int:
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
    def __init__(self, song_name: str, user_score: float, song_kind: str, song_difficulty: str, song_data: Song):
        self.song_name = song_name
        self.user_score = user_score
        self.song_kind = song_kind
        self.song_difficulty = song_difficulty
        self.song_data = song_data
        #
        self.version = self.song_data.version
        for sheet in self.song_data.sheets:
            if sheet.type == self.song_kind and sheet.difficulty == song_difficulty:
                self.internalLevelValue = sheet.internal_level_value
                self.rating =  computeRa(sheet.internal_level_value, self.user_score)
        
class user_score_list:
    def __init__(self) -> None:
        pass        

    def get_user_score_list(self, pathList: list[str]) -> list[song_score]:
        score_list = []
        for path in pathList:
            soup = BeautifulSoup(open(path))
            if soup.body is None:
                continue
            original_html_data = soup.body.find(attrs={"class" : "wrapper main_wrapper t_c o_v"}).find_all(attrs={"class" : "w_450 m_15 p_r f_0"})
            for song_original_data in original_html_data:
                if song_original_data.find(attrs={"class" : "music_score_block w_120 t_r f_l f_12"}) is None : 
                    continue
                song_name = str(song_original_data.find(attrs={"class" : "music_name_block t_l f_13 break"}).text).replace('\n',' ').replace('\t','')
                user_score = str_to_float(song_original_data.find(attrs={"class" : "music_score_block w_120 t_r f_l f_12"}).text)

                song_kind = "std"
                if song_original_data.find(attrs={"src" : "https://maimaidx.jp/maimai-mobile/img/music_dx.png"}):
                    song_kind = "dx"
                
                song_difficulty = str(song_original_data.find(attrs={"class" : "h_20 f_l"})["src"]).split("diff_")[1].split(".png")[0]
                original_song_data = MaiMusicDB.find_music(song_name)
                score_list.append(song_score(song_name = song_name, 
                                    user_score = user_score, 
                                    song_kind = song_kind, 
                                    song_difficulty = song_difficulty, 
                                    song_data = original_song_data))
        self.total_song_score = score_list
        return score_list
    
    def get_b50_data(self) -> dict:
        b35_list = []
        b15_list = []

        for song_score in self.total_song_score:
            if song_score.version == "FESTiVAL PLUS":
                b15_list.append(song_score)
            else :
                b35_list.append(song_score)

        b35_list = sorted(b35_list, key=lambda song_score: song_score.rating, reverse=True)[:35]
        b15_list = sorted(b15_list, key=lambda song_score: song_score.rating, reverse=True)[:15]

        return {"b35":b35_list, "b15":b15_list}

    def get_total_rating(self) -> int:
        total_rating = 0
        print("======================================")
        print("旧曲B35成绩:")
        for song_score in self.get_b50_data()["b35"]:
            print(f"{song_score.rating:<4} {song_score.internalLevelValue:<4} {song_score.user_score:<9} {song_score.song_name}")
            total_rating += song_score.rating
        print("======================================")
        print("新曲B15成绩:")
        for song_score in self.get_b50_data()["b15"]:
            print(f"{song_score.rating:<4} {song_score.internalLevelValue:<4} {song_score.user_score:<9} {song_score.song_name}")
            total_rating += song_score.rating
        print("======================================")
        print(f"total_rating:{total_rating}")
        print("======================================")
        return total_rating

    
UserScoreList = user_score_list()