# Merge Sort: A Complete Guide

## Table of Contents

1. Introduction
2. The Core Idea
3. A Worked Example
4. The Algorithm in Detail
5. Implementations in Several Languages
6. Complexity Analysis
7. Correctness
8. Stability
9. Common Pitfalls
10. Optimizations
11. Variations
12. Applications
13. Comparison with Other Sorting Algorithms
14. Testing Your Implementation
15. Practice Problems
16. Summary

---

## 1. Introduction

Merge sort is a comparison-based sorting algorithm built on the **divide and conquer** strategy. It splits the input into two halves, sorts each half recursively, and then **merges** the two sorted halves into one sorted result. Its running time is `O(n log n)` in the best, average, and worst cases, and it is **stable**, meaning equal elements keep their original relative order.

Those two properties, guaranteed performance and stability, are why merge sort remains in wide use more than seventy years after its invention. It is the basis of the standard sorting routines in several languages: Python's `sorted()` and `list.sort()` use Timsort (a merge sort hybrid), Java uses Timsort for objects, and many C++ standard library implementations use merge sort variants for `std::stable_sort`.

### A short history

Merge sort was invented by John von Neumann in 1945, and it is among the earliest algorithms designed for a stored-program computer. A description of the method appeared in the 1948 reports on the EDVAC machine. Because merging only needs to read its inputs sequentially, the algorithm suited early storage media such as magnetic tape, and variants of it are still the standard approach for sorting data that does not fit in memory.

### What you will learn

This guide covers:

- the intuition behind divide and conquer and why merging is cheap;
- top-down (recursive) and bottom-up (iterative) implementations;
- a proof that the algorithm is correct and runs in `O(n log n)`;
- why stability matters and how merge sort preserves it;
- optimizations used in real libraries;
- variations such as linked-list sort, external sort, and k-way merge;
- applications such as counting inversions.

Most code is in Python, with versions in C++, Java, JavaScript, and Go.

---

## 2. The Core Idea

Sorting a large list is hard, but two facts make it easier:

1. Sorting a list of zero or one elements is trivial. It is already sorted.
2. **Merging two already-sorted lists into one sorted list is easy and fast**, taking time proportional to the total number of elements.

Merge sort combines these facts. To sort a list:

1. **Divide.** Split the list into two halves of roughly equal size.
2. **Conquer.** Sort each half by applying the same procedure recursively.
3. **Combine.** Merge the two sorted halves into a single sorted list.

### Why merging is cheap

Suppose you have two sorted lists, `L = [2, 5, 9]` and `R = [1, 6, 7, 8]`. The smallest element overall must be either the first element of `L` or the first element of `R`, since each list is sorted. Compare those two, take the smaller one, and advance in that list. Repeat. At every step you only compare two elements, and each element is copied exactly once. Merging lists of sizes `a` and `b` therefore takes `O(a + b)` time.

### The recursion tree

For an array of 8 elements, the recursion looks like this:

```
Level 0:               [8 elements]
                      /            \
Level 1:        [4 elements]    [4 elements]
                  /     \          /     \
Level 2:      [2]       [2]     [2]       [2]
              / \       / \     / \       / \
Level 3:    [1] [1]   [1] [1] [1] [1]   [1] [1]
```

The tree has `log2(8) = 3` levels of splitting. At each level, the merging work across all nodes totals `n` elements. Total work is therefore about `n * log2(n)`.

---

## 3. A Worked Example

Sort the array `[38, 27, 43, 3, 9, 82, 10]`.

### Divide phase

```
[38, 27, 43, 3, 9, 82, 10]
        /              \
[38, 27, 43]        [3, 9, 82, 10]
   /      \            /        \
[38]   [27, 43]    [3, 9]     [82, 10]
         /   \       / \         /  \
       [27] [43]   [3] [9]    [82] [10]
```

### Merge phase

Now merge back up from the bottom.

| Merge inputs         | Result             |
|----------------------|--------------------|
| `[27]` + `[43]`      | `[27, 43]`         |
| `[38]` + `[27, 43]`  | `[27, 38, 43]`     |
| `[3]` + `[9]`        | `[3, 9]`           |
| `[82]` + `[10]`      | `[10, 82]`         |
| `[3, 9]` + `[10, 82]`| `[3, 9, 10, 82]`   |
| `[27, 38, 43]` + `[3, 9, 10, 82]` | `[3, 9, 10, 27, 38, 43, 82]` |

### Tracing one merge in detail

Merge `L = [27, 38, 43]` and `R = [3, 9, 10, 82]`:

