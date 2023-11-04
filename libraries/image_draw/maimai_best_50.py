
import os
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
from .maimaidx_music import download_music_pictrue
from ..user_data.user_score_model import song_score

static = os.path.join(os.path.dirname(__file__), 'static')

class DrawText:

    def __init__(self, image: ImageDraw.ImageDraw, font: str) -> None:
        self._img = image
        self._font = font

    def get_box(self, text: str, size: int):
        return ImageFont.truetype(self._font, size).getbbox(text)

    def draw(self,
            pos_x: int,
            pos_y: int,
            size: int,
            text: str,
            color: Tuple[int, int, int, int] = (255, 255, 255, 255),
            anchor: str = 'lt',
            stroke_width: int = 0,
            stroke_fill: Tuple[int, int, int, int] = (0, 0, 0, 0),
            multiline: bool = False):

        font = ImageFont.truetype(self._font, size)
        if multiline:
            self._img.multiline_text((pos_x, pos_y), str(text), color, font, anchor, stroke_width=stroke_width, stroke_fill=stroke_fill)
        else:
            self._img.text((pos_x, pos_y), str(text), color, font, anchor, stroke_width=stroke_width, stroke_fill=stroke_fill)
    
    def draw_partial_opacity(self,
            pos_x: int,
            pos_y: int,
            size: int,
            text: str,
            po: int = 2,
            color: Tuple[int, int, int, int] = (255, 255, 255, 255),
            anchor: str = 'lt',
            stroke_width: int = 0,
            stroke_fill: Tuple[int, int, int, int] = (0, 0, 0, 0)):

        font = ImageFont.truetype(self._font, size)
        self._img.text((pos_x + po, pos_y + po), str(text), (0, 0, 0, 128), font, anchor, stroke_width=stroke_width, stroke_fill=stroke_fill)
        self._img.text((pos_x, pos_y), str(text), color, font, anchor, stroke_width=stroke_width, stroke_fill=stroke_fill)

