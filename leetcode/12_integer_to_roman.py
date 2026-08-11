class Solution:
    def intToRoman(self, num: int) -> str:
        # num is between 1 and 3999, so it's guaranteed to be buildable from given symbol chart
        mapping = {
            # Additive forms
            1: "I",
            5: "V",
            10: "X",
            50: "L",
            100: "C",
            500: "D",
            1000: "M",
            # Subtractive forms
            4: "IV",
            9: "IX",
            40: "XL",
            90: "XC",
            400: "CD",
            900: "CM",
        }

        # Continuously subtract the largest number we can
        numbers = sorted([(k, v) for k, v in mapping.items()], reverse=True)
        idx = 0
        roman = []
        while num > 0:
            while idx < len(numbers) and num - numbers[idx][0] >= 0:
                roman.append(numbers[idx][1])
                num -= numbers[idx][0]
            idx += 1

        return "".join(roman)
