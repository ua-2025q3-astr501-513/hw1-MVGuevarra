#!/usr/bin/env python3
#
# Please look for "TODO" in the comments, which indicate where you
# need to write your code.
#
# Part 3: Implement a Numerically Stable Quadratic Equation Solver (1 point)
#
# * Objective:
#   Implement a numerically stable quadratic equation solver that does
#   not catastrophic cancellation.
# * Details:
#   The description of the problem and the solution template can be
#   found in `hw1/p3.py`.
#
# From lecture `01w`, we learned about catastrophic cancellation---the
# significant loss of precision that occurs when subtracting two
# nearly equal numbers.
# This problem actually appeared in CK's research!
# While solving for the initial conditions of (unstable) spherical
# photon orbits around a black hole for the convergence test of
# [GRay2](https://ui.adsabs.harvard.edu/abs/2018ApJ...867...59C),
# catastrophic cancellation introduced errors so severe that photons
# would not remain on their spherical orbits for an radian.
# CK suspected a bug in the integrator and spent an entire month
# debugging the wrong part of the code.
# At the end, he realized the real problem.
# The standard quadratic formula we all learn in high school was
# simply not accurate enough for reliable numerical computation.
#
# Here, let's implement a numerically stable quadratic equation solver
# to overcome catastrophic cancellation.
# Please make sure that you take care of all the special cases.

cut_off = 1e-6 # Cut-off for catastrophic cancellation

def quadratic(a, b, c):
    """Numerically stable quadratic equation solver

    The standard quadratic formula

        x = (-b +- sqrt(b^2 - 4ac)) / (2a)

    is algebraically correct but can suffer from *catastrophic
    cancellation* when b^2 >> 4ac and the sign of b matches the
    chosen +-.
    In that case, subtracting two nearly equal numbers causes a large
    loss of precision.

    A more stable alternative is obtained by multiplying top and
    bottom by the conjugate, leading to two equivalent forms.
    To avoid cancellation, choose the version that keeps the
    subtraction well-separated:

        x1 = (-b - sign(b) * sqrt(b^2 - 4ac)) / (2a)
        x2 = (c / a) / x1

    This way, at least one root is always computed stably.

    Args:
        a, b, c: coefficients for the quadratic equation
                 a x^2 + b x + c = 0.

    Returns:
        x1, x2: the two roots of the quadratic equation.
                If there are two real roots, x1 < x2.
                If there is only one real root, x2 == None.
                If there is no real root, x1 == x2 == None.
    """
    # TODO: implement the stable quadratic equation solver here

    # So, wanna do some 'edge' cases here. Like, obviously, the x1 and x2 stuff aren't well-defined if a = 0.

    if a == 0:
        if b == 0:
            return (None)
        else:
            return c / b
    else: # We also wish to classify complex roots.
        if b**2 - 4*a*c < 0: # This implies both roots complex
            x1,x2 = None,None # Restrict domain to reals.
            return x1,x2
        elif b**2 == 4*a*c: # This implies a single real root
            x1,x2 = -b/(2*a), None # Standard stuff.
            return x1,x2
        elif b**2 - 4*a*c > 0: # This implies two real roots... the real thing to watch out for for 
        # catastrophically unstable crap.
        # So how do I do that? From the notes, we see catastrophic instability if b >> a,c, such that
        # \frac{-b \pm \sqrt{b^2 - 4ac}}{2a} = -\frac{b}{2a} \left(1 \mp \sqrt{1 - \frac{4ac}{b^2}} \right)
        # \approx -\frac{b}{2a} (1 \mp (1 - \frac{2ac}{b^2})) = -\frac{b}{2a}((1 \mp 1) \pm \frac{2ac}{b^2})
        # = -\frac{b(1 \mp 1)}{2a} \mp \frac{c}{b}
        # Clearly one root will be approximately -c/b ~ 0 (linear approx.), the other c/b + b/a ~ b/a (eventually ax^2 is
        # large enough to reach back to zero). Let's imagine some cut-off, 1e-6, such that these approximations come into play
        # if b^2 - 4ac < \varepsilon, \varepsilon = 1e-6
            if b**2 - 4*a*c < cut_off:
                x1, x2 = -c/b, c/b + b/a
                return x1, x2
            else:
                x1,x2 = (-b - (b**2 - 4*a*c)**0.5)/(2*a),(-b + (b**2 - 4*a*c)**0.5)/(2*a)
                return x1,x2
