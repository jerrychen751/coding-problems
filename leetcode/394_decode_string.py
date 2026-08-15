class Solution:
    def decodeString(self, s: str) -> str:
        """
        s is encoded string
        need to decode
        k[string] -> string repeated k times

        k is positive int
        brackets may contain nested encoded strings, i.e., k1[ak2[b]] -> if k1 = 2 and k2 = 2 then it's abbabb
        will number always be followed by opening bracket? yes original data contains no digits so any number is a repeat ct

        recursion: we have subproblems that we operate on in the same way
        At most, we have CHAR INT [subproblem]
        result is char + INT * func(subproblem)
        open bracket -> entering subproblem, closing bracket -> return func val

        def decode(s: str, idx: int) -> str:
            read chars, if any -> if we reach end of string OR right bracket just return these chars
            greedily read positive integer as multiplier, if any, if there is we're guaranteed a subproblem
            read until we run into left bracket -> curr_str = LEFT_CHARS + INT * decode(s, curr_idx, curr_s)
            greedily read more letters, if exists, and return curr_str + RIGHT_CHARS
        """

        # Return a decoded string with a cursor for next number/letter to read
        # This function focuses on decoding any nested structure of INT[xxx]
        def read_chars(idx: int) -> tuple[str, int]:
            """Returns letters as well as idx of next non-letter char to read"""
            start = idx
            while idx < len(s) and s[idx].isalpha():
                idx += 1
            return s[start:idx], idx

        def read_int(idx: int) -> tuple[int, int]:
            """Greedily reads positive int and returns idx for next non-numeric char to read"""
            start = idx
            while idx < len(s) and s[idx].isnumeric():
                idx += 1
            return int(s[start:idx]), idx

        def decode(idx: int) -> tuple[str, int]:
            left_chars, idx = read_chars(idx)
            if idx >= len(s):
                return left_chars, idx
            if s[idx] == ']':
                return left_chars, idx + 1
            multiplier, idx = read_int(idx)
            middle_chars, idx = decode(idx + 1) # idx is currently on '['
            right_chars, idx = decode(idx)
            return left_chars + multiplier * middle_chars + right_chars, idx

        decoded, _ = decode(0)
        return decoded