class DrawBest:
    def __init__(self, content) -> None:
        self.userName = content['user_name']
        self.user_cover = content['user_cover']
        self.Rating = content['total_rating']
        self.best35 = content["b35"]
        self.best15 = content["b15"]
        self.cource_rank = content["cource_rank"]
        self.class_rank = content["class_rank"]
        self.cover_dir = os.path.join(static, 'mai', 'cover')
        self.maimai_dir = os.path.join(static, 'mai', 'pic')

    def _getCharWidth(self, o) -> int:
        widths = [
            (126, 1), (159, 0), (687, 1), (710, 0), (711, 1), (727, 0), (733, 1), (879, 0), (1154, 1), (1161, 0),
            (4347, 1), (4447, 2), (7467, 1), (7521, 0), (8369, 1), (8426, 0), (9000, 1), (9002, 2), (11021, 1),
            (12350, 2), (12351, 1), (12438, 2), (12442, 0), (19893, 2), (19967, 1), (55203, 2), (63743, 1),
            (64106, 2), (65039, 1), (65059, 0), (65131, 2), (65279, 1), (65376, 2), (65500, 1), (65510, 2),
            (120831, 1), (262141, 2), (1114109, 1),
        ]
        if o == 0xe or o == 0xf:
            return 0
        for num, wid in widths:
            if o <= num:
                return wid
        return 1

    def _coloumWidth(self, s: str) -> int:
        res = 0
        for ch in s:
            res += self._getCharWidth(ord(ch))
        return res

    def _changeColumnWidth(self, s: str, len: int) -> str:
        res = 0
        sList = []
        for ch in s:
            res += self._getCharWidth(ord(ch))
            if res <= len:
                sList.append(ch)
        return ''.join(sList)

    def _findRaPic(self) -> str:
        if self.Rating < 1000:
            num = '01'
        elif self.Rating < 2000:
            num = '02'
        elif self.Rating < 4000:
            num = '03'
        elif self.Rating < 7000:
            num = '04'
        elif self.Rating < 10000:
            num = '05'
        elif self.Rating < 12000:
            num = '06'
        elif self.Rating < 13000:
            num = '07'
        elif self.Rating < 14000:
            num = '08'
        elif self.Rating < 14500:
            num = '09'
        elif self.Rating < 15000:
            num = '10'
        else:
            num = '11'
        return f'UI_CMN_DXRating_{num}.png'

    async def whiledraw(self, data: List[song_score], type: bool) -> Image.Image:
        # y为第一排纵向坐标，dy为各排间距
        y = 430 if type else 1670
        dy = 170

        TEXT_COLOR = {
            'basic' : (255, 255, 255, 255),
            'advanced' : (255, 255, 255, 255), 
            'expert' : (255, 255, 255, 255), 
            'master' : (255, 255, 255, 255), 
            'remaster' : (103, 20, 141, 255)}
        DXSTAR_DEST = [0, 330, 320, 310, 300, 290]

        totalNum = len(data)
        for num, info in enumerate(data):
            print(f'当前进度: {num} / {totalNum}')
            if num % 5 == 0:
                x = 70
                y += dy if num != 0 else 0
            else:
                x += 416

            cover = Image.open(await download_music_pictrue(info.song_data.image_name)).resize((135, 135)).convert('RGBA')
            version = Image.open(os.path.join(self.maimai_dir, f'UI_RSL_MBase_Parts_{info.song_kind.upper()}.png')).resize((55, 19))
            rate = Image.open(os.path.join(self.maimai_dir, f'UI_TTR_Rank_{computeRa(info.user_score)}.png')).resize((95, 44))

            self._im.alpha_composite(self._diff[info.song_difficulty], (x, y))
            self._im.alpha_composite(cover, (x + 5, y + 5))
            self._im.alpha_composite(version, (x + 80, y + 141))
            self._im.alpha_composite(rate, (x + 150, y + 98))

            for tag in ['APP', 'AP', 'FCP', 'FC']:
                if tag in info.tag_list:
                    icon = Image.open(os.path.join(self.maimai_dir, f'UI_MSS_MBase_Icon_{tag}.png')).resize((45, 45))
                    self._im.alpha_composite(icon, (x + 260, y + 98))
                    break

            for tag in ['FSDP', 'FSD', 'FSP', 'FS']:
                if tag in info.tag_list:
                    icon = Image.open(os.path.join(self.maimai_dir, f'UI_MSS_MBase_Icon_{tag}.png')).resize((45, 45))
                    self._im.alpha_composite(icon, (x + 315, y + 98))
                    break

            title = info.song_name
            if self._coloumWidth(title) > 18:
                title = self._changeColumnWidth(title, 17) + '...'
            self._siyuan.draw(x + 155, y + 20, 20, title, TEXT_COLOR[info.song_difficulty], anchor='lm')
            p, s = f'{info.user_score:.4f}'.split('.')
            r = self._tb.get_box(p, 32)
            self._tb.draw(x + 155, y + 70, 32, p, TEXT_COLOR[info.song_difficulty], anchor='ld')
            self._tb.draw(x + 155 + r[2], y + 68, 22, f'.{s}%', TEXT_COLOR[info.song_difficulty], anchor='ld')
            self._tb.draw(x + 155, y + 80, 22, f'{info.internalLevelValue} -> {info.rating}', TEXT_COLOR[info.song_difficulty], anchor='lm')

    async def draw(self):
        
        meiryo = os.path.join(static, 'meiryo.ttc')
        siyuan = os.path.join(static, 'SourceHanSansSC-Bold.otf')
        Torus_SemiBold = os.path.join(static, 'Torus SemiBold.otf')
        
        logo = Image.open(os.path.join(self.maimai_dir, 'logo.png')).resize((378, 223))
        dx_rating = Image.open(os.path.join(self.maimai_dir, self._findRaPic())).resize((300, 59))
        Name = Image.open(os.path.join(self.maimai_dir, 'Name.png'))
        MatchLevel = Image.open(os.path.join(self.maimai_dir, f'UI_DNM_DaniPlate_{self.cource_rank}.png')).resize((134, 55))
        ClassLevel = Image.open(os.path.join(self.maimai_dir, f'UI_FBR_Class_{self.class_rank}.png')).resize((144, 87))
        rating = Image.open(os.path.join(self.maimai_dir, 'UI_CMN_Shougou_Rainbow.png')).resize((454, 50))
        self._diff = {
            'basic' : Image.open(os.path.join(self.maimai_dir, 'b40_score_basic.png')), 
            'advanced' : Image.open(os.path.join(self.maimai_dir, 'b40_score_advanced.png')), 
            'expert' : Image.open(os.path.join(self.maimai_dir, 'b40_score_expert.png')), 
            'master' : Image.open(os.path.join(self.maimai_dir, 'b40_score_master.png')), 
            'remaster' : Image.open(os.path.join(self.maimai_dir, 'b40_score_remaster.png'))
            }

        # 作图
        self._im = Image.open(os.path.join(self.maimai_dir, 'b40_bg.png')).convert('RGBA')

        self._im.alpha_composite(logo, (5, 104))
        plate = Image.open(os.path.join(self.maimai_dir, 'UI_Plate_300101.png')).resize((1420, 230))
        self._im.alpha_composite(plate, (390, 100))

        icon = Image.open(self.user_cover).resize((214, 214))
        self._im.alpha_composite(icon, (398, 108))
        
        self._im.alpha_composite(dx_rating, (620, 122))
        Rating = f'{self.Rating:05d}'
        for n, i in enumerate(Rating):
            self._im.alpha_composite(Image.open(os.path.join(self.maimai_dir, f'UI_NUM_Drating_{i}.png')).resize((20, 26)), (763 + 23 * n, 140))
        self._im.alpha_composite(Name, (620, 200))
        self._im.alpha_composite(MatchLevel, (935, 205))
        self._im.alpha_composite(ClassLevel, (926, 105))
        self._im.alpha_composite(rating, (620, 275))

        text_im = ImageDraw.Draw(self._im)
        self._meiryo = DrawText(text_im, meiryo)
        self._siyuan = DrawText(text_im, siyuan)
        self._tb = DrawText(text_im, Torus_SemiBold)

        self._meiryo.draw(635, 235, 40, self.userName, (0, 0, 0, 255), 'lm')
        self._meiryo.draw(847, 300, 22, 'BUDDiES Rating System By AnchorCat', (0, 0, 0, 255), 'mm', 3, (255, 255, 255, 255))

        await self.whiledraw(self.best35, True)
        await self.whiledraw(self.best15, False)

        return self._im
    
def computeRa(achievement: float) -> str:
    if achievement < 50:
        rate = 'D'
    elif achievement < 60:
        rate = 'C'
    elif achievement < 70:
        rate = 'B'
    elif achievement < 75:
        rate = 'BB'
    elif achievement < 80:
        rate = 'BBB'
    elif achievement < 90:
        rate = 'A'
    elif achievement < 94:
        rate = 'AA'
    elif achievement < 97:
        rate = 'AAA'
    elif achievement < 98:
        rate = 'S'
    elif achievement < 99:
        rate = 'SP'
    elif achievement < 99.5:
        rate = 'SS'
    elif achievement < 100:
        rate = 'SSP'
    elif achievement < 100.5:
        rate = 'SSS'
    else:
        rate = 'SSSP'

    return rate

async def generate(content: dict):
    draw_best = DrawBest(content)
    pic = await draw_best.draw()
    pic.show()
    pic.save('result.png')
    return pic