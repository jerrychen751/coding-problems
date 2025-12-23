#include <array>
#include <cstddef>
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

class Solution {
public:
    std::vector<std::string> letterCombinations(const std::string& digits) {
        if (digits.empty()) return {};

        static constexpr std::array<std::string_view, 10> mp{
            "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"
        };

        // Optional: validate input + reserve exact result size
        std::size_t total = 1;
        for (char ch : digits) {
            if (ch < '2' || ch > '9') return {}; // or handle differently
            total *= mp[ch - '0'].size();
        }

        std::vector<std::string> res;
        res.reserve(total);

        std::string path;
        path.reserve(digits.size());

        backtrack(digits, 0, mp, path, res);
        return res;
    }

private:
    static void backtrack(const std::string& digits,
                          std::size_t i,
                          const std::array<std::string_view, 10>& mp,
                          std::string& path,
                          std::vector<std::string>& res) {
        if (i == digits.size()) {
            res.emplace_back(path); // copy once per complete combination
            return;
        }

        const std::string_view letters = mp[digits[i] - '0'];
        for (char c : letters) {
            path.push_back(c);
            backtrack(digits, i + 1, mp, path, res);
            path.pop_back();
        }
    }
};

int main() {
    Solution s;
    std::string digits = "23";
    auto ans = s.letterCombinations(digits);

    for (const auto& x : ans) {
        std::cout << x << '\n';
    }
}
