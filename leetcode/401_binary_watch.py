from typing import List


class Solution:
    def readBinaryWatch(self, turnedOn: int) -> List[str]:
        # 2**4 possibilities to represent hour, 2**6 possibilities for minutes
        # contrained within 0-11 and 0-59 for hours and minutes

        # Given an integer turnedOn, return all possible times the watch can represent
        # Constrains times to just those within the range
        # No leading zeros

        # Backtracking
        # Can represent the number as a bitstring of length 10
        # First 6 represent mins, next 4 represent hours
        # First check if the time is in valid range, if not exit
        # Then if turnedOn is zero, compute time and append to list and return
        # If turnedOn is not zero, perform a for loop iterating over possible remaining values to use curr bit on
        
        times = []
        def backtrack(remaining: int, bits: int, curr_bit: int, curr_mins: int, curr_hrs: int) -> None:            
            # At this point, we have a valid time so far
            if remaining == 0:
                times.append(str(curr_hrs) + ":" + str(curr_mins).zfill(2))
                return
            
            for idx in range(curr_bit, 10):
                if idx < 6:
                    curr_mins += 2 ** idx
                else:
                    curr_hrs += 2 ** (idx - 6)
                
                if curr_mins <= 59 and curr_hrs <= 11:
                    # Valid time -> recurse with 1 fewer LED remaining
                    bits &= (1 << idx)
                    backtrack(remaining - 1, bits, idx + 1, curr_mins, curr_hrs)
                    bits &= ~(1 << idx)
                    
                # Undo / backtrack
                if idx < 6:
                    curr_mins -= 2 ** idx
                else:
                    curr_hrs -= 2 ** (idx - 6)

        backtrack(turnedOn, 0, 0, 0, 0)
        return times
