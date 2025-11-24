## DLL
### Generic Type
```code
from typing import TypeVar, Generic, Optional, Any

T = TypeVar('T')  # Generic type variable

class ListNode(Generic[T]):
    def __init__(self, val: T):
        self.val: T = val
        self.next: Optional['ListNode[T]'] = None
        self.prev: Optional['ListNode[T]'] = None

class MyLinkedList(Generic[T]):
    def __init__(self):
        self.size = 0
        # Sentinel nodes - can use None since they're never accessed for value
        self.head: ListNode[Optional[T]] = ListNode(None)
        self.tail: ListNode[Optional[T]] = ListNode(None)
        self.head.next = self.tail
        self.tail.prev = self.head
        
    def get(self, index: int) -> Optional[T]:
        """
        Get the value of the index-th node in the linked list. 
        If the index is invalid, return None.
        """
        if index < 0 or index >= self.size:
            return None
        
        # Choose the fastest way: from head or tail
        if index + 1 < self.size - index:
            curr = self.head
            for _ in range(index + 1):
                curr = curr.next
        else:
            curr = self.tail
            for _ in range(self.size - index):
                curr = curr.prev
                
        return curr.val
            
    def addAtHead(self, val: T) -> None:
        """Add a node of value val before the first element."""
        pred, succ = self.head, self.head.next
        
        self.size += 1
        to_add = ListNode(val)
        to_add.prev = pred
        to_add.next = succ
        pred.next = to_add
        succ.prev = to_add
        
    def addAtTail(self, val: T) -> None:
        """Append a node of value val to the last element."""
        succ, pred = self.tail, self.tail.prev
        
        self.size += 1
        to_add = ListNode(val)
        to_add.prev = pred
        to_add.next = succ
        pred.next = to_add
        succ.prev = to_add
        
    def addAtIndex(self, index: int, val: T) -> None:
        """Add a node of value val before the index-th node."""
        if index > self.size:
            return
        
        if index < 0:
            index = 0
        
        # Find predecessor and successor
        if index < self.size - index:
            pred = self.head
            for _ in range(index):
                pred = pred.next
            succ = pred.next
        else:
            succ = self.tail
            for _ in range(self.size - index):
                succ = succ.prev
            pred = succ.prev
        
        # Insertion
        self.size += 1
        to_add = ListNode(val)
        to_add.prev = pred
        to_add.next = succ
        pred.next = to_add
        succ.prev = to_add
        
    def deleteAtIndex(self, index: int) -> None:
        """Delete the index-th node if the index is valid."""
        if index < 0 or index >= self.size:
            return
        
        # Find predecessor and successor
        if index < self.size - index:
            pred = self.head
            for _ in range(index):
                pred = pred.next
            succ = pred.next.next
        else:
            succ = self.tail
            for _ in range(self.size - index - 1):
                succ = succ.prev
            pred = succ.prev.prev
            
        # Delete
        self.size -= 1
        pred.next = succ
        succ.prev = pred
    
    def __str__(self) -> str:
        """String representation of the list."""
        values = []
        curr = self.head.next
        while curr != self.tail:
            values.append(str(curr.val))
            curr = curr.next
        return " <-> ".join(values)
    
    def __len__(self) -> int:
        """Return the size of the list."""
        return self.size
```
```Testcase
# Integer list
int_list: MyLinkedList[int] = MyLinkedList()
int_list.addAtHead(1)
int_list.addAtTail(3)
print(int_list)  # 1 <-> 3

# String list
str_list: MyLinkedList[str] = MyLinkedList()
str_list.addAtHead("hello")
str_list.addAtTail("world")
print(str_list)  # hello <-> world

# Custom object list
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def __str__(self):
        return f"{self.name}({self.age})"

person_list: MyLinkedList[Person] = MyLinkedList()
person_list.addAtHead(Person("Alice", 30))
person_list.addAtTail(Person("Bob", 25))
print(person_list)  # Alice(30) <-> Bob(25)

# Mixed type list (using Any)
mixed_list: MyLinkedList[Any] = MyLinkedList()
mixed_list.addAtHead(42)
mixed_list.addAtTail("text")
mixed_list.addAtTail([1, 2, 3])
```