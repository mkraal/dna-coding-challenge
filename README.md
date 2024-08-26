# DNA Nexus coding challenge

* **autor:** michalkraal@gmail.com
* **created:** 2024-07-15

## Dependencies

Everything apart from mocking the data and linting/formatting uses standard Python libraries.
Built with Python 3.10.
Simple linting and formatting done with `ruff`.
Data mocking is done with `faker`.

## Problem 1

### Usage
```
python main.py <path/to/data> <target>
```

### Description
The solutions uses two classes - `FileMeta` and `FileSearcher`.

`FileSearcher` contains methods necessary to find the target row in the input text file.
`FileMeta` is a class that handles some metadata of both index and input files and helps with readability.

#### General approach

If index is not built, it starts with:
1. Open the input file
2. Iterate over it and write the number of current line and byte offset of each start of line to an index file
3. Write total length of input file, length of index file and total number of lines to a metadata json file

The search itself:
1. Take the target value on the input
2. Look for it in the index file using binary search (using the byte size of the index file)
3. When found, return the byte offset in the input file
4. Open the input file
5. Find the offset in the input file and return it
6. Print it out

It is possible to generate test data using (and/or parameterizing) `mock_data.py`. A few simple unit tests are based on `data/small_sample.txt`. 

### Room for improvement
- parameterize the cache path
- implement other algorithms for benchmarking the solution
- Dockerization

## Problem 2

### Usage
```
python problem_2.py
```

### Description

A way simpler implementation using binary search again.

In order to test the algorithm, the input needs to be changed manually in the file of the script itself.

Some edge cases can be resolved in O(1) time, then we perform the binary search and return the valid index that, if valid, will be stored in the `low` variable.

### Room for improvement
- implement at least some testing
- let user provide the input and/or have more test cases


## Requirements

See [`pyproject.toml`](./pyproject.toml)