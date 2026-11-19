
import sqlite3

# Create an in-memory SQLite database
conn = sqlite3.connect(":memory:")

conn.execute("CREATE TABLE signups (event TEXT, count INTEGER)")

conn.executemany(
    "INSERT INTO signups VALUES (?, ?)",
    [
        ("AI Club Talk", 12),
        ("Hackathon Kickoff", 9),
        ("Robotics Demo", 15)
    ]
)

conn.commit()

# Mock file and API data
MOCK_FILES = {
    "README.md": "Agentic AI Systems - mini MCP server demo."
}

MOCK_API = {
    "events_today": ["AI Club Talk", "Robotics Demo"]
}

# Available capabilities
CAPABILITIES = [
    {
        "name": "read_file",
        "kind": "resource",
        "input": {"path": "str"},
        "output": {"content": "str"}
    },
    {
        "name": "query_db",
        "kind": "tool",
        "input": {"sql": "str"},
        "output": {"rows": "list"}
    },
    {
        "name": "call_api",
        "kind": "tool",
        "input": {"endpoint": "str"},
        "output": {"data": "any"}
    }
]

ALLOWED_CALLERS = {"planning_agent"}


class MCPServer:

    def list_capabilities(self):
        return CAPABILITIES

    def read_file(self, path):
        if path not in MOCK_FILES:
            return {"error": f"file not found: {path}"}

        return {"content": MOCK_FILES[path]}

    def query_db(self, sql, caller):

        if caller not in ALLOWED_CALLERS:
            return {
                "error": f"caller '{caller}' is not permitted to use query_db"
            }

        if not sql.strip().upper().startswith("SELECT"):
            return {
                "error": "only SELECT statements are permitted through this tool"
            }

        cur = conn.execute(sql)

        return {"rows": cur.fetchall()}

    def call_api(self, endpoint):
        if endpoint not in MOCK_API:
            return {"error": f"unknown endpoint: {endpoint}"}

        return {"data": MOCK_API[endpoint]}


class MCPClient:

    def __init__(self, server, caller_name):
        self.server = server
        self.caller_name = caller_name

    def discover(self):
        return self.server.list_capabilities()

    def call(self, capability_name, **kwargs):

        manifest = {
            c["name"]: c for c in self.discover()
        }

        if capability_name not in manifest:
            raise ValueError(
                f"unknown capability: {capability_name}"
            )

        method = getattr(self.server, capability_name)

        if capability_name == "query_db":
            return method(
                caller=self.caller_name,
                **kwargs
            )

        return method(**kwargs)


if __name__ == "__main__":

    server = MCPServer()

    client = MCPClient(
        server,
        caller_name="planning_agent"
    )

    print("=== Capability discovery ===")

    for c in client.discover():
        print(
            f" {c['name']} ({c['kind']}) "
            f"input={c['input']} output={c['output']}"
        )

    print("\n=== Call 1: read_file ===")
    print(
        client.call(
            "read_file",
            path="README.md"
        )
    )

    print("\n=== Call 2: query_db ===")
    print(
        client.call(
            "query_db",
            sql="SELECT event, count FROM signups"
        )
    )

    print("\n=== Call 3: call_api ===")
    print(
        client.call(
            "call_api",
            endpoint="events_today"
        )
    )

    print("\n=== Rejection path: disallowed statement ===")
    print(
        client.call(
            "query_db",
            sql="DELETE FROM signups"
        )
    )

    print("\n=== Rejection path: disallowed caller ===")

    other_client = MCPClient(
        server,
        caller_name="unregistered_agent"
    )

    print(
        other_client.call(
            "query_db",
            sql="SELECT * FROM signups"
        )
    )
