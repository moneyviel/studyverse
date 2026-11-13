"""Real JEE Main questions — Physics Unit 16: Optics. Our own solutions; chk re-solves each one a different way:
mirrors and lenses by tracing a near-axis ray through the actual curved surfaces with the law of reflection or
Snell's law (no mirror/lens formula used), prisms and slabs by applying Snell's law surface by surface, and
interference/diffraction by adding wave phasors numerically. Skipped: items whose printed figure or key we could
not confirm."""
import math, cmath
from common import new_registry, pick, verify
P, add = new_registry()
pi = math.pi
def P4(opts, v, tol=1e-3): return pick([o / v for o in opts], 1.0, tol) if v else pick(opts, v, tol)
def snell(n1, n2, th): s = n1 * math.sin(th) / n2; return math.asin(s) if abs(s) <= 1 else None
def surf(z0, R, n1, n2, ray):
    """refract a ray (z, y, slope) at a spherical surface with vertex z0, radius R (R > 0: centre to the right); R = None for flat"""
    z, y, m = ray
    if R is None: zs = z0
    else:
        c = z0 + R; dz, dy = 1.0, m   # line (z + t, y + m t); solve |P − C| = |R| nearest the vertex
        a = 1 + m * m; b = 2 * ((z - c) + m * y); cc = (z - c) ** 2 + y * y - R * R; d = math.sqrt(b * b - 4 * a * cc)
        ts = [(-b - d) / (2 * a), (-b + d) / (2 * a)]; t = min(ts, key=lambda t: abs(z + t - z0)); zs = z + t
    ys = y + m * (zs - z)
    d = (1 / math.sqrt(1 + m * m), m / math.sqrt(1 + m * m))   # travelling to the right
    nv = (1.0, 0.0) if R is None else ((zs - (z0 + R)) / R, ys / R)   # unit normal pointing along +z near the axis
    if nv[0] < 0: nv = (-nv[0], -nv[1])
    r = n1 / n2; ci = d[0] * nv[0] + d[1] * nv[1]; k = 1 - r * r * (1 - ci * ci)
    t = (r * d[0] + (math.sqrt(k) - r * ci) * nv[0], r * d[1] + (math.sqrt(k) - r * ci) * nv[1])
    return (zs, ys, t[1] / t[0])
def axis_cross(ray): z, y, m = ray; return z - y / m
def lens_image(u, surfaces, h=1e-5):
    """object on the axis at z = u (negative = left). surfaces = list of (z0, R, n1, n2). returns image position (z)"""
    ray = (u, 0.0, h)
    for s in surfaces: ray = surf(*s, ray)
    return axis_cross(ray)
def focal(surfaces, h=1e-6):   # parallel ray from far left
    ray = (-1.0, h, 0.0)
    for s in surfaces: ray = surf(*s, ray)
    return axis_cross(ray)
def mirror_image(u, R, h=1e-6):
    """concave mirror R < 0 (centre to the left, vertex at 0, light from the left); convex R > 0. returns image z"""
    c = R; m = h; z, y = u, 0.0
    a = 1 + m * m; b = 2 * ((z - c) + m * y); cc = (z - c) ** 2 + y * y - R * R; d = math.sqrt(b * b - 4 * a * cc)
    t = min([(-b - d) / (2 * a), (-b + d) / (2 * a)], key=lambda t: abs(z + t)); zs = z + t; ys = y + m * t
    nx, ny = (zs - c) / abs(R), ys / abs(R); dx, dy = 1 / math.sqrt(1 + m * m), m / math.sqrt(1 + m * m); dot = dx * nx + dy * ny
    rx, ry = dx - 2 * dot * nx, dy - 2 * dot * ny
    return zs - ys * rx / ry
def yd(path_diff, lam, I1=1.0, I2=1.0): return abs(math.sqrt(I1) + math.sqrt(I2) * cmath.exp(2j * pi * path_diff / lam)) ** 2
def biconvex(R1, R2, n, nm=1.0): return [(0, R1, nm, n), (0, -R2, n, nm)]
def thin_f(R1, R2, n, nm=1.0): return focal([(0, R1, nm, n), (0, R2, n, nm)])
def slit_minima(a, lam, m): return math.asin(m * lam / a)
def single_slit_I(a, lam, th, n=2000):   # sum of phasors across the slit
    return abs(sum(cmath.exp(2j * pi * (a * (k + 0.5) / n) * math.sin(th) / lam) for k in range(n)) / n) ** 2
def first_zero(a, lam, lo=1e-9, hi=None):
    hi = hi or min(pi / 2, 1.5 * lam / a); f = lambda th: single_slit_I(a, lam, th, 400)
    th = lo; step = (hi - lo) / 2000
    while f(th + step) < f(th): th += step   # walk down to the first minimum
    return th

# ---------- sheets 1–2
def _f3():   # equi-convex glass lens: bisect on its focal length until an object 10 cm away gives a virtual image 30 cm away
    lo, hi = 0.11, 1.0
    for _ in range(80):
        f = (lo + hi) / 2; R = f   # n = 1.5 equi-convex: f = R
        v = lens_image(-0.10, biconvex(R, R, 1.5))
        if v < -0.30: lo = f
        else: hi = f
    return (lo + hi) / 2
add(('2024', 'Feb', '2024-02-01', 1), 'wave', 'A monochromatic light of wavelength 6000 Å is incident on the single slit of width 0.01 mm. If the diffraction pattern is formed at the focus of the convex lens of focal length 20 cm, the linear width of the central maximum is :',
    ['60 mm', '24 mm', '120 mm', '12 mm'], 2, lambda: P4([60, 24, 120, 12], 2 * 0.2 * math.tan(first_zero(1e-5, 6e-7)) * 1000, 5e-3), ['First minima at sin θ = \\f{λ}{a} = 0.06.', 'Width = \\f{2fλ}{a} = \\f{2 × 0.2 × 6 × 10^{−7}}{10^{−5}} = 0.024 m = 24 mm.'], 'wave', 1)
add(('2024', 'Feb', '2024-02-01', 1), 'lens', 'The distance between object and its 3 times magnified virtual image as produced by a convex lens is 20 cm. The focal length of the lens used is ______ cm.', None, 15,
    lambda: round(_f3() * 100, 3),
    ['Virtual image on the same side: v = 3u, and |v| − |u| = 20 cm → u = −10 cm, v = −30 cm.', '\\f{1}{f} = \\f{1}{v} − \\f{1}{u} = −\\f{1}{30} + \\f{1}{10} → f = 15 cm.'], 'lens', 1)
add(('2024', 'Feb', '2024-02-01', 2), 'wave', 'A microwave of wavelength 2.0 cm falls normally on a slit of width 4.0 cm. The angular spread of the central maxima of the diffraction pattern obtained on a screen 1.5 m away from the slit, will be:',
    ['30°', '15°', '60°', '45°'], 3, lambda: P4([30, 15, 60, 45], 2 * math.degrees(first_zero(0.04, 0.02, hi=pi / 2 - 1e-3)), 3e-3), ['First minima at sin θ = \\f{λ}{a} = 0.5 → θ = 30° on each side.', 'Angular spread = 2θ = 60°.'], 'wave', 1)
def _half():
    lam, d, D = 5e-7, 1e-3, 1.0; y = 0.0
    while yd(d * y / D, lam) > 2.0: y += 1e-9   # maximum is 4 for equal slits
    return round(y / 1e-6)
add(('2024', 'Feb', '2024-02-01', 2), 'wave', 'In Young\'s double slit experiment, monochromatic light of wavelength 5000 Å is used. The slits are 1.0 mm apart and screen is placed at 1.0 m away from slits. The distance from the centre of the screen where intensity becomes half of the maximum intensity for the first time is ______ × 10^{−6} m.', None, 125,
    lambda: _half(), ['I = I_{max} cos^{2}\\f{φ}{2}: half intensity when φ = \\f{π}{2}, i.e. path difference \\f{λ}{4}.', 'y = \\f{λD}{4d} = \\f{5 × 10^{−7} × 1}{4 × 10^{−3}} = 125 × 10^{−6} m.'], 'wave', 2)
add(('2025', 'Apr', '2025-04-02', 1), 'refr', 'A spherical surface (radius R = 0.4 m, centre of curvature C in medium 2) separates two media of refractive indices n_{1} = 1 and n_{2} = 1.5. An object O is in medium 1 at 0.2 m from the surface. Distance of the image of the object O is :',
    ['0.24 m left to the spherical surface', '0.4 m right to the spherical surface', '0.24 m right to the spherical surface', '0.4 m left to the spherical surface'], 4,
    lambda: pick([-0.24, 0.4, 0.24, -0.4], round(lens_image(-0.2, [(0, 0.4, 1.0, 1.5)]), 6)), ['\\f{n_{2}}{v} − \\f{n_{1}}{u} = \\f{n_{2} − n_{1}}{R} with u = −0.2, R = +0.4.', '\\f{1.5}{v} = 1.25 − 5 → v = −0.4 m: a virtual image 0.4 m to the left.'], 'refr', 2)
def _slant():
    S = biconvex(0.2, 0.2, 1.5)   # f = 20 cm
    A = (-0.30, 0.0); B = (-0.29, 0.02)
    vA = lens_image(A[0], S); vB = lens_image(B[0], S); hB = B[1] * vB / B[0]   # thin lens: image height y·v/u (through the centre)
    return round(math.degrees(math.atan2(hB, vB - vA)), 6)
add(('2025', 'Apr', '2025-04-02', 1), 'lens', 'A slanted object AB is placed on one side of a convex lens of focal length 20 cm. End A is on the principal axis 30 cm from the lens; end B is 2 cm above the axis and 1 cm nearer to the lens (so AB makes angle α with the axis). The image is formed on the opposite side. Angle made by the image with principal axis is :',
    ['−45°', '−\\f{α}{2}', '+45°', '−α'], 1, lambda: pick([-45, -math.degrees(math.atan(2)) / 2, 45, -math.degrees(math.atan(2))], _slant(), 1e-6),
    ['A (u = −30 cm): v = 60 cm on the axis.', 'B (u = −29 cm, 2 cm high): v = \\f{580}{9} cm, height −2 × \\f{580/9}{29} = −\\f{40}{9} cm.', 'Image slope = \\f{−40/9}{580/9 − 60} = −1 → −45°.'], 'lens', 3)
add(('2025', 'Apr', '2025-04-02', 1), 'wave', 'If the measured angular separation between the second minimum to the left of the central maximum and the third minimum to the right of the central maximum is 30° in a single slit diffraction pattern recorded using 628 nm light, then the width of the slit is ______ μm. (Use small-angle approximation, π = 3.14)', None, 6,
    lambda: round(5 * 628e-9 / (30 * 3.14 / 180) / 1e-6, 6), ['Minima at θ ≈ \\f{mλ}{a}: from m = −2 to m = +3 spans \\f{5λ}{a}.', '\\f{5λ}{a} = \\f{π}{6} → a = \\f{30λ}{π} = \\f{30 × 628 × 10^{−9}}{3.14} = 6 μm.'], 'wave', 2)
add(('2025', 'Apr', '2025-04-02', 2), 'mirror', 'Two identical objects are placed in front of convex mirror and concave mirror having same radii of curvature of 12 cm, at same distance of 18 cm from the respective mirrors. The ratio of sizes of the images formed by convex mirror and by concave mirror is :',
    ['1/3', '1/2', '3', '2'], 2, lambda: P4([1 / 3, 0.5, 3, 2], abs(mirror_image(-0.18, 0.12) / 0.18) / abs(mirror_image(-0.18, -0.12) / 0.18)),
    ['f = 6 cm. Convex: \\f{1}{v} = \\f{1}{6} + \\f{1}{18} → v = 4.5 cm, m = \\f{1}{4}.', 'Concave: \\f{1}{v} = −\\f{1}{6} + \\f{1}{18} → v = −9 cm, m = −\\f{1}{2}.', 'Ratio of sizes = \\f{1/4}{1/2} = \\f{1}{2}.'], 'mirror', 1)
add(('2025', 'Apr', '2025-04-02', 2), 'lens', 'A bi-convex lens has radius of curvature of both the surfaces same as 1/6 cm. If this lens is required to be replaced by another convex lens having different radii of curvatures on both sides (R_{1} ≠ R_{2}), without any change in lens power then possible combination of R_{1} and R_{2} is :',
    ['\\f{1}{5} cm and \\f{1}{7} cm', '\\f{1}{3} cm and \\f{1}{3} cm', '\\f{1}{6} cm and \\f{1}{9} cm', '\\f{1}{3} cm and \\f{1}{7} cm'], 1,
    lambda: pick([round(1 / thin_f(a / 100, -b / 100, 1.5), 3) for a, b in ((1 / 5, 1 / 7), (1 / 3, 1 / 3), (1 / 6, 1 / 9), (1 / 3, 1 / 7))], round(1 / thin_f(1 / 600, -1 / 600, 1.5), 3)),
    ['Same glass: P ∝ \\f{1}{R_{1}} + \\f{1}{R_{2}}, which is 6 + 6 = 12 per cm now.', 'Only 5 + 7 = 12 matches (and R_{1} ≠ R_{2}).'], 'lens', 1)
def _mindev():
    A, n = pi / 3, math.sqrt(2); best = (1e9, 0)
    for k in range(1, 9000):
        i = k * 1e-4 * 1.5; r1 = snell(1, n, i); r2 = A - r1; e = snell(n, 1, r2)
        if e is None: continue
        d = i + e - A; best = min(best, (d, i))
    return round(math.degrees(best[1]))
add(('2025', 'Apr', '2025-04-02', 2), 'refr', 'A ray of light suffers minimum deviation when incident on a prism having angle of the prism equal to 60°. The refractive index of the prism material is √{2}. The angle of incidence (in degrees) is ______', None, 45,
    lambda: _mindev(), ['At minimum deviation r = \\f{A}{2} = 30°.', 'sin i = √{2} sin 30° = \\f{1}{√{2}} → i = 45°.'], 'refr', 1)

# ---------- sheets 3–4
def _prism_facts():
    A, n = pi / 3, 1.5
    dev = lambda i, A: (lambda r1: (lambda e: i + e - A if e is not None else None)(snell(n, 1, A - r1)))(snell(1, n, i))
    ds = [(dev(k * 1e-4, A), k * 1e-4) for k in range(1, 15700) if dev(k * 1e-4, A) is not None]; dmin, imin = min(ds); r1 = snell(1, n, imin)
    A_ok = abs(r1 - A / 2) < 1e-3   # inside ray symmetric → parallel to the base of an isosceles prism
    A2 = 5 * pi / 12; d2 = min(d for d in (dev(k * 1e-4, A2) for k in range(1, 15700)) if d is not None); B_ok = d2 < dmin   # a 75° prism vs the 60° one
    C_ok = abs(snell(n, 1, A - r1) - imin) < 2e-3
    D_ok = sum(1 for d, i in ds if abs(d - (dmin + 0.05)) < 2e-5) >= 2
    E_ok = abs(r1 - 2 * A) < 1e-3
    return ''.join(k for k, ok in zip('ABCDE', [A_ok, B_ok, C_ok, D_ok, E_ok]) if ok)
add(('2025', 'Apr', '2025-04-03', 1), 'refr', 'Consider following statements for refraction of light through prism, when angle of deviation is minimum. A. The refracted ray inside prism becomes parallel to the base. B. Larger angle prisms provide smaller angle of minimum deviation. C. Angle of incidence and angle of emergence becomes equal. D. There are always two sets of angle of incidence for which deviation will be same except at minimum deviation setting. E. Angle of refraction becomes double of prism angle.',
    ['B, D and E Only', 'B, C and D Only', 'A, C and D Only', 'A, B and E Only'], 3, lambda: pick(['BDE', 'BCD', 'ACD', 'ABE'], _prism_facts()),
    ['At minimum deviation the path is symmetric: i = e and r_{1} = r_{2} = \\f{A}{2} (so E is false), and the ray inside runs parallel to the base.', 'A bigger prism angle gives a BIGGER minimum deviation, so B is false.', 'Any other deviation is reached by two incidence angles (i and e swap): D is true.'], 'refr', 2)
add(('2025', 'Apr', '2025-04-03', 1), 'lens', 'The radii of curvature for a thin convex lens are 10 cm and 15 cm respectively. The focal length of the lens is 12 cm. The refractive index of the lens material is',
    ['1.8', '1.4', '1.5', '1.2'], 3, lambda: P4([1.8, 1.4, 1.5, 1.2], next(n for n in [1 + k / 1000 for k in range(1, 1000)] if abs(thin_f(0.10, -0.15, n) - 0.12) < 2e-5), 2e-3),
    ['\\f{1}{f} = (n − 1)(\\f{1}{10} + \\f{1}{15}) = \\f{n − 1}{6}.', '\\f{1}{12} = \\f{n − 1}{6} → n = 1.5.'], 'lens', 1)
add(('2025', 'Apr', '2025-04-03', 1), 'wave', 'Two coherent monochromatic light beams of intensities 4I and 9I are superimposed. The difference between the maximum and minimum intensities in the resulting interference pattern is xI. The value of x is ______.', None, 24,
    lambda: round(max(yd(k / 360, 1, 4, 9) for k in range(361)) - min(yd(k / 360, 1, 4, 9) for k in range(361))), ['I_{max} = (√{4} + √{9})^{2} I = 25I, I_{min} = (3 − 2)^{2} I = I.', 'Difference = 24I.'], 'wave', 1)
add(('2025', 'Apr', '2025-04-03', 2), 'refr', 'A monochromatic light of frequency 5 × 10^{14} Hz travelling through air, is incident on a medium of refractive index \'2\'. Wavelength of the refracted light will be:',
    ['500 nm', '400 nm', '300 nm', '600 nm'], 3, lambda: P4([500, 400, 300, 600], 3e8 / 2 / 5e14 / 1e-9), ['Frequency stays the same; speed becomes \\f{c}{2}.', 'λ = \\f{c}{nf} = \\f{3 × 10^{8}}{2 × 5 × 10^{14}} = 300 nm.'], 'refr', 1)
