from datetime import datetime
from pathlib import Path
import shutil
import subprocess

import pytest


ROOT_DIR = Path(__file__).resolve().parent
REPORT_DIR = ROOT_DIR / "reports"
ALLURE_RESULTS_DIR = REPORT_DIR / "allure-results"
ALLURE_HTML_DIR = REPORT_DIR / "allure-html"


def build_allure_generate_command(results_dir, html_dir):
    allure_command = shutil.which("allure")
    if allure_command is not None:
        return [
            allure_command,
            "generate",
            str(results_dir),
            "-o",
            str(html_dir),
            "--clean",
        ]

    npx_command = shutil.which("npx")
    if npx_command is not None:
        # 如果没有安装 Allure CLI，就用 npx 临时调用 allure-commandline。
        return [
            npx_command,
            "--yes",
            "allure-commandline",
            "generate",
            str(results_dir),
            "-o",
            str(html_dir),
            "--clean",
        ]

    return None


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    report_dir = session.config.option.allure_report_dir
    if not report_dir:
        return

    results_dir = Path(report_dir)
    if not results_dir.is_absolute():
        results_dir = ROOT_DIR / results_dir

    if not results_dir.exists():
        print("\n没有找到 Allure 原始结果目录，跳过 HTML 报告生成。")
        return

    run_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    archived_results_dir = ALLURE_RESULTS_DIR / run_time
    html_dir = ALLURE_HTML_DIR / run_time
    latest_html_dir = ALLURE_HTML_DIR / "latest"

    # pytest.ini 中的 latest results 每次会被覆盖；这里再复制一份带时间戳的原始结果。
    if results_dir.resolve() != archived_results_dir.resolve():
        if archived_results_dir.exists():
            shutil.rmtree(archived_results_dir)
        shutil.copytree(results_dir, archived_results_dir)

    command = build_allure_generate_command(results_dir, html_dir)
    if command is None:
        print("\n没有找到 allure 或 npx，已保留 Allure 原始结果:")
        print(results_dir)
        print("安装 Allure CLI 后可以执行: brew install allure")
        return

    result = subprocess.run(command, cwd=ROOT_DIR)
    if result.returncode != 0:
        print("\nAllure HTML 报告生成失败，原始结果保留在:")
        print(results_dir)
        return

    if latest_html_dir.exists():
        shutil.rmtree(latest_html_dir)
    shutil.copytree(html_dir, latest_html_dir)

    print("\nAllure HTML 报告已生成:")
    print(html_dir / "index.html")
    print("最近一次报告:")
    print(latest_html_dir / "index.html")
