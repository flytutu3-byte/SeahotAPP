import os

try:
    import local_config
except ImportError:
    local_config = None


def get_config_value(name: str, default: str = "") -> str:
    """优先读取环境变量，其次读取 local_config.py，最后使用默认值。"""

    return os.getenv(name, getattr(local_config, name, default))


# 以下是测试数据，不是接口逻辑。
# # 换账号、换环境、换测试角色时，只需要改 local_config.py 或环境变量，不需要改用例代码。
TEST_ACCOUNT_ID = get_config_value("TEST_ACCOUNT_ID", "c58eea592bb603ecbfee174c89c6fa71")
TEST_CHARACTER_ID = get_config_value("TEST_CHARACTER_ID", "ffc9be04c678e14a2fa5b63887f7c273")
TEST_FCM_TOKEN = get_config_value("TEST_FCM_TOKEN", "python-demo-fcm-token")