add(('2025', 'Apr', '2025-04-03', 2), 'wave', 'Two monochromatic light beams have intensities in the ratio 1 : 9. An interference pattern is obtained by these beams. The ratio of the intensities of maximum to minimum is',
    ['4 : 1', '3 : 1', '8 : 1', '9 : 1'], 1, lambda: P4([4, 3, 8, 9], yd(0, 1, 1, 9) / yd(0.5, 1, 1, 9)), ['Amplitudes are in the ratio 1 : 3.', '\\f{I_{max}}{I_{min}} = \\f{(1 + 3)^{2}}{(3 − 1)^{2}} = 4.'], 'wave', 1)
add(('2025', 'Apr', '2025-04-03', 2), 'wave', 'Width of one of the two slits in a Young\'s double slit interference experiment is half of the other slit. The ratio of the maximum to the minimum intensity in the interference pattern is :',
    ['(2√{2} + 1) : (2√{2} − 1)', '3 : 1', '(3 + 2√{2}) : (3 − 2√{2})', '9 : 1'], 3,
    lambda: P4([(2 * math.sqrt(2) + 1) / (2 * math.sqrt(2) - 1), 3, (3 + 2 * math.sqrt(2)) / (3 - 2 * math.sqrt(2)), 9], yd(0, 1, 2, 1) / yd(0.5, 1, 2, 1)),
    ['Intensity through a slit ∝ its width: I_{1} = 2I_{2}, amplitudes √{2} : 1.', '\\f{I_{max}}{I_{min}} = \\f{(√{2} + 1)^{2}}{(√{2} − 1)^{2}} = \\f{3 + 2√{2}}{3 − 2√{2}}.'], 'wave', 2)
def _src():
    lo, hi = 0.6, 50.0   # bisect on the source distance until the image is 2 m inside the glass
    for _ in range(100):
        u = (lo + hi) / 2; v = lens_image(-u, [(0, 0.5, 1.0, 1.5)])
        if v < 0 or v > 2.0: lo = u
        else: hi = u
    return round((lo + hi) / 2, 6)
add(('2025', 'Apr', '2025-04-03', 2), 'refr', 'Light from a point source in air falls on a spherical glass surface (refractive index μ = 1.5 and radius of curvature = 50 cm, convex towards the source). The image is formed at a distance of 200 cm from the glass surface inside the glass. The magnitude of distance of the light source from the glass surface is ______ m.', None, 4,
    lambda: round(_src(), 4), ['\\f{μ}{v} − \\f{1}{u} = \\f{μ − 1}{R}: \\f{1.5}{2} − \\f{1}{u} = \\f{0.5}{0.5}.', '\\f{1}{u} = −0.25 → |u| = 4 m.'], 'refr', 2)
add(('2025', 'Apr', '2025-04-04', 1), 'wave', 'In a Young\'s double slit experiment, the slits are separated by 0.2 mm. If the slits separation is increased to 0.4 mm, the percentage change of the fringe width is :',
    ['0%', '100%', '25%', '50%'], 4, lambda: P4([1e-9, 100, 25, 50], abs(1 - (1 / 0.4) / (1 / 0.2)) * 100), ['β = \\f{λD}{d}: doubling d halves β.', 'Change = 50%.'], 'wave', 1)
def _m13():
    lo, hi = 0.01, 5.0   # find the mirror (convex) for which an object at 40 cm gives m = 1/2, then where m = 1/3
    for _ in range(100):
        R = (lo + hi) / 2; m = mirror_image(-0.4, R) / 0.4
        if m < 0.5: lo = R
        else: hi = R
    R = (lo + hi) / 2; lo2, hi2 = 0.4, 5.0
    for _ in range(100):
        u = (lo2 + hi2) / 2
        if mirror_image(-u, R) / u > 1 / 3: lo2 = u
        else: hi2 = u
    return round((lo2 + hi2) / 2 - 0.4, 4)
add(('2025', 'Apr', '2025-04-04', 1), 'mirror', 'When an object is placed 40 cm away from a spherical mirror an image of magnification \\f{1}{2} is produced. To obtain an image with magnification of \\f{1}{3}, the object is to be moved :',
    ['20 cm towards the mirror.', '40 cm away from the mirror.', '80 cm away from the mirror.', '20 cm away from the mirror.'], 2, lambda: pick([-0.2, 0.4, 0.8, 0.2], _m13()),
    ['A positive (erect) diminished image means a convex mirror: m = \\f{f}{f − u}.', '\\f{1}{2} = \\f{f}{f + 40} → f = 40 cm.', '\\f{1}{3} = \\f{40}{40 + |u|} → |u| = 80 cm: move 40 cm away.'], 'mirror', 2)
def _m3():
    def u_for(R):   # concave mirror of radius R: object distance giving m = −1/3 (real image)
        lo, hi = abs(R) / 2 * 1.0001, 100.0
        for _ in range(100):
            u = (lo + hi) / 2; m = mirror_image(-u, R) / u   # m = −v/u with v negative → v/u
            if -m < 1 / 3: hi = u
            else: lo = u
        return (lo + hi) / 2
    lo, hi = 0.01, 1.0
    for _ in range(80):
        R = -(lo + hi) / 2; u = u_for(R); gap = u - abs(mirror_image(-u, R))
        if gap < 0.30: lo = -R
        else: hi = -R
    return (lo + hi) / 2 / 2 * 100 * 4
add(('2025', 'Apr', '2025-04-04', 2), 'mirror', 'Distance between object and its image (magnified by −\\f{1}{3}) is 30 cm. The focal length of the mirror used is (\\f{x}{4}) cm, where magnitude of value of x is ______', None, 45,
    lambda: round(_m3()), ['m = −\\f{v}{u} = −\\f{1}{3}: real image at a third of the distance, both in front.', '|u| − |v| = 30 → |u| = 45, |v| = 15 cm.', '\\f{1}{f} = −\\f{1}{15} − \\f{1}{45} → f = −\\f{45}{4} cm, |x| = 45.'], 'mirror', 2)

# ---------- sheets 5–6
def _planecv():
    v = mirror_image(-0.30, 0.60)   # convex mirror f = 30 cm: virtual image behind it (z = v > 0); object at z = −0.30
    mid = (-0.30 + v) / 2   # a plane mirror images the object at the same distance behind itself → place it midway
    return round(0 - mid, 6)
add(('2025', 'Apr', '2025-04-04', 2), 'mirror', 'A finite size object is placed normal to the principal axis at a distance of 30 cm from a convex mirror of focal length 30 cm. A plane mirror is now placed in such a way that the image produced by both the mirrors coincide with each other. The distance between the two mirrors is :',
    ['7.5 cm', '22.5 cm', '45 cm', '15 cm'], 1, lambda: P4([0.075, 0.225, 0.45, 0.15], _planecv()),
    ['Convex mirror: \\f{1}{v} = \\f{1}{30} + \\f{1}{30} → v = 15 cm behind it, i.e. 45 cm from the object.', 'A plane mirror forms its image as far behind as the object is in front, so it must sit 22.5 cm from the object.', 'Distance between mirrors = 30 − 22.5 = 7.5 cm.'], 'mirror', 2)
add(('2024', 'Apr', '2024-04-04', 2), 'wave', 'In a Young\'s double slit experiment, two slits are located 1.5 mm apart. The distance of screen from slits is 2 m and the wavelength of the source is 400 nm. If the 20 maxima of the double slit pattern are contained within the central maximum of the single slit diffraction pattern, then the width of each slit is x × 10^{−3} cm, where x-value is ______.', None, 15,
    lambda: round(1.5e-3 * 2 / 20 / 1e-5, 6), ['Central diffraction maximum: width \\f{2λD}{a}; fringe width \\f{λD}{d}.', '\\f{2λD}{a} = 20\\f{λD}{d} → a = \\f{d}{10} = 0.15 mm = 15 × 10^{−3} cm.'], 'wave', 2)
add(('2024', 'Apr', '2024-04-04', 2), 'wave', 'The width of one of the two slits in a Young\'s double slit experiment is 4 times that of the other slit. The ratio of the maximum of the minimum intensity in the interference pattern is :',
    ['9 : 1', '16 : 1', '1 : 1', '4 : 1'], 1, lambda: P4([9, 16, 1, 4], yd(0, 1, 4, 1) / yd(0.5, 1, 4, 1)), ['Intensities 4 : 1 → amplitudes 2 : 1.', '\\f{(2 + 1)^{2}}{(2 − 1)^{2}} = 9.'], 'wave', 1)
def _slab():
    n, t = math.sqrt(2), 4 * math.sqrt(3); i = math.asin(1 / n); r = snell(1, n, i)
    return t / math.cos(r) * math.sin(i - r)   # path length in the slab × sin of the turn
add(('2024', 'Apr', '2024-04-04', 1), 'refr', 'A light ray is incident on a glass slab of thickness 4√{3} cm and refractive index √{2}. The angle of incidence is equal to the critical angle for the glass slab with air. The lateral displacement of ray after passing through glass slab is ______ cm. (Given sin 15° = 0.25)', None, 2,
    lambda: round(_slab() * 4 * 0.25 / (4 * math.sin(pi / 12)), 6), ['Critical angle: sin C = \\f{1}{√{2}} → i = 45°; inside sin r = \\f{sin 45°}{√{2}} = ½ → r = 30°.', 'd = \\f{t sin(i − r)}{cos r} = \\f{4√{3} × 0.25}{√{3}/2} = 2 cm.'], 'refr', 2)
def _ferr():
    u, v, du, dv = 0.3, 0.6, 1e-4, 2e-4; f = lambda u, v: u * v / (u + v)
    num = abs(f(u + du, v) - f(u, v)) + abs(f(u, v + dv) - f(u, v)); F = f(u, v)
    c = [du / u + dv / v, F * F * (du / u ** 2 + dv / v ** 2), 2 * F * (du / u + dv / v), F * (du / u + dv / v)]; return P4(c, num, 2e-3)
add(('2024', 'Apr', '2024-04-04', 1), 'lens', 'In an experiment to measure focal length (f) of convex lens, the least counts of the measuring scales for the position of object (u) and for the position of image (v) are Δu and Δv, respectively. The error in the measurement of the focal length of the convex lens will be :',
    ['\\f{Δu}{u} + \\f{Δv}{v}', 'f^{2}[\\f{Δu}{u^{2}} + \\f{Δv}{v^{2}}]', '2f[\\f{Δu}{u} + \\f{Δv}{v}]', 'f[\\f{Δu}{u} + \\f{Δv}{v}]'], 2, lambda: _ferr(),
    ['Differentiate \\f{1}{f} = \\f{1}{v} + \\f{1}{|u|} (magnitudes): \\f{Δf}{f^{2}} = \\f{Δu}{u^{2}} + \\f{Δv}{v^{2}}.', 'Δf = f^{2}(\\f{Δu}{u^{2}} + \\f{Δv}{v^{2}}).'], 'lens', 2)
add(('2024', 'Apr', '2024-04-05', 2), 'lens', 'An effective power of a combination of 5 identical convex lenses which are kept in contact along the principal axis is 25 D. Focal length of each of the convex lens is :',
    ['20 cm', '50 cm', '500 cm', '25 cm'], 1, lambda: P4([0.2, 0.5, 5, 0.25], 1 / (25 / 5)), ['Powers add: each lens has 5 D.', 'f = \\f{1}{5} m = 20 cm.'], 'lens', 1)
add(('2024', 'Apr', '2024-04-05', 2), 'wave', 'Two wavelengths λ_{1} and λ_{2} are used in Young\'s double slit experiment λ_{1} = 450 nm and λ_{2} = 650 nm. The minimum order of fringe produced by λ_{2} which overlaps with the fringe produced by λ_{1} is n. The value of n is ____.', None, 9,
    lambda: next(n for n in range(1, 100) if any(n * 650 == m * 450 for m in range(1, 200))), ['Bright fringes coincide when n × 650 = m × 450, i.e. 13n = 9m.', 'Smallest n = 9 (with m = 13).'], 'wave', 1)
def _disp():
    A = pi / 6; n = {'red': 1.513, 'yellow': 1.517, 'violet': 1.532}   # crown-glass-like: n falls with wavelength
    dev = {k: math.asin(v * math.sin(A)) - A for k, v in n.items()}   # normal incidence on the first face
    return 1 if dev['red'] < dev['yellow'] < dev['violet'] and len(set(n.values())) == 3 else 0
add(('2024', 'Apr', '2024-04-05', 1), 'refr', 'Statement I : When the white light passed through a prism, the red light bends lesser than yellow and violet. Statement II : The refractive indices are different for different wavelengths in dispersive medium.',
    ['Both Statement I and Statement II are true.', 'Statement I is true but Statement II is false.', 'Both Statement I and Statement II are false.', 'Statement I is false but Statement II is true.'], 1, lambda: _disp(),
    ['Glass has a larger refractive index for shorter wavelengths (dispersion): II is true.', 'So violet deviates most and red least: I is true.'], 'refr', 1)
add(('2024', 'Apr', '2024-04-06', 2), 'wave', 'Light emerges out of a convex lens when a source of light kept at its focus. The shape of wave front of the light is:',
    ['Both spherical and cylindrical', 'Cylindrical', 'Spherical', 'Plane'], 4, lambda: 4 if abs(math.atan((lambda r: r[2])(surf(0, -0.1, 1.5, 1.0, surf(0, 0.1, 1.0, 1.5, (-0.1, 0.0, 0.003)))))) < 1e-6 else 0,
    ['From the focus the rays leave the lens parallel to the axis.', 'Parallel rays mean a plane wavefront.'], 'wave', 1)
add(('2024', 'Apr', '2024-04-06', 2), 'wave', 'In Young\'s double slit experiment, carried out with light of wavelength 5000 Å, the distance between the slits is 0.3 mm and the screen is at 200 cm from the slits. The central maximum is at x = 0 cm. The value of x for third maxima is ______ mm.', None, 10,
    lambda: round(_thirdmax()), ['x_{n} = \\f{nλD}{d}.', 'x_{3} = \\f{3 × 5 × 10^{−7} × 2}{3 × 10^{−4}} = 10^{−2} m = 10 mm.'], 'wave', 1)
def _thirdmax():
    lam, d, D = 5e-7, 3e-4, 2.0; peaks = []; y, step = 0.0, 1e-7; prev = yd(0, lam)
    while len(peaks) < 4:
        y += step; cur = yd(d * y / D, lam); nxt = yd(d * (y + step) / D, lam)
        if cur >= prev and cur >= nxt: peaks.append(y)
        prev = cur
    return round(peaks[2] * 1000, 2)

# ---------- sheets 7–8
def _tm():
    lc = (1 / 20) / 50   # 50 VSD = 49 MSD and 1 MSD = 1/20 cm
    r = [ms + vc * lc for ms, vc in ((8.45, 26), (7.12, 41), (4.05, 1))]
    return (r[0] - r[2]) / (r[1] - r[2])   # real depth ÷ apparent depth
add(('2024', 'Apr', '2024-04-06', 2), 'refr', 'In finding out refractive index of glass slab the following observations were made through travelling microscope: 50 vernier scale divisions = 49 MSD; 20 divisions on main scale in each cm. For mark on paper: MSR = 8.45 cm, VC = 26. For mark on paper seen through slab: MSR = 7.12 cm, VC = 41. For powder particle on the top surface of the glass slab: MSR = 4.05 cm, VC = 1. Refractive index of the glass slab is:',
    ['1.42', '1.52', '1.24', '1.35'], 1, lambda: P4([1.42, 1.52, 1.24, 1.35], _tm(), 5e-3),
    ['Least count = \\f{1 MSD}{50} = \\f{0.05}{50} = 0.001 cm. Readings: 8.476, 7.161, 4.051 cm.', 'Real thickness = 8.476 − 4.051 = 4.425 cm; apparent = 7.161 − 4.051 = 3.110 cm.', 'n = \\f{4.425}{3.110} ≈ 1.42.'], 'refr', 2)
add(('2024', 'Apr', '2024-04-06', 2), 'lens', 'For the thin convex lens, the radii of curvature are at 15 cm and 30 cm respectively. The focal length of the lens is 20 cm. The refractive index of the material is :',
    ['1.2', '1.4', '1.5', '1.8'], 3, lambda: P4([1.2, 1.4, 1.5, 1.8], next(n for n in [1 + k / 1000 for k in range(1, 1000)] if abs(thin_f(0.15, -0.30, n) - 0.20) < 3e-5), 2e-3),
    ['\\f{1}{20} = (n − 1)(\\f{1}{15} + \\f{1}{30}) = \\f{n − 1}{10}.', 'n = 1.5.'], 'lens', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'wave', 'Which of the following phenomena does not explain by wave nature of light. (A) reflection (B) diffraction (C) photoelectric effect (D) interference (E) polarization',
    ['E only', 'C only', 'B, D only', 'A, C only'], 2,
    lambda: (lambda h, phi, f1, f2: 2 if (h * f1 < phi) and (h * f2 > phi) else 0)(6.63e-34, 2.3 * 1.6e-19, 4e14, 8e14),
    ['Reflection, diffraction, interference and polarisation all follow from waves.', 'The photoelectric effect has a threshold FREQUENCY however bright the light (bright red light: no electrons; dim violet: electrons) — it needs photons: C only.'], 'wave', 1)
def _A():
    n = math.sqrt(3)
    for k in range(1, 9000):
        A = k * 1e-4 * 1.2; dm = 2 * math.asin(min(1, n * math.sin(A / 2))) - A
        if dm >= A: return round(math.degrees(A))
