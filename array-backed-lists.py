import numpy as np

class ArrayList:
    def __init__(self):
        self.data = np.empty(1,dtype=object)
        self.size = 0
    # subscript-based access ###
    def _normalize_idx(self,idx):
        if idx < 0:
            idx += self.size
        if idx < 0 or idx > self.size - 1:
            raise IndexError('Index out of range!')
        return idx

    def __getitem__(self, idx):
        """Implements `x = self[idx]`"""
        assert (isinstance(idx, int))
        idx = self._normalize_idx(idx)
        return self.data[idx]
        
    def __setitem__(self, idx, value):
        """Implements `self[idx] = x`"""
        assert (isinstance(idx, int))
        idx = self._normalize_idx(idx)
        self.data[idx] = value
        
    def __delitem__(self, idx):
        """Implements `del self[idx]`"""
        assert (isinstance(idx, int))
        idx = self._normalize_idx(idx)
        for i in range(idx, self.size - 1):
            self.data[i] = self.data[i + 1]
        self.size -= 1
    ## stringification ##
    def __str__(self):
        """Implements `str(self)`. Returns '[]' if the list is empty, else
        returns `str(x)` for all values `x` in this list, separated by commas
        and enclosed by square brackets. E.g., for a list containing values
        1, 2 and 3, returns '[1, 2, 3]'."""
        
        return '[' + ', '.join(str(self.data[i]) for i in range(self.size)) + ']'
        
    def __repr__(self):
        """Supports REPL inspection."""
        return '[' + ', '.join(repr(self.data[i]) for i in range(self.size)) + ']'

    
    ## single-element manipulation ###
    
    def _check_expand_array(self):
        if self.size == len(self.data):
            ndata = np.empty(len(self.data) * 2, dtype=object)
            for i in range(len(self.data)):
                ndata[i] = self.data[i]
            self.data = ndata

    def append(self, value):
        """Appends value to the end of this list."""
        self._check_expand_array()    
        self.data[self.size] = value
        self.size += 1
        
 
    def insert(self, idx, value):
        """Inserts value at position idx, shifting the original elements down the
        list, as needed. Note that inserting a value at len(self) --- equivalent
        to appending the value --- is permitted. Raises IndexError if idx is invalid."""
        self.size += 1
        idx = self._normalize_idx(idx)
        self._check_expand_array()
        for i in range(self.size -1, idx, -1):
            self.data[i] = self.data[i-1]
        self.data[idx] = value
                
    def pop(self, idx=-1):
        """Deletes and returns the element at idx (which is the last element,
        by default)."""
        element = self.data[idx]
        self.__delitem__(idx)
        
        return element

    def remove(self, value):
        """Removes the first (closest to the front) instance of value from the
        list. Raises a ValueError if value is not found in the list."""
        for i in range(self.size):
            if self.data[i] == value:
                self.__delitem__(i)
                break
        else:
            raise ValueError('Value not in the list!')
        
    ### predicates (T/F queries) ###

    def __eq__(self, other):
        """Returns True if this ArrayList contains the same elements (in order) as
        other. If other is not an ArrayList, returns False."""
        if type(other) != type(self):
            return False
        try:
            for i in range(other.index(self.data[0]), self.size):
                if self.data[i] != other.data[i]:
                    return False
            else:
                return True 
        except ValueError:
            return False

    def __contains__(self, value):
        """Implements `val in self`. Returns true if value is found in this list."""
        for i in range(self.size):
            if self.data[i] == value:
                return True
        else:
            return False
        

        ### queries ###

    def __len__(self):
        """Implements `len(self)`"""
        return self.size

    def min(self):
        """Returns the minimum value in this list."""
        n = self.data[0]
        for i in range(1, self.size):
            if self.data[i] < n:
                n = self.data[i]
        return n
        
    def max(self):
        """Returns the maximum value in this list."""
        n = self.data[0]
        for i in range(1, self.size):
            if self.data[i] > n:
                n = self.data[i]
        return n
        

    def index(self, value, i=0, j=None):
        """Returns the index of the first instance of value encountered in
        this list between index i (inclusive) and j (exclusive). If j is not
        specified, search through the end of the list for value. If value
        is not in the list, raise a ValueError."""
        try:
            if j is None:
                j = self.size
            else:
                j = self._normalize_idx(j)
            i = self._normalize_idx(i)
        except IndexError:
            raise ValueError
        for k in range(i, j):
            if value == self.data[k]:
                return k
        else:
            raise ValueError('Value not in the list!')
        
    def count(self, value):
        """Returns the number of times value appears in this list."""
        count = 0
        for i in range(self.size):
            if self.data[i] == value:
                count += 1
        return count
        
    ### bulk operations ###

    def __add__(self, other):
        """Implements `self + other_array_list`. Returns a new ArrayList
        instance that contains the values in this list followed by those
        of other."""
        array = ArrayList()
        for i in range(self.size):
            array.append(self.data[i])
        for i in range(other.size):
            array.append(other.data[i])
        return array

    def clear(self):
        self.data = np.empty(1, dtype=object)
        self.size = 0

    def copy(self):
        """Returns a new ArrayList instance (with a separate data store), that
        contains the same values as this list."""
        array = ArrayList()
        for i in range(self.size):
            array.append(self.data[i])
        return array

    def extend(self, other):
        """Adds all elements, in order, from other --- an Iterable --- to this list."""
        for i in other:
            self.append(i)

    ### iteration ###

    def __iter__(self):
        """Supports iteration (via `iter(self)`)"""
        for i in range(len(self.data)):
            yield self.data[i]
