import helper
import random
import itertools
import sys

def swap(a, x, y):
    a[x], a[y] = a[y], a[x]

def selection_sort(a):
    for i in range(len(a)):
        min_index = i
        min_value = a[i]
        for j in range(i+1, len(a)):
            if a[j] < min_value:
                min_index = j
                min_value = a[j]
            yield (min_index, j)
        #min_index = min(range(len(a[i:])), key=lambda x: a.__getitem__(x+i))
        swap(a, i, min_index)

def bubble_sort(a):
    for j in range(len(a)-1, 0, -1):
        for i in range(j):
            yield (i, i+1)
            if a[i] > a[i+1]:
                swap(a, i, i+1)
            
def insertion_sort(a):
    for i in range(1, len(a)):
        j = i
        while j > 0 and a[j-1] > a[j]:
            yield (j-1, j)
            swap(a, j-1, j)
            j -= 1

def bogosort(a):
    while any(a[i] > a[i+1] for i in range(len(a)-1)):
        random.shuffle(a)
        yield

def bogosort2(a):
    for permutation in itertools.permutations(a):
        for i in range(len(permutation)):
            a[i] = permutation[i]
        yield
        if all(a[i] <= a[i+1] for i in range(len(a)-1)):
            return

def gnome_sort(a):
    pos = 0
    while pos < len(a):
        if pos == 0 or a[pos] >= a[pos-1]:
            pos += 1
        else:
            swap(a, pos, pos-1)
            pos -= 1
        yield (pos, pos-1)

def quicksort(a):
    if len(a) <2:
        return
    todo = [(0, len(a)-1)]
    while todo:
        lo, hi = todo.pop()
        
        # Partition the list
        pivot_index = lo
        pivot = a[lo]
        i = lo - 1
        j = hi + 1
        while i < j:
            i += 1
            while a[i] < pivot:
                yield (i, pivot_index)
                i += 1
            j -= 1
            while a[j] > pivot:
                yield (i, pivot_index)
                j -= 1
            if i < j:
                if i == pivot_index:
                    pivot_index = j
                elif j == pivot_index:
                    pivot_index = i
                swap(a, i, j)
        
        # Add the right side to the todo
        if j + 1 < hi:
            todo.append((j+1, hi))
        # Add the left side to the todo
        if lo < j:
            todo.append((lo, j))

def quicksort_with_random_pivot(a):
    if len(a) <2:
        return
    todo = [(0, len(a)-1)]
    while todo:
        lo, hi = todo.pop()
        swap(a, lo, random.randint(lo, hi))

        # Partition the list
        pivot_index = random.randint(lo, hi)
        pivot = a[pivot_index]
        i = lo - 1
        j = hi + 1
        while i < j:
            i += 1
            while a[i] < pivot:
                yield (i, pivot_index)
                i += 1
            j -= 1
            while a[j] > pivot:
                yield (i, pivot_index)
                j -= 1
            if i < j:
                if i == pivot_index:
                    pivot_index = j
                elif j == pivot_index:
                    pivot_index = i
                swap(a, i, j)
        
        # Add the right side to the todo
        if j + 1 < hi:
            todo.append((j+1, hi))
        # Add the left side to the todo
        if lo < j:
            todo.append((lo, j))

def cocktail_shaker_sort(a):
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(a)-1):
            if a[i] > a[i+1]:
                swap(a, i, i+1)
                swapped = True
                yield (i, i+1)
        if not swapped:
            break
        swapped = False
        for i in range(len(a)-2, 1, -1):
            if a[i] > a[i+1]:
                swap(a, i, i+1)
                swapped = True
                yield (i, i+1)
            
def shellsort(a):
    gaps = [701, 301, 132, 57, 23, 10, 4, 1]

    for gap in gaps:
        for i in range(gap, len(a)):
            temp = a[i]
            j = i
            while j >= gap and a[j - gap] > temp:
                yield (j-gap, i)
                a[j] = a[j - gap]
                j -= gap
            a[j] = temp

def odd_even_sort(a):
    sorted = False
    while not sorted:
        sorted = True
        for i in range(1, len(a)-1, 2):
            yield (i, i+1)
            if a[i] > a[i+1]:
                swap(a, i, i+1)
                sorted = False
        
        for i in range(0, len(a)-1, 2):
            yield (i, i+1)
            if a[i] > a[i+1]:
                swap(a, i, i+1)
                sorted = False

def circle_sort(a):
    def circle_sort_inner(a, lo, hi, swaps):
        if lo == hi:
            return
        
        lower = lo
        upper = hi
        mid = (hi - lo)//2
        
        while lo < hi:
            yield (lo, hi)
            if a[lo] > a[hi]:
                swap(a, lo, hi)
                swaps['a'] += 1
            lo += 1
            hi -= 1
        
        if lo == hi:
            yield (lo, hi + 1)
            if a[lo] > a[hi + 1]:
                swap(a, lo, hi+1)
                swaps['a']
        
        yield from circle_sort_inner(a, lower, lower+mid, swaps)
        yield from circle_sort_inner(a, lower+mid+1, upper, swaps)
    
    swaps = {'a': 1}
    while swaps['a']:
        swaps['a'] = 0
        yield from circle_sort_inner(a, 0, len(a)-1, swaps)

def stooge_sort(a):
    def stooge_sort_inner(left, right):
        yield (left, right)
        if a[left] > a[right]:
            swap(a, left, right)

        if right - left > 1:
            third = (right - left + 1) // 3
            yield from stooge_sort_inner(left, right - third)
            yield from stooge_sort_inner(left + third, right)
            yield from stooge_sort_inner(left, right - third)

    yield from stooge_sort_inner(0, len(a) - 1)

def combsort(a):
  gap = len(a)
  swapped = True
  while gap > 1 or swapped:
    gap = max(1, int(gap / 1.25))
    swapped = False
    for i in range(len(a) - gap):
      j = i + gap
      yield (i, j)
      if a[i] > a[j]:
        swap(a, i, j)
        swapped = True

def cycle_sort(a):
  for cycle_start in range(0, len(a) - 1):
    i = cycle_start
    item = a[i]
    pos = cycle_start

    for j in range(cycle_start + 1, len(a)):
        yield (i, j)
        if a[j] < item:
            pos += 1
    
    if pos == cycle_start:
        continue
    
    while item == a[pos]:
        yield (i, pos)
        pos += 1
    a[pos], item = item, a[pos]
    i = pos
    

    while pos != cycle_start:
        yield (i, pos)
        pos = cycle_start
        for j in range(cycle_start + 1, len(a)):
            yield (i, pos)
            if a[j] < item:
                pos += 1
      
        while item == a[pos]:
            yield (i, pos)
            pos += 1
        a[pos], item = item, a[pos]
        i = pos