add(('2024', 'Apr', '2024-04-06', 1), 'refr', 'The refractive index of prism is μ = √{3} and the ratio of the angle of minimum deviation to the angle of prism is one. The value of angle of prism is ______ degrees.', None, 60,
    lambda: _A(), ['With δ = A: μ = \\f{sin A}{sin(A/2)} = 2 cos\\f{A}{2}.', '2 cos\\f{A}{2} = √{3} → A = 60°.'], 'refr', 2)
add(('2025', 'Apr', '2025-04-07', 1), 'wave', 'Two plane polarized light waves combine at a certain point whose electric field components are E_{1} = E_{0} sin ωt and E_{2} = E_{0} sin(ωt + \\f{π}{3}). Find the amplitude of the resultant wave.',
    ['3.4E_{0}', '0.9E_{0}', 'E_{0}', '1.7E_{0}'], 4, lambda: P4([3.4, 0.9, 1, 1.7], max(abs(math.sin(t) + math.sin(t + pi / 3)) for t in [2 * pi * k / 100000 for k in range(100000)]), 0.02),
    ['Add phasors: A = √{E_{0}^{2} + E_{0}^{2} + 2E_{0}^{2} cos 60°} = √{3}E_{0}.', '≈ 1.7E_{0}.'], 'wave', 1)
add(('2025', 'Apr', '2025-04-07', 1), 'lens', 'A lens having refractive index 1.6 has focal length of 12 cm, when it is in air. Find the focal length of the lens when it is placed in water. (Take refractive index of water as 1.28)',
    ['288 mm', '655 mm', '355 mm', '555 mm'], 1, lambda: P4([288, 655, 355, 555], thin_f(0.144, -0.144, 1.6, 1.28) * 1000, 2e-3),
    ['\\f{1}{f} = (\\f{n}{n_{m}} − 1)(\\f{1}{R_{1}} − \\f{1}{R_{2}}): the bracket of radii stays the same.', '\\f{f_{w}}{f_{a}} = \\f{0.6}{1.6/1.28 − 1} = \\f{0.6}{0.25} = 2.4 → f_{w} = 28.8 cm = 288 mm.'], 'lens', 2)
def _pair():
    S = [(0, 0.3, 1, 1.5), (0, -0.3, 1.5, 1), (0.1, 0.1, 1, 1.5), (0.1, -0.1, 1.5, 1)]   # f = 30 cm then f = 10 cm, 10 cm apart
    ray = (-1.0, 1e-6, 0.0)
    for s in S: ray = surf(*s, ray)
    # equivalent focal length = (incoming height) / (outgoing angle)
    return 1 / (1e-6 / -ray[2])
add(('2025', 'Apr', '2025-04-07', 1), 'lens', 'Two thin convex lenses of focal lengths 30 cm and 10 cm are placed coaxially, 10 cm apart. The power of this combination is:',
    ['20 D', '10 D', '5 D', '1 D'], 2, lambda: P4([20, 10, 5, 1], _pair(), 2e-3),
    ['P = P_{1} + P_{2} − dP_{1}P_{2} (d in m).', '= \\f{10}{3} + 10 − 0.1 × \\f{10}{3} × 10 = 10 D.'], 'lens', 2)
def _apparent(H):   # trace a near-normal ray up from the bottom through both liquids
    th = 1e-4; x = 0.6 * math.tan(th); th2 = snell(1.2, 1.6, th); x += H * math.tan(th2); th3 = snell(1.6, 1.0, th2)
    return (0.6 + H) - x / math.tan(th3)
add(('2025', 'Apr', '2025-04-07', 1), 'refr', 'A container contains a liquid with refractive index of 1.2 up to a height of 60 cm and another liquid having refractive index 1.6 is added to height H above first liquid. If viewed from above, the apparent shift in the position of bottom of container is 40 cm. The value of H is ____ cm. (Consider liquids are immiscible)', None, 80,
    lambda: round(next(h for h in range(1, 500) if abs(_apparent(h / 100) - 0.40) < 1e-5)), ['Shift = Σ t(1 − \\f{1}{n}).', '60(1 − \\f{1}{1.2}) + H(1 − \\f{1}{1.6}) = 10 + 0.375H = 40 → H = 80 cm.'], 'refr', 2)
def _block():
    lo, hi = 0.0, pi / 2
    for _ in range(100):
        th = (lo + hi) / 2; r = snell(1.0, 1.25, th); top = pi / 2 - r   # angle of incidence on the top surface
        if snell(1.25, 1.0, top) is None: lo = th   # still totally reflected
        else: hi = th
    return math.sin(lo)
add(('2025', 'Apr', '2025-04-07', 2), 'refr', 'A transparent block A having refractive index μ = 1.25 is surrounded by another medium of refractive index μ = 1.0. A light ray is incident on the flat (vertical) face of the block with incident angle θ and then meets the top (horizontal) surface. What is the maximum value of θ for which light suffers total internal reflection at the top surface of the block?',
    ['tan^{−1}(4/3)', 'cos^{−1}(3/4)', 'sin^{−1}(3/4)', 'tan^{−1}(3/4)'], 3, lambda: P4([math.sin(math.atan(4 / 3)), math.sin(math.acos(0.75)), 0.75, math.sin(math.atan(0.75))], _block(), 1e-6),
    ['At the top the angle of incidence is 90° − r, and TIR needs sin(90° − r) ≥ \\f{1}{1.25} → cos r ≥ 0.8 → sin r ≤ 0.6.', 'sin θ = 1.25 sin r ≤ 0.75 → θ_{max} = sin^{−1}\\f{3}{4}.'], 'refr', 2)
add(('2025', 'Apr', '2025-04-07', 2), 'refr', 'Assertion (A) : Refractive index of glass is higher than that of air. Reason (R): Optical density of a medium is directly proportional to its mass density which results in a proportionate refractive index.',
    ['(A) is correct but (R) is not correct', 'Both (A) and (R) are correct but (R) is not the correct explanation of (A)', '(A) is not correct but (R) is correct', 'Both (A) and (R) are correct and (R) is the correct explanation of (A)'], 1,
    lambda: 1 if (1.5 > 1.0003) and not ((800 < 1000) == (1.39 < 1.33)) else 0,
    ['Glass (n ≈ 1.5) is optically denser than air: A is correct.', 'Optical density is not set by mass density — kerosene is lighter than water (800 vs 1000 kg/m^{3}) yet has a larger n (1.39 vs 1.33): R is wrong.'], 'refr', 1)
def _m4():
    lo, hi = 0.01, 2.0   # convex mirror radius: object at u, image erect with m = 1/4, |u| + |v| = 40 cm
    for _ in range(80):
        R = (lo + hi) / 2; a, b = 1e-4, 50.0
        for _ in range(100):
            u = (a + b) / 2
            if mirror_image(-u, R) / u > 0.25: a = u
            else: b = u
        u = (a + b) / 2; gap = u + mirror_image(-u, R)
        if gap > 0.40: hi = R
        else: lo = R
    return (lo + hi) / 2 / 2 * 100
add(('2025', 'Apr', '2025-04-07', 2), 'mirror', 'A mirror is used to produce an image with magnification of \\f{1}{4}. If the distance between object and its image is 40 cm, then the focal length of the mirror is',
    ['10 cm', '15 cm', '12.7 cm', '10.7 cm'], 4, lambda: P4([10, 15, 12.7, 10.7], _m4(), 5e-3),
    ['Erect and diminished: a convex mirror, image behind it with |v| = \\f{|u|}{4}.', '|u| + |v| = 40 → |u| = 32 cm, |v| = 8 cm.', '\\f{1}{f} = \\f{1}{8} − \\f{1}{32} = \\f{3}{32} → f ≈ 10.7 cm.'], 'mirror', 2)

# ---------- sheets 9–10
def thin(f): return biconvex(f, f, 1.5) if f > 0 else [(0, f, 1, 1.5), (0, -f, 1.5, 1)]   # equi-convex / equi-concave glass lens of focal length f
def at(z, S): return [(z + s[0], s[1], s[2], s[3]) for s in S]
def trace(u, S, h=1e-6):
    ray = (u, 0.0, h)
    for s in S: ray = surf(*s, ray)
    return axis_cross(ray)
add(('2025', 'Apr', '2025-04-08', 2), 'lens', 'A convex lens of focal length 30 cm is placed in contact with a concave lens of focal length 20 cm. An object is placed at 20 cm to the left of this lens system. The distance of the image from the lens in cm is ______.',
    ['30', '45', '15', '\\f{60}{7}'], 3, lambda: P4([30, 45, 15, 60 / 7], abs(trace(-0.20, thin(0.30) + thin(-0.20))) * 100, 2e-3),
    ['\\f{1}{F} = \\f{1}{30} − \\f{1}{20} = −\\f{1}{60}: a diverging pair.', '\\f{1}{v} = −\\f{1}{60} − \\f{1}{20} = −\\f{1}{15} → image 15 cm from the lens (virtual, on the object side).'], 'lens', 1)
add(('2025', 'Apr', '2025-04-08', 2), 'lens', 'A concave-convex lens of refractive index 1.5 and the radii of curvature of its surfaces are 30 cm and 20 cm, respectively. The concave surface is upwards and is filled with a liquid of refractive index 1.3. The focal length of the liquid-glass combination will be',
    ['\\f{700}{11} cm', '\\f{600}{11} cm', '\\f{800}{11} cm', '\\f{500}{11} cm'], 2,
    lambda: P4([700 / 11, 600 / 11, 800 / 11, 500 / 11], focal([(0, None, 1, 1.3), (0, -0.30, 1.3, 1.5), (0, -0.20, 1.5, 1.0)]) * 100, 2e-3),
    ['Glass meniscus: P_{g} = 0.5(\\f{1}{20} − \\f{1}{30}) = \\f{1}{120} per cm.', 'Liquid plano-convex lens filling the 30 cm hollow: P_{l} = \\f{0.3}{30} = \\f{1}{100} per cm.', 'Total \\f{11}{600} → f = \\f{600}{11} cm.'], 'lens', 3)
add(('2025', 'Apr', '2025-04-08', 2), 'wave', 'In a Young\'s double slit experiment, the source is white light. One of the slits is covered by red filter and another by a green filter. In this case',
    ['there shall be an interference pattern, where each fringe\'s pattern center is green and outer edges is red.', 'there shall be an interference pattern for red distinct from that for green.', 'there shall be no interference fringes.', 'there shall be alternate interference fringes of red and green.'], 3,
    lambda: 3 if abs(sum(math.cos(2 * pi * (4.6e14 - 5.7e14) * t) for t in [k * 1e-16 for k in range(100000)]) / 100000) < 0.05 else 0,
    ['Red and green light have different frequencies, so their phase difference keeps running: the cross term averages to zero.', 'No sustained fringes form; the screen is evenly lit (yellowish).'], 'wave', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'lens', 'An object is 30 cm to the left of a convex lens f_{1} = 10 cm. A concave lens f_{2} = −10 cm is 5 cm to the right of it, and a convex lens f_{3} = 30 cm is a further 10 cm to the right. The position of the image formed by the combination of lenses is :',
    ['30 cm (right of third lens)', '15 cm (left of second lens)', '30 cm (left of third lens)', '15 cm (right of second lens)'], 1,
    lambda: pick([0.30, -0.15, -0.30, 0.15], round(trace(-0.30, thin(0.10) + at(0.05, thin(-0.10)) + at(0.15, thin(0.30)), 1e-7) - 0.15, 3)),
    ['L_{1}: \\f{1}{v} = \\f{1}{10} − \\f{1}{30} → v = 15 cm, i.e. 10 cm beyond L_{2}.', 'L_{2}: u = +10, f = −10 → \\f{1}{v} = 0: the rays leave parallel.', 'L_{3} focuses parallel rays at its focus: 30 cm right of the third lens.'], 'lens', 2)
add(('2024', 'Apr', '2024-04-08', 2), 'wave', 'Two slits are 1 mm apart and the screen is located 1 m away from the slits. A light wavelength 500 nm is used. The width of each slit to obtain 10 maxima of the double slit pattern within the central maximum of the single slit pattern is ______ × 10^{−4} m.', None, 2,
    lambda: round(2 * 1e-3 / 10 / 1e-4, 6), ['\\f{2λD}{a} = 10\\f{λD}{d}.', 'a = \\f{d}{5} = 0.2 mm = 2 × 10^{−4} m.'], 'wave', 1)
add(('2024', 'Apr', '2024-04-08', 1), 'refr', 'Critical angle of incidence for a pair of optical media is 45°. The refractive indices of first and second media are in the ratio:',
    ['√{2} : 1', '1 : 2', '1 : √{2}', '2 : 1'], 1, lambda: P4([math.sqrt(2), 0.5, 1 / math.sqrt(2), 2], next(r for r in [1 + k / 10000 for k in range(1, 20000)] if snell(r, 1, pi / 4 + 1e-9) is None)),
    ['TIR happens going from the denser medium: sin C = \\f{n_{2}}{n_{1}}.', '\\f{n_{1}}{n_{2}} = \\f{1}{sin 45°} = √{2}.'], 'refr', 1)
add(('2024', 'Apr', '2024-04-09', 2), 'lens', 'Two biconvex lenses L_{1} and L_{2} having focal length 10 cm and 15 cm respectively are arranged so that a ray parallel to the axis through L_{1} leaves L_{2} parallel to the axis again (on the other side of the axis). The distance between L_{1} and L_{2} is :',
    ['10 cm', '15 cm', '25 cm', '35 cm'], 3,
    lambda: P4([10, 15, 25, 35], next(d for d in range(1, 60) if abs((lambda r: r[2])(_ray_thru(d / 100))) < 1e-9), 1e-6),
    ['The ray crosses the axis at L_{1}\'s focus (10 cm).', 'To come out parallel it must start from L_{2}\'s focus, 15 cm before L_{2}: d = 10 + 15 = 25 cm.'], 'lens', 1)
def _ray_thru(d, h=1e-6):
    ray = (-1.0, h, 0.0)
    for s in thin(0.10) + at(d, thin(0.15)): ray = surf(*s, ray)
    return (ray[0], ray[1], round(ray[2] / h, 4) * h)
add(('2024', 'Apr', '2024-04-09', 2), 'wave', 'Monochromatic light of wavelength 500 nm is used in Young\'s double slit experiment. An interference pattern is obtained on a screen. When one of the slits is covered with a very thin glass plate (refractive index = 1.5), the central maximum is shifted to a position previously occupied by the 4^{th} bright fringe. The thickness of the glass-plate is ______ μm.', None, 4,
    lambda: round(4 * 500e-9 / (1.5 - 1) / 1e-6, 6), ['The plate adds optical path (μ − 1)t; the centre moves by that many wavelengths.', '(1.5 − 1)t = 4 × 500 nm → t = 4 μm.'], 'wave', 1)
add(('2024', 'Apr', '2024-04-09', 1), 'lens', 'Statement (I): When an object is placed at the centre of curvature of a concave lens, image is formed at the centre of curvature of the lens on the other side. Statement (II): Concave lens always forms a virtual and erect image.',
    ['Statement I is false but Statement II is true.', 'Both Statement I and Statement II are false.', 'Statement I is true but Statement II is false.', 'Both Statement I and Statement II are true.'], 1,
    lambda: 1 if all(trace(-u, thin(-0.10)) < 0 and -trace(-u, thin(-0.10)) < u for u in (0.05, 0.10, 0.20, 0.50, 2.0)) else 0,
    ['A concave lens alone always gives a virtual, erect, diminished image on the object\'s side, between the lens and its focus: II is true.', 'So an object at 2f does NOT image at 2f on the other side: I is false.'], 'lens', 1)
def _quarter():
    lam, d, D = 600e-9, 1e-3, 1.0; lo, hi = 0.0, lam * D / (2 * d)
    for _ in range(100):
        y = (lo + hi) / 2
        if yd(d * y / D, lam) > 1.0: lo = y
        else: hi = y
    return round(lo / 1e-6, 4)
add(('2024', 'Apr', '2024-04-09', 1), 'wave', 'In a Young\'s double slit experiment, the intensity at a point is (\\f{1}{4})^{th} of the maximum intensity, the minimum distance of the point from the central maximum is ______ μm. (Given : λ = 600 nm, d = 1.0 mm, D = 1.0 m)', None, 200,
    lambda: round(_quarter()), ['cos^{2}\\f{φ}{2} = \\f{1}{4} → φ = \\f{2π}{3}, path difference \\f{λ}{3}.', 'y = \\f{λD}{3d} = \\f{600 × 10^{−9}}{3 × 10^{−3}} = 200 μm.'], 'wave', 2)

# ---------- sheets 11–12
def _thinprism():
    A, n = math.radians(4), 1.5; best = (1e9, 0)
    for k in range(1, 20000):
        i = k * 1e-5; r1 = snell(1, n, i); e = snell(n, 1, A - r1)
        if e is not None: best = min(best, (i + e - A, i))
    return best[1] / best[0]
add(('2026', 'Apr', '2026-04-02', 1), 'refr', 'For a thin symmetric prism made of glass (refractive index 1.5), the ratio of incident angle and minimum deviation will be ______.',
    ['3 : 4', '3 : 2', '2 : 1', '1 : 2'], 2, lambda: P4([0.75, 1.5, 2, 0.5], _thinprism(), 2e-3),
    ['Thin prism: δ_{min} = (n − 1)A = \\f{A}{2}.', 'At minimum deviation r = \\f{A}{2} and i ≈ nr = \\f{3A}{4}.', 'i : δ = \\f{3}{4} : \\f{1}{2} = 3 : 2.'], 'refr', 2)
def _surfimg():
    S = [(0, -0.20, 1.0, 1.54)]; v = lens_image(-0.40, S)
    return 2 * (1.0 * v) / (1.54 * -0.40)   # lateral magnification for a refracting surface: n1 v / (n2 u)
