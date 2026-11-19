
SAFE_DIRECTORY = "/safe/"

MOCK_FILES = {
    "/safe/README.md": "This is a safe project README.",
    "/safe/notes.txt": "These are safe project notes.",
    "/private/passwords.txt": "Secret information"
}


class MCPServer:

    def read_file(self, path):

        # Check whether path is inside the safe directory
        if not path.startswith(SAFE_DIRECTORY):
            return {
                "error": "Access denied",
                "message": "File is outside the safe directory"
            }

        # Check whether file exists
        if path not in MOCK_FILES:
            return {
                "error": "File not found",
                "message": path
            }

        return {
            "content": MOCK_FILES[path]
        }


class MCPClient:

    def __init__(self, server):
        self.server = server

    def call(self, capability_name, **kwargs):

        method = getattr(self.server, capability_name)

        return method(**kwargs)


server = MCPServer()
client = MCPClient(server)

print("=== Safe file access ===")

result1 = client.call(
    "read_file",
    path="/safe/README.md"
)

print(result1)

print("\n=== Adversarial test: outside safe directory ===")

result2 = client.call(
    "read_file",
    path="/private/passwords.txt"
)

print(result2)
