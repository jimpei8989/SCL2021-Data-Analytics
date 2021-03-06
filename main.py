import json
from collections import defaultdict

import pandas as pd


class DisjointSet:
    def __init__(self, N) -> None:
        self.parent = [i for i in range(N)]

    def get_parent(self, x):
        if x != self.parent[x]:
            self.parent[x] = self.get_parent(self.parent[x])
        return self.parent[x]

    def merge(self, a, b):
        self.parent[self.get_parent(a)] = self.get_parent(b)

    def finalize(self):
        ret = {}
        for i in range(len(self.parent)):
            if i == self.get_parent(i):
                ret[i] = set()

        for i in range(len(self.parent)):
            ret[self.get_parent(i)].add(i)

        return ret.values()


def main():
    with open("datasets/contacts.json") as f:
        data = json.load(f)

    print(f"> #data: {len(data)}")

    dsu = DisjointSet(len(data))

    assert all(d.keys() == data[0].keys() for d in data)

    emails = defaultdict(set)
    phones = defaultdict(set)
    order_ids = defaultdict(set)

    for i, d in enumerate(data):
        emails[d["Email"]].add(i)
        phones[d["Phone"]].add(i)
        order_ids[d["OrderId"]].add(i)

    for email, whoms in emails.items():
        if email != "":
            whoms = list(whoms)
            for a, b in zip(whoms[:-1], whoms[1:]):
                dsu.merge(a, b)

    for phone, whoms in phones.items():
        if phone != "":
            whoms = list(whoms)
            for a, b in zip(whoms[:-1], whoms[1:]):
                dsu.merge(a, b)

    for order_id, whoms in order_ids.items():
        if order_id != "":
            whoms = list(whoms)
            for a, b in zip(whoms[:-1], whoms[1:]):
                dsu.merge(a, b)

    ret = dsu.finalize()

    print(f"# disjoint groups: {len(ret)}")

    groups = {}
    contacts = {}
    belongs_to = defaultdict(int)

    for group in ret:
        group = sorted(group)
        groups[group[0]] = group
        contacts[group[0]] = 0

        for member in group:
            belongs_to[member] = group[0]
            contacts[group[0]] += data[member]["Contacts"]

    outputs = [
        "-".join(map(str, groups[belongs_to[i]])) + f",{contacts[belongs_to[i]]}"
        for i in range(len(data))
    ]

    df = pd.DataFrame(
        [[i, o] for i, o in enumerate(outputs)],
        columns=["ticket_id", "ticket_trace/contact"],
    )
    df.to_csv("output.csv", index=False)


main()