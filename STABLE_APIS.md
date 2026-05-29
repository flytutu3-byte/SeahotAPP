# 长期稳定接口清单

筛选原则：

- 只选查询类接口
- 不创建、不删除、不发送消息、不下单
- 参数简单
- 返回结构稳定
- 当前 token 实测 `status.code = 10000`

| 优先级 | 模块 | 接口名称 | Method | URL | 请求参数 | 关键断言 |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | 用户 | 当前用户信息 | POST | `/api/v1/seahot-matrix-hub/account/me` | `{}` | `data.id`, `data.name` |
| P0 | 首页 | AI 角色列表 | POST | `/api/v1/seahot-soul-hub/ai-character/list` | `page`, `page_size` | `data.items`, `data.has_more` |
| P0 | 首页 | 指定账号 AI 角色列表 | POST | `/api/v1/seahot-soul-hub/ai-character/list` | `account_id`, `page`, `page_size` | `data.items`, `data.has_more` |
| P0 | 首页 | 首页混合 Feed | POST | `/api/v1/seahot-soul-hub/ai-character/mixed-feed` | `page`, `page_size` | `data.items`, `data.has_more` |
| P1 | 用户 | 拉黑列表 | POST | `/api/v1/seahot-soul-hub/action/block-list` | `page`, `page_size` | `data.items`, `data.has_more` |
| P1 | 内容 | 推荐帖子 | POST | `/api/v1/seahot-matrix-hub/art-post/recommend` | `page`, `page_size` | `data.items`, `data.has_more` |
| P1 | 内容 | 帖子列表游标分页 | POST | `/api/v1/seahot-matrix-hub/art-post/list-by-cursor` | `page_size` | `data.items`, `data.next_cursor` |
| P1 | 内容 | 我的帖子 | POST | `/api/v1/seahot-matrix-hub/art-post/my-posts` | `page`, `page_size` | `data.items`, `data.has_more` |
| P1 | 私聊 | 用户私聊会话列表 | POST | `/api/v1/seahot-soul-hub/ai-message/user-session/list` | `page`, `page_size` | `data.items`, `data.has_more` |
| P1 | 聊天 | AI 会话列表 | POST | `/api/v1/seahot-soul-hub/ai-session/list-by-cursor` | `limit` | `data.items`, `data.has_more` |
| P1 | 消息 | 互动未读数 | POST | `/api/v1/seahot-matrix-hub/message/unread/count` | `{}` | `data.total` |
| P1 | 商品 | 商品列表 | POST | `/api/v1/seahot-soul-hub/ai-goods/list` | `{}` | `data.items`, `data.total` |
| P1 | 钱包 | 钱包余额 | POST | `/api/v1/seahot-soul-hub/ai-wallet/balance` | `{}` | `data.balance` |
| P1 | 权益 | 用户权益 | POST | `/api/v1/seahot-soul-hub/ai-benefits/user` | `{}` | `data.benefits_id`, `data.type` |
| P1 | 商品 | 首充检查 | POST | `/api/v1/seahot-soul-hub/ai-goods/check-first-pay` | `{}` | `data.has_purchased` |
| P2 | 聊天权益 | 跳过冷却状态 | POST | `/api/v1/seahot-soul-hub/ai-benefits/skip-cooldown-status` | `{}` | `data.can_skip`, `data.coin_balance` |
| P2 | 小说 | 小说生成状态 | POST | `/api/v1/seahot-soul-hub/ai-novel/chapter/generate-stats` | `{}` | `data.can_generate`, `data.coin_balance` |
| P2 | 生图 | 图片生成状态 | POST | `/api/v1/seahot-soul-hub/ai-character/image-generate-stats` | `{}` | `data.can_generate`, `data.coin_balance` |
| P2 | 弹窗 | 评分弹窗检查 | POST | `/api/v1/seahot-soul-hub/misc-data/rating-popup-check` | `{}` | `data.reached`, `data.not_shown` |
| P2 | 问卷 | 问卷是否展示 | POST | `/api/v1/seahot-soul-hub/ai-question/should-show` | `{}` | `data.show` |

暂不建议放进长期稳定用例：

| 接口 | 原因 |
| --- | --- |
| 敏感词检测 | 当前参数实测返回 `10100 params error`，需要先从真实 curl 确认请求体 |
| 用户装扮 | 空 body 可成功，但长用例运行中出现连接超时，先放备选 |
| SoulMatch剩余次数 | 空 body 可成功，但长用例运行中出现连接超时，先放备选 |
| AI 任务列表 | 本次探测返回 `10200 server error` |
| APP 版本检查 | 空 body 实测返回 `10100 params error`，需要确认真实请求参数 |
| 创建会话、发送消息、删除消息、关注、点赞、下单 | 会修改业务数据，不适合作为最早期稳定回归用例 |
