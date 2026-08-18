class Solution:
    def removeDuplicates(self, s: str) -> str:
        '''
        abbaca
        bb -> aaca
        aa -> ca
        s is lowercase letters
        continuously remove adjacent duplicates

        continuously iterated through word, removing duplicates
        n^2

        [c, a]
        n time, n space

        stack = []
        for each char in s:
            if stack and stack[-1] == char:
                stack.pop()
            else:
                stack.append(char)
        '''

        stack = []
        for char in s:
            if stack and stack[-1] == char:
                stack.pop()
            else:
                stack.append(char)

        return "".join(stack)
