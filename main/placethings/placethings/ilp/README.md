This file describes the ILP algorithm we used.

## Linear programming in python

We use Pulp, an python ILP API which interfaces with many common ILP solvers, including glpk, gurobi, cplex, etc.
For more information, please see https://www.coin-or.org/PuLP/index.html

In our code, we use glpk to solve ILP problems. You can install glpk use the following:
```
sudo apt-get install glpk
```

## Algorithm

Our method and detailed algorithm are described in the comments of the code. Please see
https://github.com/nesl/Heliot/blob/dev/main/placethings/placethings/ilp/solver.py#L22

A mathematical problem formulation is described in the PDF file.
https://github.com/nesl/Heliot/blob/dev/main/placethings/placethings/ilp/problem_formulation.pdf