| Step | i (in L) | j (in R) | Compare   | Output so far                  |
|------|----------|----------|-----------|--------------------------------|
| 1    | 0        | 0        | 27 vs 3   | `[3]`                          |
| 2    | 0        | 1        | 27 vs 9   | `[3, 9]`                       |
| 3    | 0        | 2        | 27 vs 10  | `[3, 9, 10]`                   |
| 4    | 0        | 3        | 27 vs 82  | `[3, 9, 10, 27]`               |
| 5    | 1        | 3        | 38 vs 82  | `[3, 9, 10, 27, 38]`           |
| 6    | 2        | 3        | 43 vs 82  | `[3, 9, 10, 27, 38, 43]`       |
| 7    | 3 (done) | 3        | L empty   | append rest of R: `..., 82`   |

When one list runs out, the remainder of the other is already sorted and can be copied directly.

---

## 4. The Algorithm in Detail

### Pseudocode

```
function merge_sort(A):
    if length(A) <= 1:
        return A

    mid   <- length(A) / 2
    left  <- merge_sort(A[0 .. mid))
    right <- merge_sort(A[mid .. end))

    return merge(left, right)


function merge(L, R):
    result <- empty list
    i <- 0
    j <- 0

    while i < length(L) and j < length(R):
        if L[i] <= R[j]:
            append L[i] to result
            i <- i + 1
        else:
            append R[j] to result
            j <- j + 1

    append remaining elements of L (from i) to result
    append remaining elements of R (from j) to result
    return result
```

### Design decisions

**The comparison `<=` matters.** In the merge step, when the two front elements are equal, we take from the **left** list first. This is what makes merge sort stable. Using `<` instead would take the right element first on ties and break stability.

**Choosing the split point.** Using `mid = n // 2` gives halves that differ in size by at most one. Balanced splits guarantee a recursion depth of `ceil(log2(n))`. An unbalanced split would hurt performance.

**Where to put the temporary storage.** The naive version allocates new lists at every level, which is simple but wasteful. Production implementations allocate one auxiliary buffer of size `n` up front and reuse it. See the optimizations section.

**Top-down versus bottom-up.** The recursive formulation splits first and merges on the way back. The bottom-up formulation skips splitting: it treats each element as a sorted run of length 1, merges adjacent pairs into runs of length 2, then 4, then 8, and so on until one run remains.

---

## 5. Implementations in Several Languages

### Python (simple, top-down)

This version favors clarity. It creates new lists at each step.

```python
def merge_sort(arr):
    """Return a new sorted list."""
    if len(arr) <= 1:
        return arr[:]

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:        # <= keeps the sort stable
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
# [3, 9, 10, 27, 38, 43, 82]
```

### Python (in place with an auxiliary buffer)

This version sorts the original list and reuses a single buffer, avoiding repeated allocation.

```python
def merge_sort_inplace(arr):
    buf = [None] * len(arr)
    _sort(arr, buf, 0, len(arr))


def _sort(arr, buf, lo, hi):
    """Sort arr[lo:hi]."""
    if hi - lo <= 1:
        return
    mid = lo + (hi - lo) // 2
    _sort(arr, buf, lo, mid)
    _sort(arr, buf, mid, hi)
    _merge(arr, buf, lo, mid, hi)


def _merge(arr, buf, lo, mid, hi):
    buf[lo:hi] = arr[lo:hi]            # copy the range into the buffer
    i, j = lo, mid
    for k in range(lo, hi):
        if i >= mid:
            arr[k] = buf[j]; j += 1
        elif j >= hi:
            arr[k] = buf[i]; i += 1
        elif buf[i] <= buf[j]:
            arr[k] = buf[i]; i += 1
        else:
            arr[k] = buf[j]; j += 1
```

### Python (bottom-up, iterative)

```python
def merge_sort_bottom_up(arr):
    n = len(arr)
    buf = [None] * n
    width = 1

    while width < n:
        for lo in range(0, n, 2 * width):
            mid = min(lo + width, n)
            hi = min(lo + 2 * width, n)
            _merge(arr, buf, lo, mid, hi)   # reuse _merge from above
        width *= 2
```

When `mid == hi` the right run is empty and `_merge` simply copies the left run back, which is harmless.

### C++

