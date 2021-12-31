# Graph-Generation-Tool
Graph generation tool which labels the vertices of an input graph according to a power law distribution.

## Run
```
argv[1], input graph file
argv[2], partition degree
argv[3], log function constant
argv[4], log function exponent
argv[5], power function constant
argv[6], power function exponent
argv[7], number of labels
argv[8], scale
```

Example:

```sh
python labeling.py example.graph 100 0.4322 -1.9466 15225 -2.234 3 1 
```

## Input File Format
The graph file foramt is a text format to store an unlabeled, undirected graph.

- Each line of "vertex-ID1 vertex-ID2" in the file represents an edge of the graph. The vertex-ID is an integer.

Example:
```
1 2
1 3 
1 4
2 5
3 5
4 6
5 7
6 9
6 8
10 2
11 2
```

## License

Distributed under the Apache License 2.0. See ``LICENSE`` for more information.
