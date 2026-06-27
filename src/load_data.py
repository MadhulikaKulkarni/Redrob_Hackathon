import json

def load_candidates():

    candidates=[]

    with open(
        "data/candidates.jsonl",
        "r",
        encoding="utf8"
    ) as f:

        for line in f:
            candidates.append(
                json.loads(line)
            )

    return candidates