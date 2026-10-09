# Binary Search: A Complete Guide

## Table of Contents

1. Introduction
2. The Core Idea
3. A Worked Example
4. The Algorithm in Detail
5. Implementations in Several Languages
6. Complexity Analysis
7. Correctness and Loop Invariants
8. Common Pitfalls
9. Boundary Variations
10. Searching Rotated and Special Arrays
11. Binary Search on the Answer
12. Binary Search on Real Numbers
13. Standard Library Support
14. Comparison with Other Search Techniques
15. Testing Your Implementation
16. Practice Problems
17. Summary

---

## 1. Introduction

Binary search is one of the most fundamental algorithms in computer science. Given a collection that is **sorted**, it finds a target value (or reports that the value is absent) by repeatedly cutting the region of interest in half. Where a linear scan might need to inspect every element, binary search needs only about `log2(n)` comparisons. For a sorted list of one million items, that is roughly 20 comparisons instead of up to 1,000,000. For a billion items it is about 30.

The idea is familiar from everyday life. When you look up a word in a printed dictionary, you do not start on page one. You open the book near the middle, see whether your word comes before or after the page you landed on, and then repeat the process on the relevant half. Guessing a number between 1 and 100 in the game "higher or lower" is the same thing: the best strategy is always to guess the midpoint.

### A short history

The concept was described as early as 1946 by John Mauchly in the context of early computing. Despite its apparent simplicity, the first published binary search that worked correctly for arrays of every size did not appear until 1962. Donald Knuth noted in *The Art of Computer Programming* that while the idea is simple, the details are surprisingly easy to get wrong. A famous example came in 2006, when Joshua Bloch reported that the binary search in the Java standard library, which had been in use for nearly a decade, contained an integer overflow bug that only manifested with very large arrays. We will return to this bug in the pitfalls section.

### What you will learn

This guide covers:

- the algorithm and the intuition behind it;
- iterative and recursive implementations;
- a rigorous argument for why it is correct and fast;
- the mistakes that trip up even experienced programmers;
- the many variations (first occurrence, last occurrence, insertion point);
- how to apply binary search to problems that do not look like searching an array at all.

The code examples are mostly in Python, with additional versions in C++, Java, and JavaScript.

---

## 2. The Core Idea

Binary search relies on one key property: **the data is ordered**, so a single comparison tells you which half of the remaining data can be discarded.

Suppose you are looking for the value `x` in a sorted array `A`. Look at the middle element `A[mid]`:

- If `A[mid] == x`, you are done.
- If `A[mid] < x`, then everything to the left of `mid` is also smaller than `x` (because the array is sorted), so `x` cannot be there. Discard the left half and `mid` itself.
- If `A[mid] > x`, then everything to the right of `mid` is also larger than `x`. Discard the right half and `mid` itself.

Each step removes at least half of the candidates. After `k` steps, at most `n / 2^k` candidates remain. The search ends when no candidates remain or the target is found.

### Preconditions

Binary search requires:

1. **Random access.** You must be able to jump to the middle element in constant time. Arrays and array-backed lists qualify. Linked lists do not, because finding the middle takes linear time, which destroys the benefit.
2. **Sorted order.** The order must be consistent with the comparison you use. If the array is sorted ascending and you compare as if it were descending, the algorithm will silently return wrong answers.
3. **A consistent comparison.** The comparison function must define a strict weak ordering. Comparing floating-point values with `NaN` present, for example, breaks this assumption.

### A more general view

The most powerful way to think about binary search is not as "finding a value in an array" but as **finding the boundary in a monotonic predicate**. Imagine a sequence of booleans that looks like this:

```
false false false false true true true true
```

Binary search can find the position of the first `true` in `O(log n)` time. Searching for a value `x` in a sorted array is just the special case where the predicate is `A[i] >= x`. Once you adopt this view, many seemingly unrelated problems (computing square roots, finding the minimum capacity of a shipping container, locating the first buggy commit in a history) turn out to be binary search problems.

---

## 3. A Worked Example

Consider the sorted array:

```
index:  0   1   2   3    4    5    6    7    8    9
value:  2   5   8   12   16   23   38   56   72   91
```

We want to find `target = 23`.

**Step 1.** `low = 0`, `high = 9`. `mid = 0 + (9 - 0) // 2 = 4`. `A[4] = 16`. Since `16 < 23`, the target must be to the right. Set `low = 5`.

**Step 2.** `low = 5`, `high = 9`. `mid = 5 + (9 - 5) // 2 = 7`. `A[7] = 56`. Since `56 > 23`, the target must be to the left. Set `high = 6`.

**Step 3.** `low = 5`, `high = 6`. `mid = 5 + (6 - 5) // 2 = 5`. `A[5] = 23`. Found. Return index `5`.