```cpp
#include <vector>

void merge(std::vector<int>& a, std::vector<int>& tmp,
           int lo, int mid, int hi) {
    int i = lo, j = mid, k = lo;
    while (i < mid && j < hi) {
        if (a[i] <= a[j]) tmp[k++] = a[i++];
        else              tmp[k++] = a[j++];
    }
    while (i < mid) tmp[k++] = a[i++];
    while (j < hi)  tmp[k++] = a[j++];
    for (k = lo; k < hi; ++k) a[k] = tmp[k];
}

void sortRange(std::vector<int>& a, std::vector<int>& tmp, int lo, int hi) {
    if (hi - lo <= 1) return;
    int mid = lo + (hi - lo) / 2;
    sortRange(a, tmp, lo, mid);
    sortRange(a, tmp, mid, hi);
    merge(a, tmp, lo, mid, hi);
}

void mergeSort(std::vector<int>& a) {
    std::vector<int> tmp(a.size());
    sortRange(a, tmp, 0, static_cast<int>(a.size()));
}
```

### Java

```java
public static void mergeSort(int[] a) {
    int[] tmp = new int[a.length];
    sort(a, tmp, 0, a.length);
}

private static void sort(int[] a, int[] tmp, int lo, int hi) {
    if (hi - lo <= 1) return;
    int mid = lo + (hi - lo) / 2;
    sort(a, tmp, lo, mid);
    sort(a, tmp, mid, hi);
    merge(a, tmp, lo, mid, hi);
}

private static void merge(int[] a, int[] tmp, int lo, int mid, int hi) {
    int i = lo, j = mid, k = lo;
    while (i < mid && j < hi) {
        tmp[k++] = (a[i] <= a[j]) ? a[i++] : a[j++];
    }
    while (i < mid) tmp[k++] = a[i++];
    while (j < hi)  tmp[k++] = a[j++];
    System.arraycopy(tmp, lo, a, lo, hi - lo);
}
```

### JavaScript

```javascript
function mergeSort(arr) {
  if (arr.length <= 1) return arr;

  const mid = Math.floor(arr.length / 2);
  const left = mergeSort(arr.slice(0, mid));
  const right = mergeSort(arr.slice(mid));

  const result = [];
  let i = 0, j = 0;
  while (i < left.length && j < right.length) {
    if (left[i] <= right[j]) result.push(left[i++]);
    else result.push(right[j++]);
  }
  return result.concat(left.slice(i), right.slice(j));
}
```

### Go

```go
func mergeSort(a []int) []int {
    if len(a) <= 1 {
        return a
    }
    mid := len(a) / 2
    left := mergeSort(a[:mid])
    right := mergeSort(a[mid:])

    result := make([]int, 0, len(a))
    i, j := 0, 0
    for i < len(left) && j < len(right) {
        if left[i] <= right[j] {
            result = append(result, left[i])
            i++
        } else {
            result = append(result, right[j])
            j++
        }
    }
    result = append(result, left[i:]...)
    result = append(result, right[j:]...)
    return result
}
```

### Sorting with a custom key

To sort records by a field, compare the keys rather than the elements:

```python
def merge_sort_by(items, key):
    if len(items) <= 1:
        return items[:]
    mid = len(items) // 2
    left = merge_sort_by(items[:mid], key)
    right = merge_sort_by(items[mid:], key)

    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out


people = [("Ana", 31), ("Ben", 24), ("Chloe", 31), ("Dev", 24)]
print(merge_sort_by(people, key=lambda p: p[1]))
# [('Ben', 24), ('Dev', 24), ('Ana', 31), ('Chloe', 31)]
```

Notice that Ben stays ahead of Dev, and Ana stays ahead of Chloe. That is stability in action.

---

## 6. Complexity Analysis

### Time complexity

Let `T(n)` be the time to sort `n` elements. The algorithm makes two recursive calls on halves and then does a linear-time merge:

```
T(n) = 2 * T(n / 2) + c * n,      T(1) = c0
```

Here `c * n` is the cost of the merge and `c0` is a constant.

**Recursion-tree argument.** At depth `d` of the recursion tree there are `2^d` subproblems, each of size `n / 2^d`. The merge work at that depth is:

```
2^d * c * (n / 2^d) = c * n
```

So every level contributes the same `c * n`. The tree has `log2(n) + 1` levels (the last being the leaves). The total is:

```
T(n) = c * n * log2(n) + c0 * n  =  O(n log n)
```

**Master theorem.** The recurrence has the form `T(n) = a * T(n / b) + f(n)` with `a = 2`, `b = 2`, and `f(n) = Theta(n)`. Since `n^(log_b a) = n^1 = n` matches `f(n)`, case 2 of the master theorem applies and gives `T(n) = Theta(n log n)`.

### Best, average, and worst case

Unlike quicksort, merge sort's running time barely depends on the input order. The split is always in the middle, and the merge always examines each element once.

| Case    | Comparisons (approx.)       | Time        |
|---------|-----------------------------|-------------|
| Best    | about `(n log2 n) / 2`      | O(n log n)  |
| Average | about `n log2 n - 1.25 n`   | O(n log n)  |
| Worst   | at most `n log2 n - n + 1`  | O(n log n)  |

