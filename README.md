# README

Submission for Expensify - Remote Infrastructure Challenge
## INTRO

TODO

## REQUIREMENTS

Below are the requirements laid out for this challenge:

Webservers:
- Quantity: 2
- One serves "A" while the other serves "B"

Load Balancer:
- Utilize any balance scheme (Round Robin, random, load based, etc.)
- Needs to be "sticky" (i.e. Same host should hit the same webserver for repeated requests).  Can only switch when a webserver goes down, and not switching back when the webserver comes back up.
- Pass the original requesting IP to the webservers
- Make port range 60000-65000 on the load balancer all get fed to the webservers on port 80

Nagios:
- Configure to monitor the two webservers and the load balancer
- Write a custom Nagios check (in python) that does the following:
    - Reads in the list of webservers from a file
    - Shows a warning if one of the webservers is offline
    - Shows a failure if both are offline

Users:
- Add user `expensify` to the boxes
- Grant sudo access
- Install provided public key as auth credential

Network:
- Only allow public ssh access on one server
- Use that server as a jumphost to the others 
- Block all other unused/unnecessary ports


## ARCHITECTURE

There have been four ubuntu 20.04 servers provisioned for me.

<INSERT TABLE HERE WITH IPs AND THEIR PURPOSE>

<INSERT ARCHITECTURE DIAGRAM>

## WORK LOGS

Daily work logs will be stored in `worklogs/`.  These files will detail my thought process during this exercise: All notes, photos/sketches, challenges encountered and how I addressed them, etc.  

## RESOURCES
Ansible - https://docs.ansible.com/ansible/latest/getting_started/index.html
HAProxy (docs)- https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/
HAProxy (configuration)- https://www.haproxy.com/blog/the-four-essential-sections-of-an-haproxy-configuration
Load Balancing Algorithms - https://www.haproxy.com/glossary/what-are-load-balancing-algorithms
Dynamic/Ephemeral Ports - https://www.techtarget.com/searchnetworking/definition/dynamic-port-numbers#:~:text=User%20ports%2C%20also%20known%20as,65535%20and%20are%20never%20assigned.
Stick Tables - https://www.haproxy.com/blog/introduction-to-haproxy-stick-tables
Jinja - https://jinja.palletsprojects.com/en/stable/
Nagios - https://documentation.ubuntu.com/server/how-to/observability/install-nagios/index.html