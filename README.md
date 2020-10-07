# check-blacklistD
Python Script for Domain Check blacklist

Checks a list of DNS blocklists for hosts and IPs.

This will try to resolve the matching IP/hostname, and check for both in all blocklists. For every match that is found. Gevent is used for concurrent lookups, the number of active greenlets is limited to (the constant) PARALLELISM.

<h3><b>Example usage:</b><br></h3>
<b>python3 check-blacklistD.py 8.8.8.8<br></b>
<i>
8.8.8.8 Found in blacklist of bl.emailbasura.org
dns.google Found in blacklist of bl.emailbasura.org
dns.google Found in blacklist of multi.uribl.com
8.8.8.8 Found in blacklist of multi.uribl.com
8.8.8.8 Found in blacklist of bl.spamcannibal.org
dns.google Found in blacklist of bl.spamcannibal.org
dns.google Found in blacklist of dynip.rothen.com
8.8.8.8 Found in blacklist of dynip.rothen.com
</i>