In the best case (for example, an already sorted array), each merge finishes comparing as soon as the left list is exhausted, so only about half the comparisons are needed. The overall time remains `O(n log n)` because copying still happens.

### Space complexity

- The simple version that allocates new lists uses `O(n)` extra space at any time, plus `O(log n)` for the call stack. Total allocations over the run are `O(n log n)`, though they are freed along the way.
- The single-buffer version uses exactly `n` extra slots plus `O(log n)` stack depth.
- Sorting an array with merge sort in `O(1)` extra space is possible with complicated in-place merge algorithms, but these are slower in practice. See the variations section.

### Is O(n log n) optimal?

For comparison-based sorting, yes. A sorting algorithm must distinguish among `n!` possible orderings. Each comparison has two outcomes, so a decision tree with `n!` leaves has height at least `log2(n!)`. By Stirling's approximation, `log2(n!)` is about `n log2 n - 1.44 n`. Therefore **no comparison sort can beat `Omega(n log n)` in the worst case**, and merge sort is asymptotically optimal.

Practical numbers:

| n               | n log2 n (approx.)  |
|-----------------|---------------------|
| 1,000           | 10 thousand         |
| 1,000,000       | 20 million          |
| 1,000,000,000   | 30 billion          |

Compare this with `n^2` for simple sorts like bubble sort or insertion sort: for a million elements, `10^12` operations versus about `2 * 10^7`. That is a gap of roughly 50,000 times.

---

## 7. Correctness

We prove that merge sort is correct by first proving `merge` correct, then using induction for the sort itself.

### Correctness of merge

**Claim.** If `L` and `R` are sorted, `merge(L, R)` returns a sorted list containing exactly the elements of `L` and `R`.

**Loop invariant.** At the start of each iteration of the main loop:

1. `result` is sorted;
2. `result` contains exactly the elements `L[0..i)` and `R[0..j)`;
3. every element of `result` is less than or equal to every element in `L[i..]` and `R[j..]`.

*Initialization.* With `i = j = 0`, `result` is empty and all three conditions hold trivially.

*Maintenance.* Suppose `L[i] <= R[j]`. Because `L` is sorted, `L[i]` is also less than or equal to every later element of `L`. Together with `L[i] <= R[j]` and `R` sorted, `L[i]` is less than or equal to every remaining element. By invariant 3, every element already in `result` is at most `L[i]`, so appending `L[i]` keeps `result` sorted. The other two conditions are updated consistently. The case `L[i] > R[j]` is symmetric.

*Termination.* The loop ends when one input is exhausted. The remaining elements of the other list are sorted and, by invariant 3, all at least as large as anything in `result`. Appending them yields a sorted list that contains every element exactly once.

### Correctness of merge sort

**Claim.** For every list `A`, `merge_sort(A)` returns a sorted permutation of `A`.

We use strong induction on the length `n`.

*Base case.* If `n <= 1` the list is already sorted, and it is returned unchanged.

*Inductive step.* Assume the claim holds for all lists shorter than `n`, where `n >= 2`. The algorithm splits `A` into two non-empty halves, each strictly shorter than `n`. By the inductive hypothesis, the recursive calls return sorted permutations of each half. By the correctness of `merge`, merging them yields a sorted list containing every element of `A`. 

Termination follows because every recursive call has strictly smaller input, and the base case stops the recursion.

---

## 8. Stability

A sorting algorithm is **stable** if elements that compare equal appear in the output in the same relative order as in the input.

### Why stability matters

Consider sorting a list of employees first by name and then by department. If the second sort is stable, employees within each department remain ordered by name. If the second sort is unstable, the name ordering inside departments may be scrambled. Stability lets you build multi-key sorts by applying single-key sorts from the least significant key to the most significant.

```python
employees = [
    ("Zoe",   "Sales"),
    ("Adam",  "Eng"),
    ("Maya",  "Sales"),
    ("Brian", "Eng"),
]

step1 = merge_sort_by(employees, key=lambda e: e[0])   # sort by name
step2 = merge_sort_by(step1,     key=lambda e: e[1])   # then by department (stable)
# [('Adam','Eng'), ('Brian','Eng'), ('Maya','Sales'), ('Zoe','Sales')]
```

### How merge sort stays stable

Stability depends entirely on the merge step. Elements from the left half originally came before elements from the right half. When a left element and a right element are equal, taking the left one first preserves that order. That is why the condition is `L[i] <= R[j]` and not `L[i] < R[j]`.

Elements within the same half remain in order because each half is sorted stably by induction, and the merge never reorders elements taken from the same list.

