import math

class Vector:
    x: float
    y: float
    z: float

    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, c):
        if type(c) == int:
            return Vector(c * self.x, c * self.y, c * self.z)
        
    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"

def norm(v: Vector):
    return math.sqrt(v.x ** 2 + v.y ** 2 + v.z ** 2)

def get_angle(u: Vector, v: Vector):
    dot_prod = u.x * v.x + u.y * v.y + u.z * v.z
    return math.acos(dot_prod/(norm(u) * norm(v)))

class Node:
    v: Vector
    word: str
    theta: float
    neg: int

    def __init__(self, v, word, theta, neg = 1) -> None:
        self.v = v
        self.word = word
        self.theta = theta
        self.neg = neg

        self.left = None
        self.right = None
        self.parent = None
    
    def __repr__(self, padding = ""):
        return f"{padding} v: {self.v * self.neg} word: {self.word} theta: {self.theta}\n{padding} l_child: {self.left.word if self.left else None}\n{padding} r_child: {self.right.word if self.right else None}\n{padding} parent: {self.parent.word if self.parent else None}"
    
    def pprint(self, padding = ""):
        print(self.__repr__(padding))
        if self.left != None:
            print(padding + " left:")
            self.left.pprint(padding + " ..")
        if self.right != None:
            print(padding + " right:")
            self.right.pprint(padding + " ..")

    def right_rotate(self):
        global root
        y = self.parent
        A  = self.left
        B = self.right
        C = y.right
        if C is None or get_angle(self.v, C.v) <= math.pi/2:
            self.left = y
            self.right = B
            y.left = A
            y.right = C
            if A:
                A.parent = y
            self.parent = y.parent
            if y.parent:
                z = y.parent
                if z.left == y:
                    z.left = self
                else:
                    z.right = self
            y.parent = self
        else:
            self.left = y
            self.right = C
            y.left = A
            y.right = B
            if B:
                B.v *= -1
                B.neg = -1
                B.left, B.right = B.right, B.left
                B.parent = y
            if A:
                A.parent = y
            if C:
                C.parent = self
            self.parent = y.parent
            if y.parent:
                z = y.parent
                if z.left == y:
                    z.left = self
                else:
                    z.right = self
            y.parent = self
        
        if self.parent == None:
            root = self
    
    def left_rotate(self):
        global root
        y = self.parent
        A  = y.left
        B = self.left
        C = self.right
        if A is None or get_angle(self.v, A.v) <= math.pi/2:
            self.left = A
            self.right = y
            y.left = B
            y.right = C
            if B:
                B.v *= -1
                B.neg = -1
                B.left, B.right = B.right, B.left
                B.parent = y
            if A:
                A.parent = self
            if C:
                C.parent = y
            self.parent = y.parent
            if y.parent:
                z = y.parent
                if z.left == y:
                    z.left = self
                else:
                    z.right = self
            y.parent = self
        else:
            self.right = y
            self.left = B
            y.left = A
            y.right = C
            self.parent = y.parent
            if y.parent:
                z = y.parent
                if z.left == y:
                    z.left = self
                else:
                    z.right = self
            y.parent = self
            if C:
                C.parent = y
        
        if self.parent == None:
            root = self


    def splay(self):
        global root
        while self.parent != None:
            y = self.parent
            if y.parent == None:
                # Single rotation
                if y.left == self:
                    self.right_rotate()
                
                if y.right == self:
                    self.left_rotate()
            else:
                z = y.parent
                if z.left == y and y.left == self:
                    y.right_rotate()
                    self.right_rotate()
                elif z.right == y and y.right == self:
                    y.left_rotate()
                    self.left_rotate()
                elif z.left == y and y.right == self:
                    self.left_rotate()
                    self.right_rotate()
                else:
                    self.right_rotate()
                    self.left_rotate()

    
    def access(self, v_in: Vector):
        alpha = get_angle(self.v * self.neg, v_in)
        if alpha <= self.theta:
            w = self.word
            self.splay()
            return w
        else:
            if alpha <= math.pi/2 and self.left != None:
                return self.left.access(v_in)
            elif alpha > math.pi/2 and self.right != None:
                return self.right.access(v_in)
            else:
                return None
    
    def insert(self, other):
        alpha = get_angle(self.v, other.v)
        if alpha <= math.pi/2:
            if self.left == None:
                self.left = other
                other.parent = self
                other.splay()
                return
            else:
                self.left.insert(other)
        else:
            if self.right == None:
                self.right = other
                other.parent = self
                other.splay()
                return
            else:
                self.right.insert(other)