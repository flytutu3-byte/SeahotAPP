import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def main():
    # pytest.ini 已经配置了 Allure 原始结果目录；
    # conftest.py 会在 pytest 结束后自动生成 HTML 报告。
    return subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=ROOT_DIR).returncode


if __name__ == "__main__":
    raise SystemExit(main())
