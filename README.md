# Circuit Solver

C++ circuit analysis tools I built for my EE diploma at TAR UMT.

Does nodal analysis, Delta-Star transform. Mostly used for homework verification and lab prep.

## Build

```
g++ circuit_solver.cpp -o solver
g++ delta_star.cpp -o delta_star
```

## Files

- `circuit_solver.cpp` — MNA-based DC solver (voltage divider example)
- `delta_star.cpp` — Delta <-> Star conversion (interactive, for(;;) loop)
- `requirements.txt` — nothing needed, pure C++

## TODO

- add mesh analysis
- add thevenin equivalent
- add more component types (capacitor, inductor for AC)
