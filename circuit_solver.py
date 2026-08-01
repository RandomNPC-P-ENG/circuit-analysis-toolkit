"""
Circuit solver using Modified Nodal Analysis (MNA).
Supports resistors, voltage sources, current sources.
"""

import numpy as np


class Resistor:
    def __init__(self, name, node1, node2, resistance):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.resistance = resistance
        self.current = 0.0
        self.voltage = 0.0


class VoltageSource:
    def __init__(self, name, node_pos, node_neg, voltage):
        self.name = name
        self.node1 = node_pos
        self.node2 = node_neg
        self.voltage = voltage
        self.current = 0.0


class CurrentSource:
    def __init__(self, name, node_from, node_to, current):
        self.name = name
        self.node1 = node_from
        self.node2 = node_to
        self.current = current


class Circuit:
    def __init__(self):
        self.resistors = []
        self.voltage_sources = []
        self.current_sources = []
        self.nodes = set()
        self.voltages = {}

    def add_resistor(self, name, node1, node2, resistance):
        self.resistors.append(Resistor(name, node1, node2, resistance))
        self.nodes.add(node1)
        self.nodes.add(node2)

    def add_voltage_source(self, name, node_pos, node_neg, voltage):
        self.voltage_sources.append(VoltageSource(name, node_pos, node_neg, voltage))
        self.nodes.add(node_pos)
        self.nodes.add(node_neg)

    def add_current_source(self, name, node_from, node_to, current):
        self.current_sources.append(CurrentSource(name, node_from, node_to, current))
        self.nodes.add(node_from)
        self.nodes.add(node_to)

    def solve(self):
        # MNA stamp
        nodes = sorted(self.nodes - {"GND"})
        if not nodes:
            return
        n = len(nodes)
        m = len(self.voltage_sources)
        size = n + m
        idx = {node: i for i, node in enumerate(nodes)}

        G = np.zeros((size, size))
        I = np.zeros(size)

        # stamp resistors
        for r in self.resistors:
            g = 1.0 / r.resistance
            i1 = idx.get(r.node1)
            i2 = idx.get(r.node2)
            if i1 is not None:
                G[i1, i1] += g
            if i2 is not None:
                G[i2, i2] += g
            if i1 is not None and i2 is not None:
                G[i1, i2] -= g
                G[i2, i1] -= g

        # stamp voltage sources
        for k, vs in enumerate(self.voltage_sources):
            row = n + k
            i1 = idx.get(vs.node1)
            i2 = idx.get(vs.node2)
            if i1 is not None:
                G[i1, row] += 1
                G[row, i1] += 1
            if i2 is not None:
                G[i2, row] -= 1
                G[row, i2] -= 1
            I[row] = vs.voltage

        # stamp current sources
        for cs in self.current_sources:
            i1 = idx.get(cs.node1)
            i2 = idx.get(cs.node2)
            if i1 is not None:
                I[i1] -= cs.current
            if i2 is not None:
                I[i2] += cs.current

        try:
            x = np.linalg.solve(G, I)
        except np.linalg.LinAlgError:
            print("singular matrix — check your circuit")
            return

        self.voltages = {"GND": 0.0}
        for node, i in idx.items():
            self.voltages[node] = x[i]

        for k, vs in enumerate(self.voltage_sources):
            vs.current = x[n + k]

        for r in self.resistors:
            v1 = self.voltages.get(r.node1, 0)
            v2 = self.voltages.get(r.node2, 0)
            r.voltage = v1 - v2
            r.current = r.voltage / r.resistance

    def print_voltages(self):
        print("\nNode Voltages:")
        for node in sorted(self.voltages.keys()):
            print(f"  V_{node} = {self.voltages[node]:.4f} V")

    def print_currents(self):
        print("\nCurrents:")
        for r in self.resistors:
            print(f"  {r.name}: {r.current*1000:.4f} mA ({r.voltage:.4f} V)")
        for vs in self.voltage_sources:
            print(f"  {vs.name}: {vs.current*1000:.4f} mA")

    def get_voltage(self, node):
        return self.voltages.get(node, 0.0)


# TODO: thevenin equivalent — need to figure out Rth via short-circuit method
# TODO: superposition — run solve() with each source active one at a time


if __name__ == "__main__":
    # voltage divider: 10V -> 1k -> 2k -> GND
    c = Circuit()
    c.add_voltage_source("VS", "A", "GND", 10)
    c.add_resistor("R1", "A", "B", 1000)
    c.add_resistor("R2", "B", "GND", 2000)
    c.solve()
    c.print_voltages()
    c.print_currents()
