# 这里的schema只检验了respose的data字段中数据类型

# 接口里有些字段可能返回 null，所以这里提前定义“可为空”的类型。
# 例如 source_stats 可能是 dict，也可能是 null。
NULLABLE_STR = (str, type(None))
NULLABLE_INT = (int, type(None))
NULLABLE_DICT = (dict, type(None))
NULLABLE_BOOL = (bool, type(None))
NULLABLE_NUMBER = (int, float, type(None))


# 所有接口公共的 status 结构。
# code 和 msg 是固定值校验：必须分别等于 10000 和 success。
STATUS_SCHEMA = {
    "code": 10000,
    "msg": "success",
    "request_id": str,
}
#FCM_token接口，向服务器发送到token，后续服务器通过fcm_token来推送消息
FCM_TOKEN_SCHEMA = None

# 通用分页列表结构：只校验 data 下最外层分页字段。
PAGED_LIST_SCHEMA = {
    "items": list,
    "has_more": bool,
}

# 指定账号主页的 AI 角色列表。
# 当前真实返回里 items 可能为空，所以这里只校验已经确定的分页外层字段。
SPECIFIED_ACCOUNT_AI_CHARACTER_LIST_SCHEMA = {
    "items": list,
    "has_more": bool,
}

# 拉黑列表接口。
# 当前真实返回里 items 为空，所以先校验已经确定的分页外层字段。
BLOCK_LIST_SCHEMA = {
    "items": list,
    "has_more": bool,
}

# 游标分页结构：next_cursor 可能是字符串，也可能是 null。
CURSOR_LIST_SCHEMA = {
    "items": list,
    "next_cursor": NULLABLE_STR,
}

USER_HOME_SET_SCHEMA = {
    "sex": int,
    "region": str,
    "show_sex": int,
    "intro": str,
    "notice": str,
    "notice_at": int,
    "background_img_nsfw_level": int,
    "background_img": str,
    "interest_tag": NULLABLE_DICT,
    "interest_module": NULLABLE_DICT,
    "skip": bool,
    "mbti": str,
    "birthday": str,
    "profession": str,
    "disable_notice": bool,
}

USER_STATS_SCHEMA = {
    "follower_count": int,
    "following_count": int,
}

# 当前用户信息接口，对应 account/me。
USER_INFO_SCHEMA = {
    "id": str,
    "uid": str,
    "name": str,
    "account_no": str,
    "type": int,
    "third_type": int,
    "email": str,
    "app_id": str,
    "avatar": str,
    "avatar_frame": NULLABLE_DICT,
    "owned_avatar_frame": NULLABLE_DICT,
    "background": NULLABLE_DICT,
    "owned_background": NULLABLE_DICT,
    "chat_bubble": NULLABLE_DICT,
    "owned_chat_bubble": NULLABLE_DICT,
    "device_id": str,
    "device_os": str,
    "device_type": str,
    "is_online": bool,
    "home_set": USER_HOME_SET_SCHEMA,
    "stats": USER_STATS_SCHEMA,
    "status": int,
    "source": int,
    "create_at": int,
    "update_at": int,
    "country_code": str,
    "im_user_created": bool,
    "is_banned": bool,
    "is_muted": bool,
    "is_post_ban": bool,
}

FOLLOWING_USER_HOME_SET_SCHEMA = {
    "sex": int,
    "region": str,
    "show_sex": int,
    "intro": str,
    "notice": str,
    "notice_at": int,
    "background_img_nsfw_level": int,
    "background_img": str,
    "interest_tag": (list, type(None)),
    "interest_module": NULLABLE_DICT,
    "skip": bool,
    "mbti": str,
    "birthday": str,
    "profession": str,
    "disable_notice": bool,
}

