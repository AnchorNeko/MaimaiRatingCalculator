from typing import Optional
import os
import json

try:
    import aiohttp
except ModuleNotFoundError:
    aiohttp = None

# 创建 Sheets 类
class Sheet:
    def __init__(self, type, difficulty, level, level_value, internal_level, internal_level_value, note_designer, note_counts, regions, version):
        self.type = type
        self.difficulty = difficulty
        self.level = level
        self.level_value = level_value
        self.internal_level = internal_level
        self.internal_level_value = internal_level_value
        self.note_designer = note_designer
        self.note_counts = note_counts
        self.regions = regions
        self.version = version

class Song:
    def __init__(self, song_id, category, title, artist, bpm, image_name, version, release_date, is_new, is_locked, sheets):
        self.song_id = song_id
        self.category = category
        self.title = title
        self.artist = artist
        self.bpm = bpm
        self.image_name = image_name
        self.version = version
        self.release_date = release_date
        self.is_new = is_new
        self.is_locked = is_locked
        self.sheets = sheets

    def gene(data):
        sheets = [Sheet(sheet.get('type'), sheet.get('difficulty'), sheet.get('level'), sheet.get('levelValue'), sheet.get('internalLevel'), sheet.get('internalLevelValue'), sheet.get('noteDesigner'), sheet.get('noteCounts'), sheet.get('regions'), sheet.get('version')) for sheet in data.get('sheets')]
        song = Song(data.get('songId'), data.get('category'), data.get('title'), data.get('artist'), data.get('bpm'), data.get('imageName'), data.get('version'), data.get('releaseDate'), data.get('isNew'), data.get('isLocked'), sheets)
        return song
    
class MaiMusicModel:
    def __init__(self) -> None:
        pass

    async def get_music(self, updateLocal: bool = False) -> list[Song]:
        print("""
        ==========开始获取远端数据==========
        """)
        data = None
        if updateLocal == False and os.path.exists(file := os.path.join(os.path.dirname(__file__), 'remote_music_data.json')):
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        if data == None:
            if aiohttp is None:
                raise ModuleNotFoundError("缺少 aiohttp，无法在线更新歌曲数据。请先安装 aiohttp，或将 update_local 设为 false 并使用本地 remote_music_data.json。")
            try:
                async with aiohttp.request('GET', 'https://dp4p6x0xfi5o9.cloudfront.net/maimai/data.json', timeout=aiohttp.ClientTimeout(total=30)) as obj_data:
                    if obj_data.status == 200:
                        data = await obj_data.json()
                        with open(os.path.join(os.path.dirname(__file__), 'remote_music_data.json'), 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
            except Exception:
                pass
        if data is None:
            raise RuntimeError("歌曲数据加载失败：未读取到本地缓存，且在线拉取失败。请检查网络，或确认 remote_music_data.json 存在。")
        self.total_list = [Song.gene(song_data) for song_data in data['songs']]
        self.newest_version = [data['versions'][-1]['version'], data['versions'][-2]['version']]
        self.diff_list = data['difficulties']
        print("""
        ==========远端数据获取完毕==========
        """)
        return self.total_list

    def find_music(self, music_name:str) -> Song:
        for song in self.total_list:
            if song.song_id == music_name:
                return song
        print("未找到对应歌曲：", music_name)
        return None
    
    def get_newest_version(self) -> list[str]:
        return self.newest_version
    
    def get_diff_name(self, diff:int) -> str:
        return self.diff_list[diff]["name"]

MaiMusicDB = MaiMusicModel()
