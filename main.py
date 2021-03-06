import json
from argparse import ArgumentParser
from collections import defaultdict
from itertools import chain

import pandas as pd


class DisjointSet:
    def __init__(self, N) -> None:
        self.parent = [i for i in range(N)]

    def get_parent(self, x):
        if x != self.parent[x]:
            self.parent[x] = self.get_parent(self.parent[x])
        return self.parent[x]

    def merge(self, a, b):
        x, y = map(self.get_parent, [a, b])
        if x < y:
            x, y = y, x

        self.parent[x] = y

    def finalize(self):
        groups = {}
        for i in range(len(self.parent)):
            if i == self.get_parent(i):
                groups[i] = set()
            groups[self.get_parent(i)].add(i)

        return groups


def main(args):
    key_properties = ["Email", "Phone", "OrderId"]

    with open(args.data_json) as f:
        data = json.load(f)

    print(f"> #data: {len(data)}")

    dsu = DisjointSet(len(data))

    assert all(d.keys() == data[0].keys() for d in data)

    property_keys = {p: defaultdict(set) for p in key_properties}

    for i, d in enumerate(data):
        for p in key_properties:
            property_keys[p][d[p]].add(i)

    for key, whoms in chain.from_iterable(map(lambda p: property_keys[p].items(), key_properties)):
        if key != "":
            whoms = list(whoms)
            for a, b in zip(whoms[:-1], whoms[1:]):
                dsu.merge(a, b)

    groups = dsu.finalize()  # leader [int] -> set of members [int]

    print(f"> #disjoint groups: {len(groups)}")

    belongs_to = {}  # member [int] -> leader [int]
    num_contacts = {}  # leader [int] -> int

    for leader, members in groups.items():
        members = sorted(members)
        num_contacts[leader] = 0

        for member in members:
            belongs_to[member] = leader
            num_contacts[leader] += data[member]["Contacts"]

    outputs = [
        "-".join(map(str, sorted(groups[belongs_to[i]]))) + f", {num_contacts[belongs_to[i]]}"
        for i in range(len(data))
    ]

    df = pd.DataFrame(
        [[i, o] for i, o in enumerate(outputs)],
        columns=["ticket_id", "ticket_trace/contact"],
    )
    df.to_csv(args.output_csv, index=False)


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("--data_json", default="data/contacts.json")
    parser.add_argument("--output_csv", default="output.csv")
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_arguments())
