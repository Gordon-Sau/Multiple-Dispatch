# Multiple-Dispatch
The idea is based on this https://stackoverflow.com/a/4641463, which is a modification of the code in artima.com/weblogs/viewpost.jsp?thread=101605 by Guido van van Rossum.
However, the problem with that approach is that it is not predictable which function will be dispatched as stated in the answer.

Therefore, I have written this program. It tries to fit the type in the method resolution order (mro). 

# How it works
I created a trie-like data structure. The type of the first argument will be at the top layer, the type of the second argument will be at the second layer, and so on.
`None` deontes the end of the arguments. This allows a depth first search to be done easily.
