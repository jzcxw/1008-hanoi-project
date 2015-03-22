__author__ = 'Elson'

from sys import *

class Stack:
    def __init__(self):
        self.top = -1
        self.data = []

    def push(self, value):
        self.top = self.top + 1
        self.data.extend([value])
        # print(self.data)

    def pop(self):
        if(self.top == -1): #If nothing in the stack
            return
        value = self.data[self.top]
        del self.data[self.top]
        self.top = self.top - 1
        # print(self.data)
        return value

    def isEmpty(self):
        if(self.top == -1):
            return True
        return False

    def peek(self):
        value = self.data[self.top]
        # print(value)
        return value

    def peekAt(self, i):
        #Return the value of the element at index i without removing it from the stack
        return self.data[i]

    def copyFrom(self, aStack):
        #Copy all the elements and properties (include top value) from the input stack aStack to this stack
        self.data = []
        for i in range(aStack.size()):
            self.data.append(aStack.peekAt(i))
        self.top = aStack.top

    def printstack(self):
        for i in range(len(self.data)-1, 0, -1):
            if(i == 1):
                stdout.write(str(self.data[i]))
            else:
                stdout.write(str(self.data[i]) + ", ")
        stdout.write("\n")

    def size(self):
        return len(self.data)

    def gettitle(self):
        return self.data[0]

    def isEqual(self, stack):
        if((len(self.data))!= (stack.size())):
            return False
        else:
            for i in range(len(self.data)):
                if(self.data[i] != stack.data[i]):
                    return False
            return True
# aStack = Stack()
# aStack.push(10)
# aStack.push(100)
# aStack.pop()
# aStack.push(99)
# aStack.peek()
# aStack.peek()
# aStack.isEmpty()
# aStack.pop()
# aStack.pop()
# aStack.isEmpty()
