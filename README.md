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

## License

Distributed under the Apache License 2.0. See ``LICENSE`` for more information.
