# super-reflective
A fun little programming language based on permutations.
### Note: At the moment this readme is mostly a bunch of disorganized thoughts, so it may or not make much sense.

Note that in the following, 'group' is not used in the algebraic sense, but rather in a sense similar to groups in regexes.

[] contains 'groups'

<> contains dataless 'groups' - get filled in a permutation step and turn into groups (when read they give out 0, so <...><...>[(-1-2)] evaluates to [0][0][(-1-2)])

A group can have:
  - data - a signed number (or char)
  - permutation - e.g. (+1+2) swaps the next two groups, (-1-2) swaps the previous 2 (as long as it has non-zero data)
    - if a permutation falls out of bounds, it is not executed
  - '+' - add the data from the left to the data to the right
  - '-' - subtract the data on the left from the data on the right, maybe stopping at zero
  - '/', '*', '^'(xor), '|'
  - '!' - don't print this group

Interpreting a program then consists of:
  - Read a bunch of groups from stdin
  - Then loop
    - Record the indexes of permutations (if a permutation itself gets moved, it still acts according to its initial spot)
    - 'Execute' the (optional) permutation of each group from left to right
    - Execute arithmetic groups
    - output the rightmost group unless it has a '!'

```
[+] [0] [1] [-] <(-3+5)> [0] [&] [1(-9-3)] [^] [!0(-8+0)]
[5] [5] [+] [0] [1] [-] <(-3+5)> [0] [&] [1(-9-3)] [^] [!0(-8+0)] // read
[0] [5] [+] [0] [1] [-] [5(-3+5)] [0] [&] [1(-9-3)] [^] [!0(-8+0)] // permute
[0] [5] [+] [5] [1] [-] [4(-3+5)] [0] [&] [0(-9-3)] [^] [!1(-8+0)] // operate
// Nothing to print
// Presumably no input
// Now record the eligible permutations: (-3+5) around the 7th element, and (-8+0) around the 12th
[0] [5] [+] [!1(-8+0)] [1] [-] [4(-3+5)] [0] [&] [0(-9-3)] [^] [5] // permute the [4(-3+5)] around the 7th element
[0] [5] [+] [5] [1] [-] [4(-3+5)] [0] [&] [0(-9-3)] [^] [!1(-8+0)] // permute the [!1(-8+0)] around the 12th element
[0] [5] [+] [10] [1] [-] [3(-3+5)] [0] [&] [0(-9-3)] [^] [!1(-8+0)] // operate
// Now record the eligible permutations: (-3+5) around the 7th element, and (-8+0) around the 12th
[0] [5] [+] [!1(-8+0)] [1] [-] [3(-3+5)] [0] [&] [0(-9-3)] [^] [10] // permute the [4(-3+5)] around the 7th element
[0] [5] [+] [10] [1] [-] [3(-3+5)] [0] [&] [0(-9-3)] [^] [!1(-8+0)] // permute the [!1(-8+0)] around the 12th element
[0] [5] [+] [15] [1] [-] [2(-3+5)] [0] [&] [0(-9-3)] [^] [!1(-8+0)] // operate
// Now record the eligible permutations: (-3+5) around the 7th element, and (-8+0) around the 12th
[0] [5] [+] [!1(-8+0)] [1] [-] [2(-3+5)] [0] [&] [0(-9-3)] [^] [15] // permute the [4(-3+5)] around the 7th element
[0] [5] [+] [15] [1] [-] [2(-3+5)] [0] [&] [0(-9-3)] [^] [!1(-8+0)] // permute the [!1(-8+0)] around the 12th element
[0] [5] [+] [20] [1] [-] [1(-3+5)] [0] [&] [0(-9-3)] [^] [!1(-8+0)] // operate
// Now record the eligible permutations: (-3+5) around the 7th element, and (-8+0) around the 12th
[0] [5] [+] [!1(-8+0)] [1] [-] [1(-3+5)] [0] [&] [0(-9-3)] [^] [20] // permute the [4(-3+5)] around the 7th element
[0] [5] [+] [20] [1] [-] [1(-3+5)] [0] [&] [0(-9-3)] [^] [!1(-8+0)] // permute the [!1(-8+0)] around the 12th element
[0] [5] [+] [25] [1] [-] [0(-3+5)] [0] [&] [0(-9-3)] [^] [!1(-8+0)] // operate
// Now record the eligible permutations: this time just (-8+0) around the 12th
[0] [5] [+] [!1(-8+0)] [1] [-] [0(-3+5)] [0] [&] [0(-9-3)] [^] [25] // permute the [!1(-8+0)] around the 12th element
[0] [5] [+] [!6(-8+0)] [1] [-] [0(-3+5)] [0] [&] [0(-9-3)] [^] [25] // operate
// Finally, the last group is something printable.  In this case it's 25, though that will get printed forever.
```
