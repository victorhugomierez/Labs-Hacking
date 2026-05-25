# Network Concepts & the OSI Model

---

## Overview

Networking underpins virtually every piece of modern technology — from smartphones to smart televisions. At the heart of it all sits the **TCP/IP stack**, upon which the entire contemporary technology ecosystem has been built. To make sense of how networks function, engineers use two key reference models: the **OSI Model** and the **TCP/IP Model**.

---

## The OSI Model

The **Open Systems Interconnection (OSI)** model breaks down network communication into **seven distinct layers**, each with a specific responsibility. Think of it as a set of departments in a large organisation — each one handles its own job, but they all work together to get the task done.

---

### Layer 1 — Physical
**What it does:** Transmits raw bits (0s and 1s) over a physical medium.

> 📡 **Example:** An Ethernet cable connecting your laptop to a router, or a Wi-Fi radio signal carrying data through the air.

---

### Layer 2 — Data Link
**What it does:** Transfers data between two directly connected devices, handling error detection and using **MAC addresses** to identify hardware.

>  **Example:** A network switch in an office directing traffic between computers on the same local network, using each device's MAC address.

---

### Layer 3 — Network
**What it does:** Routes packets across multiple networks using **IP addresses**, choosing the most efficient path.

>  **Example:** A router directing your web request from your home in Buenos Aires through several international nodes to reach a server in London.

---

### Layer 4 — Transport
**What it does:** Manages end-to-end data delivery, segmentation, flow control, and error checking via **TCP** or **UDP**.

>  **Example:** When downloading a file, **TCP** ensures every packet arrives and is reassembled in the correct order. When watching a live stream, **UDP** prioritises speed over perfection — a few dropped frames are acceptable.

---

### Layer 5 — Session
**What it does:** Establishes, maintains, and terminates communication sessions between applications.

>  **Example:** When you log in to an online banking portal, the session layer keeps your connection alive and can resume it if briefly interrupted — without forcing you to log in again.

---

### Layer 6 — Presentation
**What it does:** Translates, encrypts, and compresses data so it is readable by the receiving application.

>  **Example:** When you visit a website over **HTTPS**, this layer handles the **TLS encryption** that scrambles your data in transit. It also converts formats — for instance, ensuring an image sent as JPEG is rendered correctly on the other end.

---

### Layer 7 — Application
**What it does:** Provides network services directly to the end user's applications.

>  **Example:** Every time you open a browser and visit a website, you are using **HTTP/HTTPS**. Sending an e-mail uses **SMTP**; looking up a website address uses **DNS**.

---

## Quick Reference Table

| Layer | Name | Key Protocols / Devices | Real-World Example |
|---|---|---|---|
| 7 | Application | HTTP, FTP, SMTP, DNS | Browsing the web |
| 6 | Presentation | TLS/SSL, JPEG, ASCII | Encrypted HTTPS connection |
| 5 | Session | NetBIOS, RPC | Staying logged in to a website |
| 4 | Transport | TCP, UDP | File download (TCP) / Video call (UDP) |
| 3 | Network | IP, ICMP, Routers | Packet routing across the internet |
| 2 | Data Link | Ethernet, Switches, MAC | Local office network switching |
| 1 | Physical | Cables, Hubs, Radio waves | Ethernet cable / Wi-Fi signal |

---

