"""
Delta-Star (triangle <-> Y) transformation.
Used this for Tutorial 7 assignment.
"""


def delta_to_star(r1, r2, r3):
    # R1=A-B, R2=B-C, R3=C-A
    # Ra=at A, Rb=at B, Rc=at C
    s = r1 + r2 + r3
    ra = r2 * r3 / s
    rb = r1 * r3 / s
    rc = r1 * r2 / s
    return (ra, rb, rc)


def star_to_delta(ra, rb, rc):
    p = ra * rb + rb * rc + ra * rc
    r1 = p / rc
    r2 = p / rb
    r3 = p / ra
    return (r1, r2, r3)


def verify(r1, r2, r3, ra, rb, rc):
    s = r1 + r2 + r3
    # check all 3 terminal pairs
    d_ab = r1 * (r2 + r3) / s
    d_bc = r2 * (r1 + r3) / s
    d_ca = r3 * (r1 + r2) / s
    ok = (abs(d_ab - (ra + rb)) < 0.01 * d_ab and
          abs(d_bc - (rb + rc)) < 0.01 * d_bc and
          abs(d_ca - (rc + ra)) < 0.01 * d_ca)
    return ok


if __name__ == "__main__":
    # Tutorial 7 values
    r1, r2, r3 = 680, 1000, 1200
    print(f"Delta: R1={r1}, R2={r2}, R3={r3}")

    ra, rb, rc = delta_to_star(r1, r2, r3)
    print(f"Star: Ra={ra:.1f}, Rb={rb:.1f}, Rc={rc:.1f}")

    if verify(r1, r2, r3, ra, rb, rc):
        print("verification OK")
    else:
        print("verification FAILED")

    # reverse check
    r1b, r2b, r3b = star_to_delta(ra, rb, rc)
    print(f"\nReverse: R1={r1b:.1f}, R2={r2b:.1f}, R3={r3b:.1f}")
