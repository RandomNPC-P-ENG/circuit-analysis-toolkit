"""
Circuit Analysis Toolkit — Nodal & Mesh Analysis Solver
电路分析工具箱 — 节点分析 & 网孔分析求解器

Supports: DC analysis, Thevenin/Norton, Delta-Star, Superposition
"""

import numpy as np
from typing import Dict, List, Tuple, Optional


class Component:
    """Base circuit component"""
    def __init__(self, name: str, node1: str, node2: str):
        self.name = name
        self.node1 = node1
        self.node2 = node2


class Resistor(Component):
    def __init__(self, name: str, node1: str, node2: str, resistance: float):
        super().__init__(name, node1, node2)
        self.resistance = resistance
        self.current = 0.0
        self.voltage = 0.0


class VoltageSource(Component):
    def __init__(self, name: str, node_pos: str, node_neg: str, voltage: float):
        super().__init__(name, node_pos, node_neg)
        self.voltage = voltage
        self.current = 0.0


class CurrentSource(Component):
    def __init__(self, name: str, node_from: str, node_to: str, current: float):
        super().__init__(name, node_from, node_to)
        self.current = current


class Circuit:
    """
    DC Circuit Solver using Nodal Analysis
    
    Usage:
        c = Circuit()
        c.add_voltage_source("VS1", "A", "GND", 10)
        c.add_resistor("R1", "A", "B", 1000)
        c.add_resistor("R2", "B", "GND", 2000)
        c.solve()
        c.print_voltages()
    """
    
    def __init__(self):
        self.resistors: List[Resistor] = []
        self.voltage_sources: List[VoltageSource] = []
        self.current_sources: List[CurrentSource] = []
        self.nodes: set = set()
        self.voltages: Dict[str, float] = {}
    
    def add_resistor(self, name: str, node1: str, node2: str, resistance: float):
        r = Resistor(name, node1, node2, resistance)
        self.resistors.append(r)
        self.nodes.add(node1)
        self.nodes.add(node2)
    
    def add_voltage_source(self, name: str, node_pos: str, node_neg: str, voltage: float):
        vs = VoltageSource(name, node_pos, node_neg, voltage)
        self.voltage_sources.append(vs)
        self.nodes.add(node_pos)
        self.nodes.add(node_neg)
    
    def add_current_source(self, name: str, node_from: str, node_to: str, current: float):
        cs = CurrentSource(name, node_from, node_to, current)
        self.current_sources.append(cs)
        self.nodes.add(node_from)
        self.nodes.add(node_to)
    
    def solve(self):
        """Solve circuit using Modified Nodal Analysis (MNA)"""
        nodes = sorted(self.nodes - {"GND"})
        if not nodes:
            return
        
        n = len(nodes)
        m = len(self.voltage_sources)
        size = n + m
        
        node_index = {node: i for i, node in enumerate(nodes)}
        
        G = np.zeros((size, size))
        I = np.zeros(size)
        
        # Stamp resistors (conductance matrix)
        for r in self.resistors:
            g = 1.0 / r.resistance
            i1 = node_index.get(r.node1)
            i2 = node_index.get(r.node2)
            
            if i1 is not None:
                G[i1, i1] += g
            if i2 is not None:
                G[i2, i2] += g
            if i1 is not None and i2 is not None:
                G[i1, i2] -= g
                G[i2, i1] -= g
        
        # Stamp voltage sources
        for k, vs in enumerate(self.voltage_sources):
            row = n + k
            i1 = node_index.get(vs.node1)
            i2 = node_index.get(vs.node2)
            
            if i1 is not None:
                G[i1, row] += 1
                G[row, i1] += 1
            if i2 is not None:
                G[i2, row] -= 1
                G[row, i2] -= 1
            
            I[row] = vs.voltage
        
        # Stamp current sources
        for cs in self.current_sources:
            i1 = node_index.get(cs.node1)
            i2 = node_index.get(cs.node2)
            
            if i1 is not None:
                I[i1] -= cs.current
            if i2 is not None:
                I[i2] += cs.current
        
        # Solve
        try:
            x = np.linalg.solve(G, I)
        except np.linalg.LinAlgError:
            print("Error: Circuit has no unique solution (singular matrix)")
            return
        
        # Extract results
        self.voltages = {"GND": 0.0}
        for node, idx in node_index.items():
            self.voltages[node] = x[idx]
        
        for k, vs in enumerate(self.voltage_sources):
            vs.current = x[n + k]
        
        # Calculate component voltages and currents
        for r in self.resistors:
            v1 = self.voltages.get(r.node1, 0)
            v2 = self.voltages.get(r.node2, 0)
            r.voltage = v1 - v2
            r.current = r.voltage / r.resistance
    
    def print_voltages(self):
        """Print all node voltages"""
        print("\n=== Node Voltages | 节点电压 ===")
        for node in sorted(self.voltages.keys()):
            print(f"  V_{node} = {self.voltages[node]:.4f} V")
    
    def print_currents(self):
        """Print all component currents"""
        print("\n=== Component Currents | 元件电流 ===")
        for r in self.resistors:
            print(f"  {r.name}: {r.current*1000:.4f} mA  ({r.voltage:.4f} V across {r.resistance} Ω)")
        for vs in self.voltage_sources:
            print(f"  {vs.name}: {vs.current*1000:.4f} mA")
    
    def get_voltage(self, node: str) -> float:
        return self.voltages.get(node, 0.0)
    
    def get_current(self, component_name: str) -> float:
        for r in self.resistors:
            if r.name == component_name:
                return r.current
        for vs in self.voltage_sources:
            if vs.name == component_name:
                return vs.current
        return 0.0


def thevenin(circuit: Circuit, node_a: str, node_b: str) -> Tuple[float, float]:
    """
    Calculate Thevenin equivalent between two nodes.
    Returns (Vth, Rth)
    """
    vth = circuit.get_voltage(node_a) - circuit.get_voltage(node_b)
    
    # Rth: deactivate sources, calculate equivalent resistance
    # For simple circuits, Rth = Vth / I_sc (short circuit current)
    # This is a simplified version
    return vth, 0.0  # Rth needs short-circuit calculation


def superposition(circuit_template, sources_list, node_a, node_b="GND"):
    """
    Superposition theorem: solve with each source independently.
    circuit_template: function that takes a Circuit and adds components
    sources_list: list of source names to activate one at a time
    """
    results = []
    for active_source in sources_list:
        c = Circuit()
        circuit_template(c, active_only=active_source)
        c.solve()
        v = c.get_voltage(node_a) - c.get_voltage(node_b)
        results.append(v)
    return sum(results)


if __name__ == "__main__":
    # Example: Simple voltage divider
    print("=== Example: Voltage Divider ===")
    c = Circuit()
    c.add_voltage_source("VS", "A", "GND", 10)
    c.add_resistor("R1", "A", "B", 1000)
    c.add_resistor("R2", "B", "GND", 2000)
    c.solve()
    c.print_voltages()
    c.print_currents()
    
    # Example: Delta-Star
    print("\n=== Example: Delta-Star Transform ===")
    from delta_star import delta_to_star
    Ra, Rb, Rc = delta_to_star(680, 1000, 1200)
    print(f"Delta (680, 1000, 1200) -> Star: Ra={Ra:.1f}Ω, Rb={Rb:.1f}Ω, Rc={Rc:.1f}Ω")
