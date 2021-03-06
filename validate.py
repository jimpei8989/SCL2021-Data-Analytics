import json

import pandas as pd


def main():
    properties = ["Email", "Phone", "OrderId"]

    with open("datasets/contacts.json") as f:
        data = json.load(f)

    df = pd.read_csv("output.csv")

    uniques = set(df["ticket_trace/contact"])

    for s in uniques:
        a, b = s.split(",")
        members = [int(x) for x in a.split("-")]
        num_contacts = int(b)

        assert sorted(members) == members
        assert len(members) == len(set(members))
        assert all(
            any(any(data[x][p] == data[y][p] for p in properties) for y in members)
            for x in members
        )
        assert sum(data[x]["Contacts"] for x in members) == num_contacts


main()
