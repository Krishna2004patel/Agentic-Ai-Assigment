
# Mock files
MOCK_FILES = {
    "README.md": "Agentic AI Systems demo.",
    "notes.txt": "This is a project notes file.",
    "report.txt": "This is the final project report."
}

# Add the fourth capability
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
    },
    {
        "name": "list_files",
        "kind": "resource",
        "input": {},
        "output": {"files": "list"}
    }
]


class MCPServer:

    def list_capabilities(self):
        return CAPABILITIES

    def read_file(self, path):
        if path not in MOCK_FILES:
            return {"error": "file not found"}

        return {"content": MOCK_FILES[path]}

    def list_files(self):
        return {"files": list(MOCK_FILES.keys())}


class MCPClient:

    def __init__(self, server):
        self.server = server

    def discover(self):
        return self.server.list_capabilities()

    def call(self, capability_name, **kwargs):

        manifest = {
            c["name"]: c for c in self.discover()
        }

        if capability_name not in manifest:
            raise ValueError("Unknown capability")

        method = getattr(self.server, capability_name)

        return method(**kwargs)


server = MCPServer()
client = MCPClient(server)

print("=== Capability discovery ===")

for capability in client.discover():
    print(
        capability["name"],
        "(" + capability["kind"] + ")"
    )

print("\n=== Calling list_files ===")

result = client.call("list_files")

print(result)