FOLLOWING_USER_SCHEMA = {
    "id": str,
    "uid": str,
    "name": str,
    "account_no": str,
    "type": int,
    "third_type": int,
    "email": str,
    "app_id": str,
    "avatar": str,
    "avatar_frame": NULLABLE_DICT,
    "owned_avatar_frame": NULLABLE_DICT,
    "background": NULLABLE_DICT,
    "owned_background": NULLABLE_DICT,
    "chat_bubble": NULLABLE_DICT,
    "owned_chat_bubble": NULLABLE_DICT,
    "device_id?": str,
    "device_os?": str,
    "device_type": str,
    "is_online": bool,
    "language?": str,
    "home_set": FOLLOWING_USER_HOME_SET_SCHEMA,
    "stats": USER_STATS_SCHEMA,
    "status": int,
    "source": int,
    "create_at": int,
    "update_at": int,
    "country_code": str,
    "im_user_created": bool,
    "is_banned": bool,
    "is_muted": bool,
    "is_post_ban": bool,
    "follow_type": int,
    "follow_type_desc": str,
    "follow_at": int,
}

# 查看自己关注 following，对应 action/following。
FOLLOWING_LIST_SCHEMA = {
    "has_more": bool,
    "items": [FOLLOWING_USER_SCHEMA],
}

#未读数统计，接口unread/count
UNREAD_COUNT_SCHEMA = {
    "total": int,
    "like_count": int,
    "comment_count": int,
    "reply_count": int,
    "follow_count": int,
    "system_count": int,
    "report_count": int,
    "collect_count": int,
    "character_chat_count": int,
    "character_exposure_count": int,
    "post_exposure_count": int,
    "last_update_time": int,
}
#数字人图片
CHARACTER_COVER_SCHEMA = {
    "width": int,
    "height": int,
    "uri": str,
}

CHARACTER_STAT_SCHEMA = {
    "msg_count_virtual": int,
    "msg_count_real": int,
    "like_count_virtual": int,
    "like_count_real": int,
    "sess_count_virtual": int,
    "sess_count_real": NULLABLE_INT,
}

# 指定数字人详情页，对应 ai-character/detail。
# 详情页比列表多了 account、msg_send_count、session_count、unlocked 等字段。
AI_CHARACTER_DETAIL_SCHEMA = {
    "id": str,
    "create_at": int,
    "update_at": int,
    "app_id": str,
    "account_id": str,
    "name": str,
    "avatar": str,
    "first_msg": str,
    "description": str,
    "scenario": str,
    "personality": str,
    "model_id": str,
    "cover": CHARACTER_COVER_SCHEMA,
    "tag": str,
    "type": str,
    "visibility": int,
    "status": int,
    "safety_tag": str,
    "stat": CHARACTER_STAT_SCHEMA,
    "original_first_msg": str,
    "original_scenario": str,
    "original_description": str,
    "account": NULLABLE_DICT,
    "msg_send_count": int,
    "session_count": int,
    "unlocked": NULLABLE_BOOL,
}

# recommend 接口里的图片对象，对应 items[].images[]。
POST_MEDIA_IMAGE_SCHEMA = {
    "url": str,
    "thumbnail": str,
    "width": int,
    "height": int,
}

# recommend 接口里的视频对象，对应 items[].videos[]。
POST_MEDIA_VIDEO_SCHEMA = {
    "url": str,
    "thumbnail": str,
    "width": int,
    "height": int,
    "size": int,
    "duration": int,
    "mime_type": str,
    "name": str,
}

# 帖子的计数字段，对应 items[].stats。
POST_STATS_SCHEMA = {
    "view_count": int,
    "like_count": int,
    "collect_count": int,
    "comment_count": int,
    "share_count": int,
}

# 帖子关联数字人时，link_obj.stat 里的字段比角色列表里的 stat 少。
POST_LINK_CHARACTER_STAT_SCHEMA = {
    "msg_count_virtual": int,
    "msg_count_real": int,
    "like_count_virtual": int,
    "like_count_real": int,
}