Only three comparisons were needed for a ten-element array.

Now consider searching for `target = 7`, which is not in the array.

| Step | low | high | mid | A[mid] | Decision          |
|------|-----|------|-----|--------|-------------------|
| 1    | 0   | 9    | 4   | 16     | 16 > 7, high = 3  |
| 2    | 0   | 3    | 1   | 5      | 5 < 7, low = 2    |
| 3    | 2   | 3    | 2   | 8      | 8 > 7, high = 1   |
| 4    | 2   | 1    | n/a | n/a    | low > high, stop  |

When `low` exceeds `high`, the search range is empty and we conclude the value is absent. Notice that at this point `low = 2`, which is exactly the index where `7` would need to be inserted to keep the array sorted. This is not a coincidence, and we will exploit it later.

---

## 4. The Algorithm in Detail

### Pseudocode

```
function binary_search(A, target):
    low  <- 0
    high <- length(A) - 1

    while low <= high:
        mid <- low + (high - low) / 2      // integer division

        if A[mid] == target:
            return mid
        else if A[mid] < target:
            low <- mid + 1
        else:
            high <- mid - 1

    return NOT_FOUND
```

### Design decisions

Several small choices define a binary search implementation. Understanding them is the key to getting it right.

**Inclusive versus exclusive bounds.** In the version above, both `low` and `high` are *inclusive*: the search range is `[low, high]`. An alternative is the half-open range `[low, high)`, where `high` is one past the last candidate. In that style, the loop condition is `low < high`, and when the target is smaller you set `high = mid` rather than `mid - 1`. Both styles are correct as long as you are consistent. Mixing them is the single most common source of bugs.

**Computing the midpoint.** The expression `(low + high) / 2` is mathematically correct but can overflow when `low + high` exceeds the maximum integer value. The safe form is `low + (high - low) / 2`. In Python, integers have arbitrary precision so the problem does not occur, but writing the safe form is a good habit.

**Returning on equality versus continuing.** The basic version returns as soon as it finds a match. This is fine when values are unique. If duplicates exist and you need the first or last occurrence, you must continue searching after a match. Section 9 covers this.

**What to return when not found.** Returning `-1` is common, but it throws away useful information. A better design returns the insertion point, as Python's `bisect` module does, or returns `-(insertion_point) - 1`, as Java's `Arrays.binarySearch` does.

### Recursive formulation

Binary search can be expressed recursively because each step reduces the problem to a smaller instance of itself:

```
function search(A, target, low, high):
    if low > high:
        return NOT_FOUND
    mid <- low + (high - low) / 2
    if A[mid] == target:
        return mid
    else if A[mid] < target:
        return search(A, target, mid + 1, high)
    else:
        return search(A, target, low, mid - 1)
```

The recursion depth is `O(log n)`, so stack overflow is not a practical concern. However, because the recursive call is always the last action (tail position), the iterative version is typically preferred. It uses constant extra space and avoids function call overhead.

---

## 5. Implementations in Several Languages

### Python (iterative)

```python
def binary_search(arr, target):
    """Return the index of target in sorted arr, or -1 if absent."""
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = low + (high - low) // 2

        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1
```

### Python (recursive)

```python
def binary_search_recursive(arr, target, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low > high:
        return -1

    mid = low + (high - low) // 2

    if arr[mid] == target:
        return mid
    if arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    return binary_search_recursive(arr, target, low, mid - 1)
```

### C++

```cpp
#include <vector>

int binarySearch(const std::vector<int>& arr, int target) {
    int low = 0;
    int high = static_cast<int>(arr.size()) - 1;

    while (low <= high) {
        int mid = low + (high - low) / 2;

        if (arr[mid] == target) return mid;
        if (arr[mid] < target)  low = mid + 1;
        else                    high = mid - 1;
    }
    return -1;
}
```

### Java

```java
public static int binarySearch(int[] arr, int target) {
    int low = 0;
    int high = arr.length - 1;

    while (low <= high) {
        int mid = low + (high - low) / 2;   // or (low + high) >>> 1

        if (arr[mid] == target) return mid;
        if (arr[mid] < target)  low = mid + 1;
        else                    high = mid - 1;
    }
    return -1;
}
```

### JavaScript

```javascript
function binarySearch(arr, target) {
  let low = 0;
  let high = arr.length - 1;

  while (low <= high) {
    const mid = low + Math.floor((high - low) / 2);

    if (arr[mid] === target) return mid;
    if (arr[mid] < target) low = mid + 1;
    else high = mid - 1;
  }
  return -1;
}
```

### Go

