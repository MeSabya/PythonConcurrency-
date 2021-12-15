# Iterable and Iterators
## Iterable
- In Python an iterable is an object which can be looped over its member elements using a for loop.
- Example: lists, strings and tuples. They support efficient access via indexing. The __getitem()__ can be invoked to return a member at the specified index. They also return their lengths via the __length()__ method.
- Dictionaries, sets, file objects and generators aren't indexable but are iterable.
- In order to qualify as an iterable, an object must define one of the two methods:

	 ✔__iter__()  

	 ✔__getitem__()
  
  - Container objects need to define the __iter__() method to support iteration. 
  - The __iter__() method returns an iterator for the object. Using the iterator we can sequentially access the elements of an iterable object.

## Iterator
- Iterator is an object which can be used to sequentially access the elements of an Iterable object.
- An iterator must support the following methods:

  ✔__iter__()

  ✔__next__()
  
  ## Example:
  ```python
  if __name__ == "__main__":
    lstOfInts = list()
    lstOfInts.append(1)
    lstOfInts.append(2)
    lstOfInts.append(3)

    # get iterator of list using __iter__()
    it = lstOfInts.__iter__()
    print("iterator of list: " + str(it))

    # get member element of list using __getitem__()
    print("iterator of list: " + str(lstOfInts.__getitem__(2)))

    # iterator returns itself when passed to the iter function
    print("it is iter(it) = " + str(it is iter(it)))

    # get another iterator for list using the built in iter() method
    it_another = iter(lstOfInts)
    print("it_another = " + str(it_another))

    print("iteration using iterator in a for loop")
    # iterate using the iterator
    for element in it_another:
        print(element)

    print("iteration using iterable in a for loop")
    # iterate using the iterable
    for element in lstOfInts:
        print(element)
  ```
