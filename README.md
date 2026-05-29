# SeaHot API 自动化测试项目

## 项目介绍

这是一个基于 Python、pytest、requests 和 Allure 的 SeaHot App 接口自动化测试项目。

当前项目覆盖用户信息、帖子流、推荐、关注/粉丝、AI 角色、消息、未读数、FCM Token 等核心接口。用例通过 pytest 参数化组织，公共请求逻辑封装在 `APIClient` 中，接口响应通过自定义 `schema_validator` 做结构校验。

项目已经接入 GitHub Actions，支持以下触发方式：

- push 到 `main` 分支后自动运行全部接口用例
- pull request 到 `main` 分支后自动运行全部接口用例
- 在 GitHub Actions 页面手动运行
- 每天 09:00 Asia/Shanghai 定时运行

## 环境要求

本地运行需要：

- Python 3.11 或 3.12，GitHub Actions 当前使用 Python 3.12
- pip
- 可访问 SeaHot 测试环境网络
- 有效的 `SEAHOT_TOKEN`
- 可选：Allure CLI 或 Node.js/npx，用于生成 Allure HTML 报告

Windows、macOS、Linux 都可以运行。Windows 建议使用 PowerShell 或 Git Bash。

## 安装依赖

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

如果 PowerShell 禁止激活虚拟环境，可以先执行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## local_config.py 配置

`local_config.py` 用来保存本地 token 和测试数据，已被 `.gitignore` 忽略，不会提交到 GitHub。

在项目根目录创建 `local_config.py`：

```python
SEAHOT_TOKEN = "你的真实 token"

# 测试数据配置，换账号或换测试对象时只改这里。
TEST_ACCOUNT_ID = "测试账号 id"
TEST_CHARACTER_ID = "测试数字人 id"
TEST_FCM_TOKEN = "测试 fcm_token"
```

配置读取优先级：

1. 环境变量
2. `local_config.py`
3. 代码里的默认值

支持的环境变量：

```text
SEAHOT_BASE_URL
SEAHOT_TOKEN
SEAHOT_TIMEOUT
SEAHOT_RETRY
SEAHOT_USE_ENV_PROXY
TEST_ACCOUNT_ID
TEST_CHARACTER_ID
TEST_FCM_TOKEN
```

如果没有配置 `SEAHOT_TOKEN`，真实接口用例会被跳过，只会运行不依赖 token 的本地 smoke 测试。

## 本地运行

运行全部用例：

```bash
pytest -q
```

或使用 Python 模块方式运行：

```bash
python -m pytest -q
```

运行本地 smoke 测试：

```bash
pytest -q tests/test_smoke.py
```

运行完成后，`conftest.py` 会自动生成 Allure 结果和 HTML 报告。

也可以使用快捷脚本：

```bash
python scripts/run_allure.py
```

## GitHub Actions 运行

GitHub Actions 配置文件：

```text
.github/workflows/api-test.yml
```

当前 CI 执行命令：

```bash
pytest -q
```

需要在 GitHub 仓库的 `Settings -> Secrets and variables -> Actions` 中配置以下 Secrets：

```text
SEAHOT_TOKEN
TEST_ACCOUNT_ID
TEST_CHARACTER_ID
TEST_FCM_TOKEN
```

手动运行步骤：

1. 打开 GitHub 仓库
2. 进入 `Actions`
3. 左侧选择 `API Tests`
4. 点击右侧 `Run workflow`
5. Branch 选择 `main`
6. 点击绿色的 `Run workflow`

运行成功后，页面会显示绿色对勾，`api-test` job 和 `Run API tests` step 都应为 success。

## 查看 Allure 报告

本地报告目录：

```text
reports/allure-results/latest
reports/allure-results/时间戳
reports/allure-html/latest/index.html
reports/allure-html/时间戳/index.html
```

如果本机安装了 Allure CLI，项目会直接使用 `allure generate` 生成 HTML 报告。

如果没有 Allure CLI，但安装了 Node.js/npx，项目会自动使用：

```bash
npx --yes allure-commandline generate ...
```

查看本地报告时，建议在 `reports/allure-html/latest` 目录启动 HTTP 服务：

```bash
cd reports/allure-html/latest
python3 -m http.server 8080
```

然后浏览器打开：

```text
http://localhost:8080
```

不要直接双击 `index.html`。Allure 页面需要加载 `data/`、`widgets/` 等 JSON 文件，直接打开本地文件可能出现 `500 Failed to fetch`。

GitHub Actions 报告查看方式：

1. 打开某一次 Actions run
2. 滚动到 `Artifacts`
3. 下载 `allure-html-report`
4. 解压 zip
5. 在解压后的 `index.html` 所在目录启动 HTTP 服务
6. 浏览器访问本地服务地址

## 目录结构

```text
.
├── .github/
│   └── workflows/
│       └── api-test.yml          # GitHub Actions CI 配置
├── scripts/
│   └── run_allure.py             # 本地运行 pytest 的快捷脚本
├── tests/
│   ├── test_api.py               # 真实接口自动化用例
│   └── test_smoke.py             # 不依赖 token 的本地 smoke 测试
├── client.py                     # APIClient，请求封装、header、timeout、retry
├── config.py                     # 测试数据配置读取
├── conftest.py                   # pytest hook，生成 Allure HTML 报告
├── schemas.py                    # 各接口响应 schema 定义
├── schema_validator.py           # 自定义响应结构校验器
├── pytest.ini                    # pytest 配置和 Allure 原始结果目录
├── requirements.txt              # Python 依赖
├── STABLE_APIS.md                # 稳定接口清单
├── local_config.py               # 本地私有配置，不提交 GitHub
└── reports/                      # 本地测试报告目录，不提交 GitHub
```

## 新增接口用例

在 `tests/test_api.py` 的参数列表中新增一组数据：

```python
(
    "接口名称",
    "/api/path",
    {"请求参数": "值"},
    RESPONSE_SCHEMA,
)
```

如果接口返回结构是新的，先在 `schemas.py` 中定义 schema，再在用例中引用。

通用响应校验由 `schema_validator.py` 完成，支持：

- dict 字段校验
- list 元素校验
- 多类型字段，例如 `(str, type(None))`
- 可选字段，例如 `"avatar?": str`
- 固定值校验，例如 `"code": 10000`
