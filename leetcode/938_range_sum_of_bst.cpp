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
    int rangeSumBST(TreeNode* root, int low, int high) {
        // Inorder traversal; increment sum if falling within range; early exit if exceeding high
        int sum = 0;
        dfs(root, low, high, sum);
        return sum;
    }

private:
    void dfs(TreeNode* curr, int low, int high, int& sum) {
        if (!curr) {
            return;
        }

        if (curr->val < low) {
            dfs(curr->right, low, high, sum);
        } else if (curr->val > high) {
            dfs(curr->left, low, high, sum);
        } else {
            sum += curr->val;
            dfs(curr->left, low, high, sum);
            dfs(curr->right, low, high, sum);
        }
    }
};