#include <vector>
#include <algorithm>

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
    int maxDepth(Node* root) {
        if (root == nullptr) {
            return 0;
        }

        int max_depth = 0;
        for (auto child : root->children) {
            max_depth = std::max(max_depth, maxDepth(child));
        }
        return max_depth + 1;
    }
};