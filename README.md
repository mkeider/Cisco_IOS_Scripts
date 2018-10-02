# Cisco_IOS_Scripts
Cisco IOS Scripts


The Cisco IOS Scripts automate the process of gathering the unstructured data from legacy IOS "show" commands and convert it to structured data. The output of this data is written to csv file format.

These scripts utilize the Netmiko work done by Kirk Byers and NTC-Templates based around the TEXTFSM parsing engine. NTC (Network to Code) is a network automation company founded by Jason Edelman in 2014.


REQUIREMENTS

The scripts require a Python3 environment, latest version of Netmiko, and the installation of ntc-templates. A full step-by-step instruction to install this environment can be found at Kirk Byers "Python for Network Engineers" site: https://pynet.twb-tech.com/blog/automation/netmiko-textfsm.html


SCRIPT FEATURES

Device Authentication: The Username/Password are manually entered. Credentials are not stored in the script and passwords entered do not appear on command line.

Exception Handling: Exception handling is configured for ssh timeout and ssh authentication.

Logging: Logging of all ssh exception handling to json file