```go
func binarySearch(arr []int, target int) int {
    low, high := 0, len(arr)-1

    for low <= high {
        mid := low + (high-low)/2

        switch {
        case arr[mid] == target:
            return mid
        case arr[mid] < target:
            low = mid + 1
        default:
            high = mid - 1
        }
    }
    return -1
}
```

### Searching with a custom comparator

Often you do not search for a raw number but for a record by some key. Python's `bisect` accepts a `key` function (Python 3.10+), and you can write your own version as well:

```python
def binary_search_by(items, target, key):
    low, high = 0, len(items) - 1
    while low <= high:
        mid = low + (high - low) // 2
        k = key(items[mid])
        if k == target:
            return mid
        if k < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


people = [
    {"name": "Ana",   "age": 19},
    {"name": "Ben",   "age": 24},
    {"name": "Chloe", "age": 31},
    {"name": "Dev",   "age": 45},
]

idx = binary_search_by(people, 31, key=lambda p: p["age"])
print(people[idx]["name"])   # Chloe
```

The list must be sorted by the same key used in the search.

---

## 6. Complexity Analysis

### Time complexity

Let `T(n)` be the number of comparisons needed in the worst case for an array of `n` elements. Each iteration examines one element and then reduces the problem to at most `floor(n / 2)` elements. This gives the recurrence:

```
T(n) = T(floor(n / 2)) + 1,    T(0) = 0
```

Unrolling it, after `k` iterations the range has at most `n / 2^k` elements. The range becomes empty when `n / 2^k < 1`, that is, when `k > log2(n)`. The worst case is therefore:

```
T(n) = floor(log2(n)) + 1
```

So binary search runs in **O(log n)** time in the worst case and on average. The best case is **O(1)**, when the target happens to be at the first midpoint.

To make this tangible:

| Array size n       | Worst-case comparisons |
|--------------------|------------------------|
| 10                 | 4                      |
| 1,000              | 10                     |
| 1,000,000          | 20                     |
| 1,000,000,000      | 30                     |
| 1,000,000,000,000  | 40                     |

Doubling the data adds just one more comparison. This is what makes logarithmic algorithms so powerful.

### Space complexity

The iterative version uses a constant number of variables, so its space complexity is **O(1)**. The recursive version uses **O(log n)** stack space, one frame per level of recursion.

### The cost of sorting

Binary search requires sorted data. Sorting costs `O(n log n)`. This means:

- If you search only once, sorting first and then binary searching is slower than a simple linear scan, which costs `O(n)`.
- If you search many times, the sorting cost is amortized. For `m` searches, the total cost is `O(n log n + m log n)` versus `O(m * n)` for repeated linear scans. The break-even point is surprisingly low, around `log n` searches.

### Real-world performance notes

Big-O hides constants. On modern hardware, a few effects matter:

- **Cache behavior.** Binary search jumps around memory. For very large arrays, each probe may cause a cache miss. For small arrays (a few dozen elements), a linear scan can be faster because it reads memory sequentially and the CPU can predict branches.
- **Branch misprediction.** The comparison outcome in each iteration is essentially random, so the CPU's branch predictor performs poorly. Branchless implementations that use conditional moves can be noticeably faster.
- **Memory layouts.** Layouts such as the Eytzinger (breadth-first) order or B-trees reorder data to improve cache locality for repeated searches.

---

## 7. Correctness and Loop Invariants

It is not enough to say the algorithm "seems right." Because binary search is so prone to subtle errors, it is worth reasoning about it formally using a **loop invariant**.

### The invariant

For the inclusive-bounds version, the invariant is:

> At the start of every iteration, if `target` is present in the array, then its index lies in the range `[low, high]`.

### Initialization

Before the first iteration, `low = 0` and `high = n - 1`. The range `[0, n - 1]` covers the entire array, so the invariant holds trivially.

### Maintenance

Assume the invariant holds at the start of an iteration, and `low <= high`. Let `mid` be the midpoint. There are three cases:

1. `A[mid] == target`. We return `mid`, which is correct.
2. `A[mid] < target`. Because the array is sorted, every `A[i]` with `i <= mid` satisfies `A[i] <= A[mid] < target`. None of these can equal the target. So if the target exists, its index is in `[mid + 1, high]`. Setting `low = mid + 1` preserves the invariant.
3. `A[mid] > target`. By symmetry, every `A[i]` with `i >= mid` is greater than the target. If the target exists, its index is in `[low, mid - 1]`. Setting `high = mid - 1` preserves the invariant.

### Termination

In each iteration that does not return, the quantity `high - low + 1` (the size of the range) strictly decreases. This is because `mid` lies in `[low, high]`, and we exclude at least `mid` from the new range. A strictly decreasing non-negative integer cannot decrease forever, so the loop terminates.

### Conclusion

