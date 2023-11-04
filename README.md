# maimaiRatingCalculator (WIP) 
a simple maimai rating calculator for Japan

Thanks:
Data Source : https://arcade-songs.zetaraku.dev/maimai/

Usage steps:
1. 准备一个临时帐号，该帐号和要查询的帐号为亲密好友关系 
2. 填写config.json中的friend_code，值为待查询帐号的好友id
3. 使用chrome登陆日服maimai官网，F12打开开发者面板，切换到网络标签，搜索maimai-mobile/，点击右边的cookies，将所有的cookies全部填入config.json里面的cookies里
4. 执行脚本