add(('2026', 'Apr', '2026-04-02', 1), 'refr', 'An object O of height 2 cm stands 40 cm in front of a spherical refracting surface P (air μ_{1} = 1 on the object side, lens material μ_{2} = 1.54 beyond). The centre of curvature C is on the object side, 20 cm from P (the surface is concave towards the object). The height of image will be nearly ______ cm.',
    ['1', '0.5', '1.2', '0.25'], 1, lambda: P4([1, 0.5, 1.2, 0.25], _surfimg(), 0.05),
    ['\\f{1.54}{v} − \\f{1}{−40} = \\f{0.54}{−20} → \\f{1.54}{v} = −0.052 → v ≈ −29.6 cm (virtual).', 'm = \\f{μ_{1}v}{μ_{2}u} = \\f{−29.6}{1.54 × (−40)} ≈ 0.48 → height ≈ 0.96 cm ≈ 1 cm.'], 'refr', 2)
add(('2026', 'Apr', '2026-04-02', 1), 'wave', 'In single slit diffraction pattern, the wavelength of light used is 628 nm and slit width is 0.2 mm, the angular width of central maximum is α × 10^{−2} degrees. The value of α is ______ . (π = 3.14)', None, 36,
    lambda: round(2 * first_zero(2e-4, 628e-9) * 180 / 3.14 / 1e-2), ['Angular width = \\f{2λ}{a} = \\f{2 × 628 × 10^{−9}}{2 × 10^{−4}} = 6.28 × 10^{−3} rad.', 'In degrees: 6.28 × 10^{−3} × \\f{180}{3.14} = 0.36° = 36 × 10^{−2}°.'], 'wave', 1)
add(('2026', 'Jan', '2026-01-21', 1), 'wave', 'In a double slit experiment the distance between the slits is 0.1 cm and the screen is placed at 50 cm from the slits plane. When one slit is covered with a transparent sheet having thickness t and refractive index n (= 1.5), the central fringe shifts by 0.2 cm. The value of t is ______ cm.',
    ['8 × 10^{−4}', '6.0 × 10^{−3}', '5.6 × 10^{−4}', '5.0 × 10^{−3}'], 1, lambda: P4([8e-4, 6e-3, 5.6e-4, 5e-3], 0.2 * 0.1 / 50 / 0.5),
    ['Shift = \\f{(n − 1)tD}{d}.', 't = \\f{0.2 × 0.1}{50 × 0.5} = 8 × 10^{−4} cm.'], 'wave', 1)
def _expander():
    f1, h = 0.040, 1e-6
    def out(f2):
        ray = (-1.0, h, 0.0)
        for s in thin(f1) + at(f1 + f2, thin(f2)): ray = surf(*s, ray)   # lenses sharing a focus
        return ray
    for f2 in [k * 1e-3 for k in range(41, 1000)]:
        r = out(f2)
        if abs(r[2]) < 1e-3 * h and abs(abs(r[1]) / h - 7) < 1e-3: return round(f2 * 1000)
add(('2026', 'Jan', '2026-01-21', 1), 'lens', 'A collimated beam of light of diameter 2 mm is propagating along x-axis. The beam is required to be expanded in a collimated beam of diameter 14 mm using a system of two convex lenses. If first lens has focal length 40 mm, then the focal length of second lens is ______ mm.', None, 280,
    lambda: _expander(), ['Lenses sharing a focus (separation f_{1} + f_{2}) keep the beam parallel.', 'Width scales by \\f{f_{2}}{f_{1}} = 7 → f_{2} = 280 mm.'], 'lens', 2)
add(('2026', 'Jan', '2026-01-21', 1), 'lens', 'In a microscope the objective is having focal length f_{o} = 2 cm and eye-piece is having focal length f_{e} = 4 cm. The tube length is 32 cm. The magnification produced by this microscope for normal adjustment is ______ .', None, 100,
    lambda: round(_micro()),
    ['Normal adjustment (final image at infinity): m = \\f{L}{f_{o}} × \\f{D}{f_{e}}.', '= \\f{32}{2} × \\f{25}{4} = 100.'], 'lens', 1)
def _micro():   # objective forms its image at its focus + tube length (34 cm); eyepiece then gives D/f_e
    lo, hi = 0.0201, 0.2
    for _ in range(100):
        u = (lo + hi) / 2
        if trace(-u, thin(0.02)) > 0.34: lo = u
        else: hi = u
    u = (lo + hi) / 2; return trace(-u, thin(0.02)) / u * (0.25 / 0.04)
def _two():
    S = [(0, 0.15, 1.0, 1.5), (0, None, 1.5, 1.2), (0, -0.12, 1.2, 1.0)]; v = trace(-0.30, S); return round(v / -0.30, 4)
add(('2026', 'Jan', '2026-01-28', 2), 'lens', 'A biconvex lens is formed by using two thin planoconvex lenses: the left one has μ = 1.5 and curved-surface radius 15 cm, the right one has μ = 1.2 and radius 12 cm. When an object is placed on the left side of lens at a distance of 30 cm from the biconvex lens, the magnification of the image will be :',
    ['+2', '−2', '−2.5', '+2.5'], 2, lambda: pick([2, -2, -2.5, 2.5], _two(), 1e-3),
    ['P = \\f{0.5}{15} + \\f{0.2}{12} = \\f{1}{30} + \\f{1}{60} = \\f{1}{20} per cm → f = 20 cm.', '\\f{1}{v} = \\f{1}{20} − \\f{1}{30} → v = 60 cm, m = \\f{v}{u} = −2.'], 'lens', 2)
add(('2026', 'Jan', '2026-01-28', 2), 'wave', 'A beam of light consisting of wavelengths 650 nm and 550 nm illuminates the Young\'s double slits with separation of 2 mm such that the interference fringes are formed on a screen, placed at a distance of 1.2 m from the slits. The least distance of a point from the central maximum, where the bright fringes due to both the wavelengths coincide, is ______ × 10^{−5} m.', None, 429,
    lambda: round(next(y for y in [k * 1e-7 for k in range(1000, 100000)] if yd(2e-3 * y / 1.2, 650e-9) > 3.999 and yd(2e-3 * y / 1.2, 550e-9) > 3.999) / 1e-5),
    ['Coincidence: n × 650 = m × 550 → 13n = 11m, smallest n = 11.', 'y = \\f{11 × 650 × 10^{−9} × 1.2}{2 × 10^{−3}} = 4.29 × 10^{−3} m = 429 × 10^{−5} m.'], 'wave', 2)
def _paint():
    n = 1.6; inc = pi / 3   # normal entry, so the ray meets the base at 60°
    lo, hi = 1.0, 1.6
    for _ in range(100):
        n2 = (lo + hi) / 2
        if snell(n, n2, inc) is None: lo = n2
        else: hi = n2
    return lo
add(('2026', 'Apr', '2026-04-02', 2), 'refr', 'One side (the base) of an equilateral prism is painted by a transparent material of refractive index n_{2}. The refractive index of prism is 1.6. A ray enters normally through one face and strikes the painted face. The limiting value of n_{2} for total internal reflection from the painted face is ______.',
    ['3√{3}/1.6', '√{3}', '3.2/√{3}', '4√{3}/5'], 4, lambda: P4([3 * math.sqrt(3) / 1.6, math.sqrt(3), 3.2 / math.sqrt(3), 4 * math.sqrt(3) / 5], _paint(), 1e-6),
    ['Entering normally, the ray meets the base at 60°.', 'TIR needs 1.6 sin 60° ≥ n_{2} → limit n_{2} = 0.8√{3} = \\f{4√{3}}{5}.'], 'refr', 2)

# ---------- sheets 13–14
def _path_at(frac):
    lo, hi = 0.0, 0.5
    for _ in range(100):
        p = (lo + hi) / 2
        if yd(p, 1.0) / 4 > frac: lo = p
        else: hi = p
    return lo
add(('2026', 'Apr', '2026-04-02', 2), 'wave', 'In a Young\'s double slit experiment, the intensity at some point on the screen is found to be \\f{3}{4} times of the maximum of the interference pattern. The path difference between the interfering waves at this point is \\f{λ}{x} where λ is wavelength of the incident light. The value of x is ______.', None, 6,
    lambda: round(1 / _path_at(0.75), 6), ['cos^{2}\\f{φ}{2} = \\f{3}{4} → φ = \\f{π}{3}.', 'Path difference = \\f{φ}{2π}λ = \\f{λ}{6} → x = 6.'], 'wave', 1)
add(('2026', 'Apr', '2026-04-02', 2), 'lens', 'If sunlight is focused on a paper using an equi-convex lens, it starts burning the paper in shortest time when the lens is kept at 30 cm above the paper. If the radius of curvature of the lens is 60 cm then the refractive index of the lens material is \\f{α}{10}. The value of α is ______.', None, 20,
    lambda: round(next(n for n in [1 + k / 1000 for k in range(1, 2000)] if abs(focal(biconvex(0.6, 0.6, n)) - 0.30) < 1e-4) * 10, 6), ['Sunlight focuses at the focal point: f = 30 cm.', '\\f{1}{30} = (n − 1)\\f{2}{60} → n = 2 → α = 20.'], 'lens', 1)
add(('2026', 'Jan', '2026-01-21', 2), 'wave', 'Statement I: In a Young\'s double slit experiment, the angular separation of fringes will increase as the screen is moved away from the plane of the slits. Statement II: In a Young\'s double slit experiment, the angular separation of fringes will increase when monochromatic source is replaced by another monochromatic source of higher wavelength.',
    ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is false but Statement II is true', 'Statement I is true but Statement II is false'], 3,
    lambda: (lambda ang: 3 if abs(ang(500e-9, 1.0) - ang(500e-9, 2.0)) < 1e-9 and ang(600e-9, 1.0) > ang(500e-9, 1.0) else 0)(lambda lam, D: math.atan(lam * D / 1e-3 / D)),
    ['Angular fringe width = \\f{λ}{d}: it does not depend on D (I is false).', 'A longer wavelength widens it (II is true).'], 'wave', 1)
def _graze():
    n = math.sqrt(2); r1 = snell(1, n, pi / 4); C = math.asin(1 / n)
    A = r1 + C; return round(180 - 45 - math.degrees(A), 6)
add(('2026', 'Jan', '2026-01-21', 2), 'refr', 'A prism has a base angle of 45° on the left and angle θ on the right. When the incident ray is parallel to the base of the prism, the emergent ray grazes along the second surface. If refractive index of the material of prism is √{2}, the angle θ of prism is :',
    ['60°', '75°', '90°', '45°'], 1, lambda: P4([60, 75, 90, 45], _graze()),
    ['A ray parallel to the base meets the 45°-inclined face at i = 45°: sin r_{1} = \\f{sin 45°}{√{2}} → r_{1} = 30°.', 'Grazing exit means r_{2} = critical angle = 45°, so the apex angle A = 30° + 45° = 75°.', 'θ = 180° − 45° − 75° = 60°.'], 'refr', 2)
add(('2026', 'Jan', '2026-01-21', 2), 'wave', 'In a Young\'s double slit experiment set up, the two slits are kept 0.4 mm apart and screen is placed at 1 m from slits. If a thin transparent sheet of thickness 20 μm is introduced in front of one of the slits then center bright fringe shifts by 20 mm on the screen. The refractive index of transparent sheet is given by \\f{α}{10}, where α is ______', None, 14,
    lambda: round((1 + 0.02 * 0.4e-3 / (20e-6 * 1.0)) * 10, 6), ['Shift = \\f{(μ − 1)tD}{d}.', 'μ − 1 = \\f{0.02 × 0.4 × 10^{−3}}{20 × 10^{−6} × 1} = 0.4 → μ = 1.4, α = 14.'], 'wave', 1)
add(('2025', 'Jan', '2025-01-22', 1), 'wave', 'Assertion (A) : If Young\'s double slit experiment is performed in an optically denser medium than air, then the consecutive fringes come closer. Reason (R) : The speed of light reduces in an optically denser medium than air while its frequency does not change.',
    ['Both (A) and (R) are true but (R) is not the correct explanation of (A)', 'Both (A) and (R) are true and (R) is the correct explanation of (A)', '(A) is false but (R) is true', '(A) is true but (R) is false'], 2,
    lambda: (lambda f, n: 2 if (3e8 / n) / f < 3e8 / f else 0)(5e14, 1.33),
    ['Same frequency, slower speed → shorter wavelength λ/n.', 'β = \\f{λD}{nd} shrinks: A is true and R explains it.'], 'wave', 1)
def _silv():
    mu, R = 1.5, 0.3
    # lens surface (refract in) → silvered back (concave mirror seen from inside) → lens surface (refract out); find u that images onto itself
    def back(u):
        z, y, m = -u, 0.0, 1e-6
        r = surf(0, R, 1.0, mu, (z, y, m))   # enter through the front surface (convex)
        # reflect at the back surface, centre on the front side (R_back = −R, vertex at 0 for a thin lens)
        z0, y0, m0 = r; c = -R; a = 1 + m0 * m0; b = 2 * ((z0 - c) + m0 * y0); cc = (z0 - c) ** 2 + y0 * y0 - R * R; d = math.sqrt(b * b - 4 * a * cc)
        t = min([(-b - d) / (2 * a), (-b + d) / (2 * a)], key=lambda t: abs(z0 + t)); zs, ys = z0 + t, y0 + m0 * t
        nx, ny = (zs - c) / R, ys / R; L = math.sqrt(1 + m0 * m0); dx, dy = 1 / L, m0 / L; dot = dx * nx + dy * ny; rx, ry = dx - 2 * dot * nx, dy - 2 * dot * ny
        # back out through the front surface going left: mirror the geometry (flip z) and refract μ → 1
        r2 = surf(0, -R, mu, 1.0, (-zs, ys, -ry / rx))   # in flipped coordinates the front surface's centre is at −R
        return -axis_cross(r2)
    lo, hi = 0.01, 5.0
    for _ in range(100):
        u = (lo + hi) / 2
        if back(u) < -u: lo = u   # image further left than the object
        else: hi = u
    return (lo + hi) / 2 / R
add(('2025', 'Jan', '2025-01-22', 1), 'mirror', 'Given is a thin convex lens of glass (refractive index μ) and each side having radius of curvature R. One side is polished for complete reflection. At what distance from the lens, an object be placed on the optic axis so that the image gets formed on the object itself?',
    ['μR', 'R/μ', 'R/(2μ − 1)', 'R/(2μ − 3)'], 3, lambda: P4([1.5, 1 / 1.5, 0.5, 1e9], _silv(), 2e-3),
    ['A silvered lens acts as a mirror of power P = 2P_{lens} + P_{mirror} = \\f{4(μ − 1)}{R} + \\f{2}{R} = \\f{2(2μ − 1)}{R}.', 'Its focal length is \\f{R}{2(2μ − 1)}; an object at its centre of curvature (2f) images onto itself: \\f{R}{2μ − 1}.'], 'mirror', 3)
def _sideacc():
    f, v0 = 1.0, 25.0
    img = lambda u: u * f / (u + f)   # convex mirror, object distance u (magnitude) → virtual image distance
    u = lambda t: 24.0 - v0 * t; h = 1e-3
    return abs(img(u(h)) - 2 * img(u(0)) + img(u(-h))) / h ** 2
add(('2025', 'Jan', '2025-01-22', 1), 'mirror', 'The driver sitting inside a parked car is watching vehicles approaching from behind with the help of his side view mirror, which is a convex mirror with radius of curvature R = 2 m. Another car approaches him from behind with a uniform speed of 90 km/hr. When the car is at a distance of 24 m from him, the magnitude of the acceleration of the image of the car in the side view mirror is \'a\'. The value of 100a is ______ m/s^{2}.', None, 8,
    lambda: round(100 * _sideacc(), 3), ['f = 1 m; image distance v = \\f{uf}{u + f} (magnitudes) → \\f{dv}{dt} = \\f{f^{2}}{(u + f)^{2}}\\f{du}{dt}.', 'a = \\f{2f^{2}}{(u + f)^{3}}(\\f{du}{dt})^{2} = \\f{2 × 625}{25^{3}} = 0.08 m/s^{2} → 100a = 8.'], 'mirror', 3)
add(('2025', 'Jan', '2025-01-22', 2), 'lens', 'A symmetric thin biconvex lens is cut into four equal parts by two planes: AB along the principal axis and CD along the plane of the lens (through its middle). If the power of original lens is 4 D then the power of a part of the divided lens is',
    ['D', '4D', '8D', '2D'], 4, lambda: P4([1, 4, 8, 2], 1 / focal([(0, 0.25, 1, 1.5), (0, None, 1.5, 1)]), 2e-3),
    ['Cutting along the axis (AB) does not change focal length.', 'Cutting along CD leaves plano-convex halves: each has half the power, 2 D.'], 'lens', 1)
def _film():
    lam, nf, ng = 550e-9, 2.0, 1.45
    def R(t):   # thin-film reflection amplitude with both reflections and their phases
        r1 = (1 - nf) / (1 + nf); r2 = (nf - ng) / (nf + ng); d = cmath.exp(2j * 2 * pi * nf * t / lam); return abs((r1 + r2 * d) / (1 + r1 * r2 * d)) ** 2
    ts = [k * 1e-10 for k in range(1, 5000)]; return min(ts, key=R) / 1e-9
add(('2025', 'Jan', '2025-01-22', 2), 'wave', 'A transparent film of refractive index, 2.0 is coated on a glass slab of refractive index, 1.45. What is the minimum thickness of transparent film to be coated for the maximum transmission of Green light of wavelength 550 nm. [Assume that the light is incident nearly perpendicular to the glass surface.]',
    ['68.7 nm', '137.5 nm', '94.8 nm', '275 nm'], 2, lambda: P4([68.7, 137.5, 94.8, 275], _film(), 3e-3),
    ['Maximum transmission = minimum reflection.', 'Only the top reflection (air → film) gets a π flip, so the reflections cancel when 2nt = λ.', 't = \\f{λ}{2n} = \\f{550}{4} = 137.5 nm.'], 'wave', 2)
