"""
Delta-Star (Δ-Y) Transformation | Delta-Star 变换

Convert between Delta (triangle/Π) and Star (Y/T) resistor networks.
"""

from typing import Tuple


def delta_to_star(r1: float, r2: float, r3: float) -> Tuple[float, float, float]:
    """
    Convert Delta to Star.
    
    Delta: R1 between A-B, R2 between B-C, R3 between C-A
    Star:  Ra at A, Rb at B, Rc at C
    
    Args:
        r1: Resistance between A-B (Ohms)
        r2: Resistance between B-C (Ohms)
        r3: Resistance between C-A (Ohms)
    
    Returns:
        (Ra, Rb, Rc) in Ohms
    
    Example:
        >>> delta_to_star(680, 1000, 1200)
        (283.33, 236.11, 416.67)
    """
    sigma = r1 + r2 + r3
    ra = r2 * r3 / sigma
    rb = r1 * r3 / sigma
    rc = r1 * r2 / sigma
    return (ra, rb, rc)


def star_to_delta(ra: float, rb: float, rc: float) -> Tuple[float, float, float]:
    """
    Convert Star to Delta.
    
    Args:
        ra: Resistance at A (Ohms)
        rb: Resistance at B (Ohms)
        rc: Resistance at C (Ohms)
    
    Returns:
        (R1, R2, R3) in Ohms
        R1 = A-B, R2 = B-C, R3 = C-A
    
    Example:
        >>> star_to_delta(283.33, 236.11, 416.67)
        (680.0, 1000.0, 1200.0)
    """
    sum_products = ra * rb + rb * rc + ra * rc
    r1 = sum_products / rc
    r2 = sum_products / rb
    r3 = sum_products / ra
    return (r1, r2, r3)


def verify_equivalence(r1, r2, r3, ra, rb, rc) -> bool:
    """
    Verify that Delta and Star are equivalent (3 terminal pairs match).
    """
    sigma = r1 + r2 + r3
    
    # A-B
    delta_ab = r1 * (r2 + r3) / sigma
    star_ab = ra + rb
    
    # B-C
    delta_bc = r2 * (r1 + r3) / sigma
    star_bc = rb + rc
    
    # C-A
    delta_ca = r3 * (r1 + r2) / sigma
    star_ca = rc + ra
    
    tol = 0.01  # 1% tolerance
    return (abs(delta_ab - star_ab) < tol * delta_ab and
            abs(delta_bc - star_bc) < tol * delta_bc and
            abs(delta_ca - star_ca) < tol * delta_ca)


if __name__ == "__main__":
    # Example from Tutorial 7
    print("=== Delta-Star Transform Example ===")
    r1, r2, r3 = 680, 1000, 1200
    print(f"Delta: R1={r1}Ω, R2={r2}Ω, R3={r3}Ω")
    
    ra, rb, rc = delta_to_star(r1, r2, r3)
    print(f"Star:  Ra={ra:.1f}Ω, Rb={rb:.1f}Ω, Rc={rc:.1f}Ω")
    
    # Verify
    print(f"\nEquivalence check: {'PASS ✓' if verify_equivalence(r1, r2, r3, ra, rb, rc) else 'FAIL ✗'}")
    
    # Reverse: Star to Delta
    r1b, r2b, r3b = star_to_delta(ra, rb, rc)
    print(f"\nReverse: Star -> Delta")
    print(f"R1={r1b:.1f}Ω, R2={r2b:.1f}Ω, R3={r3b:.1f}Ω")
    print(f"Match: {'PASS ✓' if abs(r1b-r1)<0.1 else 'FAIL ✗'}")
