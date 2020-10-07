#!/usr/bin/env python
"""
Angel Reynoso.
kp01aj@gmail.com
https://github.com/kp01aj/check-blacklistD

"""

from gevent import monkey
monkey.patch_all()
import gevent
import gevent.pool
import sys
import socket
from dnsblModel import dnsbldb

LOOKUP_TIMEOUT = 10
PARALELLISM = 10

# DBL only lists hostnames. Spamhaus doesn't want you to query it for IPs,
# so they return a false positive for each IP address.
HOST_LOOKUP_ONLY = set([
    'dbl.spamhaus.org',
])

DNS_BLS = dnsbldb()

class Host:
    def __init__(self, hostname=None, addr=None):
        self.hostname = hostname
        self.addr = addr

    def inverse_addr(self):
        """
        IPs are listed backwards, e.g. IP 1.2.3.4 -> 4.3.2.1.pbl.spamhaus.org
        """
        if self.addr is None:
            return None
        addr_split = self.addr.split(".")
        addr_split.reverse()
        return ".".join(addr_split)

def lookup(host_rbl):
    """
    Looks up a host in blacklist, returns whether it exists.
    Expects a tuple of (host, rbl), where host again is a tuple, of any
    length. The first field of host is used for the lookup (i.e. hostname
    or inverse ip), and the last field is printed in warning messages.
    """
    host, rbl = host_rbl
    rblhost = host[0] + "." + rbl
    try:
        socket.gethostbyname(rblhost)
        sys.stderr.write("%s Found in blacklist of %s\n" % (host[-1], rbl))
        sys.stderr.flush()
        return True
    except socket.gaierror:
        return False

def lookup_parallel(hosts_rbls):
    pool = gevent.pool.Pool(size=PARALELLISM)
    in_rbl = False
    for result in pool.imap_unordered(lookup, hosts_rbls):
        in_rbl = in_rbl or result
    return in_rbl

def print_usage():
    sys.stderr.write("usage: %s <host.name or IP> [host2.name or IP] ...\n" % sys.argv[0])
    sys.stderr.flush()

def get_host_and_ip(host_or_ip):
        """
        Given a hostname or ip address, this returns a Host instance with
        hostname and ip. One of the Host fields may be None, if a lookup
        fails.
        """
        host = host_or_ip
        addr = None
        try:
            addr = socket.gethostbyname(host)
            if addr == host:
                # addr and host are the same ip address
                host = socket.gethostbyaddr(addr)[0]
        except socket.gaierror:
            # no addr for hostname
            return Host(hostname=host)
        except socket.herror:
            # no hostname for addr
            return Host(addr=addr)
        return Host(hostname=host, addr=addr)

def main():
    dnsbldb()
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    socket.setdefaulttimeout(LOOKUP_TIMEOUT)
    hosts_rbls = []
    for hostname_or_ip in sys.argv[1:]:
        host = get_host_and_ip(hostname_or_ip)
        for rbl in DNS_BLS:
            if host.hostname is not None:
                hosts_rbls.append(((host.hostname,), rbl))
            if rbl not in HOST_LOOKUP_ONLY and host.addr is not None:
                hosts_rbls.append(((host.inverse_addr(), host.addr), rbl))

    in_rbl = lookup_parallel(hosts_rbls)
    if in_rbl:
        sys.exit(1)

if __name__ in "__main__":
    main()