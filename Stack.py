from array import array

class Stack:
    def __init__(self, typecode='H'):
        self.stack = array(typecode)
        self.top = -1
        self.capacity = 0

    def is_empty(self):
        return self.top == -1

    def push(self, value):
        self.top += 1
        if self.top < self.capacity:
            self.stack[self.top] = value
        else:
            self.stack.append(value)
            self.capacity += 1

    def pop(self):
        value = self.stack[self.top]
        self.top -= 1
        return value