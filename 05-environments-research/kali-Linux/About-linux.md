# About Kali Linux

Kali Linux is an enterprise-ready security auditing Linux distribution based on Debian GNU/Linux. Kali is aimed at security professionals and IT administrators, enabling them to conduct advanced penetration testing, forensic analysis, and security auditing.
What is a Linux distribution?

Although it is commonly used as a name for the entire operating system, Linux is just the name of the kernel, a piece of software that handles interactions between the hardware and end-user applications.

The expression Linux distribution, on the other hand, refers to a complete operating system (OS) built on top of the Linux kernel, usually including an installation program and many applications, which are either pre-installed or packaged in an easily installable way.

# Exploring the Kali Linux Platform

The summary you shared highlights that Kali Linux is far more than just an operating system; it is a versatile platform deployed on laptops, cloud servers, and compact ARM devices. 

Since the main menu is organised by theme based on professional security tasks, we can explore how these tool categories operate. Let's dive into one of these core areas together:

    Information gathering : How professionals map out a network and discover active devices or open ports.

    Vulnerability analysis : The process of scanning systems to identify known security flaws and misconfigurations.

    Wireless attacks : The methods used to audit Wi-Fi networks and examine signal security.

### Let's explore how these phases operate in practice. We can choose a couple of these interconnected categories to see how they work together:

    The Discovery Phase 🔍: Combining Information Gathering and Vulnerability Analysis to map out a target and find its weak points.

    The Access Phase 🔑: Seeing how Exploitation Tools are used once a vulnerability is found, followed by Post Exploitation to maintain that access.

    The Human & App Phase 🌐: Exploring how Web Application Analysis and Social Engineering Tools target the most exposed parts of an organisation.

# Kali Linux: the ability to run a Live System 💿. 

This means you can boot a fully functional security environment directly from a USB drive without touching the host computer's hard drive or altering its existing operating system.By default, a live system runs entirely in the computer's volatile memory (RAM). This creates two distinct operational modes:


| Live Mode | Description | Key Characteristic |
| :--- | :--- | :--- |
| **Standard Live ⚡** | Runs completely in RAM. | All changes, files, and configurations are wiped upon reboot. |
| **Live with Persistence 💾** | Allocates a special partition on the USB drive to save data. | Customisations, reports, and packages are preserved across reboots. |


#  Forensics Mode

In general, when doing forensic work on a system, you want to avoid any activity that would alter the data on the analyzed system in any way. Unfortunately, modern desktop environments tend to interfere with this objective by trying to auto-mount any disk(s) they detect. To avoid this behavior, Kali Linux has a forensics mode that can be enabled from the boot menu: it will disable all such features.

The live system is particularly useful for forensics purposes, because it is possible to reboot any computer into a Kali Linux system without accessing or modifying its hard disks.

# Completely Customizable

The ability to completely customise a Kali Linux ISO using live-build is incredibly powerful. 🛠️ Instead of modifying a system after booting, security teams can build a bespoke operating system image from scratch with their own scripts, specific network configurations, and precise toolsets pre-installed.

When you use live-build, the customisation engine allows you to inject changes at different layers of the build process:


| Feature | Description | Real-World Use Case |
| :--- | :--- | :--- |
| Package Selection 📦 | Choose exactly which software is included or removed. | Removing heavy desktop environments to create a lightweight, CLI-only attack image. |
| Hooks 🪝 | Run arbitrary scripts or commands during the image creation phase. | Pre-configuring custom firewall rules or automatically enabling specific network services on boot. |
| Overlay Files 📂 | Add supplementary files directly into the system directories. | Pre-loading specific wordlists, company VPN profiles, or API keys directly into the ~/project directory. |


#  A Trustable Operating System

The text highlights a fundamental principle in cybersecurity: trust through transparency 🤝. For a security operating system, knowing exactly how the software is built and verified is just as important as the tools it contains.

Kali Linux achieves this by using a fully auditable supply chain. Let's look at the key mechanisms they use to ensure integrity:


| Security Mechanism | Description | Purpose |
| :--- | :--- | :--- |
| Signed Source Packages 🔏 | Developers sign the code using cryptographic keys before upload. | Proves the code genuinely comes from a trusted Kali developer. |
| Dedicated Build Daemons ⚙️ | Isolated servers that compile the source code into binary packages. | Prevents tampering during the compilation process. |
| Signed Repositories 📦 | The final collection of packages is cryptographically signed. | Ensures the files haven't been altered on the download mirrors. |
| Git Repositories & Tracker 🔍 | Publicly viewable source code history with signed version tags. | Allows anyone to inspect the code for backdoors or flaws. |


