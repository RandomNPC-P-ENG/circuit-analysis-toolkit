# Circuit Solver

Python circuit analysis tools I built for my EE diploma at TAR UMT, KL.

Does nodal analysis, mesh analysis, Delta-Star transform, Thevenin equivalent. Mostly used for homework verification and lab prep.

## Setup

```
pip install numpy
```

## Usage

```python
from circuit_solver import Circuit

c = Circuit()
c.add_voltage_source("VS", "A", "GND", 10)
c.add_resistor("R1", "A", "B", 1000)
c.add_resistor("R2", "B", "GND", 2000)
c.solve()
c.print_voltages()
```

Delta-Star transform:
```python
from delta_star import delta_to_star
Ra, Rb, Rc = delta_to_star(680, 1000, 1200)
```

## Files

- `circuit_solver.py` — MNA-based DC solver
- `delta_star.py` — Delta <-> Star conversion
- `requirements.txt` — just numpy

## Notes

- Tested with Python 3.11, numpy 1.24
- The Thevenin function is incomplete (TODO)
- Superposition is a placeholder, not fully working
