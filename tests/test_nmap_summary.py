from summaries.nmap_summary import generate_nmap_summary

sample = [
    {
        "port": "22/tcp",
        "state": "open",
        "service": "ssh",
        "version": ""
    },
    {
        "port": "80/tcp",
        "state": "open",
        "service": "http",
        "version": ""
    }
]

print(generate_nmap_summary(sample))