### Which algorithms are stable?

| Algorithm      | Stable? |
|----------------|---------|
| Merge sort     | Yes     |
| Insertion sort | Yes     |
| Bubble sort    | Yes     |
| Timsort        | Yes     |
| Quicksort      | No (typical in-place versions) |
| Heapsort       | No      |
| Selection sort | No (typical versions) |

---

## 9. Common Pitfalls

### 9.1 Using `<` instead of `<=` in the merge

The result is still sorted, but ties now take from the right half first, so the algorithm is no longer stable. This is easy to miss because tests with distinct values pass.

### 9.2 Forgetting to copy the leftover elements

After the main merge loop, one input still has elements. If you forget to append them, the output silently loses data. Always flush both remainders.

### 9.3 Off-by-one errors in the split

With half-open ranges `[lo, hi)`, the base case is `hi - lo <= 1` and the split is `[lo, mid)` and `[mid, hi)`. With inclusive ranges `[lo, hi]`, the base case is `lo >= hi` and the split is `[lo, mid]` and `[mid + 1, hi]`. Mixing the two causes infinite recursion (a range that never shrinks) or skipped elements.

A classic infinite recursion occurs if the split can produce an empty half and a half equal to the whole range. With `mid = lo + (hi - lo) // 2` and a base case of size at most one, both halves are always strictly smaller.

### 9.4 Integer overflow in the midpoint

As with binary search, `(lo + hi) / 2` can overflow with fixed-width integers. Prefer `lo + (hi - lo) / 2`.

### 9.5 Allocating inside the recursion

Creating new arrays at every call produces many allocations and puts pressure on the memory allocator and garbage collector. For large inputs, allocate one buffer at the start and pass it down.

### 9.6 Slicing cost in Python

In Python, `arr[:mid]` copies the slice. That is fine for clarity but doubles memory traffic. The index-based version avoids repeated copying.

### 9.7 Recursion depth

The depth is only `log2(n)`, so even a billion elements needs around 30 frames. Stack overflow is not a concern for merge sort itself, unlike a poorly pivoted quicksort.

### 9.8 Sorting linked lists by index

Merge sort suits linked lists well, but only if you split by walking pointers (slow/fast pointer technique), not by indexing. Indexing into a linked list costs `O(n)` and ruins the complexity.

---

## 10. Optimizations

The textbook algorithm is already efficient, but a few well-known improvements make it noticeably faster in practice.

### 10.1 Switch to insertion sort for small subarrays

Recursion has overhead, and for tiny arrays simple insertion sort is faster than the full machinery. Real implementations stop recursing when the range is smaller than a cutoff, typically between 7 and 64 elements, and finish with insertion sort.

```python
CUTOFF = 16

def insertion_sort(arr, lo, hi):
    for i in range(lo + 1, hi):
        x = arr[i]
        j = i - 1
        while j >= lo and arr[j] > x:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = x


def _sort(arr, buf, lo, hi):
    if hi - lo <= CUTOFF:
        insertion_sort(arr, lo, hi)
        return
    mid = lo + (hi - lo) // 2
    _sort(arr, buf, lo, mid)
    _sort(arr, buf, mid, hi)
    if arr[mid - 1] <= arr[mid]:       # already in order (see next section)
        return
    _merge(arr, buf, lo, mid, hi)
```

Because insertion sort is stable, the overall algorithm stays stable.

### 10.2 Skip the merge when already ordered

If the largest element of the left half is not greater than the smallest element of the right half, the two halves are already in the correct relative order and the merge can be skipped. The check is a single comparison: `arr[mid - 1] <= arr[mid]`. This makes merge sort run in `O(n)` on already sorted input.

### 10.3 Avoid copying with alternating buffers

The simple merge copies from the array to the buffer and back at every level. A smarter approach alternates the roles of the two arrays at each level of recursion: one level merges from `A` into `B`, the next merges from `B` into `A`. This eliminates the copy step and reduces memory traffic by about half.

### 10.4 Copy only half

Only the left half needs to be saved to the buffer. During the merge, the output pointer can never overtake the unread part of the right half, because every output position is filled by an element that has been consumed. So we copy just `arr[lo:mid]` and merge back into `arr` directly.

```python
def merge_half_buffer(arr, buf, lo, mid, hi):
    buf[0:mid - lo] = arr[lo:mid]       # copy only the left run
    i, j, k = 0, mid, lo
    left_len = mid - lo

    while i < left_len and j < hi:
        if buf[i] <= arr[j]:
            arr[k] = buf[i]; i += 1
        else:
            arr[k] = arr[j]; j += 1
        k += 1

    while i < left_len:                 # leftover from the buffered half
        arr[k] = buf[i]; i += 1; k += 1
    # leftover from the right half is already in place
```