When the loop exits, `low > high`, meaning the range is empty. By the invariant, if the target were present its index would have to be in an empty range, which is impossible. Therefore the target is absent, and returning "not found" is correct.

### A useful corollary

When the loop exits without finding the target, `low` equals the index of the first element greater than the target (or `n` if there is none). This is the *insertion point*. This follows from the fact that all elements before `low` are known to be smaller than the target, and all elements from `high + 1 = low` onward are known to be larger.

---

## 8. Common Pitfalls

Knuth observed that although the first binary search was published in 1946, the first bug-free version did not appear until 1962. These are the mistakes that most often cause problems.

### 8.1 Integer overflow in the midpoint

In languages with fixed-width integers, `(low + high) / 2` can overflow when `low` and `high` are both large. With 32-bit signed integers, if `low = 1.5 billion` and `high = 1.6 billion`, the sum exceeds 2^31 - 1 and wraps to a negative number. The resulting `mid` is negative and the program crashes or misbehaves.

This is the bug that sat in the Java standard library until 2006. It went unnoticed because arrays with more than about a billion elements were rare when the code was written. Safe alternatives:

```java
int mid = low + (high - low) / 2;
int mid = (low + high) >>> 1;   // unsigned shift, valid in Java
```

### 8.2 Off-by-one errors in the bounds

Choosing between `<` and `<=` in the loop condition, and between `mid` and `mid + 1` in the updates, must match your range convention.

| Convention        | Initial high | Loop condition | Update when too small | Update when too large |
|-------------------|--------------|----------------|-----------------------|-----------------------|
| Inclusive `[l,h]` | `n - 1`      | `low <= high`  | `low = mid + 1`       | `high = mid - 1`      |
| Half-open `[l,h)` | `n`          | `low < high`   | `low = mid + 1`       | `high = mid`          |

Mixing these, for example initializing `high = n` but using `low <= high`, will eventually read `arr[n]`, which is out of bounds.

### 8.3 Infinite loops

An infinite loop happens when neither bound moves. Consider this broken version:

```python
# BROKEN: can loop forever
while low < high:
    mid = (low + high) // 2
    if arr[mid] < target:
        low = mid        # should be mid + 1
    else:
        high = mid
```

When `high = low + 1`, `mid` equals `low`. If `arr[mid] < target`, `low` is set to `mid`, which equals itself, and nothing changes. The fix is `low = mid + 1`. When you write a variant where you do set a bound to `mid`, make sure the midpoint rounds in the right direction. For a lower midpoint (floor), only `high = mid` is safe. For an upper midpoint (`mid = low + (high - low + 1) // 2`), only `low = mid` is safe.

### 8.4 Searching unsorted data

Binary search on unsorted data does not raise an error. It returns wrong answers quietly. If a search seems to randomly fail on valid inputs, verify that the data is sorted, and sorted by the same criterion used in the comparison. A frequent cause is data sorted case-insensitively but searched case-sensitively, or sorted as strings but searched as numbers (so `"10"` sorts before `"9"`).

### 8.5 Duplicates

With duplicate values, the basic algorithm returns *some* index of a matching element, not necessarily the first or last. If your program depends on which one, use the boundary variations in the next section.

### 8.6 Floating-point equality

Comparing floating-point numbers with `==` is unreliable. When binary searching over real values, never rely on exact equality as the stopping condition. Section 12 explains the right approach.

### 8.7 Using it on the wrong data structure

Binary search on a linked list costs `O(n)` to reach the midpoint on each step, giving `O(n)` overall (or worse). Use an array, or switch to a balanced search tree, skip list, or hash table.

---

## 9. Boundary Variations

Many real problems ask for more than "is the value present." They ask about the **boundary** where something changes. The two fundamental operations are the *lower bound* and the *upper bound*.

- **Lower bound:** the index of the first element that is **greater than or equal to** the target.
- **Upper bound:** the index of the first element that is **strictly greater than** the target.

Both return `n` if no such element exists. Using the half-open convention:

```python
def lower_bound(arr, target):
    """First index i such that arr[i] >= target (or len(arr))."""
    low, high = 0, len(arr)
    while low < high:
        mid = low + (high - low) // 2
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid
    return low


def upper_bound(arr, target):
    """First index i such that arr[i] > target (or len(arr))."""
    low, high = 0, len(arr)
    while low < high:
        mid = low + (high - low) // 2
        if arr[mid] <= target:
            low = mid + 1
        else:
            high = mid
    return low
```

The only difference between the two is `<` versus `<=`.

### Derived operations

With these two functions, a whole family of questions becomes easy:

