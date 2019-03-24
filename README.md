# PowerDnsPipeBackendExample

Add to pdns.conf:

    launch=pipe
    pipe-command=/etc/powerdns/pdns_backend.py
    pipe-abi-version=2

Now query for answer:

    nslookup example.com 127.0.0.1
