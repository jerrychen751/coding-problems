#include <vector>
#include <deque>
#include <algorithm>

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

class Solution {
public:
    std::vector<int> largestValues(TreeNode* root) {
        if (!root) {
            return {};
        }

        std::deque<TreeNode*> queue{root};
        std::vector<int> res;
        while (!queue.empty()) {
            int max_val = queue.front()->val;
            size_t level_size = queue.size();
            for (size_t i = 0; i < level_size; ++i) {
                TreeNode* curr = queue.front();
                queue.pop_front();

                max_val = std::max(max_val, curr->val);

                if (curr->left) {
                    queue.push_back(curr->left);
                }
                if (curr->right) {
                    queue.push_back(curr->right);
                }
            }
            res.push_back(max_val);
        }

        return res;
    }
};