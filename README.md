# maimaiRatingCalculator (WIP)  
本脚本用于在日服环境下获取特定亲密好友的Best50并生成相应图片。  
相较于登录目标账户获取对应数据，虽然不能获取dxScore和当前将牌等装饰性信息，但较为安全。  
本脚本还在测试中，欢迎体验并提交issue  
  
致谢：  
日服歌曲数据来源网站 https://arcade-songs.zetaraku.dev/maimai/  
Best50图片生成代码部份 参考于该项目 https://github.com/Yuri-YuzuChaN/maimaiDX  
  
适用人群：  
能运行py脚本  
  
使用步骤:  
1. 准备一个临时查分用帐号，该帐号和要查询的帐号为亲密好友关系  
2. 复制 `config.example.json` 为 `config.json`  
3. 填写 `config.json` 中的 `friend_code`，值为待查询帐号的好友id  
4. 填写 `config.json` 中的 `user_name`（帐号）和 `password`（密码），帐号为查分用帐号  
5. 若需要更新本地缓存歌曲信息，将 `config.json` 中的 `update_local` 设置为 ture  
6. 先执行 `pip/pip3 install -r requirements.txt` 安装依赖  
7. 执行目录中的 `__init__`.py 文件  
  
关注嘉然谢谢喵～  
