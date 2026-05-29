import pytest

from client import APIClient, has_token
from config import TEST_ACCOUNT_ID, TEST_CHARACTER_ID, TEST_FCM_TOKEN
from schema_validator import validate_schema
from schemas import (
    # 指定数字人详情页，对应 ai-character/detail。
    AI_CHARACTER_DETAIL_SCHEMA,
    # AI 角色私聊会话列表，对应 ai-session/list-by-cursor。
    AI_SESSION_LIST_SCHEMA,
    # 拉黑列表接口，对应 action/block-list。
    BLOCK_LIST_SCHEMA,
    # 游标分页接口，例如 list-by-cursor。
    CURSOR_LIST_SCHEMA,
    # FCM token 推送接口，对应 account/set-fcm-token，data 必须是 null。
    FCM_TOKEN_SCHEMA,
    # 查看自己关注 following，对应 action/following。
    FOLLOWING_LIST_SCHEMA,
    # 角色feed流 mixed-feed 接口，里面是 feed item + character。
    MIX_FEED_SCHEMA,
    # 我的帖子接口，对应 art-post/my-posts。
    MY_POSTS_SCHEMA,
    # 普通（基本没有特色） page/page_size 分页接口，返回 items + has_more。
    PAGED_LIST_SCHEMA,
    # 推荐帖子接口，对应 art-post/recommend。
    POST_RECOMMEND_SCHEMA,
    # 指定账号主页的 AI 角色列表，对应带 account_id 的 ai-character/list。
    SPECIFIED_ACCOUNT_AI_CHARACTER_LIST_SCHEMA,
    # 所有接口公共的 status，要求 code=10000 且 msg=success。
    STATUS_SCHEMA,
    # 用户私聊会话列表，对应 ai-message/user-session/list。
    USER_SESSION_LIST_SCHEMA,
    # 互动未读数接口，对应 message/unread/count。
    UNREAD_COUNT_SCHEMA,
    # 当前用户信息接口，对应 account/me。
    USER_INFO_SCHEMA,
    #AI—question的接口，对应ai-question/should-show
    AI_QUESTION_SHOULD_SHOW_SCHEMA,
)


pytestmark = pytest.mark.skipif(not has_token(), reason="缺少 SEAHOT_TOKEN")
client = APIClient()


# 每一组参数就是一个接口用例：
# case_name 用来在失败时提示哪个接口有问题，response_schema 用来校验 data 的结构。
@pytest.mark.parametrize(
    "case_name,path,body,response_schema",
    [
        #登录后
        (
            "当前用户信息",
            "/api/v1/seahot-matrix-hub/account/me",
            {},
            USER_INFO_SCHEMA,
        ),
        #首页两条接口
        (
                "帖子列表new页流",
                "/api/v1/seahot-matrix-hub/art-post/list-by-cursor",
                {"page_size": 35},
                CURSOR_LIST_SCHEMA,
        ),
        (
                "推荐帖子",
                "/api/v1/seahot-matrix-hub/art-post/recommend",
                {"page": 1, "page_size": 35},
                POST_RECOMMEND_SCHEMA,
        ),
        (
            "账号个人主页AI角色列表",
            "/api/v1/seahot-soul-hub/ai-character/list",
            {
                "account_id": TEST_ACCOUNT_ID,
                "page": "1",
                "page_size": "20",
            },
            SPECIFIED_ACCOUNT_AI_CHARACTER_LIST_SCHEMA,
        ),
        (
            "拉黑列表",
            "/api/v1/seahot-soul-hub/action/block-list",
            {"page": 1, "page_size": 20},
            BLOCK_LIST_SCHEMA,
        ),
        (
            "我的帖子",
            "/api/v1/seahot-matrix-hub/art-post/my-posts",
            {"page": "1", "page_size": "20"},
            MY_POSTS_SCHEMA,
        ),
        (
            "查看自己关注following",
            "/api/v1/seahot-matrix-hub/action/following",
            {"follower_id": TEST_ACCOUNT_ID, "page": "1", "page_size": "20"},
            FOLLOWING_LIST_SCHEMA,
        ),
        (
            "查看自己粉丝followers列表",
            "/api/v1/seahot-matrix-hub/action/followers",
            {
                "following_id": TEST_ACCOUNT_ID, "page": "1", "page_size": "20"
            },
            PAGED_LIST_SCHEMA,
        ),
        #数字人角色feed流两条
        (
            "数字人角色单独Feed流（向下刷新操作）",
            "/api/v1/seahot-soul-hub/ai-character/mixed-feed",
            {"page": "1", "page_size": "35"},
            MIX_FEED_SCHEMA,
        ),
        (
                "指定数字人详情页",
                "/api/v1/seahot-soul-hub/ai-character/detail",
                {"id": TEST_CHARACTER_ID},
                AI_CHARACTER_DETAIL_SCHEMA,
        ),
        #消息页三条
        (
            "用户私聊会话列表",
            "/api/v1/seahot-soul-hub/ai-message/user-session/list",
            {"page": 1, "page_size": 100},
            USER_SESSION_LIST_SCHEMA,
        ),
        (
            "AI角色私聊会话列表",
            "/api/v1/seahot-soul-hub/ai-session/list-by-cursor",
            {"limit": "35"},
            AI_SESSION_LIST_SCHEMA,
        ),
        (
            "AI数字人主动发消息",
            "/api/v1/seahot-soul-hub/ai-question/should-show",
            {},
            AI_QUESTION_SHOULD_SHOW_SCHEMA,
        ),
        #互未读数是一个轮询接口，时间就触发
        (
            "互动未读数",
            "/api/v1/seahot-matrix-hub/message/unread/count",
            {},
            UNREAD_COUNT_SCHEMA,
        ),
        (
            "push_fcm_token推送消息接口",
            "/api/v1/seahot-matrix-hub/account/set-fcm-token",
            {"fcm_token": TEST_FCM_TOKEN},
            FCM_TOKEN_SCHEMA,
        ),
    ],
)
def test_api(case_name, path, body, response_schema):
    res  = client.post(path, body)

    # 先校验所有接口通用的外层结构（外层结构就是，data和status
    assert "data" in res, case_name
    assert "status" in res, case_name
    assert isinstance(res["status"], dict), case_name

    # 校验所有接口公共的 status的中业务码。
    # code 必须是 10000，msg 必须是 success，request_id 必须是字符串。
    validate_schema(res["status"], STATUS_SCHEMA,path = "status")

    # 再用每个接口自己的 schema 校验 data 里面的字段和类型。
    validate_schema(res["data"], response_schema, path = "data")

    # 分页接口的 items 数量不应该超过请求的 page_size 或 limit。
    # 注意：这里校验的是“最多返回多少条”，不是“必须返回多少条”。
    # 因为服务端可能由于数据不足、审核过滤、黑名单过滤等原因少返回。
    page_size = body.get("page_size") or body.get("limit")
    if isinstance(res["data"], dict) and "items" in res["data"] and page_size is not None:
        assert len(res["data"]["items"]) <= int(page_size), case_name
