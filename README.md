# check-blacklistD
Python Script for Domain Check blacklist

Checks a list of DNS blocklists for hosts and IPs.

This will try to resolve the matching IP/hostname, and check for both in all blocklists. For every match that is found. Gevent is used for concurrent lookups, the number of active greenlets is limited to (the constant) PARALLELISM.

<h3><b>Example usage:</b><br></h3>
<b>check-dnsbl.py gmail.com test 8.8.8.8<br></b>
<i>
WARNING: test found in spam blocklist dob.sibl.support-intelligence.net<br>
WARNING: test found in spam blocklist dbl.spamhaus.org<br>
WARNING: 8.8.8.8 found in spam blocklist cblless.anti-spam.org.cn<br>
WARNING: 8.8.8.8 found in spam blocklist cbl.anti-spam.org.cn<br>
WARNING: 8.8.8.8 found in spam blocklist cblplus.anti-spam.org.cn<br>
</i>
