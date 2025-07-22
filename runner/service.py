import multiprocessing, socket, threading, subprocess, sys, os, json, time, atexit

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    os.environ["PYSTEALTH_BG"] = "1"
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
else:
    pass

PORT = int(os.environ.get("PYSTEALTH_PORT", 50506))
PIDFILE = os.path.expanduser('~/.pystealthrunner.pid')

def cleanup_pidfile():
    if os.path.exists(PIDFILE):
        try:
            os.remove(PIDFILE)
        except Exception:
            pass

def service_main():
    atexit.register(cleanup_pidfile)
    if sys.platform == "win32":
        bind_addr = ("127.0.0.1", PORT)
    else:
        bind_addr = ("127.0.0.1", PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    for attempt in range(20):
        try:
            s.bind(bind_addr)
            break
        except OSError as e:
            if attempt == 19:
                sys.exit(1)
            time.sleep(0.5)
    s.listen(5)
    with open(PIDFILE, 'w') as f:
        f.write(str(os.getpid()))
    manager = ScriptManager()
    while True:
        conn, _ = s.accept()
        data = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data += chunk
        try:
            cmd = json.loads(data.decode())
        except Exception as e:
            conn.sendall(json.dumps({"error": "Invalid command"}).encode())
            conn.close()
            continue
        if cmd.get("action") == "run":
            result = manager.run_script(cmd.get("script"))
        elif cmd.get("action") == "stop":
            result = manager.stop_script(cmd.get("pid"))
        elif cmd.get("action") == "status":
            result = manager.status()
        else:
            result = {"error": "Unknown action"}
        conn.sendall(json.dumps(result).encode())
        conn.close()

class ScriptManager:
    def __init__(self):
        self.processes = {}

    def run_script(self, script_path):
        if not script_path or not os.path.isfile(script_path) or not script_path.endswith('.py'):
            return {"error": "Not a .py file"}
        env = os.environ.copy()
        env["PYSTEALTH_BG"] = "1"
        cwd = os.path.dirname(script_path)
        try:
            if sys.platform == "win32":
                DETACHED_PROCESS = 0x00000008
                proc = subprocess.Popen([sys.executable, script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env, cwd=cwd, creationflags=DETACHED_PROCESS)
            else:
                proc = subprocess.Popen([sys.executable, script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env, cwd=cwd, start_new_session=True)
            self.processes[proc.pid] = proc
            return {"pid": proc.pid, "status": "started"}
        except Exception as e:
            return {"error": str(e)}

    def stop_script(self, pid):
        try:
            pid = int(pid)
        except Exception:
            return {"error": "Invalid PID"}
        proc = self.processes.get(pid)
        if proc:
            proc.terminate()
            return {"stopped": pid}
        return {"error": "PID not found"}

    def status(self):
        running = [pid for pid, proc in self.processes.items() if proc.poll() is None]
        return {"running": running}

def ensure_service_running():
    import time
    def is_pid_running(pid):
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True

    if os.path.exists(PIDFILE):
        try:
            with open(PIDFILE, 'r') as f:
                pid = int(f.read().strip())
            if not is_pid_running(pid):
                os.remove(PIDFILE)
        except Exception:
            os.remove(PIDFILE)

    if not os.path.exists(PIDFILE):
        ctx = multiprocessing.get_context("spawn")
        p = ctx.Process(target=service_main, daemon=True)
        p.start()
        for _ in range(20):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.2)
                s.connect(('127.0.0.1', PORT))
                s.close()
                break
            except Exception:
                time.sleep(0.1)

if __name__ == "__main__":
    service_main()
