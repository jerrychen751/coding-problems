#include <string>
#include <utility>
#include <numeric>
#include <vector>
#include <algorithm>
#include <print>

class Solution {
public:
    int minDistance(std::string& word1, std::string& word2) {
        // Edge cases
        if (word1.empty()) {
            return word2.size();
        }
        if (word2.empty()) {
            return word1.size();
        }

        // DP problem, since by choosing the best of 3 operations on top of previously computed optimal subproblem gives the global best answer

        // Represent edit distance from word1[:i] -> word2[:j] as dp[i][j]
        // Then dp[i][j] = std::min({dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + repl_cost})
        // where repl_cost = (word1[i - 1] == word2[j - 1]) ? 0 : 1

        // Since the computation of next state only requires values to left/top, and we only compute one row after its above row is completed, we can compress to a 1D dp array

        // Initialize base case values
        // Taking avantage of symmetry, let the shorter of the two words be in the row, and longer be in column
        const std::string* row_word = &word1; // pointer to row_word
        const std::string* col_word = &word2; // pointer to col_word
        if (row_word->size() > col_word->size()) { // swap pointer values / addresses
            std::swap(row_word, col_word);
        }

        std::vector<int> dp(row_word->size() + 1);
        std::iota(dp.begin(), dp.end(), 0);

        for (size_t i = 1; i <= col_word->size(); ++i) {
            int prev_diag = dp[0]; // dp[i - 1][j - 1]
            dp[0] = static_cast<int>(i); // dp[i][0] = i
            for (size_t j = 1; j <= row_word->size(); ++j) {
                int top = dp[j]; // dp[i - 1][j] is number of edits for col_word[:i-1] -> row_word[:j]; spend 1 delete operation for col_word[:i] -> row_word[:j]
                int left = dp[j - 1]; // dp[i][j - 1] is number of edits for col_word[:i] -> row_word[:j - 1]; spend 1 insert operation for col_word[:i] -> row_word[:j]
                int cost = ((*col_word)[i - 1] == (*row_word)[j - 1]) ? 0 : 1; // 1 if current chars don't match up; index i-1 and j-1 due to adding of extra row/col for DP matrix

                dp[j] = std::min({top + 1, left + 1, prev_diag + cost});
                prev_diag = top; // as j increments, dp[i - 1][j] -> dp[i - 1][j - 1]
            }
        }

        return dp.back();
    }
};

int main() {
    std::string word1 = "intention";
    std::string word2 = "execution";
    Solution s;
    std::print("{}", s.minDistance(word1, word2));
}