```python
arr = [1, 2, 2, 2, 3, 5, 5, 8]

# First occurrence
i = lower_bound(arr, 2)
first = i if i < len(arr) and arr[i] == 2 else -1          # 1

# Last occurrence
j = upper_bound(arr, 2) - 1
last = j if j >= 0 and arr[j] == 2 else -1                  # 3

# Count of a value
count = upper_bound(arr, 2) - lower_bound(arr, 2)           # 3

# Does the value exist?
exists = lower_bound(arr, 5) != upper_bound(arr, 5)         # True

# Number of elements strictly less than x
less = lower_bound(arr, 3)                                  # 4

# Number of elements less than or equal to x
leq = upper_bound(arr, 3)                                   # 5

# Number of elements in the range [a, b]
in_range = upper_bound(arr, 5) - lower_bound(arr, 2)        # 6
```

### Floor and ceiling

The *floor* of `x` is the largest element less than or equal to `x`. The *ceiling* is the smallest element greater than or equal to `x`.

```python
def floor_value(arr, x):
    i = upper_bound(arr, x) - 1
    return arr[i] if i >= 0 else None

def ceiling_value(arr, x):
    i = lower_bound(arr, x)
    return arr[i] if i < len(arr) else None
```

### The general template

Nearly every binary search can be written in this shape, which finds the first index where a monotonic predicate becomes true:

```python
def first_true(low, high, predicate):
    """Smallest x in [low, high) with predicate(x) True; high if none."""
    while low < high:
        mid = low + (high - low) // 2
        if predicate(mid):
            high = mid
        else:
            low = mid + 1
    return low
```

The lower bound is `first_true(0, n, lambda i: arr[i] >= target)`. The upper bound is `first_true(0, n, lambda i: arr[i] > target)`. Memorizing this single template, and being able to phrase problems as "find the first index where X holds," will serve you better than memorizing a dozen separate variants.

---

## 10. Searching Rotated and Special Arrays

Binary search does not strictly require a fully sorted array. It needs enough structure that one comparison eliminates part of the search space.

### 10.1 Rotated sorted array

A sorted array rotated at an unknown pivot looks like `[16, 23, 38, 56, 72, 91, 2, 5, 8, 12]`. Although the whole array is not sorted, at every midpoint at least one of the two halves is sorted. We can detect which, check whether the target lies in the sorted half, and discard accordingly.

```python
def search_rotated(arr, target):
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            return mid

        if arr[low] <= arr[mid]:                    # left half is sorted
            if arr[low] <= target < arr[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:                                       # right half is sorted
            if arr[mid] < target <= arr[high]:
                low = mid + 1
            else:
                high = mid - 1

    return -1
```

This runs in `O(log n)` for arrays with distinct values. If duplicates are allowed, the check `arr[low] <= arr[mid]` can be ambiguous (for example `[1, 1, 1, 2, 1]`), and the worst case degrades to `O(n)`.

### 10.2 Finding the minimum in a rotated array

The minimum is the pivot point. Compare the midpoint with the right end:

```python
def find_min_rotated(arr):
    low, high = 0, len(arr) - 1
    while low < high:
        mid = low + (high - low) // 2
        if arr[mid] > arr[high]:
            low = mid + 1       # minimum is to the right of mid
        else:
            high = mid          # minimum is at mid or to its left
    return arr[low]
```

### 10.3 Finding a peak element

A *peak* is an element greater than its neighbors. In an array where adjacent elements differ, a peak always exists, and we can find one in `O(log n)` by following the upward slope:

```python
def find_peak(arr):
    low, high = 0, len(arr) - 1
    while low < high:
        mid = low + (high - low) // 2
        if arr[mid] < arr[mid + 1]:
            low = mid + 1       # slope goes up; a peak lies to the right
        else:
            high = mid          # slope goes down; a peak is at mid or left
    return low
```

This works because if `arr[mid] < arr[mid + 1]`, then moving right either keeps climbing until the end of the array (the last element is a peak) or reaches a point where it starts to fall (a peak). The same argument applies to the left.

### 10.4 Searching a sorted 2D matrix

If each row is sorted and the first element of each row is greater than the last element of the previous row, the matrix can be treated as one flattened sorted array:

```python
def search_matrix(matrix, target):
    if not matrix or not matrix[0]:
        return False
    rows, cols = len(matrix), len(matrix[0])
    low, high = 0, rows * cols - 1

    while low <= high:
        mid = low + (high - low) // 2
        value = matrix[mid // cols][mid % cols]
        if value == target:
            return True
        if value < target:
            low = mid + 1
        else:
            high = mid - 1
    return False
```

The trick is mapping a flat index to row and column with integer division and modulo.

### 10.5 Unknown size: exponential search

If the array size is unknown or effectively infinite (for example a stream), first find an upper bound by doubling, then binary search inside it:

