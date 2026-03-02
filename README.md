# maimaiRatingCalculator

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-GPL--3.0-green.svg)](LICENSE)

一个用于 **maimai DX（日服）** 的 Best50 生成工具。  
项目通过登录“查询账号”，读取其亲密好友（目标玩家）的成绩页，计算 B35 + B15，并生成一张汇总图片。

## 功能特性

- 拉取并缓存日服歌曲数据（可选择本地缓存或在线更新）
- 抓取目标好友在 5 个难度下的成绩数据
- 按当前版本规则计算单曲 Rating 与总 Rating
- 生成 Best50 可视化结果图（`result.png`）

## 效果预览

![result preview](./result.png)

## 工作方式说明

本项目使用“查询账号”登录 maimai mobile 并访问好友页面，因此：

- 目标账号需要与查询账号建立亲密好友关系
- 不直接登录目标账号，相对更安全
- 由于数据来源限制，部分装饰性信息（如部分界面元素）可能无法完整还原

## 快速开始

### 1. 环境要求

- Python `3.9+`
- 可访问 maimai 日服相关网络资源

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置文件

复制示例配置：

```bash
cp config.example.json config.json
```

编辑 `config.json`：

```json
{
  "user_name": "your_query_account",
  "password": "your_query_password",
  "friend_code": "target_friend_code",
  "update_local": false
}
```

配置项说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `user_name` | `string` | 查询账号用户名（用于登录） |
| `password` | `string` | 查询账号密码 |
| `friend_code` | `string` | 目标好友在查询账号好友列表中的 `idx` |
| `update_local` | `boolean` | `true` 时强制在线更新歌曲数据并写入本地缓存 |

### 4. 运行

```bash
python __init__.py
```

运行完成后会在项目根目录生成：

- `result.png`：Best50 结果图

## 项目结构

```text
.
├── __init__.py                          # 程序入口
├── config.example.json                  # 配置示例
├── libraries
│   ├── music_data/music_model.py        # 曲库拉取、缓存与查询
│   ├── user_data/user_score_model.py    # 好友成绩抓取与 Rating 计算
│   └── image_draw/maimai_best_50.py     # 图片绘制与导出
└── requirements.txt
```

## 常见问题

### 1) 运行时报网络或超时错误

- 检查网络连通性
- 如果本地已有曲库缓存，可先将 `update_local` 设为 `false` 再试

### 2) 提示缺少 `aiohttp`

```bash
pip install aiohttp
```

### 3) 生成图片时字体或显示异常

- 项目依赖 `libraries/image_draw/static/` 下的资源文件
- 请确认仓库完整拉取，且文件未被删除

## 安全与使用建议

- 建议仅使用临时查询账号，不要使用主账号
- `config.json` 含明文凭据，请勿提交到公开仓库
- 本项目仅用于学习与个人研究，请遵守相关服务条款

## 贡献

欢迎提交 Issue 和 Pull Request。  
建议在提交前说明复现步骤、运行环境和预期行为，便于快速定位问题。

## 致谢

- 歌曲数据参考：[arcade-songs.zetaraku.dev](https://arcade-songs.zetaraku.dev/maimai/)
- 图片生成逻辑参考：[Yuri-YuzuChaN/maimaiDX](https://github.com/Yuri-YuzuChaN/maimaiDX)

## License

本项目使用 [GPL-3.0](./LICENSE) 协议开源。
