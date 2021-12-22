import functools

known = [65001687610455615650, 880901038222735, 16032398895653777]
[s0,s1,s2] = [65001687610455615650, 880901038222735, 16032398895653777]

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def modinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    gcd = egcd(s1,s0)
    modulus = abs(reduce(gcd, zeroes))
    return crack_unknown_multiplier(states, modulus)

print crack_unknown_modulus(known)