# 帖子关联的数字人对象，对应 items[].link_obj。
POST_LINK_CHARACTER_SCHEMA = {
    "id": str,
    "create_at": int,
    "update_at": int,
    "app_id": str,
    "account_id": str,
    "name": str,
    "avatar": str,
    "first_msg": str,
    "description": str,
    "scenario": str,
    "personality": str,
    "model_id": str,
    "cover": CHARACTER_COVER_SCHEMA,
    "tag": str,
    "type": str,
    "visibility": int,
    "status": int,
    "safety_tag": str,
    "stat": POST_LINK_CHARACTER_STAT_SCHEMA,
    "original_first_msg?": str,
    "original_scenario?": str,
    "original_description?": str,
}

# recommend 的单条帖子结构。
# 字段名后面加 ? 表示“这个字段可以不返回”；如果返回了，仍然会校验类型。
# 例如纯文本帖子没有 images/videos，图片帖子没有 videos。
POST_ITEM_SCHEMA = {
    "id": str,
    "create_at": int,
    "update_at": int,
    "account_id": str,
    "app_id": str,
    "content": str,
    "post_type": int,
    "status": int,
    "visibility": int,
    "is_top": int,
    "publish_at": int,
    "stats": POST_STATS_SCHEMA,
    "source": str,
    "source_stats": NULLABLE_DICT,
    "author_name": str,
    "author_avatar": str,
    "account_online": bool,
    "is_liked": bool,
    "is_collected": bool,
    "follow_type": int,
    "style": int,
    "pt": str,
    "images?": [POST_MEDIA_IMAGE_SCHEMA],
    "videos?": [POST_MEDIA_VIDEO_SCHEMA],
    "link_type?": str,
    "link?": str,
    "link_obj?": POST_LINK_CHARACTER_SCHEMA,
    "nsfw_level?": int,
}

# recommend 接口 data 的整体结构。
# items 使用 [POST_ITEM_SCHEMA] 表示：items 是列表，并且列表里的每一项都按 POST_ITEM_SCHEMA 校验。
POST_RECOMMEND_SCHEMA = {
    "items": [POST_ITEM_SCHEMA],
    "has_more": bool,
}

# 我的帖子接口里的单条帖子结构，对应 art-post/my-posts 的 items[]。
# my-posts 里草稿/审核失败等状态的帖子可能没有 publish_at，也没有 pt 字段。
MY_POST_ITEM_SCHEMA = {
    "id": str,
    "create_at": int,
    "update_at": int,
    "account_id": str,
    "app_id": str,
    "content": str,
    "post_type": int,
    "status": int,
    "visibility": int,
    "is_top": int,
    "publish_at?": int,
    "stats": POST_STATS_SCHEMA,
    "source": str,
    "source_stats": NULLABLE_DICT,
    "author_name": str,
    "author_avatar": str,
    "account_online": bool,
    "is_liked": bool,
    "is_collected": bool,
    "follow_type": int,
    "style": int,
    "images?": [POST_MEDIA_IMAGE_SCHEMA],
    "videos?": [POST_MEDIA_VIDEO_SCHEMA],
    "link_type?": str,
    "link?": str,
    "link_obj?": POST_LINK_CHARACTER_SCHEMA,
    "nsfw_level?": int,
}

# 我的帖子接口 data 的整体结构。
# 除了 has_more，还会返回上一页标识和当前页首尾帖子 id。
MY_POSTS_SCHEMA = {
    "items": [MY_POST_ITEM_SCHEMA],
    "has_more": bool,
    "has_prev": bool,
    "first_id": str,
    "last_id": str,
}

USER_SESSION_USER_HOME_SET_SCHEMA = {
    "sex": int,
    "region": str,
    "show_sex": int,
    "intro": str,
    "notice": str,
    "notice_at": int,
    "background_img_nsfw_level": int,
    "background_img": str,
    "interest_tag": (list, type(None)),
    "interest_module": NULLABLE_DICT,
    "skip": bool,
    "mbti": str,
    "birthday": str,
    "profession": str,
    "disable_notice": bool,
}