This halves the temporary storage to `n / 2` and removes a large amount of copying.

### 10.5 Natural merge sort and Timsort

Real-world data is often partially sorted. **Natural merge sort** begins by scanning for existing **runs**, maximal ascending (or strictly descending, which are reversed) sequences, and merges those instead of starting from runs of length one. An already sorted array consists of a single run and is handled in one pass.

**Timsort**, designed by Tim Peters in 2002 for Python and now used by Java, Android, Swift, and others, builds on this idea. It:

1. finds natural runs and extends short runs to a minimum length with insertion sort;
2. keeps pending runs on a stack and merges them according to rules that keep merges balanced;
3. uses **galloping mode** (exponential search) when one run wins many comparisons in a row, which speeds up merges of very uneven data;
4. runs in `O(n)` on sorted or reverse-sorted input and `O(n log n)` otherwise, and is stable.

If you need a production sort, use the library function rather than writing your own.

### 10.6 Reduce comparisons with sentinels

Some implementations place a sentinel (a value larger than any real element) at the end of each input so the loop does not need to check for exhaustion. This removes one comparison per iteration but requires reserving a value, so it is awkward with generic types and is rarely worth the trouble in modern code.

### 10.7 Parallelism

The two recursive calls are independent, so merge sort parallelizes naturally. Sort each half in separate threads down to some depth, then merge. The merge step itself can also be parallelized by choosing split points with binary search, so that different threads merge disjoint pieces of the output. This is why merge sort is popular in multi-core and GPU sorting libraries.

---

## 11. Variations

### 11.1 Merge sort on linked lists

Merge sort is the algorithm of choice for sorting linked lists. It needs no random access, it merges by relinking nodes (so it needs only `O(1)` extra space for the merge), and it is stable. Only the recursion stack, `O(log n)`, is extra.

```python
class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def sort_list(head):
    if head is None or head.next is None:
        return head

    # find the middle with slow/fast pointers
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    second = slow.next
    slow.next = None                   # cut the list in two

    left = sort_list(head)
    right = sort_list(second)
    return merge_lists(left, right)


def merge_lists(a, b):
    dummy = tail = Node(None)
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next
```

The dummy head node avoids special-casing the first element.

### 11.2 External merge sort

When data is too large to fit in memory, for example sorting a 500 GB file with 8 GB of RAM, merge sort is the standard solution because merging needs only sequential reads and writes.

1. **Run generation.** Read as much data as fits in memory, sort it with any in-memory sort, and write it to disk as a sorted *run*.
2. **Merge passes.** Merge several runs at a time into longer runs, reading each input run sequentially through a small buffer.
3. Repeat until one run remains.

Merging `k` runs at once (a **k-way merge**) reduces the number of passes over the data from `log2(runs)` to `log_k(runs)`. Database engines use this approach for `ORDER BY` on large tables. Techniques such as *replacement selection* can produce initial runs about twice as long as memory.

### 11.3 K-way merge with a heap

To merge `k` sorted lists with a total of `n` elements, keep the current front element of each list in a min-heap. Repeatedly pop the smallest and push the next element from the same list. The cost is `O(n log k)`.

```python
import heapq

def k_way_merge(lists):
    heap = []
    for idx, lst in enumerate(lists):
        if lst:
            heap.append((lst[0], idx, 0))
    heapq.heapify(heap)

    result = []
    while heap:
        value, list_idx, pos = heapq.heappop(heap)
        result.append(value)
        if pos + 1 < len(lists[list_idx]):
            heapq.heappush(heap, (lists[list_idx][pos + 1], list_idx, pos + 1))
    return result

print(k_way_merge([[1, 4, 7], [2, 5, 8], [3, 6, 9]]))
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

The tuple includes `list_idx` so ties never compare the later fields in unpredictable ways, and the standard library offers `heapq.merge` for the same purpose.

### 11.4 In-place merge sort

It is possible to merge sort with only `O(1)` extra space using algorithms such as block merge sort (WikiSort, Grail sort) or rotation-based merging. These achieve `O(n log n)` time and stability, but they are considerably more complex, and the constant factors are larger than for the buffered version. They are mainly of interest when memory is extremely constrained.

A simple in-place merge using rotations is `O(n log n)` per merge, giving `O(n log^2 n)` overall, which is easier to write but slower.

### 11.5 Three-way and multiway splits

You can split into three or more parts instead of two. The recursion depth shrinks to `log_3(n)`, but each merge needs more comparisons per output element. The product is roughly the same, so the asymptotic cost does not change, and two-way splitting remains the standard.

### 11.6 Descending order and custom comparators

To sort in descending order, flip the comparison in the merge: take from the left when `L[i] >= R[j]`. To accept a generic comparator, replace the `<=` test with a call such as `cmp(L[i], R[j]) <= 0`, preserving the tie-breaking rule that keeps the sort stable.

---

## 12. Applications

### 12.1 Counting inversions

An **inversion** is a pair of indices `i < j` with `A[i] > A[j]`. The number of inversions measures how far an array is from being sorted: zero for a sorted array and `n(n-1)/2` for a reversed one. A brute-force count takes `O(n^2)`, but merge sort counts inversions in `O(n log n)` with a tiny change.

During a merge, whenever an element is taken from the right half while `k` elements remain in the left half, that right element forms an inversion with each of those `k` elements.

```python
def count_inversions(arr):
    buf = [0] * len(arr)
    work = list(arr)
    return _count(work, buf, 0, len(work))


