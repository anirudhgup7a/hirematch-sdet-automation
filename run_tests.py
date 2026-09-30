"""
HireMatch SDET Automation — Master Test Suite Runner
────────────────────────────────────────────────────
Convenient CLI runner to execute various test suites, generate HTML reports,
and validate test readiness across all test layers.

Usage:
    python run_tests.py --suite api
    python run_tests.py --suite db
    python run_tests.py --suite ui --browser chromium
    python run_tests.py --suite smoke
    python run_tests.py --suite all
    python run_tests.py --suite perf
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
REPORTS_DIR = ROOT_DIR / "reports"

def ensure_reports_dir():
    REPORTS_DIR.mkdir(exist_ok=True)

def run_command(cmd_list, env=None):
    print(f"\n🚀 Running: {' '.join(cmd_list)}")
    print("=" * 60)
    current_env = os.environ.copy()
    if env:
        current_env.update(env)
    current_env["PYTHONPATH"] = str(ROOT_DIR)
    
    result = subprocess.run(cmd_list, cwd=str(ROOT_DIR), env=current_env)
    return result.returncode

def main():
    parser = argparse.ArgumentParser(description="HireMatch SDET Test Suite Runner")
    parser.add_argument(
        "--suite",
        choices=["api", "db", "ui", "smoke", "regression", "perf", "all"],
        default="api",
        help="Test suite category to execute"
    )
    parser.add_argument(
        "--html",
        action="store_true",
        default=True,
        help="Generate self-contained HTML test report"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        default=True,
        help="Run UI tests in headless browser mode"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Parallel test workers (xdist)"
    )

    args = parser.parse_args()
    ensure_reports_dir()

    report_file = REPORTS_DIR / f"{args.suite}_report.html"

    if args.suite == "perf":
        print("\n⚡ Launching Locust Performance Test Suite...")
        cmd = [
            sys.executable, "-m", "locust",
            "-f", "tests/performance/locustfile.py",
            "--headless",
            "-u", "10",
            "-r", "2",
            "-t", "20s",
            "--host", "http://127.0.0.1:8000",
            "--html", str(REPORTS_DIR / "locust_report.html")
        ]
        return sys.exit(run_command(cmd))

    # Pytest execution
    pytest_cmd = [sys.executable, "-m", "pytest"]

    if args.suite == "api":
        pytest_cmd.extend(["tests/api", "-m", "api"])
    elif args.suite == "db":
        pytest_cmd.extend(["tests/db"])
    elif args.suite == "ui":
        pytest_cmd.extend(["tests/ui", "-m", "ui"])
    elif args.suite == "smoke":
        pytest_cmd.extend(["tests", "-m", "smoke"])
    elif args.suite == "regression":
        pytest_cmd.extend(["tests", "-m", "regression"])
    elif args.suite == "all":
        pytest_cmd.extend(["tests"])

    if args.html:
        pytest_cmd.extend([f"--html={report_file}", "--self-contained-html"])

    if args.workers > 1:
        pytest_cmd.extend(["-n", str(args.workers)])

    exit_code = run_command(pytest_cmd)

    if exit_code == 0:
        print(f"\n✅ Test Suite '{args.suite}' PASSED! Report generated at: {report_file}")
    else:
        print(f"\n❌ Test Suite '{args.suite}' FAILED with exit code {exit_code}. See report: {report_file}")

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
