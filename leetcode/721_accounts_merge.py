from typing import List


class UnionFind:
    def __init__(self) -> None:
        self.root = {}
        self.size = {}
        self.owner = {} # maps component -> name

    def find(self, node: str, name: str) -> str:
        if node not in self.root:
            self.root[node] = node
            self.size[node] = 1
            self.owner[node] = name
        if self.root[node] != node:
            self.root[node] = self.find(self.root[node], name)
        return self.root[node]

    def union(self, n1: str, n2: str) -> bool:
        r1 = self.find(n1, "")
        r2 = self.find(n2, "")
        if r1 == r2:
            return False
        if self.size[r1] < self.size[r2]:
            r1, r2 = r2, r1
        del self.owner[self.root[r2]]
        self.root[r2] = self.root[r1]
        self.size[r1] += self.size[r2]
        del self.size[r2]
        return True

class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        '''
        accounts = list of lists
        for some account, account[0] is a name, rest are emails
        account is always at least len 2, 1 name first and 1 or more emails
        may be duplicate emails in the same account

        union find
        John: j1@mail.com, j2@mail.com
        John: j2@mail.com

        j1@mail.com -> j1@mail.com
        j2@mail.com -> j1@mail.com

        if uf.find(mail) in mail_to_owner mapping keys, then these belong to the same person / same component

        j1@mail.com -> John (value is not necessarily unique)

        for account in accounts:
            name = account[0]
            group_root = uf.find(account[1])
            for i in range(2, len(account)):
                root = uf.find(account[i])
                uf.union(group_root, root)

        iterate through uf.root, which maps emails to root
        for email in sorted(uf.root):
            root = uf.find(email)
            name = uf.owner[root]
            mapping[name].append(email)

        for k, v in mapping:
            return [k] + v

        N = total number of emails in accounts
        aNk + NlogN
        '''
        uf = UnionFind()
        for account in accounts:
            name = account[0]
            group_root = uf.find(account[1], name)
            for i in range(2, len(account)):
                root = uf.find(account[i], name)
                uf.union(group_root, root)

        mapping = {} # maps component id (some email address belonging to that person
        # maps to a list of [name, emails...]
        for email, name in uf.owner.items():
            mapping[email] = [name]

        for email in sorted(uf.root.keys()):
            root = uf.find(email, "")
            mapping[root].append(email)

        return list(mapping.values())