add(('2025', 'Jan', '2025-01-22', 2), 'wave', 'Assertion (A): In Young\'s double slit experiment, the fringes produced by red light are closer as compared to those produced by blue light. Reason (R): The fringe width is directly proportional to the wavelength of light.',
    ['Both (A) and (R) are true and (R) is the correct explanation of (A)', 'Both (A) and (R) are true but (R) is NOT the correct explanation of (A)', '(A) is true but (R) is false', '(A) is false but (R) is true'], 4,
    lambda: 4 if 700e-9 * 1 / 1e-3 > 450e-9 * 1 / 1e-3 else 0, ['β = \\f{λD}{d} ∝ λ: R is true.', 'Red has the longer wavelength, so its fringes are WIDER apart: A is false.'], 'wave', 1)

# ---------- sheets 15–16
def silvered(u, front, back, n_out, n_glass):
    """thin lens in a medium n_out: front surface radius `front` (centre at +front), back surface silvered with radius `back`
    (centre at +back, None = flat). object at distance u on the left. returns the z of the returned image (negative = left)"""
    r = surf(0, front, n_out, n_glass, (-u, 0.0, 1e-6)); z0, y0, m0 = r
    L = math.sqrt(1 + m0 * m0); dx, dy = 1 / L, m0 / L
    if back is None: zs, ys, nx, ny = 0.0, y0 + m0 * (0 - z0), 1.0, 0.0
    else:
        c = back; a = 1 + m0 * m0; b = 2 * ((z0 - c) + m0 * y0); cc = (z0 - c) ** 2 + y0 * y0 - back * back; d = math.sqrt(b * b - 4 * a * cc)
        t = min([(-b - d) / (2 * a), (-b + d) / (2 * a)], key=lambda t: abs(z0 + t)); zs, ys = z0 + t, y0 + m0 * t; nx, ny = (zs - c) / abs(back), ys / abs(back)
    dot = dx * nx + dy * ny; rx, ry = dx - 2 * dot * nx, dy - 2 * dot * ny
    r2 = surf(0, -front, n_glass, n_out, (-zs, ys, -ry / rx))   # flip z for the return trip
    return -axis_cross(r2)
def self_image(front, back, n_out, n_glass):
    lo, hi = 1e-3, 50.0
    for _ in range(100):
        u = (lo + hi) / 2
        if silvered(u, front, back, n_out, n_glass) < -u: lo = u
        else: hi = u
    return (lo + hi) / 2
add(('2025', 'Jan', '2025-01-23', 1), 'refr', 'A spherical surface of radius of curvature R, separates air from glass (refractive index = 1.5). The centre of curvature is in the glass medium. A point object \'O\' placed in air on the optic axis of the surface, so that its real image is formed at \'I\' inside glass. The line OI intersects the spherical surface at P and PO = PI. The distance PO equals to',
    ['5R', '3R', '2R', '1.5R'], 1, lambda: P4([5, 3, 2, 1.5], next(x for x in [k / 1000 for k in range(1001, 20000)] if abs(lens_image(-x, [(0, 1.0, 1.0, 1.5)]) - x) < 2e-3)),
    ['\\f{1.5}{v} − \\f{1}{u} = \\f{0.5}{R} with u = −x, v = +x.', '\\f{2.5}{x} = \\f{0.5}{R} → x = 5R.'], 'refr', 2)
add(('2025', 'Jan', '2025-01-23', 1), 'mirror', 'Given a thin convex lens (refractive index μ_{2}), kept in a liquid (refractive index μ_{1}, μ_{1} < μ_{2}) having radii of curvatures |R_{1}| and |R_{2}|. Its second surface is silver polished. Where should an object be placed on the optic axis so that a real and inverted image is formed at the same place?',
    ['\\f{μ_{1}|R_{1}|·|R_{2}|}{μ_{2}(|R_{1}| + |R_{2}|) − μ_{1}|R_{2}|}', '\\f{(μ_{2} + μ_{1})|R_{1}|}{(μ_{2} − μ_{1})}', '\\f{μ_{1}|R_{1}|·|R_{2}|}{μ_{2}(2|R_{1}| + |R_{2}|) − μ_{1}√{|R_{1}|·|R_{2}|}}', '\\f{μ_{1}|R_{1}|·|R_{2}|}{μ_{2}(|R_{1}| + |R_{2}|) − μ_{1}|R_{1}|}'], 1,
    lambda: (lambda m1, m2, R1, R2: P4([m1 * R1 * R2 / (m2 * (R1 + R2) - m1 * R2), (m2 + m1) * R1 / (m2 - m1), m1 * R1 * R2 / (m2 * (2 * R1 + R2) - m1 * math.sqrt(R1 * R2)), m1 * R1 * R2 / (m2 * (R1 + R2) - m1 * R1)], self_image(R1, -R2, m1, m2), 2e-3))(1.2, 1.6, 0.3, 0.5),
    ['The ray must hit the silvered surface normally to retrace its path, i.e. after the first refraction it heads for the centre of the silvered surface.', 'First surface: \\f{μ_{2}}{−|R_{2}|} − \\f{μ_{1}}{−x} = \\f{μ_{2} − μ_{1}}{|R_{1}|}.', 'x = \\f{μ_{1}|R_{1}||R_{2}|}{μ_{2}(|R_{1}| + |R_{2}|) − μ_{1}|R_{2}|}.'], 'mirror', 3)
add(('2025', 'Jan', '2025-01-23', 1), 'refr', 'What is the lateral shift of a ray refracted through a parallel-sided glass slab of thickness \'h\' in terms of the angle of incidence \'i\' and angle of refraction \'r\', if the glass slab is placed in air medium?',
    ['\\f{h cos(i − r)}{sin r}', 'h', '\\f{h tan(i − r)}{tan r}', '\\f{h sin(i − r)}{cos r}'], 4,
    lambda: (lambda h, i: (lambda r: (lambda x_in: P4([h * math.cos(i - r) / math.sin(r), h, h * math.tan(i - r) / math.tan(r), h * math.sin(i - r) / math.cos(r)], (h * math.tan(i) - x_in) * math.cos(i), 1e-9))(h * math.tan(r)))(snell(1, 1.5, i)))(0.02, 0.6),
    ['Inside, the ray travels \\f{h}{cos r}.', 'It is turned by (i − r) from its original direction, so the sideways shift is \\f{h}{cos r} sin(i − r).'], 'refr', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'mirror', 'A concave mirror of focal length f in air is dipped in a liquid of refractive index μ. Its focal length in the liquid will be:',
    ['μf', '\\f{f}{μ}', 'f', '\\f{f}{(μ − 1)}'], 3, lambda: P4([1.33, 1 / 1.33, 1, 1 / 0.33], mirror_image(-1e3, -0.2) / -0.1, 1e-3),
    ['Reflection does not depend on the medium: angle in = angle out.', 'So f = \\f{R}{2} is unchanged.'], 'mirror', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'wave', 'The width of one of the two slits in Young\'s double slit experiment is d while that of the other slit is xd. If the ratio of the maximum to the minimum intensity in the interference pattern on the screen is 9 : 4 then what is the value of x? (Assume that the field strength varies according to the slit width.)',
    ['5', '4', '3', '2'], 1, lambda: P4([5, 4, 3, 2], next(x for x in [1 + k / 1000 for k in range(1, 10000)] if yd(0, 1, 1, x * x) / yd(0.5, 1, 1, x * x) <= 9 / 4 + 1e-9)),
    ['Field amplitudes 1 : x.', '\\f{(x + 1)^{2}}{(x − 1)^{2}} = \\f{9}{4} → \\f{x + 1}{x − 1} = \\f{3}{2} → x = 5.'], 'wave', 2)
add(('2025', 'Jan', '2025-01-23', 2), 'refr', 'The refractive index of the material of a glass prism is √{3}. The angle of minimum deviation is equal to the angle of the prism. What is the angle of the prism?',
    ['50°', '58°', '48°', '60°'], 4, lambda: P4([50, 58, 48, 60], _A()), ['√{3} = \\f{sin A}{sin(A/2)} = 2 cos\\f{A}{2}.', 'A = 60°.'], 'refr', 1)
add(('2025', 'Jan', '2025-01-24', 1), 'wave', 'The Young\'s double slit interference experiment is performed using light consisting of 480 nm and 600 nm wavelengths to form interference patterns. The least number of the bright fringes of 480 nm light that are required for the first coincidence with the bright fringes formed by 600 nm light is',
    ['4', '8', '5', '6'], 3, lambda: P4([4, 8, 5, 6], next(n for n in range(1, 50) if any(n * 480 == m * 600 for m in range(1, 50)))), ['n × 480 = m × 600 → 4n = 5m.', 'Smallest n = 5.'], 'wave', 1)
add(('2025', 'Jan', '2025-01-24', 1), 'lens', 'What is the relative decrease in focal length of a lens for an increase in optical power by 0.1 D from 2.5 D?',
    ['0.1', '0.04', '0.40', '0.01'], 2, lambda: P4([0.1, 0.04, 0.4, 0.01], (1 / 2.5 - 1 / 2.6) / (1 / 2.5), 0.04),
    ['f = \\f{1}{P} → \\f{Δf}{f} = \\f{ΔP}{P}.', '= \\f{0.1}{2.5} = 0.04.'], 'lens', 1)
add(('2025', 'Jan', '2025-01-24', 1), 'lens', 'A plano-convex lens having radius of curvature of first surface 2 cm exhibits focal length of f_{1} in air. Another plano-convex lens with first surface radius of curvature 3 cm has focal length of f_{2} when it is immersed in a liquid of refractive index 1.2. If both the lenses are made of same glass of refractive index 1.5, the ratio of f_{1} and f_{2} will be',
    ['2 : 3', '3 : 5', '1 : 2', '1 : 3'], 4, lambda: P4([2 / 3, 0.6, 0.5, 1 / 3], focal([(0, 0.02, 1, 1.5), (0, None, 1.5, 1)]) / focal([(0, 0.03, 1.2, 1.5), (0, None, 1.5, 1.2)]), 2e-3),
    ['Air: \\f{1}{f_{1}} = \\f{0.5}{2} → f_{1} = 4 cm.', 'Liquid: \\f{1}{f_{2}} = (\\f{1.5}{1.2} − 1)\\f{1}{3} = \\f{1}{12} → f_{2} = 12 cm.', 'f_{1} : f_{2} = 1 : 3.'], 'lens', 2)
add(('2025', 'Jan', '2025-01-24', 1), 'mirror', 'A thin plano convex lens made of glass of refractive index 1.5 is immersed in a liquid of refractive index 1.2. When the plane side of the lens is silver coated for complete reflection, the lens immersed in the liquid behaves like a concave mirror of focal length 0.2 m. The radius of curvature of the curved surface of the lens is',
    ['0.15 m', '0.20 m', '0.25 m', '0.10 m'], 4, lambda: P4([0.15, 0.2, 0.25, 0.1], next(R for R in [k / 1000 for k in range(20, 500)] if abs(self_image(R, None, 1.2, 1.5) - 0.4) < 2e-3)),
    ['Equivalent mirror: P = 2P_{lens} + P_{plane mirror} = 2(\\f{1.5}{1.2} − 1)\\f{1}{R} = \\f{1}{2R}.', 'Focal length 2R = 0.2 m → R = 0.1 m.'], 'mirror', 2)
add(('2025', 'Jan', '2025-01-24', 2), 'wave', 'Young\'s double slit interference apparatus is immersed in a liquid of refractive index 1.44. It has slit separation of 1.5 mm. The slits are illuminated by a parallel beam of light whose wavelength in air is 690 nm. The fringe-width on a screen placed behind the plane of slits at a distance of 0.72 m, will be:',
    ['0.63 mm', '0.23 mm', '0.46 mm', '0.33 mm'], 2, lambda: P4([0.63, 0.23, 0.46, 0.33], 690e-9 / 1.44 * 0.72 / 1.5e-3 * 1000, 2e-3),
    ['In the liquid λ\' = \\f{690}{1.44} nm.', 'β = \\f{λ\'D}{d} = \\f{479 × 10^{−9} × 0.72}{1.5 × 10^{−3}} = 0.23 mm.'], 'wave', 1)
def _pol3():
    E = math.sqrt(0.5)   # each slit: unpolarised I0 → I0/2 after P1 or P2 (amplitude² = 1/2)
    a1 = (E, 0.0); a2 = (0.0, E)   # P1 along x, P2 along y
    u = (1 / math.sqrt(2), 1 / math.sqrt(2))   # P3 at 45°
    p1 = a1[0] * u[0] + a1[1] * u[1]; p2 = a2[0] * u[0] + a2[1] * u[1]
    return abs(p1 + p2 * cmath.exp(2j * pi / 3)) ** 2
add(('2025', 'Jan', '2025-01-24', 2), 'wave', 'In a Young\'s double slit experiment, three polarizers are kept: P_{1} over slit S_{1} and P_{2} over slit S_{2}, with transmission axes orthogonal to each other. The polarizer P_{3} covers both the slits with its transmission axis at 45° to those of P_{1} and P_{2}. An unpolarized light of wavelength λ and intensity I_{0} is incident on P_{1} and P_{2}. The intensity at a point after P_{3} where the path difference between the light waves from S_{1} and S_{2} is \\f{λ}{3}, is',
    ['\\f{I_{0}}{3}', '\\f{I_{0}}{2}', '\\f{I_{0}}{4}', 'I_{0}'], 3, lambda: P4([1 / 3, 0.5, 0.25, 1], _pol3()),
    ['After P_{1} or P_{2}: \\f{I_{0}}{2}; after P_{3} (Malus, 45°): \\f{I_{0}}{4} each, now with the same polarisation.', 'Phase \\f{2π}{3}: I = \\f{I_{0}}{4} + \\f{I_{0}}{4} + 2\\f{I_{0}}{4} cos 120° = \\f{I_{0}}{4}.'], 'wave', 3)

# ---------- sheets 17–18
add(('2025', 'Jan', '2025-01-24', 2), 'lens', 'A photograph of a landscape is captured by a drone camera at a height of 18 km. The size of the camera film is 2 cm × 2 cm and the area of the landscape photographed is 400 km^{2}. The focal length of the lens in the drone camera is:',
    ['1.8 cm', '2.5 cm', '2.8 cm', '0.9 cm'], 1, lambda: P4([1.8, 2.5, 2.8, 0.9], (lambda f: f)(next(f for f in [k * 1e-5 for k in range(100, 10000)] if trace(-18000.0, thin(f), 1e-9) * 20000 / 18000 >= 0.02)) * 100, 2e-3),
    ['The 20 km × 20 km ground maps onto 2 cm × 2 cm: m = 10^{−6}.', 'For a distant object v ≈ f, so f = m × u = 10^{−6} × 18 000 m = 1.8 cm.'], 'lens', 2)
def _cotA():
    A = math.radians(50); n = 1 / math.tan(A / 2); best = 1e9
    for k in range(1, 15700):
        i = k * 1e-4; r1 = snell(1, n, i); e = snell(n, 1, A - r1)
        if e is not None: best = min(best, i + e - A)
    return best / A
add(('2024', 'Jan', '2024-01-27', 1), 'refr', 'If the refractive index of the material of a prism is cot(\\f{A}{2}), where A is the angle of prism then the angle of minimum deviation will be',
    ['π − 2A', '\\f{π}{2} − 2A', 'π − A', '\\f{π}{2} − A'], 1, lambda: P4([(pi - 2 * math.radians(50)) / math.radians(50), (pi / 2 - 2 * math.radians(50)) / math.radians(50), (pi - math.radians(50)) / math.radians(50), (pi / 2 - math.radians(50)) / math.radians(50)], _cotA(), 2e-3),
    ['sin\\f{A + δ}{2} = cot\\f{A}{2} sin\\f{A}{2} = cos\\f{A}{2} = sin(\\f{π}{2} − \\f{A}{2}).', '\\f{A + δ}{2} = \\f{π}{2} − \\f{A}{2} → δ = π − 2A.'], 'refr', 2)
add(('2024', 'Jan', '2024-01-27', 1), 'lens', 'A convex lens of focal length 40 cm forms an image of an extended source of light on a photoelectric cell. A current I is produced. The lens is replaced by another convex lens having the same diameter but focal length 20 cm. The photoelectric current now is :',
    ['\\f{I}{2}', '4I', '2I', 'I'], 4, lambda: P4([0.5, 4, 2, 1], (pi * 0.025 ** 2) / (pi * 0.025 ** 2)),
    ['The light energy collected depends on the lens aperture (its area), which is unchanged.', 'The same number of photons reaches the cell, so the current stays I.'], 'lens', 2)
def _coin():
    th = 1e-5; x = 0.06 * math.tan(th); t2 = snell(1.6, 1.5, th); x += 0.06 * math.tan(t2); t3 = snell(1.5, 1.0, t2); return x / math.tan(t3)   # apparent depth: where the emerging ray seems to come from
add(('2024', 'Jan', '2024-01-27', 1), 'refr', 'Two immiscible liquids of refractive indices \\f{8}{5} (bottom layer) and \\f{3}{2} (top layer) respectively are put in a beaker. The height of each column is 6 cm. A coin is placed at the bottom of the beaker. For near normal vision, the apparent depth of the coin is \\f{α}{4} cm. The value of α is', None, 31,
    lambda: round(_coin() * 100 * 4),
    ['Apparent depth = Σ \\f{t}{n}.', '\\f{6}{8/5} + \\f{6}{3/2} = 3.75 + 4 = 7.75 = \\f{31}{4} cm.'], 'refr', 1)
add(('2024', 'Jan', '2024-01-27', 2), 'wave', 'A parallel beam of monochromatic light of wavelength 5000 Å is incident normally on a single narrow slit of width 0.001 mm. The light is focused by convex lens on screen, placed on its focal plane. The first minima will be formed for the angle of diffraction of ______ (degree)', None, 30,
    lambda: round(math.degrees(first_zero(1e-6, 5e-7, hi=pi / 2 - 1e-3))), ['a sin θ = λ.', 'sin θ = \\f{5 × 10^{−7}}{10^{−6}} = 0.5 → θ = 30°.'], 'wave', 1)
