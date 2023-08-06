# Singly Linked List

This is a Python implementation of a singly linked list.

## Usage

# Singly Linked List

This is a Python implementation of a singly linked list.

## Installation

Install the `SingleLinkedList` package from PyPI using `pip`:

```bash
pip install single-linked-list==0.0.1
````

then, import the `SingleLinkedList` class

```python
from slll.slll import SingleLinkedList
```

Initialize a Singly Linked List

```python
single_linked_list = SingleLinkedList()
```

## Methods

### * Append 
- inserts a new node at the end of the linked list.

#### Method: 
- append(data)

`data(any)` : The data to be stored in the new node.
```python
single_linked_list.append(1)
single_linked_list.append(2)
```

### * Preappend
- inserts a new node at the beginning of the linked list.

#### Method: 
- preappend(data)

`data(any)` : The data to be stored in the new node.

```python
single_linked_list.preappend(0)
```

### * Insert
- inserts a new node at the specified index in the linked list.

#### Method: 
- insert(index, data)

`index(int)` : The index where the new node should be inserted.
`data(any)` : The data to be stored in the new node.

```python
single_linked_list.insert(2, 3)
```

### * Find
- returns the index of the first node containing the specified data.

#### Method: 
- find(data)

`data(any)`: The data to search for.

```python
index = single_linked_list.find(2)
print(index)  # Output: 1
```

### * Get
- returns the node at the specified index.

#### Method: 
- get(index)

`index(int)` : The index of the desired node.

```python
node = single_linked_list.get(2)
print(node.data)  # Output: 3
```

### * Set
- updates the data of the node at the specified index.

#### Method: 
- set(index, data)

`index(int)` : The index of the node to be updated.
`data(any)` : The new data to be stored in the node.

```python
single_linked_list.set(0, 9000)
```

### * Pop
- removes and returns the last node in the linked list.

#### Method: 
- pop()

```python
last_node = single_linked_list.pop()
print(last_node)  # Output: 3
```

### * Pop First
- removes and returns the first node in the linked list.

#### Method: 
- pop_first()

```python
first_node = single_linked_list.pop_first()
print(first_node)  # Output: 0
```

### * Remove
- removes the node at the specified index from the linked list.

#### Method: 
- remove(index)

`index(int)` : The index of the node to be removed.

```python
single_linked_list.remove(2)
```

### * Clear
- clears all nodes in the linked list.

#### Method: 
- clear()

```python
single_linked_list.clear()
```

### * Get Length
- returns the current size (length) of the linked list.

#### Method:
-  __len__()

```python
length = len(single_linked_list)
print(length)  # Output: 1
```

### * Traverse and print
- traverses the linked list and prints the data of each node.

#### Method: 
- traverse()

```python
single_linked_list.traverse()
# Output: 0 -> 1 -> 3
``` 

### * String representation
- returns a string representation of the linked list.

#### Method: 
- __str__()

```python
linked_list_str
```