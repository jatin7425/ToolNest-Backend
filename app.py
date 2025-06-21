import os
import sys
import subprocess
import platform
import shutil
import socket
from django.core.management import execute_from_command_line

worker_name = f"worker_{socket.gethostname()}"


def is_redis_running():
    try:
        result = subprocess.run(["redis-cli", "ping"], capture_output=True, text=True)
        return result.stdout.strip() == "PONG"
    except FileNotFoundError:
        return False


def is_redis_installed():
    return shutil.which("redis-server") is not None


def install_redis_linux():
    print("📦 Installing Redis via apt (Ubuntu/Debian)...")
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo", "apt", "install", "-y", "redis-server"])


def install_redis_macos():
    print("🍎 Installing Redis via Homebrew (macOS)...")
    subprocess.run(["brew", "update"])
    subprocess.run(["brew", "install", "redis"])


def install_redis_windows():
    print("🪟 Installing Redis via Chocolatey (Windows)...")
    subprocess.run(["choco", "install", "redis-64", "-y"])


def start_redis_server():
    print("🔄 Starting Redis server...")
    subprocess.Popen(["redis-server"])


def setup_redis():
    if is_redis_running():
        print("✅ Redis is already running.")
        return

    if not is_redis_installed():
        os_type = platform.system().lower()

        if os_type == "linux":
            install_redis_linux()
        elif os_type == "darwin":
            install_redis_macos()
        elif os_type == "windows":
            install_redis_windows()
        else:
            print(f"❌ Unsupported OS: {os_type}")
            sys.exit(1)

    # Start Redis if installed
    start_redis_server()


def start_celery():
    print("🚀 Starting Celery worker...")
    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "celery",
            "-A",
            "toolnest_backend",
            "worker",
            "-n",
            worker_name,
            "--loglevel=info",
        ]
    )


def start_celery_beat():
    print("🕒 Starting Celery Beat...")
    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "celery",
            "-A",
            "toolnest_backend",
            "beat",
            "--loglevel=info",
        ]
    )


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolnest_backend.settings")

    # Step 1: Ensure Redis is up
    setup_redis()

    # Step 2: Launch Celery
    start_celery()
    # Optional: start_celery_beat()

    # Step 3: Run Django server
    if len(sys.argv) == 1:
        sys.argv += ["runserver", "0.0.0.0:8000"]

    print("🧩 Starting Django server...")
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
