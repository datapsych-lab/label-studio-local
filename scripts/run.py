import os
import subprocess
import webbrowser
import time
from pathlib import Path

USER_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = USER_DIR.parents[1]

LABEL_STUDIO_DATA_DIR = USER_DIR / "label_studio_data"
DOCS_DIR = PROJECT_ROOT / "docs"

HOST = "127.0.0.1"
PORT = "8080"

def main():
    if not LABEL_STUDIO_DATA_DIR.exists():
        raise RuntimeError(
            f"Label Studio data directory does not exist:\n"
            f"{LABEL_STUDIO_DATA_DIR}\n\n"
            "Ask the project coordinator to prepare your annotation project."
        )

    if not DOCS_DIR.exists():
        raise RuntimeError(f"Docs directory does not exist: {DOCS_DIR}")

    env = os.environ.copy()
    env["LABEL_STUDIO_BASE_DATA_DIR"] = str(LABEL_STUDIO_DATA_DIR)

    # Required for file-based tasks
    env["LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED"] = "true"
    env["LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT"] = str(DOCS_DIR)

    url = f"http://{HOST}:{PORT}"

    print("Starting Label Studio...")
    print(f"Using data directory: {LABEL_STUDIO_DATA_DIR}")
    print(f"Using docs directory: {DOCS_DIR}")
    print(f"Opening: {url}")

    process = subprocess.Popen(
        [
            "label-studio",
            "start",
            "--host",
            HOST,
            "--port",
            PORT
        ],
        env=env
    )

    time.sleep(5)

    try:
        webbrowser.open(url)
    except Exception:
        pass

    print()
    print("Label Studio is running.")
    print("Press Ctrl+C in this terminal to stop it.")

    try:
        process.wait()
    except KeyboardInterrupt:
        print("Stopping Label Studio...")
        process.terminate()

if __name__ == "__main__":
    main()