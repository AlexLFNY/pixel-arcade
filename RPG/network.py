# network.py — handles all networking for both server and client roles.
# Used by main.py; do not run directly.

import socket
import threading
import json

PORT = 5000


class Network:
    """
    Single class that works as either a server or a client.

    Server usage (Machine A):
        net = Network("server")
        net.set_obstacles(obstacle)   # call once after generating obstacles
        keys = net.get_remote_keys()  # call each frame to get P2 inputs
        net.push_state(state)         # call each frame to send game state

    Client usage (Machine B):
        net = Network("client", "192.168.x.x")
        net.push_keys(keys)           # call each frame to send local inputs
        state = net.get_state()       # call each frame to get latest game state
        obs   = net.get_obstacles()   # call once when non-empty to get obstacles
    """

    def __init__(self, role, server_ip=None):
        self.role      = role        # "server" or "client"
        self.connected = False
        self._lock     = threading.Lock()

        if role == "server":
            self._remote_keys       = {"up": False, "down": False,
                                       "left": False, "right": False}
            self._conn              = None
            self._pending_obstacles = None
            t = threading.Thread(target=self._server_thread, daemon=True)

        else:  # client
            self._state     = {}
            self._obstacles = []
            self._sock      = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            t = threading.Thread(target=self._client_thread,
                                 args=(server_ip,), daemon=True)

        t.start()

    # ------------------------------------------------------------------ server
    def set_obstacles(self, obstacles):
        """Server: share the obstacle layout with the client on first connect."""
        self._pending_obstacles = obstacles

    def get_remote_keys(self):
        """Server: return latest key states received from the client."""
        with self._lock:
            return dict(self._remote_keys)

    def push_state(self, state):
        """Server: send current game state to the client."""
        if self._conn is None:
            return
        try:
            self._conn.sendall((json.dumps(state) + "\n").encode())
        except Exception:
            self._conn = None

    # ------------------------------------------------------------------ client
    def push_keys(self, keys):
        """Client: send local key states to the server."""
        try:
            self._sock.sendall((json.dumps(keys) + "\n").encode())
        except Exception:
            pass

    def get_state(self):
        """Client: return latest game state received from the server (or None)."""
        with self._lock:
            return dict(self._state) if self._state else None

    def get_obstacles(self):
        """Client: return obstacle list once received from server (empty until then)."""
        with self._lock:
            return list(self._obstacles)

    # --------------------------------------------------------- background threads
    def _server_thread(self):
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("0.0.0.0", PORT))
        srv.listen(1)
        try:
            _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            _s.connect(("8.8.8.8", 80))
            local_ip = _s.getsockname()[0]
            _s.close()
        except Exception:
            local_ip = "unknown"
        print(f"[server] IP: {local_ip}  — Waiting for Player 2 on port {PORT} ...")
        conn, addr = srv.accept()
        print(f"[server] Player 2 connected from {addr}")
        self._conn     = conn
        self.connected = True

        # Send obstacles so both screens look identical
        if self._pending_obstacles is not None:
            conn.sendall(
                (json.dumps({"obstacles": self._pending_obstacles}) + "\n").encode()
            )

        buf = ""
        while True:
            try:
                data = conn.recv(256).decode()
                if not data:
                    break
                buf += data
                while "\n" in buf:
                    line, buf = buf.split("\n", 1)
                    if line:
                        keys = json.loads(line)
                        with self._lock:
                            self._remote_keys.update(keys)
            except Exception:
                break

    def _client_thread(self, server_ip):
        print(f"[client] Connecting to {server_ip}:{PORT} ...")
        try:
            self._sock.connect((server_ip, PORT))
            self.connected = True
            print("[client] Connected!")
        except Exception as e:
            print(f"[client] Connection failed: {e}")
            return

        buf = ""
        while True:
            try:
                data = self._sock.recv(4096).decode()
                if not data:
                    break
                buf += data
                while "\n" in buf:
                    line, buf = buf.split("\n", 1)
                    if not line:
                        continue
                    msg = json.loads(line)
                    with self._lock:
                        if "obstacles" in msg:
                            self._obstacles[:] = [tuple(o) for o in msg["obstacles"]]
                        else:
                            self._state.update(msg)
            except Exception:
                break