def _count(a, buf, lo, hi):
    if hi - lo <= 1:
        return 0
    mid = lo + (hi - lo) // 2
    inv = _count(a, buf, lo, mid) + _count(a, buf, mid, hi)

    i, j, k = lo, mid, lo
    while i < mid and j < hi:
        if a[i] <= a[j]:
            buf[k] = a[i]; i += 1
        else:
            buf[k] = a[j]; j += 1
            inv += mid - i             # all remaining left elements are larger
        k += 1
    while i < mid:
        buf[k] = a[i]; i += 1; k += 1
    while j < hi:
        buf[k] = a[j]; j += 1; k += 1

    a[lo:hi] = buf[lo:hi]
    return inv

print(count_inversions([2, 4, 1, 3, 5]))   # 3
print(count_inversions([5, 4, 3, 2, 1]))   # 10
```

Inversion counting is used in ranking comparison (Kendall tau distance), collaborative filtering, and analysis of sorting networks.

### 12.2 Merging sorted data streams

Log aggregation, time-series databases, and search engines routinely merge many sorted streams (for example, sorted posting lists) using exactly the k-way merge pattern.

### 12.3 Related counting problems

Variations of the inversion-counting trick solve problems like "count of smaller numbers after self," "reverse pairs," and "count of range sums." In each, you augment the merge step to count qualifying pairs between the left and right sorted halves before merging them.

### 12.4 Set operations on sorted lists

Union, intersection, and difference of two sorted lists follow the same two-pointer pattern as merge, in `O(a + b)` time.

```python
def intersect_sorted(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            out.append(a[i]); i += 1; j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return out
```

### 12.5 Database joins

The **sort-merge join** sorts both tables on the join key and merges them, a standard strategy when the inputs are large or already sorted by an index.

---

## 13. Comparison with Other Sorting Algorithms

| Algorithm      | Best        | Average     | Worst       | Extra space | Stable |
|----------------|-------------|-------------|-------------|-------------|--------|
| Merge sort     | O(n log n)  | O(n log n)  | O(n log n)  | O(n)        | Yes    |
| Quicksort      | O(n log n)  | O(n log n)  | O(n^2)      | O(log n)    | No     |
| Heapsort       | O(n log n)  | O(n log n)  | O(n log n)  | O(1)        | No     |
| Timsort        | O(n)        | O(n log n)  | O(n log n)  | O(n)        | Yes    |
| Insertion sort | O(n)        | O(n^2)      | O(n^2)      | O(1)        | Yes    |
| Selection sort | O(n^2)      | O(n^2)      | O(n^2)      | O(1)        | No     |
| Bubble sort    | O(n)        | O(n^2)      | O(n^2)      | O(1)        | Yes    |

### Merge sort versus quicksort

- Quicksort is usually faster on arrays in practice thanks to excellent cache behavior and fewer data movements, and it needs only `O(log n)` extra space.
- Merge sort guarantees `O(n log n)` with no bad inputs, is stable, and works well with sequential access (linked lists, files, tapes).
- Quicksort's worst case is `O(n^2)` unless protected by randomized pivots or introsort-style fallbacks.

### Merge sort versus heapsort

Heapsort sorts in place with guaranteed `O(n log n)` time but has poor cache locality and is not stable. Merge sort is typically faster in practice and is stable, at the price of extra memory.

### When to choose merge sort

- You need a **stable** sort.
- You need guaranteed worst-case performance.
- You are sorting **linked lists** or data accessed sequentially.
- The data lives on **disk** or comes in streams.
- You want an algorithm that parallelizes easily.

### When not to

- Memory is extremely limited and stability is not required (consider heapsort or in-place quicksort).
- You are sorting tiny arrays (insertion sort wins).
- Keys are small integers in a bounded range (counting sort or radix sort run in linear time and are not limited by the comparison lower bound).

---

## 14. Testing Your Implementation

Sorting bugs often hide in edge cases, so test thoroughly.

### Cases that must pass

- Empty array and single-element array.
- Two elements, in order and reversed.
- Already sorted, reverse sorted, and all-equal arrays.
- Arrays with many duplicates.
- Odd and even lengths, and lengths that are powers of two plus or minus one (for bottom-up versions).
- Negative numbers and extreme values.
- A large random array, to check performance.

### Randomized comparison test

```python
import random

def test_merge_sort(trials=5000):
    for _ in range(trials):
        n = random.randint(0, 40)
        arr = [random.randint(-10, 10) for _ in range(n)]
        assert merge_sort(arr) == sorted(arr), arr

        copy = list(arr)
        merge_sort_inplace(copy)
        assert copy == sorted(arr), arr
    print("All tests passed")
```

### Testing stability

Attach the original index to each element and check that equal keys keep ascending original indices.

```python
def test_stability(trials=2000):
    for _ in range(trials):
        n = random.randint(0, 40)
        items = [(random.randint(0, 5), i) for i in range(n)]   # (key, original index)
        out = merge_sort_by(items, key=lambda t: t[0])
        for a, b in zip(out, out[1:]):
            if a[0] == b[0]:
                assert a[1] < b[1], out
    print("Stability verified")
```

### Measuring performance

```python
import time, random

for n in (10**4, 10**5, 10**6):
    data = [random.random() for _ in range(n)]
    start = time.perf_counter()
    merge_sort(data)
    print(n, round(time.perf_counter() - start, 3), "s")
```

When `n` grows tenfold, time should grow a little more than tenfold, consistent with `n log n`. If it grows a hundredfold, something is quadratic, often from repeated list slicing or `list.pop(0)` in the merge step.

---

## 15. Practice Problems

**Warm-up**

1. Implement top-down merge sort for an array of integers without looking at this guide.
2. Write the `merge` function that combines two sorted arrays.
3. Merge two sorted arrays where the first has extra capacity at the end, merging in place from the back.
4. Sort an array in descending order using merge sort.

**Intermediate**

5. Implement bottom-up merge sort.
6. Sort a singly linked list in `O(n log n)` time.
7. Merge `k` sorted linked lists.
8. Count the inversions in an array.
9. Sort an array of strings by length, keeping equal-length strings in their original order.
10. Merge overlapping intervals after sorting them by start time.

**Advanced**

11. Count the number of "reverse pairs" `(i, j)` with `i < j` and `A[i] > 2 * A[j]`.
12. For each element, count how many smaller elements appear to its right.
13. Implement an external merge sort that sorts a file larger than a fixed memory budget.
14. Implement the half-buffer merge and measure the speed-up against the full-copy version.
15. Implement a parallel merge sort using threads or processes and compare it with the sequential version.

**Thought questions**

16. Why does merge sort perform well on linked lists while quicksort does not?
17. What happens to stability if you replace `<=` with `<` in the merge?
18. Why can't any comparison-based sort beat `n log n` in the worst case?

---

## 16. Summary

Merge sort is a model example of divide and conquer: split the problem, solve the pieces, and combine the results cheaply.

- **Idea:** split in half, sort each half recursively, merge the two sorted halves.
- **Time:** `O(n log n)` in every case, which is optimal for comparison sorting.
- **Space:** `O(n)` auxiliary space for the standard array version, `O(log n)` for linked lists.
- **Stable:** equal elements keep their order, as long as the merge takes from the left side on ties.
- **Practical improvements:** insertion sort for small ranges, skipping merges on ordered halves, a single reusable buffer, and natural runs (the Timsort approach).
- **Strengths:** guaranteed performance, stability, sequential access, easy parallelization, and suitability for external sorting.
- **Beyond sorting:** the merge pattern powers inversion counting, k-way merging, set operations on sorted data, and sort-merge joins.

If you remember one thing, remember the merge step: two pointers, take the smaller front element (preferring the left on ties), and flush what remains. Everything else in merge sort is built on that small, reliable procedure.

### Further reading

- Donald E. Knuth, *The Art of Computer Programming, Volume 3: Sorting and Searching*, Section 5.2.4 (sorting by merging).
- Thomas H. Cormen et al., *Introduction to Algorithms*, chapter on divide and conquer.
- Robert Sedgewick and Kevin Wayne, *Algorithms*, chapter on mergesort.
- Tim Peters, "listsort.txt" in the CPython source tree, describing Timsort.