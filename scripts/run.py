import os
import subprocess
import webbrowser
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

USER_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = USER_DIR.parents[1]

LABEL_STUDIO_DATA_DIR = USER_DIR / "label_studio_data"
DOCS_DIR = PROJECT_ROOT / "docs"

HOST = "127.0.0.1"
PORT = "8080"


def wait_for_label_studio(base_url, process, timeout_seconds=90, check_interval=1):
    """
    Wait until Label Studio is actually ready before opening the browser.

    Uses the /health endpoint when available.
    """

    health_url = f"{base_url}/health"

    print("Waiting for Label Studio to start...")
    print(f"Checking: {health_url}")

    start_time = time.time()
    last_error = None

    while time.time() - start_time < timeout_seconds:
        # If the process exited, fail early.
        if process.poll() is not None:
            raise RuntimeError(
                "Label Studio exited before it became available. "
                "Check the terminal output above for errors."
            )

        try:
            request = Request(
                health_url,
                headers={
                    "User-Agent": "LabelStudioLocalRunner/1.0",
                    "Cache-Control": "no-cache",
                },
            )

            with urlopen(request, timeout=3) as response:
                status = response.getcode()

                if status == 200:
                    print("Label Studio is ready.")
                    return

        except HTTPError as e:
            last_error = f"HTTPError {e.code}"
        except URLError as e:
            last_error = f"URLError {e.reason}"
        except TimeoutError as e:
            last_error = f"TimeoutError {e}"
        except Exception as e:
            last_error = repr(e)

        time.sleep(check_interval)

    raise TimeoutError(
        f"Timed out waiting for Label Studio to start at {base_url} "
        f"after {timeout_seconds} seconds. Last error: {last_error}"
    )


def main():
    if not LABEL_STUDIO_DATA_DIR.exists():
        raise RuntimeError(
            f"Label Studio data directory does not exist:\n"
            f"{LABEL_STUDIO_DATA_DIR}\n\n"
            "Ask the project coordinator to prepare your annotation project."
        )

    env = os.environ.copy()
    env["LABEL_STUDIO_BASE_DATA_DIR"] = str(LABEL_STUDIO_DATA_DIR)

    url = f"http://{HOST}:{PORT}"

    print("Starting Label Studio...")
    print(f"Using data directory: {LABEL_STUDIO_DATA_DIR}")
    print(f"URL: {url}")

    process = subprocess.Popen(
        [
            "label-studio",
            "start",
            "--host",
            HOST,
            "--port",
            PORT,
        ],
        env=env,
    )

    try:
        wait_for_label_studio(url, process, timeout_seconds=5*60)

        print(f"Opening browser: {url}")
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Could not open browser automatically: {e}")
            print(f"Please open this URL manually: {url}")

        print()
        print("Label Studio is running.")
        print("Press Ctrl+C in this terminal to stop it.")

        process.wait()

    except KeyboardInterrupt:
        print("Stopping Label Studio...")
        process.terminate()

    finally:
        if process.poll() is None:
            process.terminate()


if __name__ == "__main__":
    main()