add(('2025', 'Jan', '2025-01-28', 1), 'refr', 'A thin prism P_{1} with angle 4° made of glass having refractive index 1.54, is combined with another thin prism P_{2} made of glass having refractive index 1.72 to get dispersion without deviation. The angle of the prism P_{2} in degrees is',
    ['4', '16/3', '1.5', '3'], 4, lambda: P4([4, 16 / 3, 1.5, 3], next(a for a in [k / 1000 for k in range(1, 10000)] if abs((1.54 - 1) * 4 - (1.72 - 1) * a) < 5e-4)),
    ['No net deviation: (n_{1} − 1)A_{1} = (n_{2} − 1)A_{2}.', 'A_{2} = \\f{0.54 × 4}{0.72} = 3°.'], 'refr', 1)
def _hemi():
    lo, hi = 1.0, 3.0   # a ray from the bottom O to the rim must leave grazing (to reach E level with the rim)
    th = math.atan(1.0)   # to the rim: tan θ = R/R
    for _ in range(100):
        n = (lo + hi) / 2
        if snell(n, 1, th) is None: hi = n
        else: lo = n
    return lo
add(('2025', 'Jan', '2025-01-28', 1), 'refr', 'A hemispherical vessel is completely filled with a liquid of refractive index μ. A small coin is kept at the lowest point (O) of the vessel. The minimum value of the refractive index of the liquid so that a person can see the coin from point E (at the level of the vessel\'s rim) is ____.',
    ['\\f{3}{2}', '√{2}', '\\f{√{3}}{2}', '√{3}'], 2, lambda: P4([1.5, math.sqrt(2), math.sqrt(3) / 2, math.sqrt(3)], _hemi(), 1e-6),
    ['To reach E the ray must leave the surface grazing (at 90°).', 'The steepest ray available hits the edge at 45° (O is R below the centre, the edge R away): μ sin 45° = 1 → μ = √{2}.'], 'refr', 2)
add(('2025', 'Jan', '2025-01-28', 1), 'wave', 'A double slit interference experiment performed with a light of wavelength 600 nm forms an interference fringe pattern on a screen with 10th bright fringe having its centre at a distance of 10 mm from the central maximum. Distance of the centre of the same 10th bright fringe from the central maximum when the source of light is replaced by another source of wavelength 660 nm would be ______ mm.', None, 11,
    lambda: round(10 * 660 / 600, 6), ['y_{n} ∝ λ.', '10 × \\f{660}{600} = 11 mm.'], 'wave', 1)
add(('2025', 'Jan', '2025-01-28', 2), 'wave', 'Which of the following phenomena can not be explained by wave theory of light?',
    ['Diffraction of light', 'Compton effect', 'Refraction of light', 'Reflection of light'], 2,
    lambda: 2 if abs(6.63e-34 / (9.1e-31 * 3e8) * (1 - math.cos(pi / 2)) - 2.43e-12) < 1e-13 else 0,
    ['Diffraction, refraction and reflection follow from waves.', 'In the Compton effect the scattered X-ray\'s wavelength grows by \\f{h}{m_{e}c}(1 − cos φ) ≈ 2.4 pm at 90° — a photon–electron collision, not a wave effect.'], 'wave', 1)
def _men():
    m = lambda R: 1.3 * lens_image(-0.13, [(0, R, 1.3, 1.4)]) / (1.4 * -0.13) + 2
    lo, hi = 2e-3, 0.012   # m changes sign across this range
    for _ in range(100):
        mid = (lo + hi) / 2
        if (m(lo) > 0) == (m(mid) > 0): lo = mid
        else: hi = mid
    return lo * 100
add(('2025', 'Jan', '2025-01-28', 2), 'refr', 'In a long glass tube, mixture of two liquids A and B with refractive indices 1.3 and 1.4 respectively, forms a convex refractive meniscus towards A. If an object placed at 13 cm from the vertex of the meniscus in A forms an image with a magnification of \'−2\' then the radius of curvature of meniscus is:',
    ['\\f{1}{3} cm', '\\f{4}{3} cm', '1 cm', '\\f{2}{3} cm'], 4, lambda: P4([1 / 3, 4 / 3, 1, 2 / 3], _men(), 2e-3),
    ['m = \\f{n_{A}v}{n_{B}u} = −2 → \\f{1.3v}{1.4 × (−13)} = −2 → v = 28 cm.', '\\f{1.4}{28} + \\f{1.3}{13} = \\f{0.1}{R} → 0.15 = \\f{0.1}{R} → R = \\f{2}{3} cm.'], 'refr', 2)
add(('2025', 'Jan', '2025-01-28', 2), 'mirror', 'A concave mirror produces an image of an object such that the distance between the object and image is 20 cm. If the magnification of the image is \'−3\', then the magnitude of the radius of curvature of the mirror is :',
    ['7.5 cm', '30 cm', '3.75 cm', '15 cm'], 4,
    lambda: P4([7.5, 30, 3.75, 15], (lambda R: R)(next(R for R in [k / 10000 for k in range(100, 5000)] if (lambda u: abs(abs(mirror_image(-u, -R)) - u - 0.2) < 2e-4)(R / 2 * (1 + 1 / 3)))) * 100, 2e-3),
    ['m = −3: v = 3u, both in front. |v| − |u| = 20 → u = −10, v = −30 cm.', '\\f{1}{f} = −\\f{1}{30} − \\f{1}{10} → f = −7.5 cm, |R| = 15 cm.'], 'mirror', 1)

# ---------- sheets 19–20
def _evap():
    n, lam, r, T = 1.4, 560e-9, 0.018, 12.0
    # transmission minima repeat each time the round-trip optical path 2nt changes by λ: find the thickness step numerically
    tr = lambda t: abs(1 + 0.04 * cmath.exp(2j * 2 * pi * n * t / lam)) ** 2   # weak internal reflections: same period as the exact film
    ts = [k * 1e-10 for k in range(1, 6000)]; mins = [t for a, t, b in zip(ts, ts[1:], ts[2:]) if tr(t) > tr(a) and tr(t) > tr(b)]
    step = mins[1] - mins[0]; return pi * r * r * step / T / (pi * 1e-13)
add(('2025', 'Jan', '2025-01-28', 2), 'wave', 'A thin transparent film with refractive index 1.4, is held on circular ring of radius 1.8 cm. The fluid in the film evaporates such that transmission through the film at wavelength 560 nm goes to a minimum every 12 seconds. Assuming that the film is flat on its two sides, the rate of evaporation is ______ π × 10^{−13} m^{3}/s.', None, 54,
    lambda: round(_evap()), ['Successive transmission minima: 2nt changes by λ → Δt = \\f{λ}{2n} = 200 nm.', 'Volume lost per 12 s = π(0.018)^{2} × 2 × 10^{−7} m^{3} → rate = 54π × 10^{−13} m^{3}/s.'], 'wave', 3)
def _half_cvx():
    lo, hi = 0.001, 2.0
    for _ in range(100):
        u = (lo + hi) / 2
        if mirror_image(-u, 0.30) / u > 0.5: lo = u
        else: hi = u
    return -(lo + hi) / 2
add(('2024', 'Jan', '2024-01-29', 1), 'mirror', 'A convex mirror of radius of curvature 30 cm forms an image that is half the size of the object. The object distance is :',
    ['−15 cm', '45 cm', '−45 cm', '15 cm'], 1, lambda: pick([-0.15, 0.45, -0.45, 0.15], round(_half_cvx(), 6)), ['m = \\f{f}{f − u} = \\f{1}{2} with f = +15 cm.', '15 − u = 30 → u = −15 cm.'], 'mirror', 1)
add(('2024', 'Jan', '2024-01-29', 1), 'lens', 'A biconvex lens of refractive index 1.5 has a focal length of 20 cm in air. Its focal length when immersed in a liquid of refractive index 1.6 will be:',
    ['−16 cm', '−160 cm', '+160 cm', '+16 cm'], 2, lambda: P4([-16, -160, 160, 16], thin_f(0.2, -0.2, 1.5, 1.6) * 100, 2e-3),
    ['\\f{f_{l}}{f_{a}} = \\f{(1.5 − 1)}{(1.5/1.6 − 1)} = \\f{0.5}{−0.0625} = −8.', 'f_{l} = −160 cm: it now diverges.'], 'lens', 1)
def _ds():
    lam, D = 400e-9, 0.2
    lo, hi = 1e-6, 1e-3
    for _ in range(200):
        d = (lo + hi) / 2; path = 2 * (math.hypot(D, d) - D)
        if path < lam / 2: lo = d
        else: hi = d
    return lo * 1000
add(('2024', 'Jan', '2024-01-29', 1), 'wave', 'In a double slit experiment, slit S_{2} lies on the line joining the source and the point P (source D to the left of the slits, P a distance D to the right), and S_{1} is a distance d directly above S_{2}. When light of wavelength 400 nm is used, dark fringe is observed at P. If D = 0.2 m, the minimum distance between the slits S_{1} and S_{2} is ______ × 10^{−1} mm.', None, 2,
    lambda: round(_ds() * 10, 4), ['Path via S_{1}: 2√{D^{2} + d^{2}}; via S_{2}: 2D. Difference ≈ \\f{d^{2}}{D}.', 'First dark: \\f{d^{2}}{D} = \\f{λ}{2} → d = √{\\f{400 × 10^{−9} × 0.2}{2}} = 2 × 10^{−4} m = 2 × 10^{−1} mm.'], 'wave', 3)
def _virt2():
    lo, hi = 0.01, 2.0   # concave mirror: object between F and the mirror, virtual image 2× → u + v (both sides) = 15 cm
    for _ in range(80):
        R = (lo + hi) / 2; a, b = 1e-4, R / 2 * 0.9999
        for _ in range(100):
            u = (a + b) / 2
            if mirror_image(-u, -R) / u > 2: b = u
            else: a = u
        u = (a + b) / 2; gap = u + mirror_image(-u, -R)
        if gap < 0.15: lo = R
        else: hi = R
    return -(lo + hi) / 2 / 2 * 100
add(('2024', 'Jan', '2024-01-29', 2), 'mirror', 'If the distance between object and its two times magnified virtual image produced by a curved mirror is 15 cm, the focal length of the mirror must be :',
    ['15 cm', '−12 cm', '−10 cm', '10/3 cm'], 3, lambda: P4([15, -12, -10, 10 / 3], _virt2(), 2e-3),
    ['Magnified and virtual: a concave mirror, image behind it with v = 2|u|.', '|u| + 2|u| = 15 → u = −5 cm, v = +10 cm.', '\\f{1}{f} = \\f{1}{10} − \\f{1}{5} → f = −10 cm.'], 'mirror', 2)
add(('2024', 'Jan', '2024-01-29', 2), 'wave', 'In Young\'s double slit experiment, light from two identical sources are superimposing on a screen. The path difference between the two lights reaching at a point on the screen is \\f{7λ}{4}. The ratio of intensity of fringe at this point with respect to the maximum intensity of the fringe is :',
    ['1/2', '3/4', '1/3', '1/4'], 1, lambda: P4([0.5, 0.75, 1 / 3, 0.25], yd(7 / 4, 1) / yd(0, 1)), ['Phase = 2π × \\f{7}{4} = \\f{7π}{2}.', '\\f{I}{I_{max}} = cos^{2}\\f{7π}{4} = \\f{1}{2}.'], 'wave', 1)
def _13():
    lam, D = 6e-7, 0.5
    lo, hi = 1e-5, 1e-3
    for _ in range(100):
        a = (lo + hi) / 2; y1 = D * math.tan(math.asin(lam / a)); y3 = D * math.tan(math.asin(3 * lam / a))
        if y3 - y1 > 3e-3: lo = a
        else: hi = a
    return lo / 1e-4
add(('2024', 'Jan', '2024-01-29', 2), 'wave', 'In a single slit diffraction pattern, a light of wavelength 6000 Å is used. The distance between the first and third minima in the diffraction pattern is found to be 3 mm when the screen in placed 50 cm away from slits. The width of the slit is ______ × 10^{−4} m.', None, 2,
    lambda: round(_13(), 2), ['Minima at y_{n} = \\f{nλD}{a}: from n = 1 to 3 is \\f{2λD}{a}.', 'a = \\f{2 × 6 × 10^{−7} × 0.5}{3 × 10^{−3}} = 2 × 10^{−4} m.'], 'wave', 1)
def _block2():
    n1, n2, d = 1.0, 1.5, 4 * math.sqrt(3)
    th = math.acos(n2 / (2 * n1)); i = pi / 2 - th; r = snell(n1, n2, i)
    return (d / 2) / math.tan(r)
add(('2025', 'Jan', '2025-01-29', 1), 'refr', 'Two light beams fall on a transparent material block at points 1 and 2 with angles θ_{1} and θ_{2} (measured from the surface), respectively. After refraction, the beams intersect at point 3 which is exactly on the interface at the other end of the block, midway below 1 and 2. Given: the distance between 1 and 2, d = 4√{3} cm and θ_{1} = θ_{2} = cos^{−1}(\\f{n_{2}}{2n_{1}}), where refractive index of the block n_{2} > refractive index of the outside medium n_{1}, then the thickness of the block is ______ cm.', None, 6,
    lambda: round(_block2(), 6), ['Angle of incidence i = 90° − θ, so sin i = cos θ = \\f{n_{2}}{2n_{1}}.', 'Snell: sin r = \\f{n_{1}}{n_{2}} sin i = ½ → r = 30°.', 'Each beam moves \\f{d}{2} = 2√{3} sideways: t = \\f{2√{3}}{tan 30°} = 6 cm.'], 'refr', 2)
add(('2025', 'Jan', '2025-01-29', 2), 'lens', 'A convex lens made of glass (refractive index = 1.5) has focal length 24 cm in air. When it is totally immersed in water (refractive index = 1.33), its focal length changes to',
    ['24 cm', '96 cm', '48 cm', '72 cm'], 2, lambda: P4([24, 96, 48, 72], thin_f(0.24, -0.24, 1.5, 4 / 3) * 100, 2e-3),
    ['\\f{f_{w}}{f_{a}} = \\f{0.5}{1.5/1.33 − 1} ≈ \\f{0.5}{0.125} = 4 (taking n_{w} ≈ \\f{4}{3}).', 'f_{w} ≈ 96 cm.'], 'lens', 1)

# ---------- sheets 21–22
add(('2025', 'Jan', '2025-01-29', 2), 'lens', 'Two identical symmetric double convex lenses of focal length f are cut: the first into two equal parts L_{1}, L_{2} by the plane AB (through the principal axis), the second into L_{3}, L_{4} by the plane XY (the plane of the lens). The ratio of focal lengths of lenses L_{1} and L_{3} is',
    ['2 : 1', '1 : 4', '1 : 2', '1 : 1'], 3, lambda: P4([2, 0.25, 0.5, 1], focal(biconvex(0.2, 0.2, 1.5)) / focal([(0, 0.2, 1, 1.5), (0, None, 1.5, 1)]), 2e-3),
    ['L_{1} is still the full double-convex profile (only its aperture is halved): focal length f.', 'L_{3} is plano-convex: focal length 2f. Ratio 1 : 2.'], 'lens', 1)
def _gap():
    R = 1.0; zA, zB = 0.0, 2.0; zO = 1.5   # A at 0, B at 2R, O midway between the midpoint P (R) and B
    # surface A, light travelling left: flip so it travels right (vertex at 0, object at −1.5R). Hollow in glass → centre on the air side
    vA = lens_image(-(zO - zA), [(0, -R, 1.0, 1.5)])   # negative = virtual, on the air side
    vB = lens_image(-(zB - zO), [(0, -R, 1.0, 1.5)])
    iA = zA - vA; iB = zB + vB   # back to the original coordinates
    return abs(iB - iA)
add(('2025', 'Jan', '2025-01-29', 2), 'refr', 'Two concave refracting surfaces of equal radii of curvature R and refractive index 1.5 face each other in air (glass blocks with hollow faces; vertices A and B are 2R apart and P is the midpoint). A point object O is placed midway between P and B. The separation between the images of O, formed by each refracting surface is:',
    ['0.114R', '0.411R', '0.124R', '0.214R'], 1, lambda: P4([0.114, 0.411, 0.124, 0.214], _gap(), 3e-3),
    ['Surface A (u = −1.5R, R = −R): \\f{1.5}{v} = −\\f{0.5}{R} − \\f{1}{1.5R} → v = −\\f{9R}{7}: 1.286R from A towards B.', 'Surface B (u = −0.5R): \\f{1.5}{v} = −\\f{0.5}{R} − \\f{2}{R} → v = −0.6R: 1.4R from A.', 'Separation = 1.4R − 1.286R ≈ 0.114R.'], 'refr', 3)
add(('2026', 'Apr', '2026-04-04', 1), 'wave', 'A slit of width a is illuminated by light of wavelength λ. The linear separation between 1^{st} and 3^{rd} minima in the diffraction pattern produced on a screen placed at a distance D from the slit system is ______.',
    ['\\f{Dλ}{a}', '1.5\\f{Dλ}{a}', '2\\f{Dλ}{a}', '3\\f{Dλ}{a}'], 3, lambda: P4([1, 1.5, 2, 3], (3 * math.tan(first_zero(1e-3, 5e-7)) - math.tan(first_zero(1e-3, 5e-7))) * 1.0 / (5e-7 / 1e-3), 2e-3),
    ['Minima at y_{n} = \\f{nλD}{a}.', 'y_{3} − y_{1} = \\f{2Dλ}{a}.'], 'wave', 1)
def _rod():
    ends = [mirror_image(-0.20, -0.20), mirror_image(-0.30, -0.20)]; return abs(ends[0] - ends[1]) * 100