USER_SESSION_USER_SCHEMA = {
    "id": str,
    "create_at": int,
    "update_at": int,
    "uid": str,
    "union_id": str,
    "name": str,
    "account_no": str,
    "email": str,
    "app_id": str,
    "avatar": str,
    "avatar_frame": NULLABLE_DICT,
    "owned_avatar_frame": NULLABLE_DICT,
    "background": NULLABLE_DICT,
    "owned_background": NULLABLE_DICT,
    "chat_bubble": NULLABLE_DICT,
    "owned_chat_bubble": NULLABLE_DICT,
    "auth_token": str,
    "device_id?": str,
    "login_device_id?": str,
    "device_os?": str,
    "device_type?": str,
    "device_token?": str,
    "language?": str,
    "is_online?": bool,
    "home_set": USER_SESSION_USER_HOME_SET_SCHEMA,
    "stats": USER_STATS_SCHEMA,
    "status": int,
    "password": str,
    "source": int,
    "type": int,
    "third_type": int,
    "fbcl_id": str,
    "country_code": str,
    "im_not_created": bool,
}

USER_SESSION_RELATION_STATUS_SCHEMA = {
    "blocked_by_me": bool,
    "blocked_by_other": bool,
}

USER_SESSION_ITEM_SCHEMA = {
    "session_id": str,
    "type": int,
    "room_id": str,
    "group_id": str,
    "is_top": bool,
    "is_online": bool,
    "account_online": bool,
    "last_message_id": str,
    "last_message": str,
    "last_message_type": str,
    "last_message_status": int,
    "last_message_at": int,
    "unread_count": int,
    "user": USER_SESSION_USER_SCHEMA,
    "relation_status": USER_SESSION_RELATION_STATUS_SCHEMA,
}

# 用户私聊会话列表，对应 ai-message/user-session/list。
USER_SESSION_LIST_SCHEMA = {
    "items": [USER_SESSION_ITEM_SCHEMA],
    "total": int,
    "has_more": bool,
}

AI_SESSION_CHARACTER_SCHEMA = {
    "id": str,
    "name": str,
    "avatar": str,
}

AI_SESSION_ITEM_SCHEMA = {
    "id": str,
    "character_id": str,
    "character": AI_SESSION_CHARACTER_SCHEMA,
    "is_top": bool,
    "last_message_id?": str,
    "last_message?": str,
    "message_count": int,
    "update_at": int,
}

# AI 角色私聊会话列表，对应 ai-session/list-by-cursor。
# 有些只有一条消息的会话可能没有 last_message_id/last_message。
AI_SESSION_LIST_SCHEMA = {
    "items": [AI_SESSION_ITEM_SCHEMA],
    "has_more": bool,
    "next_cursor": (int, str, type(None)),
}

# mixed-feed 里有些 character 只返回 account/unlocked，
# 所以角色详情字段这里做成可选，避免真实接口返回空壳对象时误报。
MIX_FEED_CHARACTER_SCHEMA = {
    "id?": str,
    "create_at?": int,
    "update_at?": int,
    "app_id?": str,
    "account_id?": str,
    "name?": str,
    "avatar?": str,
    "first_msg?": str,
    "description?": str,
    "scenario?": str,
    "personality?": str,
    "model_id?": str,
    "cover?": CHARACTER_COVER_SCHEMA,
    "tag?": str,
    "type?": str,
    "visibility?": int,
    "status?": int,
    "safety_tag?": str,
    "stat?": CHARACTER_STAT_SCHEMA,
    "original_first_msg?": str,
    "original_scenario?": str,
    "original_description?": str,
    "nsfw_level?": int,
    "quality_level?": str,
    "goods_id?": str,
    "pt?": str,
    "account": NULLABLE_DICT,
    "unlocked": NULLABLE_BOOL,
}

MIX_FEED_ITEM_SCHEMA = {
    "type": str,
    "character": MIX_FEED_CHARACTER_SCHEMA,
}

MIX_FEED_SCHEMA = {
    "items": [MIX_FEED_ITEM_SCHEMA],
    "has_more": bool,
}
# 少数
AI_QUESTION_SHOULD_SHOW_SCHEMA = {
    "show": bool,
}
