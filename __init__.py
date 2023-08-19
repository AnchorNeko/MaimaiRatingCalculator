import asyncio
import os
import json


from libraries.music_data.music_model import MaiMusicDB
from libraries.user_data.user_score_model import UserScoreList

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(MaiMusicDB.get_music())
    UserScoreList.get_user_score_list([os.path.join(os.path.dirname(__file__), '白.txt'),
                                       os.path.join(os.path.dirname(__file__), '紫.txt'),
                                       os.path.join(os.path.dirname(__file__), '红.txt')])
    UserScoreList.get_total_rating()
