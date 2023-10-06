import math

class operations:
    def minus(self, vec1, vec2):
        ans = []
        for i in range(len(vec1)):
            ans.append(vec1[i] - vec2[i])
        return ans
    
    def plus(self, vec1, vec2):
        ans = []
        for i in range(len(vec1)):
            ans.append(vec1[i] + vec2[i])
        return ans
    
    def multi(self, vec, n):
        ans = []
        for i in range(len(vec)):
            ans.append(vec[i] * n)
        return ans
    
    def divide(self, vec, n):
        ans = []
        for i in range(len(vec)):
            ans.append(vec[i] / n)
        return ans
    
    def magnitude(self, vec):
        return math.sqrt(vec[0] ** 2 + vec[1] ** 2)

    def dot_product(self, a, b):
        if len(a) != 2 or len(b) != 2:
            raise ValueError("Both input vectors must be 2D vectors.")

        dx = a[0] * b[0] + a[1] * b[1]
        return dx

    def cross_product(self, a, b):
        if len(a) != 2 or len(b) != 2:
            raise ValueError("Both input vectors must be 2D vectors.")

        cx = a[0] * b[1] - a[1] * b[0]

        return cx