```python
def exponential_search(get, target):
    """get(i) returns the i-th element, or +infinity past the end."""
    if get(0) == target:
        return 0
    bound = 1
    while get(bound) < target:
        bound *= 2

    low, high = bound // 2, bound
    while low <= high:
        mid = low + (high - low) // 2
        v = get(mid)
        if v == target:
            return mid
        if v < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

The doubling phase takes `O(log p)` steps where `p` is the target's position, and the binary search phase takes another `O(log p)`.

---

## 11. Binary Search on the Answer

Some of the most useful applications of binary search involve no array at all. Instead, you search over the space of **possible answers**, using a feasibility check to decide which half to keep.

The recipe:

1. Identify the quantity you want to minimize (or maximize).
2. Define a function `feasible(x)` that answers "is `x` good enough?"
3. Confirm monotonicity: if `x` is feasible, so is every larger value (for minimization). 
4. Binary search for the smallest feasible `x` using the `first_true` template.

### Example 1: Integer square root

Find `floor(sqrt(n))` without using floating-point math.

```python
def isqrt(n):
    low, high = 0, n + 1            # answer lies in [0, n]
    while low < high:
        mid = low + (high - low) // 2
        if mid * mid > n:           # predicate: mid is too big
            high = mid
        else:
            low = mid + 1
    return low - 1                  # last value whose square is <= n

print(isqrt(17))   # 4
print(isqrt(25))   # 5
```

Here the predicate "`mid * mid > n`" is false for small values and true for large ones, which is exactly the monotonic shape binary search needs.

### Example 2: Eating bananas

Koko has `h` hours to eat several piles of bananas. Each hour she picks one pile and eats up to `k` bananas from it. Find the minimum integer `k` that lets her finish within `h` hours.

```python
import math

def min_eating_speed(piles, h):
    def feasible(k):
        return sum(math.ceil(p / k) for p in piles) <= h

    low, high = 1, max(piles)
    while low < high:
        mid = low + (high - low) // 2
        if feasible(mid):
            high = mid
        else:
            low = mid + 1
    return low

print(min_eating_speed([3, 6, 7, 11], 8))   # 4
```

A faster speed can never hurt, so feasibility is monotonic. Each check costs `O(n)`, and there are `O(log max(piles))` checks.

### Example 3: Shipping packages within D days

Packages with given weights must be shipped in order. Find the least ship capacity that lets all packages be delivered within `days` days.

```python
def ship_within_days(weights, days):
    def feasible(capacity):
        needed, load = 1, 0
        for w in weights:
            if load + w > capacity:
                needed += 1
                load = 0
            load += w
        return needed <= days

    low, high = max(weights), sum(weights)
    while low < high:
        mid = low + (high - low) // 2
        if feasible(mid):
            high = mid
        else:
            low = mid + 1
    return low

print(ship_within_days([1,2,3,4,5,6,7,8,9,10], 5))   # 15
```

The lower bound of the search is `max(weights)` because no ship smaller than the heaviest package can work. The upper bound is `sum(weights)`, which ships everything in a single day.

### Example 4: Finding a bad commit

`git bisect` is binary search applied to version history. Given commits ordered by time, with an older "good" commit and a newer "bad" one, the predicate "this commit contains the bug" is false for early commits and true for later ones. Git tests the middle commit, then narrows the range. A history of 1,000 commits needs only about 10 tests.

### Choosing bounds

Picking bounds for an answer search requires care:

- The **lower bound** must be a value that is certainly infeasible or the smallest legal answer.
- The **upper bound** must be a value that is certainly feasible (or one past the largest legal answer, in the half-open style).
- If the bounds are enormous, binary search still takes only about 60 steps even for 64-bit ranges.

---

## 12. Binary Search on Real Numbers

When the search space is continuous, there is no "next" index, so the loop cannot terminate by `low > high`. There are two standard approaches.

### Fixed number of iterations

Each iteration halves the interval, so after `k` iterations the width is `(high - low) / 2^k`. Choose `k` to reach the desired precision. A loop of 100 iterations is more than enough for 64-bit doubles and avoids any dependence on floating-point equality.

```python
def sqrt_real(x, iterations=100):
    low, high = 0.0, max(1.0, x)
    for _ in range(iterations):
        mid = (low + high) / 2
        if mid * mid < x:
            low = mid
        else:
            high = mid
    return (low + high) / 2

print(sqrt_real(2))   # 1.4142135623730951
```

### Tolerance-based stopping

Alternatively, stop when the interval is smaller than a tolerance `eps`:

```python
def bisect_root(f, low, high, eps=1e-9):
    """Find a root of f in [low, high]; requires f(low) and f(high) to have opposite signs."""
    flow = f(low)
    while high - low > eps:
        mid = (low + high) / 2
        fmid = f(mid)
        if (fmid < 0) == (flow < 0):
            low, flow = mid, fmid
        else:
            high = mid
    return (low + high) / 2

