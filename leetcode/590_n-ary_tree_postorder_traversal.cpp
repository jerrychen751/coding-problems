#include <vector>

class Node {
public:
    int val;
    std::vector<Node*> children;

    Node() {}

    Node(int _val) {
        val = _val;
    }

    Node(int _val, std::vector<Node*> _children) {
        val = _val;
        children = _children;
    }
};

class Solution {
public:
    std::vector<int> postorder(Node* root) {
        std::vector<int> res;
        dfs(root, res);
        return res;
    }

private:
    void dfs(const Node* curr, std::vector<int>& res) {
        if (!curr) {
            return;
        }

        for (const Node* child : curr->children) {
            dfs(child, res);
        }
        res.push_back(curr->val);
    }
};