add(('2026', 'Apr', '2026-04-04', 1), 'mirror', 'A rod of length 10 cm lies along the principal axis of a concave mirror of focal length 10 cm, its nearer end 20 cm from the mirror. The length of the image is ______ cm.',
    ['2.5', '5', '7.5', '7'], 2, lambda: P4([2.5, 5, 7.5, 7], _rod(), 2e-3), ['Near end at C (20 cm) images onto itself.', 'Far end (30 cm): \\f{1}{v} = −\\f{1}{10} + \\f{1}{30} → v = −15 cm.', 'Image length = 20 − 15 = 5 cm.'], 'mirror', 2)
add(('2026', 'Apr', '2026-04-04', 1), 'lens', 'A telescope with objective diameter R is used to observe a distant star emitting light of wavelength 500 nm, at a resolution of 5 × 10^{−7} radian. The value of R is ______ cm.',
    ['61', '122', '244', '305'], 2, lambda: P4([61, 122, 244, 305], 1.22 * 500e-9 / 5e-7 * 100), ['Limit of resolution θ = \\f{1.22λ}{D}.', 'D = \\f{1.22 × 500 × 10^{−9}}{5 × 10^{−7}} = 1.22 m = 122 cm.'], 'lens', 1)
def _prism_graze():
    n, A = math.sqrt(2), pi / 3; C = math.asin(1 / n); return math.degrees(A - C)
add(('2026', 'Jan', '2026-01-22', 1), 'refr', 'Consider an equilateral prism (refractive index √{2}). A ray of light is incident on its one surface at a certain angle i. If the emergent ray is found to graze along the other surface then the angle of refraction at the incident surface is close to ______.',
    ['15°', '20°', '40°', '30°'], 1, lambda: P4([15, 20, 40, 30], _prism_graze()), ['Grazing exit: r_{2} = critical angle = 45° (sin C = \\f{1}{√{2}}).', 'r_{1} = A − r_{2} = 60° − 45° = 15°.'], 'refr', 1)
add(('2026', 'Jan', '2026-01-22', 1), 'refr', 'A parallel beam of light travelling in air (refractive index 1.0) is incident on a convex spherical glass surface of radius of curvature 50 cm. Refractive index of glass is 1.5. The rays converge to a point at a distance x cm from the centre of the curvature of the spherical surface. The value of x is ______ cm.', None, 100,
    lambda: round((focal([(0, 0.5, 1.0, 1.5)]) - 0.5) * 100, 4), ['\\f{1.5}{v} = \\f{0.5}{50} → v = 150 cm from the surface.', 'The centre is 50 cm in, so x = 100 cm.'], 'refr', 1)

# ---------- sheets 23–24
def _sec():
    a, lam, f = 2e-4, 400e-9, 1.0
    zs = [first_zero(a, lam)]; th = zs[0] * 1.01; I = lambda t: single_slit_I(a, lam, t, 400); step = zs[0] / 2000
    while not (I(th) < I(th + step) or False): th += step   # climb out of the first zero
    while I(th + step) >= I(th): th += step   # over the first secondary maximum
    while I(th + step) < I(th): th += step   # down to the second zero
    return f * (math.tan(th) - math.tan(zs[0])) * 1000
add(('2024', 'Jan', '2024-01-30', 1), 'wave', 'The diffraction pattern of a light of wavelength 400 nm diffracting from a slit of width 0.2 mm is focused on the focal plane of a convex lens of focal length 100 cm. The width of the 1^{st} secondary maxima will be :',
    ['2 mm', '2 cm', '0.02 mm', '0.2 mm'], 1, lambda: P4([2, 20, 0.02, 0.2], _sec(), 5e-3),
    ['Secondary maxima lie between successive minima, which are \\f{λf}{a} apart.', 'Width = \\f{400 × 10^{−9} × 1}{2 × 10^{−4}} = 2 × 10^{−3} m = 2 mm.'], 'wave', 1)
def _real2():
    lo, hi = 0.01, 0.5
    for _ in range(80):
        f = (lo + hi) / 2; a, b = f * 1.0001, 10.0
        for _ in range(100):   # object distance giving m = −2
            u = (a + b) / 2
            if trace(-u, thin(f)) / u > 2: a = u
            else: b = u
        u = (a + b) / 2; gap = u + trace(-u, thin(f))
        if gap < 0.45: lo = f
        else: hi = f
    return (lo + hi) / 2 * 100
add(('2024', 'Jan', '2024-01-30', 1), 'lens', 'The distance between object and its two times magnified real image as produced by a convex lens is 45 cm. The focal length of the lens used is ______ cm.', None, 10,
    lambda: round(_real2(), 3), ['Real and 2×: v = 2|u| on the other side; |u| + v = 45 → |u| = 15, v = 30 cm.', '\\f{1}{f} = \\f{1}{30} + \\f{1}{15} → f = 10 cm.'], 'lens', 1)
add(('2024', 'Jan', '2024-01-30', 2), 'wave', 'A beam of unpolarised light of intensity I_{0} is passed through a polaroid A and then through another polaroid B which is oriented so that its principal plane makes an angle of 45° relative to that of A. The intensity of emergent light is :',
    ['I_{0}/4', 'I_{0}', 'I_{0}/2', 'I_{0}/8'], 1, lambda: P4([0.25, 1, 0.5, 0.125], sum(math.cos(2 * pi * k / 3600) ** 2 for k in range(3600)) / 3600 * math.cos(pi / 4) ** 2),
    ['A passes half of unpolarised light: \\f{I_{0}}{2}.', 'Malus: \\f{I_{0}}{2} cos^{2} 45° = \\f{I_{0}}{4}.'], 'wave', 1)
def _cot2():
    A = math.radians(40); n = 1 / math.tan(A / 2); best = 1e9
    for k in range(1, 15700):
        i = k * 1e-4; r1 = snell(1, n, i); e = snell(n, 1, A - r1)
        if e is not None: best = min(best, i + e - A)
    return math.degrees(best)
add(('2024', 'Jan', '2024-01-31', 1), 'refr', 'The refractive index of a prism with apex angle A is cot A/2. The angle of minimum deviation is :',
    ['δ_{m} = 180° − A', 'δ_{m} = 180° − 3A', 'δ_{m} = 180° − 4A', 'δ_{m} = 180° − 2A'], 4, lambda: P4([140, 60, 20, 100], _cot2(), 2e-3),
    ['\\f{sin((A + δ)/2)}{sin(A/2)} = cot\\f{A}{2} → sin\\f{A + δ}{2} = cos\\f{A}{2}.', '\\f{A + δ}{2} = 90° − \\f{A}{2} → δ = 180° − 2A.'], 'refr', 2)
def _brew():
    i = pi / 3; n = math.tan(i)   # Brewster: the reflected and refracted rays are at right angles
    r = snell(1, n, i); return math.degrees(r)
add(('2024', 'Jan', '2024-01-31', 2), 'wave', 'When unpolarized light is incident at an angle of 60° on a transparent medium from air. The reflected ray is completely polarized. The angle of refraction in the medium is',
    ['30°', '60°', '90°', '45°'], 1, lambda: P4([30, 60, 90, 45], _brew()), ['Complete polarisation: Brewster angle, n = tan 60° = √{3}.', 'Reflected ⟂ refracted: r = 90° − 60° = 30° (Snell gives the same).'], 'wave', 1)
add(('2024', 'Jan', '2024-01-31', 2), 'refr', 'Light from a point source in air falls on a convex curved surface of radius 20 cm and refractive index 1.5. If the source is located at 100 cm from the convex surface, the image will be formed at ______ cm from the object.', None, 200,
    lambda: round((lens_image(-1.0, [(0, 0.2, 1.0, 1.5)]) + 1.0) * 100, 3), ['\\f{1.5}{v} + \\f{1}{100} = \\f{0.5}{20} → v = 100 cm inside the glass.', 'Object-to-image distance = 100 + 100 = 200 cm.'], 'refr', 1)

# ---------- sheets 25–26
add(('2026', 'Apr', '2026-04-04', 2), 'lens', 'A convex lens is made from glass material having refractive index of 1.4 with same radius of curvature on both sides. The ratio of its focal length and radius of curvature is ___ .',
    ['0.5', '2.5', '0.8', '1.25'], 4, lambda: P4([0.5, 2.5, 0.8, 1.25], focal(biconvex(0.1, 0.1, 1.4)) / 0.1, 2e-3), ['\\f{1}{f} = 0.4 × \\f{2}{R} = \\f{0.8}{R}.', '\\f{f}{R} = 1.25.'], 'lens', 1)
def _malus(axes):
    I = 0.5; prev = axes[0]   # unpolarised → first polariser passes half
    for a in axes[1:]: I *= math.cos(math.radians(a - prev)) ** 2; prev = a
    return I
add(('2026', 'Apr', '2026-04-04', 2), 'wave', 'An unpolarized light of certain intensity passes through a combination of two polarizers whose transmission axes are at 30° and 90°, respectively, with respect to the horizontal axis. A third polarizer with its transmission axis at 60° with the horizontal axis is placed between the two existing polarizers. The ratio of the output intensities with and without the third polarizer is ____.',
    ['3/4', '4/3', '9/4', '4/9'], 3, lambda: P4([0.75, 4 / 3, 2.25, 4 / 9], _malus([30, 60, 90]) / _malus([30, 90])),
    ['Without: \\f{I}{2} cos^{2} 60° = \\f{I}{8}.', 'With: \\f{I}{2} cos^{2} 30° cos^{2} 30° = \\f{9I}{32}.', 'Ratio = \\f{9}{4}.'], 'wave', 2)
add(('2026', 'Apr', '2026-04-04', 2), 'wave', 'In a double slit experiment, when one of the slits is covered by a transparent mica sheet of refractive index 1.56, the central fringe shifts to the position of 7^{th} bright fringe, obtained with both slits uncovered. If the light source wavelength is 450 nm, the thickness of mica sheet is α × 10^{−9} m. The value of α is ______.', None, 5625,
    lambda: round(7 * 450 / 0.56), ['(μ − 1)t = 7λ.', 't = \\f{7 × 450}{0.56} nm = 5625 nm.'], 'wave', 1)
add(('2026', 'Jan', '2026-01-22', 2), 'refr', 'The wavelength of light, while it is passing through water is 540 nm. The refractive index of water is 4/3. The wavelength of the same light when it is passing through a transparent medium having refractive index of 3/2 is ______ nm.',
    ['480', '840', '380', '540'], 1, lambda: P4([480, 840, 380, 540], 540 * (4 / 3) / 1.5), ['Frequency fixed, so nλ is constant: λ = \\f{540 × 4/3}{3/2}.', '= 480 nm.'], 'refr', 1)
add(('2026', 'Jan', '2026-01-22', 2), 'mirror', 'In parallax method for the determination of focal length of a concave mirror, the object should always be placed :',
    ['at any point beyond the focus (F) of the mirror', 'between the focus (F) and the centre of curvature (C) of the mirror ONLY', 'beyond the centre of the curvature (C) of the mirror ONLY', 'between the pole (P) and the focus (F) of the concave mirror ONLY'], 1,
    lambda: 1 if all(mirror_image(-u, -0.2) < 0 for u in (0.12, 0.15, 0.25, 0.4, 1.0)) and mirror_image(-0.05, -0.2) > 0 else 0,
    ['Parallax method locates a REAL image with a pin, so the object must be beyond F.', 'Any position beyond F (between F and C, at C, or beyond C) gives a real image.'], 'mirror', 1)
add(('2026', 'Apr', '2026-04-05', 1), 'wave', 'In Young\'s double slit experiment, the fringe width of the interference pattern produced on the screen is 2.4 μm. If the experiment is carried out in another medium having refractive index 1.2, the fringe width will be ______ μm.',
    ['1.2', '2', '2.4', '2.88'], 2, lambda: P4([1.2, 2, 2.4, 2.88], 2.4 / 1.2), ['β ∝ λ, and λ falls by the factor n.', '\\f{2.4}{1.2} = 2 μm.'], 'wave', 1)
def _v():
    n = 3e8 / 2.12e8; A = pi / 3; best = 1e9
    for k in range(1, 15700):
        i = k * 1e-4; r1 = snell(1, n, i); e = snell(n, 1, A - r1)
        if e is not None: best = min(best, i + e - A)
    return math.degrees(best)
add(('2026', 'Apr', '2026-04-05', 1), 'refr', 'A ray of light passing through an equilateral prism is having velocity 2.12 × 10^{8} m/s in the prism material, then the minimum angle of deviation is ______ degrees.',
    ['45', '30', '28', '58'], 2, lambda: P4([45, 30, 28, 58], _v(), 0.02), ['n = \\f{3 × 10^{8}}{2.12 × 10^{8}} ≈ 1.414 = √{2}.', 'sin\\f{60° + δ}{2} = √{2} sin 30° → \\f{60° + δ}{2} = 45° → δ = 30°.'], 'refr', 1)
add(('2026', 'Apr', '2026-04-05', 1), 'lens', 'A compound microscope is designed with two symmetric biconvex lenses. The objective lens is cut vertically, creating two identical plano-convex lenses. One of them is used in place of original objective lens. To retain same magnification keeping the object distance unchanged, the tube length has to be',
    ['increased two times', 'increased \\f{3}{2} times', 'decreased two times', 'decreased \\f{3}{2} times'], 1,
    lambda: P4([2, 1.5, 0.5, 2 / 3], (lambda f1, f2: f2 / f1)(focal(biconvex(0.02, 0.02, 1.5)), focal([(0, 0.02, 1, 1.5), (0, None, 1.5, 1)])), 2e-3),
    ['Cutting along the lens plane halves the curvature: the plano-convex objective has twice the focal length.', 'With m ≈ \\f{L}{f_{o}} × \\f{D}{f_{e}}, keeping m means doubling the tube length L.'], 'lens', 2)
add(('2026', 'Jan', '2026-01-23', 1), 'refr', 'A thin prism with angle 5° of refractive index 1.72 is combined with another prism of refractive index 1.9 to produce dispersion without deviation. The angle of second prism is ______.',
    ['4.5°', '6°', '4°', '5°'], 3, lambda: P4([4.5, 6, 4, 5], (1.72 - 1) * 5 / (1.9 - 1)), ['(n_{1} − 1)A_{1} = (n_{2} − 1)A_{2}.', 'A_{2} = \\f{0.72 × 5}{0.9} = 4°.'], 'refr', 1)

# ---------- sheets 27–28
def _crit_speed():
    nA, nB = 3e8 / 2.4e8, 3e8 / 2.7e8; lo, hi = 0.0, pi / 2
    for _ in range(100):
        th = (lo + hi) / 2
        if snell(nA, nB, th) is None: hi = th
        else: lo = th
    return math.tan(lo)
add(('2026', 'Jan', '2026-01-23', 1), 'refr', 'Consider light travelling from a medium A to medium B separated by a plane interface. If the light undergoes total internal reflection during its travel from medium A to B and the speed of light in media A and B are 2.4 × 10^{8} m/s and 2.7 × 10^{8} m/s, respectively, then the value of critical angle is :',
    ['cot^{−1}(\\f{3}{√{13}})', 'sin^{−1}(\\f{9}{8})', 'tan^{−1}(\\f{8}{√{17}})', 'cos^{−1}(\\f{8}{9})'], 3,
    lambda: P4([math.sqrt(13) / 3, 1e9, 8 / math.sqrt(17), math.tan(math.acos(8 / 9))], _crit_speed(), 1e-6),
    ['sin C = \\f{n_{B}}{n_{A}} = \\f{v_{A}}{v_{B}} = \\f{8}{9}.', 'cos C = \\f{√{17}}{9} → tan C = \\f{8}{√{17}}.'], 'refr', 2)
add(('2026', 'Jan', '2026-01-23', 1), 'wave', 'In two separate Young\'s double-slit experimental set-ups and two monochromatic light sources of different wavelengths are used to get fringes of equal width. The ratios of the slits separations and that of the wavelengths of light used are 2 : 1 and 1 : 2 respectively. The corresponding ratio of the distances between the slits and the respective screens (D_{1}/D_{2}) is ______.', None, 4,
    lambda: round(next(r for r in [k / 100 for k in range(1, 1000)] if abs(1 * r / 2 - 2 * 1 / 1) < 1e-9)), ['β = \\f{λD}{d} equal: \\f{λ_{1}D_{1}}{d_{1}} = \\f{λ_{2}D_{2}}{d_{2}}.', '\\f{D_{1}}{D_{2}} = \\f{d_{1}}{d_{2}} × \\f{λ_{2}}{λ_{1}} = 2 × 2 = 4.'], 'wave', 1)
def _contact():
    out = []
    for fc, fd in ((0.3, 0.2), (0.2, 0.3)):   # convex focal length, concave focal length (magnitudes)
        out.append(focal(thin(fc) + thin(-fd)))
    return 1 if out[0] < 0 and out[1] > 0 else 0
add(('2026', 'Apr', '2026-04-05', 2), 'lens', 'A thin convex lens and a thin concave lens are kept in contact and are co-axial. Which of the following statements is correct for this combination of two lenses?',
    ['behaves as concave lens if |f_{convex}| > |f_{concave}|', 'behaves as concave lens if |f_{convex}| < |f_{concave}|', 'behaves as convex lens if |f_{convex}| > |f_{concave}|', 'Focal length of the lens system will change if the positions of two lenses are interchanged'], 1, lambda: _contact(),
    ['P = \\f{1}{|f_{convex}|} − \\f{1}{|f_{concave}|}.', 'If |f_{convex}| > |f_{concave}| the concave lens is stronger: P < 0, a diverging (concave) combination. Order does not matter for lenses in contact.'], 'lens', 1)
def _PQ():
    h = 1e-6
    v1 = trace(-0.15, thin(0.10)); m1 = v1 / -0.15; u2 = v1 - 0.15   # image of P, measured from Q (+: to the right → virtual object)
    # the object for Q is virtual: send in a converging ray aimed at it
    ray = (0.0, h * (u2), -h)   # height at Q's plane chosen so the ray heads to the axis at z = u2 (relative to Q)
    for s in thin(0.15): ray = surf(*s, ray)
    v2 = axis_cross(ray); m2 = v2 / u2
    return (round(v2, 6), round(m1 * m2, 6))
