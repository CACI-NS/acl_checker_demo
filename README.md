# Batfish ACL Checker

> Need help getting from NetDevOops to NetDevOps? Learn about how [Network Automation and NetDevOps at CACI](https://info.caci.co.uk/network-automation-devops-caci) can help you on your journey

This project uses Batfish to perform validation checks on Access Control Lists (ACLs) extracted from device configuration files. The script sets up a Batfish session, extracts ACL names, checks for unreachable lines in the ACLs, and verifies if specific source IPs are permitted by the ACLs based on given criteria.

# Operation
The fw_checks.json file contains the traffic flows that are expected to be allowed through the ACL.
The snapshots/config directory contains the device configs.

# CICD integration
This can be integrated into a CICD pipeline.

## Makefile
The Makefile contains all the various steps used within each of the pipelines.
```
  add-venv                  Install virtualenv, create virtualenv, install requirements
  batfish-test              Execute batfish testing
  install-deps              Install pip
  remove-venv               Remove virtualenv
```

## Pre-requisites
This requires a local Batfish instance.

### Install Batfish
docker pull batfish/allinone

### Run Batfish
docker run --name batfish -v batfish-data:/data -p 8888:8888 -p 9997:9997 -p 9996:9996 batfish/allinone

# Need more help?
[Get in touch](https://info.caci.co.uk/network-automation-devops-caci) and see how we can help you run Batfish in your environment today.
