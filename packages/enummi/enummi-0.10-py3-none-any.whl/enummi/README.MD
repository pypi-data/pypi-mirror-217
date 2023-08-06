# I love enumerate(), but I hate using it with zip() - this function takes care of it 

## pip install enummi 

#### Tested against Windows 10 / Python 3.10 / Anaconda 


### Combining multiple iterables: 

It allows you to merge multiple iterables into a single sequence of tuples. This can be useful when you have several related iterables and want to process them together.

### Indexing the tuples: 

The function assigns an index value to each tuple, representing the position of the elements in the original iterables. This indexing provides a convenient way to access and reference elements based on their relative positions.

### Generates results on the fly: 

As a generator function, enummi generates and yields results one at a time, as they are needed. This lazy evaluation strategy can save memory and computational resources, especially when dealing with large or infinite sequences.

### Flexibility with input: 

The function accepts a variable number of iterables as arguments (*args), allowing you to provide any number of iterables to be combined. It can handle different lengths of input iterables and adapt accordingly.

### Compatible with different iterable types: 

The function can work with various types of iterables, such as lists, tuples, strings, or any other iterable object. It is not limited to a specific data structure, providing flexibility in terms of input.

### Simple and concise implementation: 

The implementation of enummi is relatively straightforward and concise, utilizing built-in Python functions (zip and enumerate) to achieve the desired functionality. This simplicity makes the function easy to understand and maintain.

```python
from enummi import enummi

for i, a, b, c in enummi([1, 2, 3], [4, 5, 6], [7, 8, 9]):
  print(i, a, b, c)
Output:
  0 1 4 7
  1 2 5 8
  2 3 6 9

for i, a in enummi([1, 2, 3]):
  print(i, a)
Output:
  0 1
  1 2
  2 3

for i, a in enummi([]):
  print(i, a)
Output:
  (no output)
```