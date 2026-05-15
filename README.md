================================================================================
                    INTERACTIVE HTTP REQUEST TOOL
                              httpreq.py
================================================================================

OVERVIEW
--------
An interactive command-line tool for building, editing, and executing HTTP 
requests. Perfect for API testing and debugging without leaving the terminal.

FEATURES
--------
• Interactive command-line interface with history
• Build requests with method, URL, headers, and body
• Execute requests and view responses
• Edit requests between executions
• Command history saved to ~/.httpreq_history
• Pretty-print JSON responses
• Arrow keys to navigate command history

INSTALLATION
------------
1. Ensure Python 3.6+ is installed
2. Install required dependencies:
   
   pip install requests prompt-toolkit

3. Make the script executable (optional):
   
   chmod +x httpreq.py

RUNNING THE TOOL
----------------
Start the tool by running:

   python3 httpreq.py

You'll see the interactive prompt:

   httpreq> 

COMMANDS
--------

BASIC COMMANDS:
---------------

display
  Display the current request with method, URL, headers, and body.
  Shows the current state before each input prompt.

execute
  Send the HTTP request. Shows response status, headers, and body.
  JSON responses are pretty-printed for readability.

quit / exit
  Exit the tool.

REQUEST BUILDING:
-----------------

method <METHOD>
  Set the HTTP method.
  Examples:
    httpreq> method GET
    httpreq> method POST
    httpreq> method PUT
    httpreq> method DELETE
    httpreq> method PATCH

url <URL>
  Set the request URL.
  Examples:
    httpreq> url http://localhost:8080/api/chat
    httpreq> url https://api.example.com/v1/completions

header <Key: Value>
  Add or modify a header. Use exact format with colon and space.
  Examples:
    httpreq> header Authorization: Bearer token123
    httpreq> header Content-Type: application/json
    httpreq> header X-Custom-Header: value

body
  Enter request body. Interactive multi-line editor.
  Type '.' on a new line by itself to finish editing.
  Example session:
    httpreq> body
    Enter body (type '.' on a new line to finish):
    {"messages": [{"role": "user", "content": "hello"}]}
    .
    ✓ Body updated

EDITING:
--------

show
  Display the current request in raw text format.
  Useful for reviewing the complete request structure.

edit
  Enter a raw request editor. Build the entire request in text format:
  
  Format:
    METHOD URL
    Header1: Value1
    Header2: Value2
    
    Request body here (optional)
  
  Type '.' on a new line to finish.
  
  Example:
    httpreq> edit
    Enter request (format: METHOD URL, then headers, blank line, then body):
    Type '.' alone on a line to finish:
    POST http://localhost:8080/api/chat
    Authorization: Bearer sk-123
    Content-Type: application/json
    
    {"messages": [{"role": "user", "content": "What is 2+2?"}]}
    .

clear
  Reset the request to default values (GET http://localhost:8080).

USAGE EXAMPLES
--------------

EXAMPLE 1: Simple GET Request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ python3 httpreq.py
httpreq> method GET
✓ Method set to GET
httpreq> url https://api.github.com/repos/torvalds/linux
✓ URL set to https://api.github.com/repos/torvalds/linux
httpreq> execute
→ Sending GET request to https://api.github.com/repos/torvalds/linux...
← Response: 200
...


EXAMPLE 2: POST with JSON Body
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
httpreq> method POST
✓ Method set to POST
httpreq> url http://localhost:8000/api/chat
✓ URL set to http://localhost:8000/api/chat
httpreq> header Content-Type: application/json
✓ Header added: Content-Type: application/json
httpreq> header Authorization: Bearer my-token
✓ Header added: Authorization: Bearer my-token
httpreq> body
Enter body (type '.' on a new line to finish):
{"messages": [{"role": "user", "content": "Hello"}]}
.
✓ Body updated
httpreq> execute
→ Sending POST request to http://localhost:8000/api/chat...
← Response: 200
Headers:
  Content-Type: application/json
  ...
Body:
{
  "response": "Hi there!",
  "tokens": 15
}


EXAMPLE 3: Editing Complex Requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
httpreq> edit
Enter request (format: METHOD URL, then headers, blank line, then body):
Type '.' alone on a line to finish:
PUT http://localhost:8000/api/users/123
Authorization: Bearer token
Content-Type: application/json

{"name": "John", "email": "john@example.com"}
.
✓ Request parsed
httpreq> execute


EXAMPLE 4: Using Command History
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use UP/DOWN arrow keys to navigate through previous commands.
Previous requests are saved automatically in ~/.httpreq_history.

httpreq> [UP arrow] - recalls last command
httpreq> [UP arrow] - recalls previous command
etc.


TIPS & TRICKS
-------------

1. QUICK ITERATION
   Use arrow keys to quickly recall and modify previous commands.
   Edit the URL or body slightly and re-execute.

2. HEADER SHORTCUTS
   Store common headers as commands:
     header Authorization: Bearer <your-token>
     header Content-Type: application/json

3. JSON FORMATTING
   When entering body via 'body' command, you can enter multi-line JSON
   for better readability. It's automatically handled.

4. RESPONSE VIEWING
   JSON responses are automatically pretty-printed.
   Large responses are truncated to 500 characters for plain text.

5. DEBUGGING
   Use 'show' command to verify your request before executing:
     httpreq> show
     httpreq> execute

6. CLEARING STATE
   Start fresh with a new request:
     httpreq> clear
     httpreq> method POST
     ... build new request ...

TROUBLESHOOTING
---------------

ERROR: "Unknown command"
  → Check spelling. Command names are lowercase.

ERROR: "Format: header <Key: Value>"
  → Headers must have a colon and space. Example: "Authorization: Bearer token"

ERROR: Timeout or connection refused
  → Check the URL is correct and the server is running.

ERROR: JSON parsing errors in response
  → Response is displayed as plain text if not valid JSON.

HISTORY FILE
------------
Command history is automatically saved to:
  ~/.httpreq_history

This file is preserved between sessions, so you can recall previous commands
and requests.

To clear history:
  rm ~/.httpreq_history

REQUIREMENTS
------------
• Python 3.6+
• requests library
• prompt-toolkit library

Install with:
  pip install requests prompt-toolkit

KEYBOARD SHORTCUTS
------------------
UP/DOWN ARROW    - Navigate command history
CTRL+C           - Exit (gracefully)
CTRL+A           - Move to start of line
CTRL+E           - Move to end of line

DEFAULT VALUES
--------------
When you start the tool, the default request is:
  Method:  GET
  URL:     http://localhost:8080
  Headers: (none)
  Body:    (empty)

================================================================================
For questions or issues, check the command list with: help
Happy testing!
================================================================================
