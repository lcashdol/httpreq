#!/usr/bin/env python3
"""
Interactive HTTP Request Tool
Allows editing HTTP requests with arrow keys and executing them
"""

import requests
import json
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
import os

# Default history file
HISTORY_FILE = os.path.expanduser("~/.httpreq_history")

# Custom style for the prompt
style = Style.from_dict({
    'prompt': 'bg:#0066ff #ffffff bold',
    'method': 'bg:#00aa00 #ffffff bold',
})

class HTTPRequest:
    def __init__(self):
        self.method = "GET"
        self.url = "http://localhost:8080"
        self.headers = {}
        self.body = ""

    def display(self):
        """Display the current request"""
        print("\n" + "="*60)
        print(f"[{self.method}] {self.url}")
        print("="*60)
        if self.headers:
            print("\nHeaders:")
            for k, v in self.headers.items():
                print(f"  {k}: {v}")
        if self.body:
            print("\nBody:")
            print(f"  {self.body}")
        print("="*60 + "\n")

    def to_string(self):
        """Convert request to string representation"""
        lines = [f"{self.method} {self.url}"]
        for k, v in self.headers.items():
            lines.append(f"{k}: {v}")
        if self.body:
            lines.append("")
            lines.append(self.body)
        return "\n".join(lines)

    def from_string(self, text):
        """Parse request from string"""
        lines = text.strip().split("\n")
        if not lines:
            return

        # Parse request line
        parts = lines[0].split(" ", 1)
        if len(parts) == 2:
            self.method, self.url = parts
        else:
            self.url = parts[0]

        # Parse headers and body
        self.headers = {}
        self.body = ""
        body_start = None

        for i, line in enumerate(lines[1:], 1):
            if line == "":
                body_start = i + 1
                break
            if ": " in line:
                k, v = line.split(": ", 1)
                self.headers[k] = v

        if body_start:
            self.body = "\n".join(lines[body_start:])

def print_help():
    print("\n🌐 Interactive HTTP Request Tool")
    print("━" * 60)
    print("Commands:")
    print("  display       - Show current request")
    print("  execute       - Send the request")
    print("  method <M>    - Set HTTP method (GET, POST, etc.)")
    print("  url <U>       - Set URL")
    print("  header <K: V> - Add/modify header")
    print("  body          - Edit body (enter '.' on new line to finish)")
    print("  show          - Show request as text to edit")
    print("  edit          - Edit raw request text")
    print("  clear         - Clear request")
    print("  quit          - Exit")
    print("━" * 60)

def execute_request(req):
    """Execute the HTTP request"""
    try:
        print(f"\n→ Sending {req.method} request to {req.url}...")
        
        if req.body:
            try:
                body_data = json.loads(req.body)
            except:
                body_data = req.body
        else:
            body_data = None

        response = requests.request(
            method=req.method,
            url=req.url,
            headers=req.headers,
            data=body_data,
            timeout=10
        )

        print(f"← Response: {response.status_code}")
        print("\nHeaders:")
        for k, v in response.headers.items():
            print(f"  {k}: {v}")
        
        print("\nBody:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text[:500])
        
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Main interactive loop"""
    session = PromptSession(history=FileHistory(HISTORY_FILE))
    req = HTTPRequest()

    print_help()

    while True:
        try:
            req.display()
            user_input = session.prompt("httpreq> ").strip()

            if not user_input:
                continue

            cmd = user_input.split(" ", 1)
            command = cmd[0].lower()
            args = cmd[1] if len(cmd) > 1 else ""

            if command == "quit" or command == "exit":
                print("👋 Goodbye!")
                break

            elif command == "display":
                req.display()

            elif command == "execute":
                execute_request(req)
            
            elif command == "help":
                print_help()

            elif command == "method":
                req.method = args.upper()
                print(f"✓ Method set to {req.method}")

            elif command == "url":
                req.url = args
                print(f"✓ URL set to {req.url}")

            elif command == "header":
                if ": " in args:
                    k, v = args.split(": ", 1)
                    req.headers[k] = v
                    print(f"✓ Header added: {k}: {v}")
                else:
                    print("✗ Format: header <Key: Value>")

            elif command == "body":
                print("Enter body (type '.' on a new line to finish):")
                lines = []
                while True:
                    line = input()
                    if line == ".":
                        break
                    lines.append(line)
                req.body = "\n".join(lines)
                print("✓ Body updated")

            elif command == "show":
                print("\n" + req.to_string() + "\n")

            elif command == "edit":
                print("\nEnter request (format: METHOD URL, then headers, blank line, then body):")
                print("Type '.' alone on a line to finish:")
                lines = []
                while True:
                    try:
                        line = input()
                        if line == ".":
                            break
                        lines.append(line)
                    except EOFError:
                        break
                
                if lines:
                    req.from_string("\n".join(lines))
                    print("✓ Request parsed")

            elif command == "clear":
                req = HTTPRequest()
                print("✓ Request cleared")

            else:
                print(f"✗ Unknown command: {command}")

        except KeyboardInterrupt:
            print("\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"✗ Error: {e}")


if __name__ == "__main__":
    main()
