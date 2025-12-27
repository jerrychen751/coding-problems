#include <string>
#include <vector>
#include <print>

class Solution {
public:
    std::vector<std::vector<std::string>> solveNQueens(int n) {
        std::vector<std::vector<std::string>> valid_boards;
        std::vector<char> col_used(n, false);
        std::vector<char> diag_used(2 * n - 1, false);     // (row - col) + (n - 1)
        std::vector<char> antidiag_used(2 * n - 1, false); // (row + col)
        std::vector<int> placement(n, -1);

        backtrack(valid_boards, col_used, diag_used, antidiag_used, placement, 0, n);
        return valid_boards;
    }

private:
    // Sets work as long as diagonals/anti-diagonals are same along slope and different amongst each other
    void backtrack(
        std::vector<std::vector<std::string>>& valid_boards,
        std::vector<char>& col_used,
        std::vector<char>& diag_used,     // mark by (row - col) + (n - 1)
        std::vector<char>& antidiag_used, // mark by (row + col)
        std::vector<int>& placement,
        int row,
        int n
    ) {
        // At this point, placement array is full, where placement[i] = valid queen col for i-th row
        if (row == n) {
            std::vector<std::string> curr_board;
            curr_board.reserve(n);
            for (int i = 0; i < n; ++i) { // i is row index of curr_board
                curr_board.emplace_back(n, '.'); // construct n-length string in container
                curr_board.back()[placement[i]] = 'Q';
            }
            valid_boards.push_back(std::move(curr_board)); // push_back(), because it's already constructed
            return;
        }

        for (int col = 0; col < n; ++col) {
            const int diag = row - col + (n - 1);
            const int antidiag = row + col;

            if (col_used[col] || diag_used[diag] || antidiag_used[antidiag]) {
                continue;
            }

            col_used[col] = true;
            diag_used[diag] = true;
            antidiag_used[antidiag] = true;
            placement[row] = col;
            backtrack(valid_boards, col_used, diag_used, antidiag_used, placement, row + 1, n);
            col_used[col] = false;
            diag_used[diag] = false;
            antidiag_used[antidiag] = false;
        }
    }
};

int main() {
    Solution s;
    const auto sols = s.solveNQueens(4);
    std::print("{}", sols);
}
