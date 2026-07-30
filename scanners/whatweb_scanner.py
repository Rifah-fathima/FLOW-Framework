import subprocess

def run_whatweb(target):
    print("[FLOW] Running WhatWeb...")

    cmd = ["whatweb", target]
    print("Command:", " ".join(cmd))

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False
    )

    print("Return code:", result.returncode)
    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)

    return result.stdout