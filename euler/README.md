## Project Euler Assignment
- 107 Minimal Network
- 230 Fibonacci Words
- 349 Langton's Ant

### Solution scripts (invocation from root directory, python version 3.4 or above)
```sh
python euler/_107_minimal_network.py <path_to_graph_file>
python euler/_230_fibonacci_words.py <string_1> <string_2>
python euler/_349_langton_ant.py <num_steps>
```

#### 107 Minimal Network
```sh
python euler/_107_minimal_network.py euler/assets/107_network.txt

# 259679
# Duration: 0.0077478885650634766s
```

#### 230 Fibonacci Words
```sh
python euler/_230_fibonacci_words.py 1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679 8214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196

# 850481152593119296
# Duration: 0.000453948974609375s
```

#### 349 Langton's Ant
```sh
python euler/_349_langton_ant.py 1000000000000000000

# 115384615384614952 black squares after 1000000000000000000 moves
# Duration: 0.05420112609863281s
```


### Unit tests
The unit tests cover all of the data structures used by solution scripts. Because they use relative imports, they should be run as modules as opposed to python scripts. __They must be run from the project's root directory, or else the relative imports won't work.__
```sh
# run all unit tests
python -m unittest discover euler.tests -v

# run unit tests in a single module
python -m euler.tests.test_union_find -v
python -m euler.tests.test_graph_mst -v
python -m euler.tests.test_langton -v
```

### Doc tests
Only problem 230 uses doc tests. Invoking it without any arguments will cause the script to exit, but the doc tests will still execute.
```sh
python euler/_230_fibonacci_words.py -v
```




### Choice of problems
__107 Minimal Network:__ I chose this problem because it was a very natural application of minimum spanning trees. A few years ago I took a course in algorithms taught by Robert Sedgewick, and I was impressed by an implementation of Kruskal's algorithm for computing MSTs. It made use of various data structures (priority queue, union find, edge-weighted graph) in order to produce a concise, readable way of solving a broad class of problems.

Solving this problem gave me the opportunity to write clean python implementations of these data structures, write tests for them, and use them in a client to quickly solve an interesting problem.

__230 Fibonacci Words:__ This problem, like Langton's Ant, required extrapolation to find a solution for large values of the character index, because brute force (actually building the fibonacci string) quickly exhausts memory.

I found that a functional approach was more natural than writing classes. The `fib_until()`function uses basic dynamic programming to efficiently build a list of numbers in the fibonacci sequence, and `char_at_index()` reverses this list and iterates over it in order to jump backwards from the input index to the index in one of the original input strings.

__349 Langton's Ant:__ This problem was fun to solve because it involved writing highly customized data types (`Ant`, `Grid`, `LangtonSimulate`) to produce a mix of order and chaos from a simple set of rules.

It was also interesting to find a way to exploit the eventual predictability of the ant's movement to extrapolate results for a huge number of steps. The number of steps, 10^18, specified in the problem, is not feasible to simulate, but given that only ~10000 steps are needed before the ant's movement becomes predictable, results can be found for huge numbers of steps.

### Problem-solving process
For `minimal_network`, it was clear from the beginning that computing the MST of the graph would lead to a solution to the problem, so I was most concerned with researching efficient ways to implement Kruskal's algorithm, and the various data types on which it depends.

For `fibonacci_words`, the way to solve the problem became clear after I sketched some `(input, expected output)` pairs in my notebook. Because I took a functional approach, I chose to write doc tests instead of unit tests for the functions I implemented.

For `langton_ant`, sketching the movement of the ant in my notebook made it clear that I would want `Ant` and `Grid` abstractions to keep track of the state of the ant and grid. I wrote these and used them to print out the state of the grid to get a sense of the problem, and saw that after ~10000 steps the movement became predictable. I did some research to find out more about the pattern of ant's movement, and found that from ~10000 steps onward, the ant colors 12 additional squares on the grid to black for every 104 steps it takes. I used this to write a third data type, `LangtonSimulate`, that can extrapolate to find the number of squares colored black after a huge number of steps.



### References
For ideas on how to implement data structures:
http://algs4.cs.princeton.edu/code/

For information about Langton's Ant:
http://mathworld.wolfram.com/LangtonsAnt.html

### Time spent
~15 hours
