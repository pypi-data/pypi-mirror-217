from collections.abc import Set


class ScrewHashesSet(Set):
    """
    A custom set implementation for handling all kinds of objects (hashable or not).

    This class inherits from the `collections.abc.Set` abstract base class.

    Other advantages:

    Preserving Order:
    The ScrewHashesSet class preserves the order of elements as
    they are added to the set.
    In contrast, a normal set doesn't guarantee any specific
    order of elements.
    This can be beneficial when you need to maintain the
    insertion order or rely on the order of elements in
    operations such as iteration or string representation.

    Reproducibility:
    The ScrewHashesSet class provides a __repr__ method that
    returns a string representation of the set that can
    be used to recreate the set.
    This can be useful when you need to serialize the set
    or pass it between different parts of your code
    while preserving its state.


    Methods:
    - __init__(self, i, /): Initializes the ScrewHashesSet with elements from the iterable `i`.
    - __str__(self): Returns a string representation of the ScrewHashesSet.
    - __repr__(self): Returns a string representation that can be used to recreate the ScrewHashesSet.
    - __iter__(self): Returns an iterator over the elements of the ScrewHashesSet.
    - __contains__(self, value): Checks if the given value is present in the ScrewHashesSet.
    - __len__(self): Returns the number of elements in the ScrewHashesSet.
    """
    def __init__(self, i, /):
        r"""
        Initialize the ScrewHashesSet with elements from the iterable `i`.

        Duplicate elements are removed from the ScrewHashesSet.

        Parameters:
        - i (iterable): The iterable containing the elements to initialize the ScrewHashesSet.

        Example:

            s1 = ScrewHashesSet([[(43, 5), 1, 2], 3, {3, 4, 5, 6}, {2: 3, 3: 5}, {2: 3, 3: 6}])
            s2 = ScrewHashesSet([(2, 3), [1, 2], 3, 4, {3, 4, 5}, {2: 3, 3: 5}, {1: 32}])
            print(s1 - s2)
            print(s2 - s1)
            print(s2 | s1)
            print(s2 & s1)

            # str():  {[(43, 5), 1, 2], {3, 4, 5, 6}, {2: 3, 3: 6}}
            # repr(): ScrewHashesSet([[(43, 5), 1, 2], {3, 4, 5, 6}, {2: 3, 3: 6}])

            # str():  {(2, 3), [1, 2], 4, {3, 4, 5}, {1: 32}}
            # repr(): ScrewHashesSet([(2, 3), [1, 2], 4, {3, 4, 5}, {1: 32}])

            # str():  {(2, 3), [1, 2], 3, 4, {3, 4, 5}, {2: 3, 3: 5}, {1: 32}, [(43, 5), 1, 2], {3, 4, 5, 6}, {2: 3, 3: 6}}
            # repr(): ScrewHashesSet([(2, 3), [1, 2], 3, 4, {3, 4, 5}, {2: 3, 3: 5}, {1: 32}, [(43, 5), 1, 2], {3, 4, 5, 6}, {2: 3, 3: 6}])

            # str():  {3, {2: 3, 3: 5}}
            # repr(): ScrewHashesSet([3, {2: 3, 3: 5}])

        """
        self.elements = []
        [self.elements.append(_) for _ in i if _ not in self.elements]

    def __str__(self):
        return "{" + str(self.elements)[1:-1] + "}"

    def __repr__(self):
        return f"ScrewHashesSet({repr(self.elements)})"

    def __iter__(self):
        return iter(self.elements)

    def __contains__(self, value):
        return value in self.elements

    def __len__(self):
        return len(self.elements)

