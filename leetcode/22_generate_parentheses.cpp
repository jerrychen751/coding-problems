#include <vector>
#include <string>
#include <print>

class Solution {
public:
    std::vector<std::string> generateParenthesis(int n) {
        std::vector<std::string> res;
        std::string curr;
        curr.reserve(2 * n);
        backtrack(0, 0, n, curr, res);
        return res;
    }

private:
    void backtrack(
        int open,
        int close,
        int n,
        std::string& curr_str,
        std::vector<std::string>& res
    ) {
        if (curr_str.length() == 2 * n) {
            res.emplace_back(curr_str);
            return;
        }

        if (open < n) {
            curr_str.push_back('(');
            backtrack(open + 1, close, n, curr_str, res);
            curr_str.pop_back();
        }
        if (close < open) {
            curr_str.push_back(')');
            backtrack(open, close + 1, n, curr_str, res);
            curr_str.pop_back();
        }
    }
};

int main() {
    Solution s;
    std::print("{}", s.generateParenthesis(3));
}