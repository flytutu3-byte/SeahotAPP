# SeaHot Python 接口自动化 Demo

最小结构：

- `client.py`：请求封装、公共 Header、基础断言
- `schema_validator.py`：响应 schema 校验
- `tests/test_api.py`：pytest 用例
- `STABLE_APIS.md`：长期稳定接口清单
- `local_config.py`：你的本地 token，不要发给别人

## 安装

```bash
cd /Users/xhmac374/Downloads/seahot_api_auto_demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 配置 token

创建或编辑 `local_config.py`，写入：

```python
SEAHOT_TOKEN = "你的真实token"

# 测试数据配置，换账号或换测试对象时只改这里。
TEST_ACCOUNT_ID = "测试账号id"
TEST_CHARACTER_ID = "测试数字人id"
TEST_FCM_TOKEN = "测试fcm_token"
```

## 运行

```bash
pytest -v
```

当前用例主要覆盖“只读接口”和“空 body 接口”，适合长期稳定回归。

## 生成 Allure HTML 报告

先安装 Python 依赖：

```bash
pip install -r requirements.txt
```

Allure HTML 需要本机安装 Allure CLI：

```bash
brew install allure
```

然后运行：

```bash
pytest -vs
```

报告会统一放在 `reports/allure-html` 目录下：

- `reports/allure-html/时间戳/index.html`：每次运行单独保存一份
- `reports/allure-html/latest/index.html`：最近一次运行的报告
- `reports/allure-results/latest`：最近一次 Allure 原始结果
- `reports/allure-results/时间戳`：每次运行归档的 Allure 原始结果

也可以运行这个快捷脚本：

```bash
python scripts/run_allure.py
```

## 新增接口

在 `tests/test_api.py` 的参数列表里加一行：

```python
("接口名称", "/接口URL", {"请求参数": "值"}, {"返回字段": 字段类型})
```
