import os
import sys
import inspect
from .service import ensure_service_running
from .comms import send_command
from .audit import check_consent

class Runner:
    def __init__(self):
        check_consent()
        ensure_service_running()

    def run_script(self, script_path=None):
        if os.environ.get("PYSTEALTH_BG") == "1":
            return
        if script_path is None:
            # Find the outermost script with __name__ == '__main__'
            frame = inspect.currentframe()
            main_script = None
            while frame:
                if frame.f_globals.get("__name__") == "__main__":
                    filename = frame.f_globals.get("__file__")
                    if filename and filename.endswith('.py') and os.path.isfile(filename):
                        main_script = os.path.abspath(filename)
                frame = frame.f_back
            if not main_script:
                raise RuntimeError("Could not determine script file to run in background.")
            script_path = main_script
        if not script_path or not script_path.endswith('.py') or not os.path.isfile(script_path):
            raise RuntimeError(f"Background execution target is not a .py file: {script_path}")
        abs_path = os.path.abspath(script_path)
        result = send_command({"action": "run", "script": abs_path})
        return result.get("pid")

    def stop_script(self, pid):
        return send_command({"action": "stop", "pid": pid})

    def status(self):
        return send_command({"action": "status"})
