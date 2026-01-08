// https://leetcode.com/problems/binary-tree-tilt/description/?envType=problem-list-v2&envId=tree

#include <cstdlib>
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
    int findTilt(TreeNode* root) {
        int sum_of_tilts = 0;
        dfs(root, sum_of_tilts);
        return sum_of_tilts;
    }

private:
    // Returns sum of node values (left subtree + right subtree + curr val)
    int dfs(TreeNode* curr, int& sum_of_tilts) {
        if (curr == nullptr) {
            return 0;
        }

        int left_subtree_sum = dfs(curr->left, sum_of_tilts);
        int right_subtree_sum = dfs(curr->right, sum_of_tilts);
        sum_of_tilts += std::abs(left_subtree_sum - right_subtree_sum);
        return left_subtree_sum + right_subtree_sum + curr->val;
    }
};