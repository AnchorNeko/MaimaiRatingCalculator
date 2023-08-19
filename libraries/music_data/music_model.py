from typing import Optional
import aiohttp
import aiofiles
import os
import json

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

    async def get_music(self) -> list[Song]:
        """
        获取所有曲目数据
        """
        # try:
        #     async with aiohttp.request('GET', 'https://dp4p6x0xfi5o9.cloudfront.net/maimai/data.json', timeout=aiohttp.ClientTimeout(total=30)) as obj_data:
        #         if obj_data.status == 200:
        #             data = await obj_data.json()
        #             async with aiofiles.open(os.path.join(os.path.dirname(__file__), 'remote_music_data.json'), 'w', encoding='utf-8') as f:
        #                 await f.write(json.dumps(data, ensure_ascii=False, indent=4))
        # except Exception:
        #     async with aiofiles.open(os.path.join(os.path.dirname(__file__), 'music_data.json'), 'r', encoding='utf-8') as f:
        #         data = json.loads(await f.read())
        async with aiofiles.open(os.path.join(os.path.dirname(__file__), 'remote_music_data.json'), 'r', encoding='utf-8') as f:
                data = json.loads(await f.read())
        self.total_list = [Song.gene(song_data) for song_data in data['songs']]
        return self.total_list

    def find_music(self, music_name:str) -> Song:
        for song in self.total_list:
            if song.song_id == music_name:
                return song
        return None

MaiMusicDB = MaiMusicModel()