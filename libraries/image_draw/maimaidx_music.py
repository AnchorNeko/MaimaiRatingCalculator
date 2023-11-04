import os
import urllib.request

static = os.path.join(os.path.dirname(__file__), 'static')
cover_dir = os.path.join(static, 'mai', 'cover')

async def download_music_pictrue(pic_name: str) -> str:
    if os.path.exists(file := os.path.join(static, 'mai', 'cover', pic_name)):
        return file
    img_url = f'https://dp4p6x0xfi5o9.cloudfront.net/maimai/img/cover-m/{pic_name}'
    # 下载并保存图片
    image_local_path = cover_dir + '/' + pic_name
    urllib.request.urlretrieve(img_url, image_local_path)
    return image_local_path