import math
print(bisect_root(lambda x: x**3 - x - 2, 1, 2))   # about 1.5213797
```

This is the **bisection method** from numerical analysis. It is guaranteed to converge for continuous functions that change sign over the interval, though slowly compared with methods like Newton's. Be careful with tolerances: if `eps` is smaller than the spacing between adjacent floating-point numbers near the answer, `high - low` may never fall below it, so the iteration-count approach is the safer choice.

---

## 13. Standard Library Support

You will rarely need to write binary search by hand in production code. Prefer well-tested library functions.

### Python: `bisect`

```python
import bisect

nums = [1, 3, 3, 5, 7, 9]

bisect.bisect_left(nums, 3)    # 1  (lower bound)
bisect.bisect_right(nums, 3)   # 3  (upper bound)
bisect.insort(nums, 4)         # inserts 4 keeping the list sorted

# Membership test using bisect
def contains(a, x):
    i = bisect.bisect_left(a, x)
    return i < len(a) and a[i] == x
```

Since Python 3.10, `bisect` functions accept a `key` argument.

### C++: `<algorithm>`

```cpp
#include <algorithm>
#include <vector>

std::vector<int> v = {1, 3, 3, 5, 7, 9};

bool found = std::binary_search(v.begin(), v.end(), 5);       // true
auto lo = std::lower_bound(v.begin(), v.end(), 3);            // points to index 1
auto hi = std::upper_bound(v.begin(), v.end(), 3);            // points to index 3
auto range = std::equal_range(v.begin(), v.end(), 3);         // pair {lo, hi}
```

### Java

```java
import java.util.Arrays;
import java.util.Collections;

int[] a = {1, 3, 5, 7, 9};
int idx = Arrays.binarySearch(a, 7);     // 3
int miss = Arrays.binarySearch(a, 4);    // -3, meaning insertion point 2 => -(2) - 1
```

A negative return value encodes the insertion point as `-(insertionPoint) - 1`.

### Other languages

- **Go:** `sort.SearchInts`, `sort.Search`, and (1.21+) `slices.BinarySearch`.
- **Rust:** `slice.binary_search()` and `slice.partition_point()`.
- **JavaScript:** no built-in; use a hand-written helper or a library.
- **SQL databases:** B-tree indexes perform what is effectively a binary search over pages.

---

## 14. Comparison with Other Search Techniques

| Technique            | Requirement            | Time (average)  | Notes                                           |
|----------------------|------------------------|-----------------|-------------------------------------------------|
| Linear search        | None                   | O(n)            | Simple; best for tiny or unsorted data          |
| Binary search        | Sorted, random access  | O(log n)        | The standard choice for sorted arrays           |
| Interpolation search | Sorted, uniform values | O(log log n)    | Degrades to O(n) for skewed data                |
| Exponential search   | Sorted, unknown size   | O(log p)        | Good when target is near the front              |
| Jump search          | Sorted                 | O(sqrt(n))      | Useful when going backward is expensive         |
| Hash table lookup    | Hashable keys          | O(1)            | No ordering; no range or nearest queries        |
| Balanced BST         | Comparable keys        | O(log n)        | Supports fast insertion and deletion            |
| Ternary search       | Unimodal function      | O(log n)        | Finds a maximum or minimum, not a value         |

### Binary search versus hash tables

A hash table gives expected constant-time lookups, so why use binary search? Because sorted arrays offer things hash tables cannot:

- **Range and order queries:** "all values between 10 and 20," "the next larger element," "the k-th smallest."
- **Memory efficiency:** a plain array has no per-entry overhead.
- **Determinism:** no worst-case collisions or resizing pauses.
- **Predicate searches:** finding a boundary in a monotonic function has no hash table equivalent.

### Binary search versus balanced trees

Sorted arrays are superb for static or rarely-changing data. Inserting into the middle of an array costs `O(n)`. If your data changes frequently, a balanced tree (red-black, AVL), a B-tree, or a skip list supports `O(log n)` search *and* update.

### Interpolation search

Instead of probing the midpoint, interpolation search estimates where the target should be, as a person would when opening a phone book near the end for the name "Young." The probe position is:

```
pos = low + (target - A[low]) * (high - low) / (A[high] - A[low])
```

On uniformly distributed data this averages `O(log log n)` comparisons, but on skewed data it can degrade to `O(n)`, so binary search remains the safer default.

---

## 15. Testing Your Implementation

Because binary search is easy to get subtly wrong, test it thoroughly. Good tests focus on **boundaries**.

### Cases that must pass

- Empty array.
- Single-element array, target present and absent.
- Two-element array, searching for each element and for values below, between, and above.
- Target at the first position and at the last position.
- Target smaller than every element and larger than every element.
- Arrays with all-equal elements.
- Arrays with many duplicates (for the boundary variants).
- Odd and even lengths.

### Randomized comparison test

Compare against a trusted reference, such as Python's `bisect` or a simple linear scan:

```python
import random
import bisect

