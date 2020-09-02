import random


class Solution:

    def climbStairs(self, n):
        if n == 1 or n == 2:
            return n
        a = 1
        b = 2
        c = 3
        for i in range(3, n + 1):
            c = a + b;
            a = b;
            b = c
        return c


if __name__ == '__main__':
    s = Solution()
    re = s.climbStairs(7)
    print(re)
