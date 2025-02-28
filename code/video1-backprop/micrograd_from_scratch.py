import numpy as np
import matplotlib.pyplot as plt
from graphviz import Digraph

# scalar valued function f of x
# scalar = there's a size but no direction.

def f(x):
    return 3 * x**2 - 4 * x + 5  # 3x^2 - 4x + 5

f(3.0)  # prints 20.0

xs = np.arange(
    -5, 5, 0.25
)  # return an array from -5 (inclusive) to 5 (exclusive) in steps of 0.25
ys = f(xs)  # call our function f on the array
plt.plot(xs, ys)

h = 0.00000001  # very small number to calculate slope
# we can converge towards the actual number by making it smaller
x = 2 / 3
(f(x + h) - f(x)) / h
# the slope. the rate of difference. when x changes by h, the function changes this much.
# this pretty much is the derivative. the closer h gets to 0, the closer we get to the actual derivative.

a = 2.0
b = -3.0
c = 10.0
d1 = a * b + c
b += h  # differential with respect to b
# our slope will tell us the change of b affecting the result of the whole func
# partial derivative
d2 = a * b + c

print("d1", d1)
print("d2", d2)
print("slope", (d2 - d1) / h)


class Value:
    def __init__(self, data, _children=(), _op=""):
        # children will help us write expression graphs
        # to see which values produce which values
        self.data = data  # store the main value in data
        self._prev = set(_children)  # stores previous values in a tuple
        self._op = _op  # the operation the prev elements performed
        # _ means the var is meant to be used internally

    def __repr__(self):  # defines how the object is represented
        return f"Value(data={self.data} prev={self._prev} operation={self._op})"
        # without repr we get a complicated expression when we print
        # repr makes it readable and more understandable

    def __add__(self, other):
        out = Value(self.data + other.data, (self, other), "+")
        # we're adding the values we use to get the new value to the children of the new value
        # we're building an expression graph, seeing which values lead to which values
        return out

    def __mul__(self, other):
        out = Value(self.data * other.data, (self, other), "*")
        return out

        # stuff like add and mul are hardcoded, that's why it's mul and not multiply
        # these are operator overloads

    def __sub__(self, other):
        out = Value(self.data - other.data, (self, other), "-")
        return out

    def __truediv__(self, other):
        out = Value(self.data / other.data, (self, other), "/")
        return out

    # truediv is hardcoded as well
    # handles division (obviously)


a = Value(2.0)
# a # calls __repr__ under the hood
b = Value(-3.0)
# a + b # prints Value(data=-1.0)
# works because self.data and other.data are normal floats
# a.__add__(b) # also prints Value(data=-1.0)
c = Value(10.0)

d = a * b + c
print(d)

def trace(root):
    # build a set of all nodes and edges in a graph
    nodes, edges = set(), set()

    def build(v):
        if v not in nodes:
            nodes.add(v)
            for child in v._prev:
                edges.add((child, v))
                build(child)

    build(root)
    return nodes, edges


def draw_dot(root):
    dot = Digraph(format="svg", graph_attr={"rankdir": "LR"})  # left-right

    nodes, edges = trace(root)
    for n in nodes:
        uid = str(id(n))
        # for any val in graph create a rectangular node for it
        dot.node(name=uid, label="{ data %.4f }" % (n.data,), shape="record")
        if n._op:
            # if this value is the result of some operation create an op node
            dot.node(name=uid + n._op, label=n._op)
            # connect this node to it
            dot.edge(uid + n._op, uid)

    for n1, n2 in edges:
        # connect n1 to the op node of n2
        dot.edge(str(id(n1)), str(id(n2)) + n2._op)

    return dot

draw_dot(d).render(view=True) # d is the a*b + c above