def test_binary_search(trials=10_000):
    for _ in range(trials):
        n = random.randint(0, 30)
        arr = sorted(random.randint(-20, 20) for _ in range(n))
        target = random.randint(-25, 25)

        # membership
        got = binary_search(arr, target)
        if target in arr:
            assert got != -1 and arr[got] == target, (arr, target, got)
        else:
            assert got == -1, (arr, target, got)

        # boundaries
        assert lower_bound(arr, target) == bisect.bisect_left(arr, target)
        assert upper_bound(arr, target) == bisect.bisect_right(arr, target)

    print("All tests passed")
```

Randomized tests with small value ranges produce many duplicates and edge cases quickly, which is exactly where bugs hide.

### Debugging tips

- Print `low`, `mid`, `high` on every iteration for a failing input and trace by hand.
- Check the loop invariant explicitly with an `assert` during development.
- Add a safety counter that raises an error after `2 * log2(n) + 5` iterations to catch infinite loops.

---

## 16. Practice Problems

Work through these in roughly increasing difficulty. Each one is a binary search in disguise.

**Warm-up**

1. Implement `binary_search` from scratch in your favorite language without looking at this guide.
2. Given a sorted array, return how many times a value appears.
3. Given a sorted array and a value, return the index where it should be inserted.
4. Compute `floor(sqrt(n))` for a 64-bit integer.

**Intermediate**

5. Find the first and last position of a target in a sorted array with duplicates.
6. Search for a target in a rotated sorted array (distinct values).
7. Find the minimum element in a rotated sorted array.
8. Find a peak element in an array in `O(log n)`.
9. Given two sorted arrays, find the median of the combined data in `O(log(min(m, n)))`.
10. Find the smallest letter in a sorted list that is strictly greater than a given letter (wrapping around).

**Answer-space problems**

11. Minimum eating speed (the banana problem).
12. Minimum ship capacity to deliver packages in D days.
13. Split an array into `m` subarrays so that the largest subarray sum is minimized.
14. Place `k` cows in stalls to maximize the minimum distance between any two cows.
15. Find the smallest divisor such that the sum of ceilings of `nums[i] / divisor` is at most a threshold.

**Challenge**

16. Find the k-th smallest element in a multiplication table of size `m x n` without building the table.
17. Search in a sorted array of unknown length using only an accessor function.
18. Given a function `f` that is increasing then decreasing (unimodal), find its maximum using ternary or binary search on the derivative.

For each problem, ask yourself the same three questions: *What is the search space? What is the predicate? Is it monotonic?* If you can answer these, the implementation follows directly from the `first_true` template.

---

## 17. Summary

Binary search is deceptively simple and enormously useful. The key points to carry with you:

- **It requires sorted data and random access.** Without both, the halving argument fails.
- **It runs in O(log n) time and O(1) space** when written iteratively. Doubling the input adds only one extra step.
- **Think in terms of monotonic predicates.** Searching for a value is just one instance of "find the first index where a condition becomes true."
- **Be consistent with your range convention.** Inclusive `[low, high]` and half-open `[low, high)` styles are both correct, but mixing them causes off-by-one errors and infinite loops.
- **Compute the midpoint safely** as `low + (high - low) / 2`.
- **Use lower and upper bounds** for duplicates, counting, insertion points, floors, and ceilings.
- **Apply it beyond arrays.** Square roots, resource allocation, scheduling, and bug hunting with `git bisect` are all binary searches over an answer space.
- **Prefer standard library functions** in production, and test your own implementations against a reference with randomized inputs.

Mastering this one technique unlocks a surprisingly large share of interview questions and real-world engineering problems. When you meet a problem that asks for the "minimum value such that..." or the "maximum value such that...", and larger or smaller answers are uniformly better or worse, reach for binary search first.

### Further reading

- Donald E. Knuth, *The Art of Computer Programming, Volume 3: Sorting and Searching*, Section 6.2.1.
- Thomas H. Cormen et al., *Introduction to Algorithms*, chapters on divide and conquer and loop invariants.
- Jon Bentley, *Programming Pearls*, Column 4, "Writing Correct Programs."
- Joshua Bloch, "Extra, Extra - Read All About It: Nearly All Binary Searches and Mergesorts are Broken" (2006).