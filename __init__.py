import asyncio
import json
import os
import aiofiles


from libraries.music_data.music_model import MaiMusicDB
from libraries.user_data.user_score_model import UserScoreList
from libraries.image_draw.maimai_best_50 import generate

configPath = os.path.join(os.path.dirname(__file__), 'config.json')

if __name__ == '__main__':
    content = {}
    with open(configPath, "r", encoding="utf-8") as f:
        content = json.load(f)
    asyncio.get_event_loop().run_until_complete(MaiMusicDB.get_music(content["update_local"]))
    asyncio.get_event_loop().run_until_complete(UserScoreList.get_user_score_list(configPath))
    asyncio.get_event_loop().run_until_complete(generate(UserScoreList.get_total_rating()))