add(('2026', 'Apr', '2026-04-05', 2), 'lens', 'An object AB is placed 15 cm on the left of a convex lens P of focal length 10 cm. Another convex lens Q is now placed 15 cm right of lens P. If the focal length of lens Q is 15 cm, the final image is ______.',
    ['virtual, formed at 7.5 cm right of lens Q, with a size bigger than that of AB', 'real, formed at 7.5 cm right of lens Q, with a size same as that of AB', 'formed at infinity.', 'real, formed at 7 cm right of lens Q, with a size smaller than that of AB'], 2,
    lambda: 2 if _PQ() == (0.075, -1.0) else 0,
    ['P: \\f{1}{v} = \\f{1}{10} − \\f{1}{15} → v = 30 cm, m_{1} = −2. That is 15 cm beyond Q: a virtual object (u = +15).', 'Q: \\f{1}{v} = \\f{1}{15} + \\f{1}{15} → v = 7.5 cm (real), m_{2} = \\f{7.5}{15} = ½.', 'Total m = −1: real, inverted, same size.'], 'lens', 2)
def _opp():
    lam = 1.0; d = 5 * lam; D = 10 * d; y = d / 2
    p = math.hypot(D, y + d / 2) - math.hypot(D, y - d / 2); return yd(p, lam) / 4
add(('2026', 'Apr', '2026-04-05', 2), 'wave', 'The maximum intensity in a Young\'s double slit experiment is I_{0}. Distance between the slits (d) is 5λ, where λ is the wavelength of light used. The intensity of the fringe, exactly opposite to one of the slits on the screen, placed at D = 10d is ______.',
    ['\\f{I_{0}}{4}', '\\f{I_{0}}{2}', 'I_{0}', '\\f{3I_{0}}{4}'], 2, lambda: P4([0.25, 0.5, 1, 0.75], _opp(), 0.02),
    ['Opposite a slit, y = \\f{d}{2}: path difference ≈ \\f{yd}{D} = \\f{d^{2}}{2D} = \\f{d}{20} = \\f{λ}{4}.', 'Phase \\f{π}{2} → I = I_{0} cos^{2}\\f{π}{4} = \\f{I_{0}}{2}.'], 'wave', 2)
def _brew152():
    ib = 57.7   # the value the question supplies for tan⁻¹(1.52)
    return 90 - ib   # at Brewster incidence the reflected and refracted rays are perpendicular
add(('2026', 'Jan', '2026-01-23', 2), 'wave', 'When an unpolarized light falls at a particular angle on a glass plate (placed in air), it is observed that the reflected beam is linearly polarized. The angle of refracted beam with respect to the normal is ____. (tan^{−1}(1.52) = 57.7°, refractive indices of air and glass are 1.00 and 1.52, respectively.)',
    ['39.6°', '32.3°', '42.6°', '36.3°'], 2, lambda: P4([39.6, 32.3, 42.6, 36.3], _brew152(), 2e-3), ['Brewster: i = tan^{−1} 1.52 = 57.7°.', 'Reflected ⟂ refracted → r = 90° − 57.7° = 32.3°.'], 'wave', 1)
def _equal_size():
    lo, hi = 0.09, 0.3
    for _ in range(100):
        f = (lo + hi) / 2; m1 = abs(trace(-0.08, thin(f)) / 0.08); m2 = abs(trace(-0.24, thin(f)) / 0.24)
        if m1 > m2: lo = f
        else: hi = f
    return lo * 100
add(('2026', 'Jan', '2026-01-23', 2), 'lens', 'The size of the images of an object, formed by a thin lens are equal when the object is placed at two different positions 8 cm and 24 cm from the lens. The focal length of the lens is ______ cm.', None, 16,
    lambda: round(_equal_size(), 3), ['Equal sizes from a convex lens: one virtual (inside f), one real (beyond f) with |m| = \\f{f}{|f − u|} equal.', 'f − 8 = 24 − f → f = 16 cm.'], 'lens', 2)
add(('2026', 'Apr', '2026-04-06', 1), 'wave', 'In interference experiment the path difference between two interfering waves at a point A on the screen is λ/3, where λ is the wavelength of these waves, and at another point B the path difference is λ/6. The ratio of intensities at points A and B is ______ .',
    ['3', '4', '1/3', '1/4'], 3, lambda: P4([3, 4, 1 / 3, 0.25], yd(1 / 3, 1) / yd(1 / 6, 1)), ['I ∝ cos^{2}\\f{φ}{2}: A has φ = \\f{2π}{3} → \\f{1}{4}; B has φ = \\f{π}{3} → \\f{3}{4}.', 'Ratio = \\f{1}{3}.'], 'wave', 1)
add(('2026', 'Apr', '2026-04-06', 1), 'refr', 'A spherical interface of radius R (centre of curvature in medium 2) separates two media of refractive indices 1 and 1.4 respectively. A point source is placed at a distance of 4R in front of the spherical interface. The magnitude of the magnification of point source image is ______ .',
    ['1.66', '2.33', '2.66', '1.33'], 1, lambda: P4([1.66, 2.33, 2.66, 1.33], abs(1.0 * lens_image(-4.0, [(0, 1.0, 1.0, 1.4)]) / (1.4 * -4.0)), 5e-3),
    ['\\f{1.4}{v} + \\f{1}{4R} = \\f{0.4}{R} → v = \\f{28R}{3}.', 'm = \\f{n_{1}v}{n_{2}u} = \\f{28R/3}{1.4 × (−4R)} ≈ −1.67.'], 'refr', 2)

# ---------- sheets 29–31
def _rot():
    lo, hi = 0.0, 90.0
    for _ in range(100):
        th = (lo + hi) / 2   # unpolarised I0 → I0/2 after the polariser; the solution turns the plane by θ; analyser parallel to polariser
        if _malus([0, th]) > 3 / 8: lo = th
        else: hi = th
    return lo
add(('2026', 'Apr', '2026-04-06', 1), 'wave', 'An unpolarized light of intensity I_{0} passes through polarizer and then through a certain optically active solution and finally it goes to analyser. If the angle between analyser and polariser is 0° and intensity of light emerged from analyser is \\f{3}{8}I_{0}, the angle of rotation of the light by the solution with respect to analyser is ______ degrees.', None, 30,
    lambda: round(_rot(), 4), ['After the polariser: \\f{I_{0}}{2}. The solution rotates the plane by θ; the analyser passes \\f{I_{0}}{2} cos^{2} θ.', 'cos^{2} θ = \\f{3}{4} → θ = 30°.'], 'wave', 1)
def _coat():
    for deg in [k / 100 for k in range(100, 9000)]:
        A = math.radians(deg); n = 1.6; r2 = A / 2   # minimum deviation: r1 = r2 = A/2
        if abs(math.sin(r2) - (n / 2) / n) < 1e-4: return deg
add(('2026', 'Jan', '2026-01-24', 1), 'refr', 'The exit surface of a prism with refractive index n is coated with a material having refractive index \\f{n}{2}. When this prism is set for minimum angle of deviation, it exactly meets the condition of critical angle. The prism angle is _____',
    ['60°', '15°', '30°', '45°'], 1, lambda: P4([60, 15, 30, 45], _coat(), 2e-3), ['At minimum deviation r_{2} = \\f{A}{2}.', 'Critical: sin\\f{A}{2} = \\f{n/2}{n} = \\f{1}{2} → A = 60°.'], 'refr', 2)
add(('2026', 'Jan', '2026-01-24', 1), 'lens', 'In a microscope of tube length 10 cm two convex lenses are arranged with focal length of 2 cm and 5 cm. Total magnification obtained with this system for normal adjustment is (5)^{k}. The value of k is ___.',
    ['2', '5', '3.5', '4'], 1, lambda: P4([2, 5, 3.5, 4], math.log(0.10 / 0.02 * 0.25 / 0.05, 5)), ['m = \\f{L}{f_{o}} × \\f{D}{f_{e}} = \\f{10}{2} × \\f{25}{5} = 25.', '25 = 5^{2} → k = 2.'], 'lens', 1)
def _brew23():
    n1, n2 = 2.0, 2 * math.sqrt(3)
    for k in range(1, 9000):
        i = math.radians(k / 100); r = snell(n1, n2, i)
        if abs(i + r - pi / 2) < 2e-4: return k / 100
add(('2026', 'Jan', '2026-01-24', 1), 'wave', 'An unpolarised light is incident at an interface of two dielectric media having refractive indices of 2 (incident medium) and 2√{3} (medium) respectively. To satisfy the condition that reflected and refracted rays are perpendicular to each other, the angle of incidence is _____ .',
    ['60°', '10°', '30°', '45°'], 1, lambda: P4([60, 10, 30, 45], _brew23(), 2e-3), ['Brewster: tan i = \\f{n_{2}}{n_{1}} = √{3}.', 'i = 60°.'], 'wave', 1)
def _halfA():
    for k in range(10001, 30000):
        n = k / 10000; A = pi / 3; dm = 2 * math.asin(min(1, n * math.sin(A / 2))) - A
        if dm >= A / 2: return n
add(('2026', 'Apr', '2026-04-06', 2), 'refr', 'Angle of minimum deviation is equal to the half of the angle of prism in an equilateral prism. The refractive index of the prism is ______.',
    ['1.5', '√{3}', '√{2}', '1.65'], 3, lambda: P4([1.5, math.sqrt(3), math.sqrt(2), 1.65], _halfA(), 2e-3), ['δ = 30°: n = \\f{sin 45°}{sin 30°}.', '= √{2}.'], 'refr', 1)
def _double():
    us = []
    for target in (-2, 2):
        lo, hi = (0.1, 1.0) if target < 0 else (1e-4, 0.1)
        for _ in range(100):
            u = (lo + hi) / 2; m = mirror_image(-u, -0.2) / u
            if target < 0: (lo, hi) = (u, hi) if m < target else (lo, u)
            else: (lo, hi) = (lo, u) if m > target else (u, hi)
        us.append((lo + hi) / 2)
    return abs(us[0] - us[1]) * 100
add(('2026', 'Apr', '2026-04-06', 2), 'mirror', 'A concave mirror of focal length 10 cm forms an image which is double the size of object when the object is placed at two different positions. The distance between the two positions of the object is ______ cm.', None, 10,
    lambda: round(_double(), 3), ['m = \\f{f}{f − u} = ±2 with f = −10 cm.', 'm = −2: u = −15 cm (real image); m = +2: u = −5 cm (virtual).', 'Separation = 10 cm.'], 'mirror', 2)
def _readings():
    data = [(25, 96), (30, 62), (35, 37), (45, 35), (50, 35)]; bad = []
    for k, (u, v) in enumerate(data, 1):
        vt = trace(-u / 100, thin(0.20)) * 100
        if abs(vt - v) / vt > 0.06: bad.append(k)
    return bad
add(('2026', 'Jan', '2026-01-24', 2), 'lens', 'Five persons P_{1}, P_{2}, P_{3}, P_{4} and P_{5} recorded object distance (u) and image distance (v) using same convex lens having power +5 D as (25, 96), (30, 62), (35, 37), (45, 35) and (50, 35) respectively (in cm). Identify correct statement',
    ['Readings recorded by all persons are correct', 'Readings recorded by P_{3} person are incorrect', 'Readings recorded by P_{3} and P_{2} persons are incorrect', 'Readings recorded by P_{4} and P_{5} persons are incorrect'], 2,
    lambda: pick([[], [3], [2, 3], [4, 5]], _readings()),
    ['f = 20 cm. Expected v = \\f{20u}{u − 20}: 100, 60, 46.7, 36, 33.3 cm.', 'All are within a few per cent except P_{3} (37 cm instead of about 47 cm).'], 'lens', 2)
def _front():
    lam, d, D = 6e-7, 2e-3, 10.0; y = d / 2
    p = math.hypot(D, y + d / 2) - math.hypot(D, y - d / 2); return yd(p, lam)
add(('2026', 'Jan', '2026-01-24', 2), 'wave', 'In the Young\'s double slit experiment the intensity produced by each one of the individual slits is I_{0}. The distance between two slits is 2 mm. The distance of screen from slits is 10 m. The wavelength of light is 6000 Å. The intensity of light on the screen in front of one of the slits is ______.',
    ['2I_{0}', 'I_{0}', '\\f{I_{0}}{2}', '4I_{0}'], 2, lambda: P4([2, 1, 0.5, 4], _front(), 2e-3),
    ['In front of a slit y = \\f{d}{2}: path difference \\f{yd}{D} = \\f{10^{−3} × 2 × 10^{−3}}{10} = 2 × 10^{−7} m = \\f{λ}{3}.', 'I = 2I_{0} + 2I_{0} cos 120° = I_{0}.'], 'wave', 2)
def _real3():
    lo, hi = 0.01, 1.0
    for _ in range(80):
        R = (lo + hi) / 2; a, b = R / 2 * 1.0001, 10.0
        for _ in range(100):
            u = (a + b) / 2
            if -mirror_image(-u, -R) / u > 3: a = u
            else: b = u
        u = (a + b) / 2; gap = abs(mirror_image(-u, -R)) - u
        if gap > 0.40: hi = R
        else: lo = R
    return -(lo + hi) / 4 * 100
add(('2026', 'Jan', '2026-01-24', 2), 'mirror', 'Distance between an object and three times magnified real image is 40 cm. The focal length of the mirror used is ______ cm.',
    ['−15/2', '−10', '−20', '−15'], 4, lambda: P4([-7.5, -10, -20, -15], _real3(), 2e-3),
    ['Real, 3×: v = 3u (both in front); |v| − |u| = 40 → u = −20, v = −60 cm.', '\\f{1}{f} = −\\f{1}{60} − \\f{1}{20} → f = −15 cm.'], 'mirror', 1)
add(('2026', 'Apr', '2026-04-08', 2), 'mirror', 'A thin biconvex lens is prepared from the glass (μ = 1.5) both curved surfaces of which have equal radii of 20 cm each. Left side surface of the lens is silvered from outside to make it reflecting. To have the position of image and object at the same place, the object should be placed, from the lens at a distance of ______ cm.',
    ['10', '12.5', '13', '13.5'], 1, lambda: P4([10, 12.5, 13, 13.5], self_image(0.2, -0.2, 1.0, 1.5) * 100, 2e-3),
    ['Silvered lens: P = 2P_{lens} + P_{mirror} = 2 × \\f{1}{20} + \\f{2}{20} = \\f{1}{5} per cm → f = 5 cm.', 'Object at its centre of curvature, 2f = 10 cm.'], 'mirror', 2)
add(('2026', 'Apr', '2026-04-08', 2), 'lens', 'Some distant star is to be observed by some telescope of diameter of objective lens a, at an angular resolution of 3.0 × 10^{−7} radian. If the wavelength of light from the star reaching the telescope is 500 nm, the minimum diameter of the objective lens of the telescope is ______ cm. (nearest integer)', None, 203,
    lambda: round(1.22 * 500e-9 / 3e-7 * 100), ['θ = \\f{1.22λ}{a}.', 'a = \\f{1.22 × 500 × 10^{−9}}{3 × 10^{−7}} = 2.03 m ≈ 203 cm.'], 'lens', 1)
def _r12():
    R2 = 0.2; P = 0.7 / R2   # plano-concave (n = 1.7) with radius R2
    lo, hi = 0.01, 5.0
    for _ in range(100):
        R1 = (lo + hi) / 2; Pc = 1 / thin_f(R1, -R2, 1.5)
        if Pc > P: lo = R1
        else: hi = R1
    return lo / R2
add(('2026', 'Jan', '2026-01-28', 1), 'lens', 'The magnitudes of power of a biconvex lens (refractive index 1.5) and that of a plano-concave lens (refractive index = 1.7) are same. If the curvature of planoconcave lens exactly matches with the curvature of back surface of the biconvex lens, then ratio of radius of curvature of front and back surface of the biconvex lens is _____',
    ['5 : 2', '5 : 12', '12 : 5', '2 : 5'], 1, lambda: P4([2.5, 5 / 12, 12 / 5, 0.4], _r12(), 2e-3),
    ['0.5(\\f{1}{R_{1}} + \\f{1}{R_{2}}) = \\f{0.7}{R_{2}} → \\f{0.5}{R_{1}} = \\f{0.2}{R_{2}}.', '\\f{R_{1}}{R_{2}} = \\f{5}{2}.'], 'lens', 2)
add(('2026', 'Jan', '2026-01-28', 1), 'wave', 'Statement I : A plane wave after passing through prism remains as plane wave but passing through small pin hole may become spherical wave. Statement II: The curvature of a spherical wave emerging from a slit will increase for increasing slit width.',
    ['Both Statement I and Statement II are false', 'Both Statement I and Statement II are true', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true'], 3,
    lambda: 3 if first_zero(2e-6, 5e-7) > first_zero(4e-6, 5e-7) else 0,
    ['A prism only tilts a plane wave; a pinhole diffracts it into a spreading (spherical) wave: I is true.', 'A wider slit diffracts LESS (spread ≈ λ/a), so the emerging wave is flatter: II is false.'], 'wave', 1)
add(('2026', 'Jan', '2026-01-28', 1), 'lens', 'A convex lens of refractive index 1.5 and focal length f = 18 cm is immersed in water. The difference in focal lengths of the given lens when it is in water and in air is α × f. The value of α is ______ . (refractive index of water = 4/3)', None, 3,
    lambda: round((thin_f(0.18, -0.18, 1.5, 4 / 3) - 0.18) / 0.18, 3), ['f_{w} = f × \\f{0.5}{1.5/(4/3) − 1} = 4f = 72 cm.', 'Difference = 3f → α = 3.'], 'lens', 1)
for _p in P: _p['t'] = _p['fam']
