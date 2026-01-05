#include <vector>
#include <array>
#include <utility>
#include <print>

class Solution {
public:
    std::vector<std::vector<char>> updateBoard(std::vector<std::vector<char>>& board, std::vector<int>& click) {
        int sr = click[0];
        int sc = click[1];
        if (board[sr][sc] == 'M') {
            board[sr][sc] = 'X';
            return board;
        }

        dfs(board, sr, sc);
        return board;
    }

private:
    static constexpr std::array<std::pair<int, int>, 8> dirs = {{
        {-1, -1}, {-1, 0}, {-1, 1},
        {0, -1}, {0, 1},
        {1, -1}, {1, 0}, {1, 1}
    }};

    void dfs(std::vector<std::vector<char>>& board, int r, int c) {
        // Check if already visited
        if (board[r][c] != 'E') {
            return;
        }

        // Count adjacent mines
        int adj_mines = 0;
        for (const auto& [dr, dc] : dirs) {
            int nr = r + dr;
            int nc = c + dc;
            // Check bounds
            if (
                nr < 0 || nr >= (int)board.size() ||
                nc < 0 || nc >= (int)board[0].size()
            ) {
                continue;
            }

            adj_mines += (board[nr][nc] == 'M');
        }

        // Rule 3
        if (adj_mines > 0) {
            board[r][c] = static_cast<char>(adj_mines + '0');
            return;
        }

        // Rule 4
        board[r][c] = 'B';
        for (const auto& [dr, dc] : dirs) {
            int nr = r + dr;
            int nc = c + dc;
            // Check bounds
            if (
                nr < 0 || nr >= (int)board.size() ||
                nc < 0 || nc >= (int)board[0].size()
            ) {
                continue;
            }

            dfs(board, nr, nc);
        }
    }
};

int main() {
    std::vector<std::vector<char>> board = {
        {'E','E','E','E','E'},
        {'E','E','M','E','E'},
        {'E','E','E','E','E'},
        {'E','E','E','E','E'}
    };
    std::vector<int> click = {3, 0};
    Solution s;
    std::print("{}", s.updateBoard(board, click));
}