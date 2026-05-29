# Kali Linux Installer Troubleshooting Guide

When a Kali Linux installation step fails, the system provides several virtual consoles and diagnostic options to identify, debug, and recover from the error.

---

## 1. Virtual Console Navigation

The installer runs across multiple background workspaces. Switch between them using key combinations to gather intelligence on why the process stopped:

* **Main Interface (`Ctrl + Alt + F5` or `Ctrl + Alt + F1`)**
  Hosts the graphical framework (F5) or classic text interface (F1) where you interact with user prompts.
* **System Event Log (`Ctrl + Alt + F4`)**
  Prints real-time low-level deployment text. This terminal reveals definitive, explicit causes for abrupt halts, such as critical network timeouts, corrupt archives, or fully depleted storage partitions.
* **Investigation Shells (`Ctrl + Alt + F2` or `Ctrl + Alt + F3`)**
  Provides interactive console interfaces running a condensed BusyBox terminal utility suite to query the underlying environment.

---

## 2. Diagnostic Actions Inside the Shell

When analyzing the installation environment via the `Ctrl + Alt + F2` or `Ctrl + Alt + F3` terminals, use the following operational strategies:

* **Verify System Variables**
  Use `debconf-get` and `debconf-set` tools to inspect or manually override configuration properties within the installer's active runtime database.
* **Analyze Error Files**
  Evaluate installation diagnostic markers inside `/var/log/syslog` using standard text-viewing applications like `cat`, `less`, or line-editors like `nano`.
* **Examine Target Storage**
  After disk slicing and partition phases finish, browse or tweak the target Operating System disk layout directly at the `/target` path mount boundary.
* **Extract Remote Assets**
  Once physical link layers are up, use basic binary network wrappers like `wget` or `nc` (Netcat) to copy configuration payloads or export specific state files across your local subnet.

---

## 3. Recovery and Step Retries

If you correct the root problem using an investigation shell, you can resume your progress:

1. Select **Continue** on the main failure window alert to route back to the system's structured **Main Menu**.
2. Manually trigger the specific installation node item that previously threw an error to re-execute it.

---

## 4. Exporting Debug Logs via Web Server

If an unresolvable breakdown occurs and you need to build an external diagnostic package, export logs using the integrated helper utilities:

1. Navigate the primary installer menu interfaces to select the **Save debug logs** instruction set.
2. Instruct the utility tool to host an ad-hoc local network service instance.
3. Access the generated local URL through a separate computer web browser on the same broadcast network domain to instantly package and download internal logs, system states, and captured setup screenshots.