This transparent workflow ensures that the system hasn't been modified by a malicious third party before it reaches your device.

Since we are talking about verifying the integrity of software, let's think about how you might do this on your own machine.

#  Usable on a Wide Range of ARM Devices

Kali Linux provides binary packages for the armel, armhf, and arm64 ARM architectures. Thanks to the easily installable images provided by OffSec, Kali Linux can be deployed on many interesting devices, from smartphones and tablets to Wi-Fi routers and computers of various shapes and sizes.

# Kali Linux Policies

While Kali Linux strives to follow the Debian policy whenever possible, there are some areas where we made significantly different design choices due to the particular needs of security professionals.

# Network Services Disabled by Default

In contrast to Debian, Kali Linux disables any installed service that would listen on a public network interface by default, such as HTTP and SSH.

The rationale behind this decision is to minimize exposure during a penetration test when it is detrimental to announce your presence and risk detection because of unexpected network interactions.

You can still manually enable any services of your choosing by running ```sudo systemctl enable service```. 

#  A Curated Collection of Applications
Verifying the integrity of an ISO file is an excellent practice, especially when dealing with security-focused distributions like Kali Linux. To ensure the file has not been altered or corrupted during download, professionals rely on cryptographic checksums (such as SHA-256). 🔍

In British English environments, checking these hashes is a standard part of deploying trusted software. Let's look at how Kali Linux curates its repository to maintain that trust.
The Curation Process

Unlike Debian, which aims to package almost everything, Kali Linux uses a strict evaluation process to keep its toolset lean and effective. 

Here is how the curation criteria break down:


| Evaluation Point | Description |
| :--- | :--- |
| Relevance 🎯 | The application must serve a clear purpose in a penetration testing context. |
| Uniqueness 💎 | It should offer distinct features not already covered by existing tools. |
| Licensing 📜 | Tools must comply with free-licensing standards to ensure open distribution. |
| Efficiency ⚡ | The application's resource requirements must match the platform's deployment models (e.g., lightweight enough for ARM devices). |


This careful selection ensures that users do not have to sift through hundreds of abandoned or redundant tools. Instead, they get a highly optimised environment out of the box.
Exploring Tool Evaluation

Since Kali allows users to suggest new software via the Kali Bug Tracker, submissions must be thoroughly justified. Let's think about how a tool might be judged against these criteria.

Imagine you have discovered a new open-source network scanner that you want to suggest to the Kali developers. Which of the following arguments would be the most effective way to present your request?

*    Focusing on popularity : Explaining that the tool is currently trending on GitHub and has thousands of stars.

*    Focusing on uniqueness and efficiency : Demonstrating that it consumes half the RAM of nmap and uses a unique scanning method for firewalls.

*    Focusing on simplicity : Stating that it is easier to use than existing tools, even though it performs the exact same functions.

    Live - Live boot, as usual.
    Live (amd64 failsafe) - Boots with a minimal set of drivers and hardware checks.
    Live (forensics mode) - Boots without mounting anything, suitable for forensics work.
    Live USB Persistence (and Encrypted Persistence) - After adding the needed partitions (which will be discussed in chapter 9.4), boot menu is ready for persistence.
    Start installer - Regular, text mode installation.
    Start installer with speech synthesis - Kali Installation for visually impaired users.
    Hardware Detection Tool - Designed to display low-level hardware information.
    Memory Diagnostic - Diagnoses memory.

Questions

    What versions of Debian is Kali 1.0, 2.0 and rolling based on?
    What are the main differences between a Live boot instance of Kali, and an installed instance?
    What's the difference between live and forensics mode?
    How can we verify that forensics mode is working?
    What's the best way to get a tool included in Kali?
    Name some of the cool features in Kali!

Answers:

    Kali 1.0 was based on Debian Wheezy. Kali 2.0 is based on Jessie. Kali rolling is based on Debian Testing.

    Live mode boots to RAM, and an installed instance of Kali boots to a storage device.

    Live mode boots to RAM, but may auto-mount disks. Forensics mode does not auto-mount drives.

    Use the mount command to verify that no disks are mounted. You can also MD5 the system's swap and disk devices, reboot into forensic mode and MD5 again. The MD5 hashes should match if forensics mode succeeded. Try this in a system you don't care about "tainting"!

    The best way to request for a tool addition is to open a "New Tool Requests" ticket in the Kali Bug Tracker.
    
    A live system, forensics mode, a custom Linux kernel, completely customizable, a trusted operating system with default disabled network services, ARM support, preloaded security tools, penetration testing platform! To name a few


