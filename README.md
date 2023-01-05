# ghidra-pyhidra-callgraphs

<p align="center">
<img align="center" src="">
</p>

<p align="center">
<a href="https://twitter.com/intent/follow?screen_name=clearbluejar"><img align="center" src="https://img.shields.io/twitter/follow/clearbluejar?color=blue&style=for-the-badge"></a> 
  <img align="center" src="https://img.shields.io/github/stars/clearbluejar/ghidra-python-vscode-devcontainer-skeleton?style=for-the-badge">
</p>

Blog post: [Ghidra Pyhidra Function Callgraphs](https://clearbluejar.github.io/posts/ghidra-function-callgraphs)

A demo repo leveraging a Ghidra Headless (non-GUI) Python script to generate function call graphs in mermaidsjs compatible markdown.

## Features

- Supports functions call graphs in mermaidsjs:
  - flowchart
  - sequence diagram 

## About

This repo is a starting point for your Ghidra Python scripting project in vscode. It demonstrates some useful vscode integrations and prescribes a workflow for running your python scripts. It leverages the power of devcontainers to provide a seamless development environment.

---

## TOC 
- [ghidra-pyhidra-callgraphs](#ghidra-pyhidra-callgraphs)
  - [Features](#features)
  - [About](#about)
  - [TOC](#toc)
  - [Install](#install)
    - [Option 1: Dev Container (Best Option)](#option-1-dev-container-best-option)
    - [Option 2: Virtualenv Standard setup](#option-2-virtualenv-standard-setup)
  - [Usage](#usage)
  - [Sample Call Graphs](#sample-call-graphs)
    - [Calling Flowchart](#calling-flowchart)
      - [SplGetPrinterDataEx from localspl.dll](#splgetprinterdataex-from-localspldll)
    - [Called](#called)

---

## Install  

### Option 1: Dev Container (Best Option) 

Detailed here: https://github.com/clearbluejar/ghidra-python-vscode-devcontainer-skeleton 

1. Start VS Code and run `Remote-Containers: Clone Repository in Container Volume...` from the Command Palette (F1).
2. Ctrl-V `https://github.com/clearbluejar/ghidra-python-vscode-devcontainer-skeleton`
3. VS Code will reload, clone the source code, and start building the container. 
4. After the build completes, VS Code will open with the container. You can now work with the repository source code in this independent environment as you would if you had cloned the code locally.

### Option 2: Virtualenv Standard setup

1. Install Ghidra and set environment variable GHIDRA_INSTALL_DIR to install location. This is a [requirement for Pyhidra](https://github.com/dod-cyber-crime-center/pyhidra#install).
2. `git clone git@github.com:clearbluejar/ghidra-python-vscode-devcontainer-skeleton.git`
3.
```bash
python3 -m venv .env
.env/bin/activate
pip install -r requirements.txt
```

## Usage


## Sample Call Graphs

### Calling Flowchart

#### SplGetPrinterDataEx from localspl.dll

```mermaid
flowchart TD

14["CheckForOfflinePrinterQueues"] --> 12["AddPrinterForOfflinePrinteQueue"]
25["InitializePrintProvidor"] --> 24["SplCreateSpooler"]
5["RecreateDsKey"] --> 7["UpdateDsSpoolerKey"]
19["DsUpdatePrinter"] --> 7["UpdateDsSpoolerKey"]
23["InitializeDS"] --> 22["SpawnDsUpdate"]
10["SplAddPrinter"] --> 11["SetRegistryData"]
15["FUN_18004f76a"] --> 15["FUN_18004f76a"]
10["SplAddPrinter"] --> 5["RecreateDsKey"]
15["FUN_18004f76a"] --> 14["CheckForOfflinePrinterQueues"]
26["DsPrinterPublish"] --> 34["DsPrinterUpdate"]
10["SplAddPrinter"] --> 9["GetQueueNameFromDevice"]
19["DsUpdatePrinter"] --> 4["UpdateDsDriverKeyImpl"]
8["SplSetPrinter"] --> 8["SplSetPrinter"]
2["SplSetPrinterDataEx"] --> 1["SplCopyFileEvent"]
12["AddPrinterForOfflinePrinteQueue"] --> 13["SplDeletePrinterWithJobs"]
7["UpdateDsSpoolerKey"] --> 2["SplSetPrinterDataEx"]
32["SetMandatoryProperties"] --> 2["SplSetPrinterDataEx"]
19["DsUpdatePrinter"] --> 6["SetPrinterDs"]
21["DsUpdate"] --> 20["DsUpdateSpooler"]
11["SetRegistryData"] --> 2["SplSetPrinterDataEx"]
17["LocalAddPrinter"] --> 10["SplAddPrinter"]
20["DsUpdateSpooler"] --> 19["DsUpdatePrinter"]
8["SplSetPrinter"] --> 7["UpdateDsSpoolerKey"]
24["SplCreateSpooler"] --> 23["InitializeDS"]
27["SplDeletePrinter"] --> 13["SplDeletePrinterWithJobs"]
6["SetPrinterDs"] --> 22["SpawnDsUpdate"]
31["SplDeleteForm"] --> 29["InternalDeleteForm"]
6["SetPrinterDs"] --> 26["DsPrinterPublish"]
7["UpdateDsSpoolerKey"] --> 32["SetMandatoryProperties"]
6["SetPrinterDs"] --> 6["SetPrinterDs"]
18["SplAddCSRPrinter"] --> 10["SplAddPrinter"]
12["AddPrinterForOfflinePrinteQueue"] --> 10["SplAddPrinter"]
8["SplSetPrinter"] --> 4["UpdateDsDriverKeyImpl"]
29["InternalDeleteForm"] --> 28["DsUpdateAllDriverKeys"]
30["LocalDeleteForm"] --> 29["InternalDeleteForm"]
34["DsPrinterUpdate"] --> 33["PublishMandatoryProperties"]
4["UpdateDsDriverKeyImpl"] --> 3["DevCapMultiSz"]
8["SplSetPrinter"] --> 5["RecreateDsKey"]
28["DsUpdateAllDriverKeys"] --> 22["SpawnDsUpdate"]
13["SplDeletePrinterWithJobs"] --> 6["SetPrinterDs"]
9["GetQueueNameFromDevice"] --> 8["SplSetPrinter"]
3["DevCapMultiSz"] --> 2["SplSetPrinterDataEx"]
8["SplSetPrinter"] --> 6["SetPrinterDs"]
7["UpdateDsSpoolerKey"] --> 7["UpdateDsSpoolerKey"]
16["LocalAddPrinterEx"] --> 10["SplAddPrinter"]
5["RecreateDsKey"] --> 4["UpdateDsDriverKeyImpl"]
22["SpawnDsUpdate"] --> 21["DsUpdate"]
5["RecreateDsKey"] --> 6["SetPrinterDs"]
5["RecreateDsKey"] --> 5["RecreateDsKey"]
19["DsUpdatePrinter"] --> 19["DsUpdatePrinter"]
4["UpdateDsDriverKeyImpl"] --> 2["SplSetPrinterDataEx"]
33["PublishMandatoryProperties"] --> 32["SetMandatoryProperties"]
1["SplCopyFileEvent"] --> 0["SplGetPrinterDataEx"]
```

### Called