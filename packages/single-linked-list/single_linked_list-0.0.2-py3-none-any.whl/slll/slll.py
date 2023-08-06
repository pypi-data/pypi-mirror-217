class Node:
    def __init__(self, data):
        self.data = data
        self.next = None



class SingleLinkedList:

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    
    def __len__(self):
        """
        return SLLL size
        """
        return self.length


    def treaves(self):
        """
        treaves through nodes in SLLL
        """
        node = self.head
        while node is not None:
            print(node.data)
            node = node.next


    def __str__(self) -> str:
        """
        return node in SLLL
        """
        node = self.head
        result = ''
        while node is not None:
            result += str(node.data)
            if node.next is not None:
                result += ' ---> '
            node = node.next
        return result


    def append(self, data):
        """
        insert node in SLLL
        """
        node = Node(data=data)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.length += 1


    def preappend(self, data):
        """
        insert node at the beginning of SLLL
        """
        node = Node(data=data)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.next =  self.head
            self.head = node
        self.length += 1


    def insert(self, index, data):
        """
        insert a node at given index in SLLL
        """
        node = Node(data=data)
        if index < 0 or index > self.length:
            return None
        if self.length == 0:
            self.tail = self.head = node
        if index == 0:
            node.next = self.head
            self.head = node
        else:
            for _ in range(index - 1):
                temp_node = self.head
                temp_node = temp_node.next
            node.next = temp_node.next
            temp_node.next = node
        self.length += 1


    def find(self, data):
        """
        return node index from SLLL which contain data
        """
        node = self.head
        index = 0
        while node is not None:
            if node.data == data:
                return index
            node = node.next
            index += 1
        return None


    def get(self, index):
        """
        return node from SLLL by index
        """
        if index == -1:
            return self.tail.data
        if index < -1 or index > self.length:
            return None
        node = self.head
        for _ in range(index):
            node = node.next
        return node.data
    
    def _get(self, index):
        """
        return node from SLLL by index
        """
        if index == -1:
            return self.tail
        if index < -1 or index > self.length:
            return None
        node = self.head
        for _ in range(index):
            node = node.next
        return node



    def set(self, index, data):
        """
        set node in SLLL by index and value
        """
        node = self._get(index=index)
        if node:
            node.data = data
        return node.data


    def pop(self):
        """
        remove and return last node in SLLL
        """
        node = self.tail
        if self.length == 0:
            return None
        if self.length == 1:
            self.tail = self.head =  None
            return node.data
        else:
            temp = self.head
            while temp.next is not self.tail:
                temp = temp.next
            temp.next = None
            self.tail = temp
        return node.data
    

    def pop_first(self):
        """
        remove and return first node in SLLL
        """
        if self.head is None:
            return None
        node = self.head
        if self.length == 1:
            self.head = self.tail = None
            return node.data
        else:
            self.head = self.head.next
            node.next = None
        self.length -= 1
        return node.data

    
    def remove(self, index):
        """
        remove node at given index from SLLL
        """
        if index < 0 or index >= self.length:
            return None
        if index == 0:
            self.pop_first()
        if index == self.length - 1 or index == -1:
            self.pop()
        else:
            prev_node = self._get(index=index - 1)
            node = prev_node.next
            prev_node.next = node.next
            node.next = None
        self.length -= 1


    def clear(self):
        """
        clear all nodes in SLLl
        """
        self.head = self.tail = None
        self.length = 0
