from engine.decision_engine import get_next_actions

sample = [
    {
        "port": "22/tcp",
        "state": "open",
        "service": "ssh"
    },
    {
        "port": "80/tcp",
        "state": "open",
        "service": "http"
    }
]

actions = get_next_actions(sample)

print(actions)