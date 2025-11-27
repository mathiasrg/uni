from dataclasses import dataclass
from typing import Optional
from typing import List


@dataclass
class LL:
    first: int
    rest: Optional[LL]

test =  LL(1,LL(2,LL(3,LL(4, LL(5, LL(6, LL(7, None)))))))

def sum(v:LL|None) -> int:
    if not v:
        return 0
    else:
        return v.first + sum(v.rest)


print("Sum test: ", sum(test))

def even_length(v:LL|None) -> int:
    evens = 0;
    if not v:
        return 0

    if v.first % 2 == 0:
        evens = evens + 1 + even_length(v.rest)
    else:
        evens = evens + even_length(v.rest)

    return evens

print("Even length test: ", even_length(test))

def increasing(v:LL|None) -> bool:
    if not v or not v.rest:
        return True

    if v.first < v.rest.first:
        return increasing(v.rest)
    else:
        return False

print("Increasing test: ", increasing(test))

def consec(v:LL|None) -> bool:
    if not v or not v.rest:
        return False

    if v.first == v.rest.first:
        return True
    else:
        return consec(v.rest)

print("Consec test: ", consec(test))

list_test = [1,2,3,4,5,6,2,3,4,2,5,4]

def remove_all(x:int, v:List[int]) -> List[int]:
   return [y for y in v if y != x]

print("Remove all test: ", remove_all(2, list_test))

list_test_2 = [1,2,3]
list_test_3 = [4,5,6]
def add(v:List[int],w:List[int]) -> List[int]:
    return v + w

print("Add test: ", add(list_test_2, list_test_3))

def square(n:int) -> List[int]:
    return [i*i for i in range(n, 0, -1)]

print("Square test: ", square(6))
