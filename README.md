# Circuit Analysis Toolkit | 电路分析工具箱

Python tools for DC/AC circuit analysis — nodal analysis, mesh analysis, Thevenin/Norton equivalents, Delta-Star transformation, and more.

Python 电路分析工具，支持节点分析、网孔分析、戴维南/诺顿等效、Delta-Star 变换等。

---

## Features | 功能

- **Nodal Analysis** — Automatic KCL equation generation and solving
- **Mesh Analysis** — Automatic KVL equation generation and solving
- **Thevenin/Norton** — Equivalent circuit calculation
- **Delta-Star Transform** — Δ↔Y resistance conversion
- **AC Analysis** — Phasor impedance, frequency response
- **Bode Plots** — Magnitude and phase plots
- **Superposition** — Multi-source circuit solving

## Requirements | 环境要求

```bash
pip install numpy matplotlib
```

## Quick Start | 快速开始

```python
from circuit_solver import Circuit

# Create circuit
c = Circuit()
c.add_voltage_source("VS1", "A", "GND", 10)
c.add_resistor("R1", "A", "B", 1000)
c.add_resistor("R2", "B", "GND", 2000)

# Solve
c.solve()
c.print_voltages()
c.print_currents()
```

## Delta-Star Example

```python
from delta_star import delta_to_star, star_to_delta

# Delta to Star
Ra, Rb, Rc = delta_to_star(680, 1000, 1200)
print(f"Ra={Ra:.1f}, Rb={Rb:.1f}, Rc={Rc:.1f}")
# Ra=283.3, Rb=236.1, Rc=416.7
```

## Project Structure | 项目结构

```
circuit_solver.py   # Main solver engine
delta_star.py       # Delta-Star transformation
ac_analysis.py      # AC phasor analysis
bode_plot.py        # Bode plot generator
examples/           # Example circuits
```

## License

MIT
