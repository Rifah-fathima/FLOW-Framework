from summaries.gobuster_summary import generate_gobuster_summary

sample = [
    {
        "path": "/images",
        "status": 301
    },
    {
        "path": "/index.html",
        "status": 200
    },
    {
        "path": "/admin",
        "status": 403
    }
]

print(generate_gobuster_summary(sample))