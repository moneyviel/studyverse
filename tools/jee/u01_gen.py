"""Our own practice questions for Physics Unit 1, generated from templates that mirror each real JEE question.
Every item carries its raw parameters (p) so check2.py can re-solve it by a different method."""
import random, math
from fractions import Fraction as F
from dims import Q, DEFS, D, ONE
SUP = str.maketrans('', '')

def ordn(n):
    return f'{n}^{{' + ('th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')) + '}'
def nf(x, sig=4):
    """tidy number: no float noise, no trailing zeros"""
    if isinstance(x, F): x = float(x)
    if x == 0: return '0'
    s = f'{x:.{sig}g}'
    if 'e' in s:
        m, e = s.split('e'); return f'{m} × 10^{{{int(e)}}}'
    return s
def dfmt(d):
    parts = []
    for s, x in zip('MLTAK', d):
        if x == 0: continue
        e = '' if x == 1 else (str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}').replace('-', '−')
        parts.append(s + (f'^{{{e}}}' if e else ''))
    return '[' + (''.join(parts) if parts else 'M^{0}L^{0}T^{0}') + ']'

def mcq(rng, right, wrong, n=4):
    """right answer + distinct wrong ones (as display strings), shuffled; returns options, index"""
    seen, opts = {right}, [right]
    for w in wrong:
        if w not in seen and len(opts) < n: seen.add(w); opts.append(w)
    assert len(opts) == n, ('not enough distinct distractors', right, wrong)
    rng.shuffle(opts); return opts, opts.index(right)

# ------------------------------------------------------------------ least count: vernier
def g_vlc(rng):
    t = rng.choice(['basic', 'basic', 'k2', 'micro', 'inverse', 'nplus'])
    if t == 'basic':
        N = rng.choice([10, 20, 25, 50]); s = rng.choice([1, 0.5, 0.1, 2]) ; lc = F(str(s)) / N
        q = f'{N} divisions of the vernier scale of a vernier calliper coincide with {N - 1} divisions of its main scale. If one main scale division is {nf(s)} mm, the least count of the instrument is :'
        o, a = mcq(rng, nf(lc) + ' mm', [nf(F(str(s)) / (N - 1)) + ' mm', nf(lc * 10) + ' mm', nf(F(str(s)) * (N - 1) / N) + ' mm', nf(lc / 10) + ' mm'])
        sol = [f'{N} VSD = {N - 1} MSD → 1 VSD = \\f{{{N - 1}}}{{{N}}} MSD.', f'LC = 1 MSD − 1 VSD = \\f{{1}}{{{N}}} MSD = \\f{{{nf(s)}}}{{{N}}} = {nf(lc)} mm.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='vlc', N=N, k=1, s=s), ans=float(lc))
    if t == 'k2':
        N = rng.choice([20, 25, 40, 50]); k = rng.choice([2, 3]) if N >= 25 else 2; s = rng.choice([0.05, 0.1, 0.5, 1]); lc = F(str(s)) * k / N
        q = f'In a vernier calliper, {N} vernier scale divisions are equal to {N - k} main scale divisions. If one main scale division is {nf(s)} mm, the least count of the vernier calliper is ______ mm.'
        o, a = mcq(rng, nf(lc), [nf(F(str(s)) / N), nf(F(str(s)) / (N - k)), nf(lc * 10), nf(F(str(s)) * (N - k) / N)])
        sol = [f'1 VSD = \\f{{{N - k}}}{{{N}}} MSD = {nf(F(str(s)) * (N - k) / N)} mm.', f'LC = 1 MSD − 1 VSD = {nf(s)} − {nf(F(str(s)) * (N - k) / N)} = {nf(lc)} mm.', f'Trap: it is not MSD/{N}, because {N} VSD match {N - k} (not {N - 1}) MSD.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='vlc', N=N, k=k, s=s), ans=float(lc))
    if t == 'micro':
        P = rng.choice([200, 300, 400, 500]); Lc = rng.choice([10, 15, 20, 25]); N = rng.choice([20, 25, 50]); s = F(Lc, P); lc = s / N
        q = f'A travelling microscope has a main scale in which {P} equal divisions measure {Lc} cm. Its vernier has {N} divisions equal to {N - 1} main scale divisions. The least count of the microscope is (in cm) :'
        o, a = mcq(rng, nf(lc), [nf(s), nf(lc * 10), nf(lc / 2), nf(s / (N - 1))])
        sol = [f'1 MSD = \\f{{{Lc}}}{{{P}}} = {nf(s)} cm.', f'LC = \\f{{1 MSD}}{{{N}}} = \\f{{{nf(s)}}}{{{N}}} = {nf(lc)} cm.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='vlc', N=N, k=1, s=float(s)), ans=float(lc))
    if t == 'inverse':
        N = rng.choice([10, 20, 25, 50]); s = rng.choice([0.5, 1, 2]); lc = F(str(s)) / N
        q = f'A vernier callipers has {N} divisions on the vernier scale which coincide with {N - 1} divisions of the main scale. Its least count is {nf(lc)} mm. One main scale division is equal to ______ mm.'
        o, a = mcq(rng, nf(s), [nf(lc * (N - 1)), nf(F(str(s)) * 2) if s != 1 else '5', nf(F(str(s)) / 2), nf(lc * 100)])
        sol = [f'LC = \\f{{MSD}}{{{N}}} (since {N} VSD = {N - 1} MSD).', f'MSD = {N} × {nf(lc)} = {nf(s)} mm.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='vlc_inv', N=N, k=1, lc=float(lc)), ans=float(s))
    n = rng.choice([9, 19, 24, 49]); m = rng.choice([1, 0.5, 2]); lc = F(str(m)) / (n + 1)
    q = f'One main scale division of a vernier calliper is {nf(m)} mm. If the {ordn(n)} division of the main scale coincides with the {ordn(n + 1)} division of the vernier scale, the least count is :'
    o, a = mcq(rng, nf(lc) + ' mm', [nf(F(str(m)) / n) + ' mm', nf(F(str(m)) * n / (n + 1)) + ' mm', nf(lc / 10) + ' mm', nf(F(str(m)) / (n * (n + 1))) + ' mm'])
    sol = [f'{n + 1} VSD = {n} MSD → 1 VSD = \\f{{{n}}}{{{n + 1}}} × {nf(m)} mm.', f'LC = {nf(m)} − \\f{{{n}}}{{{n + 1}}} × {nf(m)} = \\f{{{nf(m)}}}{{{n + 1}}} = {nf(lc)} mm.']
    return dict(q=q, o=o, a=a, sol=sol, p=dict(t='vlc', N=n + 1, k=1, s=m), ans=float(lc))

# ------------------------------------------------------------------ vernier zero error & reading
def g_vze(rng):
    t = rng.choice(['find', 'read', 'read', 'neg', 'msd'])
    lc = rng.choice([F(1, 10), F(1, 20), F(1, 50)])  # mm
    if t == 'find':
        z = rng.randint(2, 9); ze = z * lc
        q = f'When both jaws of a vernier calliper (least count {nf(lc)} mm) touch each other, the zero of the vernier scale lies to the right of the zero of the main scale and the {ordn(z)} vernier division coincides with a main scale division. The zero error is :'
        o, a = mcq(rng, f'+{nf(ze)} mm', [f'−{nf(ze)} mm', f'+{nf(ze * 10)} mm', f'−{nf(ze * 10)} mm', f'+{nf(lc)} mm'])
        sol = ['Vernier zero to the RIGHT of main zero → the instrument reads more than zero → positive zero error.', f'Size = {z} × LC = {z} × {nf(lc)} = {nf(ze)} mm.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='vze', lc=float(lc), z=z, side=1), ans=float(ze))
    if t in ('read', 'msd'):
        z = rng.randint(2, 7); M = rng.randint(10, 60); v = rng.randint(z + 1, 18 if lc == F(1, 20) else (9 if lc == F(1, 10) else 45))
        obs = M + v * lc; cor = obs - z * lc
        q = f'A vernier calliper has least count {nf(lc)} mm. With the jaws closed, its vernier zero is to the right of the main zero and the {ordn(z)} vernier division coincides. While measuring a rod, the main scale reading is {M} mm and the {ordn(v)} vernier division coincides. The correct length of the rod is ______ mm.'
        o, a = mcq(rng, nf(cor), [nf(obs), nf(obs + z * lc), nf(M + (v - z) * lc * 10), nf(cor - lc)])
        sol = [f'Zero error = +{z} × {nf(lc)} = +{nf(z * lc)} mm (vernier zero to the right).', f'Observed = MSR + VSR × LC = {M} + {v} × {nf(lc)} = {nf(obs)} mm.', f'Correct = observed − zero error = {nf(obs)} − {nf(z * lc)} = {nf(cor)} mm.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='vread', lc=float(lc), z=z, side=1, M=M, v=v), ans=float(cor))
    ze = rng.randint(2, 8) * lc; M = rng.randint(10, 60); v = rng.randint(1, 9)
    obs = M + v * lc; cor = obs + ze
    q = f'A vernier calliper (least count {nf(lc)} mm) has a negative zero error of {nf(ze)} mm. The main scale reading for a cylinder is {M} mm and the {ordn(v)} vernier division coincides. The correct diameter is ______ mm.'
    o, a = mcq(rng, nf(cor), [nf(obs), nf(obs - ze), nf(cor + lc), nf(M + ze)])
    sol = [f'Observed = {M} + {v} × {nf(lc)} = {nf(obs)} mm.', 'Correct = observed − (zero error) and here zero error = −' + nf(ze) + ' mm.', f'Correct = {nf(obs)} + {nf(ze)} = {nf(cor)} mm.']
    return dict(q=q, o=o, a=a, sol=sol, p=dict(t='vneg', lc=float(lc), ze=float(ze), M=M, v=v), ans=float(cor))

def g_vrd(rng):
    lc = F(1, 10); D_ = rng.randint(15, 30); v = rng.randint(1, 9); d = D_ + v * lc  # mm
    shape = rng.choice(['sphere', 'cyl'])
    if shape == 'sphere':
        rho = rng.choice([2.0, 2.5, 7.8, 8.9, 1.2]); V = 4 / 3 * math.pi * (float(d) / 20) ** 3; m = round(rho * V, 3); dens = m / V
        q = f'The diameter of a solid sphere is measured with a vernier calliper whose 10 vernier divisions equal 9 main scale divisions of 1 mm each. The main scale reading is {nf(D_ / 10)} cm and the {ordn(v)} vernier division coincides. If the mass of the sphere is {nf(m, 5)} g, its density is (in g/cm^{{3}}) :'
        right = f'{dens:.1f}'; wrong = [f'{dens * 8:.1f}', f'{m / (4 / 3 * math.pi * (D_ / 20) ** 3):.2f}', f'{dens / 2:.1f}', f'{dens * 1.5:.1f}', f'{dens + 0.6:.1f}']
        o, a = mcq(rng, right, wrong)
        sol = ['LC = 1 MSD − 1 VSD = 1 − 0.9 = 0.1 mm.', f'd = {D_} mm + {v} × 0.1 mm = {nf(d)} mm = {nf(d / 10)} cm → r = {nf(d / 20)} cm.', f'V = \\f{{4}}{{3}}πr^{{3}} ≈ {V:.3f} cm^{{3}}.', f'ρ = \\f{{{nf(m, 5)}}}{{{V:.3f}}} ≈ {right} g/cm^{{3}}.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='vsph', d=float(d), m=m), ans=float(right))
    h = rng.randint(30, 80); V = math.pi * (float(d) / 20) ** 2 * (h / 10)
    q = f'The diameter of a cylinder of length {nf(h / 10)} cm is measured with a vernier calliper of least count 0.1 mm: main scale reading {D_} mm, {ordn(v)} vernier division coinciding. Its volume is approximately (in cm^{{3}}) :'
    right = f'{V:.2f}'; o, a = mcq(rng, right, [f'{V * 4:.2f}', f'{math.pi * (D_ / 20) ** 2 * h / 10:.2f}', f'{V / 2:.2f}', f'{V * 1.1:.2f}'])
    sol = [f'd = {D_} + {v} × 0.1 = {nf(d)} mm = {nf(d / 10)} cm, r = {nf(d / 20)} cm.', f'V = πr^{{2}}h = π × ({nf(d / 20)})^{{2}} × {nf(h / 10)} ≈ {right} cm^{{3}}.']
    return dict(q=q, o=o, a=a, sol=sol, p=dict(t='vcyl', d=float(d), h=h), ans=float(right))

# ------------------------------------------------------------------ screw gauge
def g_sgr(rng):
    p = rng.choice([0.5, 1.0]); N = rng.choice([50, 100]); lc = F(str(p)) / N; M = rng.randint(1, 8) if p == 1 else rng.choice([1, 1.5, 2, 2.5, 3, 3.5]); c = rng.randint(5, N - 5)
    r = F(str(M)) + c * lc
    mult = rng.choice([20, 50, 100])
    if (r * mult).denominator == 1:
        q = f'While measuring the diameter of a wire with a screw gauge of pitch {nf(p)} mm and {N} circular divisions, the main scale reading is {nf(M)} mm and the circular scale reading is {c}. The diameter is \\f{{x}}{{{mult}}} mm. The value of x is :'
        o, a = mcq(rng, str(int(r * mult)), [str(int((F(str(M)) + c * lc * 10) * mult)), str(int(c * lc * mult) or 7), str(int(r * mult) + mult // 10 or 1), str(int(r * mult) * 2)])
        sol = [f'LC = \\f{{{nf(p)}}}{{{N}}} = {nf(lc)} mm.', f'Reading = {nf(M)} + {c} × {nf(lc)} = {nf(r)} mm.', f'x = {nf(r)} × {mult} = {int(r * mult)}.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='sgr', p=p, N=N, M=M, c=c, mult=mult), ans=int(r * mult))
    q = f'A screw gauge has pitch {nf(p)} mm and {N} divisions on its circular scale (no zero error). The main scale reading is {nf(M)} mm and the {ordn(c)} circular division is on the reference line. The reading is :'
    o, a = mcq(rng, nf(r) + ' mm', [nf(F(str(M)) + c * lc * 10) + ' mm', nf(F(str(M)) + F(c, 100)) + ' mm' if N != 100 else nf(r + F(str(p))) + ' mm', nf(c * lc) + ' mm', nf(r - lc * 5) + ' mm'])
    sol = [f'LC = {nf(p)}/{N} = {nf(lc)} mm.', f'Reading = {nf(M)} + {c} × {nf(lc)} = {nf(r)} mm.']
    return dict(q=q, o=o, a=a, sol=sol, p=dict(t='sgr', p=p, N=N, M=M, c=c, mult=1), ans=float(r))

def g_sgz(rng):
    p = rng.choice([0.5, 1.0, 0.1]); N = rng.choice([50, 100]); lc = F(str(p)) / N
    z = rng.randint(2, 8); below = rng.random() < 0.5; ze = z * lc * (1 if below else -1)
    M = rng.choice([1, 2, 3, 4, 5]); c = rng.randint(10, N - 10); obs = M + c * lc; cor = obs - ze
    q = (f'A screw gauge has {N} divisions on its circular scale and pitch {nf(p)} mm. With the studs in contact, the zero of the circular scale lies {z} divisions {"below" if below else "above"} the reference line. '
         f'For a wire, {M} mm of the linear scale is visible and the {ordn(c)} circular division is on the reference line. The correct diameter is :')
    o, a = mcq(rng, nf(cor) + ' mm', [nf(obs) + ' mm', nf(obs + ze) + ' mm', nf(cor + 10 * lc) + ' mm', nf(cor - 10 * lc) + ' mm'])
    sol = [f'LC = \\f{{{nf(p)}}}{{{N}}} = {nf(lc)} mm.',
           ('Circular zero BELOW the reference line → the gauge already reads ahead → positive zero error ' if below else 'Circular zero ABOVE the reference line → the gauge has not reached zero → negative zero error ') + f'= {"+" if below else "−"}{z} × {nf(lc)} = {nf(ze)} mm.',
           f'Observed = {M} + {c} × {nf(lc)} = {nf(obs)} mm.', f'Correct = observed − zero error = {nf(obs)} − ({nf(ze)}) = {nf(cor)} mm.']
    return dict(q=q, o=o, a=a, sol=sol, p=dict(t='sgz', p=p, N=N, z=z, below=below, M=M, c=c), ans=float(cor))

def g_sglc(rng):
    t = rng.choice(['rot', 'change', 'change'])
    if t == 'rot':
        n = rng.choice([2, 4, 5, 10]); pitch = rng.choice([0.5, 1.0, 0.25]); dist = pitch * n; N = rng.choice([50, 100, 25])
        lc = F(str(pitch)) / N
        q = f'When the circular scale of a screw gauge is given {n} complete rotations, the spindle moves {nf(dist)} mm. If the circular scale has {N} divisions, the least count is ______ × 10^{{−3}} mm.'
        return dict(q=q, o=None, a=int(lc * 1000), sol=[f'Pitch = \\f{{{nf(dist)}}}{{{n}}} = {nf(pitch)} mm.', f'LC = \\f{{{nf(pitch)}}}{{{N}}} = {nf(lc)} mm = {int(lc * 1000)} × 10^{{−3}} mm.'], p=dict(t='sglc', pitch=pitch, N=N), ans=int(lc * 1000)) if (lc * 1000).denominator == 1 else g_sglc(rng)
    base = rng.choice([F(1, 100), F(1, 200), F(1, 50)]); up = rng.choice([25, 50, 75, 100, 150]); down = rng.choice([20, 25, 50, 75])
    new = base * F(100 + up, 100) / F(100 - down, 100)
    if (new * 1000).denominator != 1: return g_sglc(rng)
    q = f'The least count of a screw gauge is {nf(base)} mm. If its pitch is increased by {up}% and the number of circular scale divisions is reduced by {down}%, the new least count will be ______ × 10^{{−3}} mm.'
    return dict(q=q, o=None, a=int(new * 1000), sol=['LC = \\f{pitch}{N}.', f'New LC = \\f{{{nf(F(100 + up, 100))} × pitch}}{{{nf(F(100 - down, 100))} × N}} = {nf(F(100 + up, 100 - down))} × {nf(base)} = {nf(new)} mm.', f'= {int(new * 1000)} × 10^{{−3}} mm.'],
                p=dict(t='sglc2', base=float(base), up=up, down=down), ans=int(new * 1000))

# ------------------------------------------------------------------ errors
VARS = 'abcdpqrsxyz'
def g_perr(rng, want=None):
    t = want or rng.choice(['pow', 'pow', 'powint', 'dens', 'ohm', 'shm', 'young', 'sphere', 'exp'])
    if t in ('pow', 'powint'):
        n = rng.choice([3, 3, 4]); vs = rng.sample('abcdpqrs', n); pw = [rng.choice([1, 2, 3, F(1, 2), F(3, 2), 4]) for _ in vs]
        e = [rng.choice([0.5, 1, 1.5, 2, 3, 4]) for _ in vs]; top = [i for i in range(n) if i < (n + 1) // 2]
        tot = sum(F(pw[i]) * F(str(e[i])) for i in range(n))
        if t == 'powint' and tot.denominator != 1: return g_perr(rng, want)
        def term(i):
            p_ = pw[i]; v = vs[i]
            return f'√{{{v}}}' if p_ == F(1, 2) else (f'{v}^{{3/2}}' if p_ == F(3, 2) else (v if p_ == 1 else f'{v}^{{{p_}}}'))
        num = ''.join(term(i) for i in top); den = ''.join(term(i) for i in range(n) if i not in top)
        q = f'A quantity X = \\f{{{num}}}{{{den}}}. The percentage errors in {", ".join(vs[:-1])} and {vs[-1]} are {", ".join(nf(x) + "%" for x in e[:-1])} and {nf(e[-1])}% respectively. The maximum percentage error in X is ' + ('______ %.' if t == 'powint' else ':')
        sol = ['For a product or quotient of powers, the maximum % error = Σ |power| × (% error).', ' + '.join(f'{nf(F(pw[i]))} × {nf(e[i])}' for i in range(n)) + f' = {nf(tot)}%.', 'Errors never cancel: a quantity in the denominator still ADDS its error.']
        if t == 'powint': return dict(q=q, o=None, a=int(tot), sol=sol, p=dict(t='pow', pw=[str(F(x)) for x in pw], e=e), ans=int(tot))
        wrong_sub = sum(F(pw[i]) * F(str(e[i])) * (1 if i in top else -1) for i in range(n))
        o, a = mcq(rng, nf(tot) + '%', [nf(abs(wrong_sub)) + '%', nf(sum(F(str(x)) for x in e)) + '%', nf(tot + 1) + '%', nf(tot * 2) + '%', nf(tot - F(1, 2)) + '%'])
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='pow', pw=[str(F(x)) for x in pw], e=e), ans=float(tot))
    if t == 'dens':
        m, dm = rng.choice([(0.60, 0.003), (2.40, 0.012), (12.5, 0.05), (80.0, 0.2)]); r, dr = rng.choice([(0.50, 0.01), (0.25, 0.005), (1.00, 0.01), (0.40, 0.004)]); l, dl = rng.choice([(10.00, 0.05), (5.00, 0.05), (20.0, 0.1), (8.00, 0.04)])
        tot = 100 * (dm / m + 2 * dr / r + dl / l)
        q = f'The density of a wire is found from mass m = ({nf(m)} ± {nf(dm)}) g, radius r = ({nf(r)} ± {nf(dr)}) cm and length l = ({nf(l)} ± {nf(dl)}) cm. The maximum percentage error in density is :'
        o, a = mcq(rng, f'{tot:.2f}%', [f'{100 * (dm / m + dr / r + dl / l):.2f}%', f'{100 * (dm / m + 3 * dr / r + dl / l):.2f}%', f'{100 * abs(dm / m - 2 * dr / r - dl / l):.2f}%', f'{tot * 2:.2f}%'])
        sol = ['ρ = \\f{m}{πr^{2}l} → \\f{Δρ}{ρ} = \\f{Δm}{m} + 2\\f{Δr}{r} + \\f{Δl}{l}.', f'= {100 * dm / m:.2f}% + 2 × {100 * dr / r:.2f}% + {100 * dl / l:.2f}% = {tot:.2f}%.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='dens', m=m, dm=dm, r=r, dr=dr, l=l, dl=dl), ans=round(tot, 2))
    if t == 'ohm':
        V, dV = rng.choice([(10, 0.5), (12, 0.2), (20, 0.5), (6, 0.1), (15, 0.3)]); I, dI = rng.choice([(5, 0.2), (2, 0.05), (4, 0.1), (3, 0.06), (0.5, 0.01)])
        R = V / I; dR = R * (dV / V + dI / I)
        q = f'In an Ohm\'s law experiment the voltmeter reads {nf(V)} V and the ammeter reads {nf(I)} A. The least counts of the voltmeter and ammeter are {nf(dV * 1000)} mV and {nf(dI * 1000)} mA. The maximum error in the resistance is ______ Ω.'
        o, a = mcq(rng, nf(round(dR, 4)), [nf(round(R * abs(dV / V - dI / I), 4)), nf(round(dV / dI, 4)), nf(round(dR * 2, 4)), nf(round(dV / I, 4)), nf(round(dR / 2, 4))])
        sol = [f'R = \\f{{{nf(V)}}}{{{nf(I)}}} = {nf(R)} Ω.', f'\\f{{ΔR}}{{R}} = \\f{{{nf(dV)}}}{{{nf(V)}}} + \\f{{{nf(dI)}}}{{{nf(I)}}} = {nf(dV / V + dI / I)}.', f'ΔR = {nf(dV / V + dI / I)} × {nf(R)} = {nf(round(dR, 4))} Ω.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='ohm', V=V, dV=dV, I=I, dI=dI), ans=round(dR, 4))
    if t == 'shm':
        m, dm = rng.choice([(10, 0.01), (50, 0.05), (100, 0.1), (20, 0.02)]); n = rng.choice([20, 25, 50, 40]); tt = rng.choice([40, 50, 60, 80, 100]); res = rng.choice([1, 2, 0.5])
        tot = 100 * (dm / m + 2 * res / tt)
        q = f'For a spring–mass system T = 2π√{{\\f{{m}}{{k}}}}. The mass is {nf(m)} g measured to {nf(dm * 1000)} mg, and the time for {n} oscillations is {tt} s on a watch of {nf(res)} s resolution. The percentage error in k is about :'
        o, a = mcq(rng, f'{tot:.2f}%', [f'{100 * (dm / m + res / tt):.2f}%', f'{100 * (2 * res / tt):.2f}%' if dm / m > 0.002 else f'{100 * (dm / m + 3 * res / tt):.2f}%', f'{tot * 2:.2f}%'])
        sol = ['k = \\f{4π^{2}m}{T^{2}} → \\f{Δk}{k} = \\f{Δm}{m} + 2\\f{ΔT}{T}.', f'\\f{{ΔT}}{{T}} = \\f{{{nf(res)}}}{{{tt}}} (timing {n} oscillations gives the same fraction for one period).', f'= {100 * dm / m:.2f}% + 2 × {100 * res / tt:.2f}% = {tot:.2f}%.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='shm', m=m, dm=dm, tt=tt, res=res), ans=round(tot, 2))
    if t == 'young':
        M = rng.choice([200, 400, 500, 1000]); dM = rng.choice([2, 5, 10]); l = rng.choice([1, 2, 4, 0.5]); dl = rng.choice([0.01, 0.02, 0.005])
        tot = 100 * (dM / M + dl / l)
        q = f'Young\'s modulus is found from Y ∝ \\f{{M}}{{l}} using a load–extension graph whose smallest divisions are {dM} g (load) and {nf(dl)} cm (extension). If M = {M} g and l = {nf(l)} cm, the percentage error in Y is :'
        o, a = mcq(rng, nf(round(tot, 3)) + '%', [nf(round(abs(100 * (dM / M - dl / l)), 3)) + '%' if abs(dM / M - dl / l) > 1e-9 else nf(round(tot / 4, 3)) + '%', nf(round(tot / 10, 3)) + '%', nf(round(tot * 2, 3)) + '%', nf(round(tot * 10, 3)) + '%'])
        sol = ['\\f{ΔY}{Y} = \\f{ΔM}{M} + \\f{Δl}{l} (take one smallest division as the error).', f'= \\f{{{dM}}}{{{M}}} + \\f{{{nf(dl)}}}{{{nf(l)}}} = {nf(round(tot / 100, 5))} → {nf(round(tot, 3))}%.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='young', M=M, dM=dM, l=l, dl=dl), ans=round(tot, 3))
    if t == 'sphere':
        which = rng.choice([('volume of a sphere', 'diameter', 3), ('surface area of a sphere', 'radius', 2), ('kinetic energy ½mv^{2} (mass exact)', 'speed', 2), ('volume of a cube', 'side', 3), ('area of a circle', 'diameter', 2)])
        e = rng.choice([0.5, 1, 1.5, 2, 2.5, 3]); tot = which[2] * e
        q = f'If there is a {nf(e)}% error in measuring the {which[1]}, the percentage error in the {which[0]} is ______.'
        o, a = mcq(rng, nf(tot), [nf(e), nf(tot * 2), nf(tot + e), nf(e / which[2]), nf(tot - e)])
        sol = [f'The quantity ∝ ({which[1]})^{{{which[2]}}}.', f'% error = {which[2]} × {nf(e)}% = {nf(tot)}%.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='pow', pw=[str(which[2])], e=[e]), ans=tot)
    n = rng.choice([2, 3, 4]); beta = rng.choice([0.1, 0.2, 0.3, 0.5]); t0 = rng.choice([2, 4, 5, 10]); ea = rng.choice([0.5, 1, 1.2, 1.5]); et = rng.choice([1, 1.6, 2, 2.5])
    tot = n * ea + beta * t0 * et
    q = f'A quantity varies as E = α^{{{n}}}e^{{−βt}} with β = {nf(beta)} s^{{−1}}. The errors in α and t are {nf(ea)}% and {nf(et)}%. At t = {t0} s, the maximum percentage error in E is :'
    o, a = mcq(rng, nf(round(tot, 4)) + '%', [nf(round(n * ea + et, 4)) + '%', nf(round(n * ea, 4)) + '%', nf(round(n * ea + beta * et, 4)) + '%', nf(round(tot + n * ea, 4)) + '%'])
    sol = [f'ln E = {n} ln α − βt → \\f{{ΔE}}{{E}} = {n}\\f{{Δα}}{{α}} + βΔt.', f'Δt = {nf(et)}% of {t0} s = {nf(et * t0 / 100)} s → βΔt = {nf(beta * et * t0 / 100)} = {nf(round(beta * et * t0, 4))}%.', f'Total = {n} × {nf(ea)} + {nf(round(beta * t0 * et, 4))} = {nf(round(tot, 4))}%.']
    return dict(q=q, o=o, a=a, sol=sol, p=dict(t='exp', n=n, beta=beta, t0=t0, ea=ea, et=et), ans=round(tot, 4))

def g_aerr(rng):
    t = rng.choice(['par', 'ser', 'diff'])
    a1, d1 = rng.choice([(10, 0.2), (12, 0.1), (25, 0.5), (40, 0.4), (6, 0.1)]); a2, d2 = rng.choice([(20, 0.3), (18, 0.2), (15, 0.3), (30, 0.2), (14, 0.4)])
    if t == 'diff' and a2 >= a1: a1, a2, d1, d2 = a2 + a1, a2, d1, d2
    S = a1 + a2 if t != 'diff' else a1 - a2; dS = d1 + d2; pct = 100 * dS / S
    names = {'par': ('two springs of constants', 'N/m', 'are joined in parallel. The percentage error in the equivalent spring constant is'),
             'ser': ('two resistors of', 'Ω', 'are joined in series. The percentage error in the equivalent resistance is'),
             'diff': ('two temperatures', '°C', 'are recorded. The percentage error in their difference is')}[t]
    q = f'{names[0].capitalize()} ({nf(a1)} ± {nf(d1)}) {names[1]} and ({nf(a2)} ± {nf(d2)}) {names[1]} {names[2]} :'
    o, a = mcq(rng, f'{pct:.2f}%', [f'{100 * (d1 / a1 + d2 / a2):.2f}%', f'{100 * abs(d1 - d2) / S:.2f}%', f'{100 * dS / (a1 + a2 if t == "diff" else abs(a1 - a2) or 1):.2f}%', f'{pct * 2:.2f}%'])
    sol = [('Sum' if t != 'diff' else 'Difference') + f' = {nf(S)} {names[1]}.', f'For a sum OR a difference the absolute errors add: Δ = {nf(d1)} + {nf(d2)} = {nf(dS)}.', f'% error = \\f{{{nf(dS)}}}{{{nf(S)}}} × 100 = {pct:.2f}%.'] + (['A difference of nearly equal numbers has a LARGE % error — a classic trap.'] if t == 'diff' else [])
    return dict(q=q, o=o, a=a, sol=sol, p=dict(t='aerr', a1=a1, d1=d1, a2=a2, d2=d2, diff=t == 'diff'), ans=round(pct, 2))

# ------------------------------------------------------------------ significant figures
def sigfigs(s):
    s = s.lstrip('+-')
    if 'e' in s.lower(): s = s.lower().split('e')[0]
    if '.' in s:
        d = s.replace('.', '').lstrip('0'); return len(d)
    return len(s.strip('0').rstrip('0')) if s.strip('0') else 1
def g_sfc(rng):
    t = rng.choice(['count', 'match'])
    def num():
        k = rng.choice(['int0', 'dec', 'lead', 'trail', 'sci'])
        if k == 'int0': return rng.choice(['1001', '30.02', '4006', '100.5', '2.0805'])
        if k == 'dec': return rng.choice(['0.0560', '2.300', '0.0010010', '45.00', '6.020'])
        if k == 'lead': return rng.choice(['0.00045', '0.0203', '0.70', '010.1', '0.0300'])
        if k == 'trail': return rng.choice(['100.100', '1.000', '250.0', '7.50', '3.0040'])
        return rng.choice(['6.02 × 10^{23}', '1.60 × 10^{−19}', '3.0 × 10^{8}', '9.110 × 10^{−31}'])
    def sf(x): return sigfigs(x.split(' × ')[0])
    if t == 'count':
        x = num(); n = sf(x)
        q = f'The number of significant figures in {x} is :'
        o, a = mcq(rng, str(n), [str(n + 1), str(n - 1) if n > 1 else str(n + 3), str(n + 2), str(len(x.split(" × ")[0].replace(".", "")))])
        sol = ['Rules: non-zero digits count; zeros between them count; leading zeros never count; trailing zeros count only when there is a decimal point.', f'{x} → {n} significant figures.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='sfc', x=x), ans=n)
    xs = []
    while len(xs) < 4:
        x = num()
        if sf(x) not in [sf(y) for y in xs]: xs.append(x)
    ns = [sf(x) for x in xs]; L = 'ABCD'
    right = ', '.join(f'{L[i]}–{ns[i]}' for i in range(4))
    wrongs = []
    for _ in range(20):
        pm = ns[:]; rng.shuffle(pm)
        w = ', '.join(f'{L[i]}–{pm[i]}' for i in range(4))
        if w != right: wrongs.append(w)
    q = 'Match each number with its count of significant figures: ' + '; '.join(f'({L[i]}) {xs[i]}' for i in range(4)) + '.'
    o, a = mcq(rng, right, wrongs)
    sol = [f'{xs[i]} → {ns[i]}' for i in range(4)] + ['Leading zeros never count; trailing zeros count only with a decimal point.']
    return dict(q=q, o=o, a=a, sol=sol, p=dict(t='sfm', xs=xs), ans=right)

def sfmt(x, n):
    """x rounded to n significant figures, trailing zeros kept (plain notation)"""
    from decimal import Decimal, ROUND_HALF_EVEN
    d = Decimal(x.numerator) / Decimal(x.denominator) if isinstance(x, F) else Decimal(str(x))
    e = d.adjusted(); q = Decimal(1).scaleb(e - n + 1)
    r = d.quantize(q, rounding=ROUND_HALF_EVEN)
    return format(r, 'f')
def tie(x, k):
    """True when x sits exactly halfway at k decimals — textbooks disagree on these, so we never generate them"""
    y = F(x) * 10 ** k; return (y - math.floor(y)) == F(1, 2)
def rdp(x, k):
    from decimal import Decimal, ROUND_HALF_UP
    x = F(x); d = Decimal(x.numerator) / Decimal(x.denominator)
    return format(d.quantize(Decimal(1).scaleb(-k), rounding=ROUND_HALF_UP), 'f')
def dp(s): return len(s.split('.')[1]) if '.' in s else 0
def g_sfa(rng):
    t = rng.choice(['add', 'add', 'mul', 'mean'])
    if t == 'add':
        xs = [rng.choice(['435.42', '52.01', '12.6', '3.172', '0.125', '201.3', '7.25', '18.0', '0.0045', '96.47'][i::3]) for i in range(3)]
        xs = list(dict.fromkeys(xs))
        while len(xs) < 3: xs.append(rng.choice(['1.2', '45.67', '0.123']))
        k = min(dp(x) for x in xs); s = sum(F(x) for x in xs)
        if tie(s, k): return g_sfa(rng)
        R = rdp(s, k); unit = rng.choice(['g', 'm', 'cm', 's'])
        q = f'Keeping significant figures in view, the sum of {", ".join(x + " " + unit for x in xs[:-1])} and {xs[-1]} {unit} is :'
        o, a = mcq(rng, f'{R} {unit}', [f'{float(s):.{max(dp(x) for x in xs)}f} {unit}', f'{round(float(s), k + 1):.{k + 1}f} {unit}', f'{round(float(s)):.0f} {unit}' if k else f'{round(float(s), -1):.0f} {unit}', f'{float(s):g} {unit}', f'{float(s):.{k + 2}f} {unit}', f'{round(float(s), k) + 10 ** -k:.{k}f} {unit}', f'{round(float(s), k) - 10 ** -k:.{k}f} {unit}'])
        sol = [f'Raw sum = {rdp(s, max(dp(x) for x in xs))} {unit}.', f'In addition/subtraction keep the fewest DECIMAL PLACES present: {k}.', f'Answer = {R} {unit}.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='sfadd', xs=xs), ans=R)
    if t == 'mul':
        a_, b_ = rng.choice([('4.237', '2.51'), ('12.0', '3.142'), ('0.0250', '16.42'), ('5.62', '0.31'), ('2.000', '1.5'), ('3.6', '2.45'), ('7.04', '1.30')])
        n = min(sigfigs(a_), sigfigs(b_)); prod = F(a_) * F(b_)
        R = sfmt(prod, n)
        if sfmt(prod, n) != sfmt(prod + F(1, 10 ** 12), n): return g_sfa(rng)
        q = f'A rectangle has sides {a_} m and {b_} m. Its area, written with the correct number of significant figures, is :'
        o, a = mcq(rng, f'{R} m^{{2}}', [f'{sfmt(prod, k)} m^{{2}}' for k in (n + 1, n + 2, n - 1, n + 3) if k >= 1])
        sol = [f'Product = {float(prod):g}.', f'In multiplication/division keep the fewest SIGNIFICANT FIGURES: {a_} has {sigfigs(a_)}, {b_} has {sigfigs(b_)} → {n}.', f'Area = {R} m^{{2}}.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='sfmul', a=a_, b=b_), ans=R)
    xs = rng.choice([['4.62', '4.632', '4.6', '4.64'], ['2.31', '2.3', '2.334', '2.32'], ['10.4', '10.42', '10.38', '10.5'], ['1.25', '1.2', '1.27', '1.24']])
    k = min(dp(x) for x in xs); m = sum(F(x) for x in xs) / len(xs)
    if tie(m, k): return g_sfa(rng)
    R = rdp(m, k)
    q = f'Readings of a time period with different clocks are {", ".join(x + " s" for x in xs)}. Their mean, written with correct significant figures, is :'
    o, a = mcq(rng, R + ' s', [f'{float(m):.3f} s', f'{float(m):.2f} s' if k != 2 else f'{float(m):.1f} s', f'{round(float(m)):.0f} s', f'{float(m):.4f} s'])
    sol = [f'Sum/{len(xs)} = {float(m):.4f} s.', f'The mean cannot be more precise than the least precise reading ({k} decimal place{"s" if k != 1 else ""}).', f'Mean = {R} s.']
    return dict(q=q, o=o, a=a, sol=sol, p=dict(t='sfmean', xs=xs), ans=R)

def g_mean(rng):
    base = rng.choice([18.0, 2.5, 1.24, 50.0, 9.8]); xs = [round(base + rng.choice([-1, 1]) * rng.uniform(0, base * 0.08), 2) for _ in range(4)]
    m = sum(xs) / 4; mad = sum(abs(x - m) for x in xs) / 4; rel = mad / m
    what = rng.choice(['rel', 'pct', 'mad'])
    val = {'rel': rel, 'pct': rel * 100, 'mad': mad}[what]
    q = f'Four measurements of a length are {", ".join(f"{x:.2f}" for x in xs)} cm. The ' + {'rel': 'relative error', 'pct': 'percentage error', 'mad': 'mean absolute error (in cm)'}[what] + ' of the mean value is about :'
    fm = lambda v: f'{v:.3g}' if what != 'pct' else f'{v:.3g}%'
    o, a = mcq(rng, fm(val), [fm(val * 2), fm(val / 2), fm(val * 4), fm((max(xs) - min(xs)) / (2 * m) * (100 if what == 'pct' else 1) if what != 'mad' else (max(xs) - min(xs)) / 2)])
    sol = [f'Mean = {m:.4f} cm.', 'Deviations: ' + ', '.join(f'{abs(x - m):.4f}' for x in xs) + f' → mean absolute error = {mad:.4f} cm.', f'Relative error = {mad:.4f}/{m:.4f} = {rel:.4f}' + (f' → {rel * 100:.2f}%.' if what == 'pct' else '.')]
    return dict(q=q, o=o, a=a, sol=sol, p=dict(t='mean', xs=xs, what=what), ans=val)

def g_lcr(rng):
    k = rng.choice([1, 2, 3]); base = rng.choice([1.2, 12.4, 0.53, 5.0])
    xs = [f'{base + rng.randint(-5, 5) / 10 ** k:.{k}f}' for _ in range(4)]
    q = f'A set of readings is {", ".join(x + " mm" for x in xs)}. The least count of the instrument is most likely ______ mm.'
    lc = 10 ** -k
    o, a = mcq(rng, nf(lc), [nf(lc * 10), nf(lc / 10), nf(lc * 5), nf(lc * 2)])
    return dict(q=q, o=o, a=a, sol=['An instrument records up to its least count, no further.', f'Every reading has {k} decimal place{"s" if k > 1 else ""} in mm → LC = {nf(lc)} mm.'], p=dict(t='lcr', xs=xs), ans=lc)

# ------------------------------------------------------------------ dimensions
EXPR = [  # (text, factors [(quantity, power)], what it equals)
    ('ε_{0}E^{2}', [('permittivity ε₀', 1), ('electric field', 2)], 'energy density'),
    ('\\f{B^{2}}{μ_{0}}', [('magnetic field', 2), ('permeability μ₀', -1)], 'energy density'),
    ('√{\\f{μ_{0}}{ε_{0}}}', [('permeability μ₀', F(1, 2)), ('permittivity ε₀', F(-1, 2))], 'resistance'),
    ('\\f{1}{√{μ_{0}ε_{0}}}', [('permeability μ₀', F(-1, 2)), ('permittivity ε₀', F(-1, 2))], 'speed'),
    ('\\f{L}{R}', [('inductance', 1), ('resistance', -1)], 'time'),
    ('RC', [('resistance', 1), ('capacitance', 1)], 'time'),
    ('√{LC}', [('inductance', F(1, 2)), ('capacitance', F(1, 2))], 'time'),
    ('\\f{E}{B}', [('electric field', 1), ('magnetic field', -1)], 'speed'),
    ('ε_{0}\\f{dΦ_{E}}{dt}', [('permittivity ε₀', 1), ('electric flux', 1), ('time', -1)], 'current'),
    ('\\f{GM}{R}', [('gravitational constant G', 1), ('mass', 1), ('length', -1)], 'gravitational potential'),
    ('\\f{h}{λ}', [("Planck's constant", 1), ('length', -1)], 'momentum'),
    ('hν', [("Planck's constant", 1), ('frequency', 1)], 'energy'),
    ('√{\\f{T}{μ}} (T tension, μ mass per length)', [('force', F(1, 2)), ('linear mass density', F(-1, 2))], 'speed'),
    ('\\f{1}{2}LI^{2}', [('inductance', 1), ('current', 2)], 'energy'),
    ('\\f{q^{2}}{C}', [('charge', 2), ('capacitance', -1)], 'energy'),
    ('qvB', [('charge', 1), ('speed', 1), ('magnetic field', 1)], 'force'),
    ('μ_{0}I^{2}', [('permeability μ₀', 1), ('current', 2)], 'force'),
    ('\\f{ηv}{r} × area', [('coefficient of viscosity', 1), ('speed', 1), ('length', -1), ('area', 1)], 'force'),
    ('√{\\f{GM}{R}}', [('gravitational constant G', F(1, 2)), ('mass', F(1, 2)), ('length', F(-1, 2))], 'speed'),
    ('\\f{V^{2}}{R}', [('electric potential', 2), ('resistance', -1)], 'power'),
    ('\\f{kT}{λ^{2}}... per area: σT^{4}', [('Stefan constant', 1), ('temperature', 4)], 'power per unit area'),
    ('qE', [('charge', 1), ('electric field', 1)], 'force'),
    ('\\f{BIL}{m}', [('magnetic field', 1), ('current', 1), ('length', 1), ('mass', -1)], 'force per unit mass'),
    ('\\f{1}{2}ε_{0}cE^{2}', [('permittivity ε₀', 1), ('speed', 1), ('electric field', 2)], 'intensity of wave'),
    ('√{uG} (u energy density)', [('energy density', F(1, 2)), ('gravitational constant G', F(1, 2))], 'force per unit mass'),
]
EXPR = [e for e in EXPR if '...' not in e[0]] + [('σT^{4}', [('Stefan constant', 1), ('temperature', 4)], 'power per unit area')]
DEFN = {'area': 'l × b', 'volume': 'l × b × h', 'speed': 'distance/time', 'acceleration': 'Δv/t', 'frequency': '1/T', 'angular velocity': 'θ/t', 'angular acceleration': 'Δω/t',
 'density': 'm/V', 'momentum': 'mv', 'impulse': 'F × t', 'force': 'ma', 'work': 'F × d', 'energy': 'same as work', 'power': 'W/t', 'pressure': 'F/A', 'stress': 'F/A',
 "Young's modulus": 'stress/strain', 'energy density': 'energy/volume', 'torque': 'r × F', 'angular momentum': 'r × p', "Planck's constant": 'E = hν → h = E/ν', 'angular impulse': 'τ × t',
 'moment of inertia': 'Σmr^{2}', 'surface tension': 'F/l', 'spring constant': 'F = kx → k = F/x', 'coefficient of viscosity': 'F = ηA(dv/dx)', 'gravitational constant G': 'F = Gm_{1}m_{2}/r^{2}',
 'gravitational potential': 'work per unit mass', 'latent heat': 'Q = mL', 'specific heat': 'Q = mcΔT', 'heat capacity': 'Q/ΔT', 'gas constant R (per mole)': 'PV = nRT',
 'Boltzmann constant': 'E = kT', 'thermal conductivity': 'Q/t = kAΔT/l', 'Stefan constant': 'P/A = σT^{4}', 'compressibility': '1/bulk modulus', 'velocity gradient': 'dv/dx',
 'intensity of wave': 'power/area', 'charge': 'q = It', 'electric potential': 'V = W/q', 'electric field': 'E = F/q', 'resistance': 'R = V/I', 'resistivity': 'R = ρl/A', 'conductance': '1/R',
 'capacitance': 'C = q/V', 'inductance': 'Φ = LI', 'magnetic field': 'F = qvB', 'magnetic flux': 'Φ = BA', 'electric flux': 'Φ = EA', 'permittivity ε₀': 'F = q_{1}q_{2}/(4πε_{0}r^{2})',
 'permeability μ₀': 'F/l = μ_{0}I_{1}I_{2}/(2πd)', 'magnetic intensity H': 'H = B/μ_{0}', 'electric dipole moment': 'p = q × d', 'magnetic dipole moment': 'm = I × A',
 'current density': 'J = I/A', 'surface charge density': 'σ = q/A', 'emf': 'work per unit charge', 'time constant': 'τ = RC', 'Rydberg constant': '1/λ = R(1/n_{1}^{2} − 1/n_{2}^{2})',
 'wavelength': 'a length', 'wave number': '1/λ', 'pressure gradient': 'dP/dx', 'force per unit mass': 'F/m', 'energy per unit mass': 'E/m', 'power per unit area': 'P/A',
 'linear mass density': 'm/l', 'torsional constant': 'τ = Cθ', 'mass': 'base', 'length': 'base', 'time': 'base', 'current': 'base', 'temperature': 'base'}
def flist(fs): return ' × '.join(f'[{n}]' + ('' if F(p) == 1 else f'^{{{F(p)}}}'.replace('-', '−')) for n, p in fs)
NAMES = [k for k in Q if k not in ('angle', 'strain', 'refractive index', 'Poisson ratio')]
def evald(fs, table=Q):
    d = ONE
    for n, p in fs: d = d * table[n] ** F(p)
    return d
def wrong_dims(rng, d, k=6):
    out = []
    for _ in range(60):
        e = list(d); i = rng.randrange(4 if any(d[3:4]) else 3); e[i] += rng.choice([-1, 1, -2, 2])
        w = D(*e)
        if w != d and dfmt(w) not in [dfmt(x) for x in out]: out.append(w)
        if len(out) >= k: break
    return out
def g_dimq(rng):
    t = rng.choice(['name', 'name', 'expr', 'expr', 'which', 'unit'])
    if t == 'name':
        n = rng.choice(NAMES); d = Q[n]
        if d == ONE: return g_dimq(rng)
        q = f'The dimensional formula of {n} is :'
        o, a = mcq(rng, dfmt(d), [dfmt(w) for w in wrong_dims(rng, d)])
        return dict(q=q, o=o, a=a, sol=[f'Start from the defining relation: {DEFN[n]}.', f'Reduce every symbol to M, L, T, A, K: [{n}] = {dfmt(d)}.'], p=dict(t='dname', n=n), ans=dfmt(d))
    if t == 'expr':
        txt, fs, eq = rng.choice(EXPR); d = evald(fs)
        q = f'The dimensions of {txt} are :'
        o, a = mcq(rng, dfmt(d), [dfmt(w) for w in wrong_dims(rng, d)])
        return dict(q=q, o=o, a=a, sol=['Multiply the dimensions of each factor (powers add):'] + [f'[{n}] = {dfmt(Q[n])}' for n, _ in fs] + [f'{txt} → {dfmt(d)}, the dimensions of {eq}.'], p=dict(t='dexpr', fs=[(n, str(F(p))) for n, p in fs]), ans=dfmt(d))
    if t == 'which':
        txt, fs, eq = rng.choice(EXPR); d = evald(fs)
        others = [n for n in NAMES if Q[n] != d]; rng.shuffle(others)
        picks = []
        for n in others:
            if Q[n] not in [Q[x] for x in picks]: picks.append(n)
            if len(picks) == 5: break
        q = f'{txt} has the same dimensions as :'
        o, a = mcq(rng, eq, picks)
        return dict(q=q, o=o, a=a, sol=[f'[{n}] = {dfmt(Q[n])}' for n, _ in fs] + [f'[{txt}] = {dfmt(d)}.', f'That matches {eq} ({DEFN.get(eq, "")}).'], p=dict(t='dwhich', fs=[(n, str(F(p))) for n, p in fs], eq=eq), ans=eq)
    UN = {'electric field': 'N C^{−1}', 'magnetic field': 'N A^{−1} m^{−1}', 'current density': 'A m^{−2}', 'magnetic intensity H': 'A m^{−1}', 'energy density': 'J m^{−3}', 'resistance': 'V A^{−1}', 'time': 's', 'speed': 'm s^{−1}', 'force': 'N', 'power per unit area': 'W m^{−2}', 'momentum': 'N s', 'current': 'C s^{−1}', 'energy': 'J', 'power': 'W', 'gravitational potential': 'J kg^{−1}', 'force per unit mass': 'N kg^{−1}', 'intensity of wave': 'W m^{−2}', 'surface charge density': 'C m^{−2}'}
    txt, fs, eq = rng.choice([e for e in EXPR if e[2] in UN]); d = evald(fs)
    wrong = [UN[k] for k in UN if Q[k] != d]; rng.shuffle(wrong)
    q = f'The SI unit of {txt} is :'
    o, a = mcq(rng, UN[eq], wrong)
    return dict(q=q, o=o, a=a, sol=[f'{txt} is a(n) {eq}, {dfmt(d)}.', f'Its SI unit: {UN[eq]}.'], p=dict(t='dunit', fs=[(n, str(F(p))) for n, p in fs], eq=eq), ans=UN[eq])

PAIRS_SAME = [('torque', 'energy'), ('pressure', "Young's modulus"), ('angular momentum', "Planck's constant"), ('impulse', 'momentum'), ('surface tension', 'spring constant'), ('latent heat', 'gravitational potential'), ('energy density', 'pressure'), ('time constant', 'time'), ('emf', 'electric potential'), ('frequency', 'velocity gradient'), ('specific heat', 'specific heat'), ('Boltzmann constant', 'heat capacity')]
PAIRS_DIFF = [('surface tension', 'impulse'), ('momentum', 'torque'), ('force', 'pressure'), ('power', 'energy'), ('stress', 'strain'), ("Planck's constant", 'energy'), ('latent heat', 'specific heat'), ('magnetic flux', 'magnetic field'), ('electric flux', 'magnetic flux'), ('gravitational constant G', 'gravitational potential'), ('capacitance', 'inductance')]
def g_dimst(rng):
    t = rng.choice(['two', 'odd'])
    if t == 'two':
        s1 = rng.random() < 0.5; s2 = rng.random() < 0.5
        p1 = rng.choice([p for p in PAIRS_SAME if p[0] != p[1]] if s1 else PAIRS_DIFF); p2 = rng.choice([p for p in (PAIRS_SAME if s2 else PAIRS_DIFF) if p != p1 and p[0] != p[1]])
        q = f'Statement (I): {p1[0][0].upper() + p1[0][1:]} and {p1[1]} have the same dimensions. Statement (II): {p2[0][0].upper() + p2[0][1:]} and {p2[1]} have the same dimensions.'
        opts = ['Both Statement I and Statement II are true', 'Both Statement I and Statement II are false', 'Statement I is true but Statement II is false', 'Statement I is false but Statement II is true']
        right = opts[0] if s1 and s2 else opts[1] if not s1 and not s2 else opts[2] if s1 else opts[3]
        o, a = mcq(rng, right, [x for x in opts if x != right])
        sol = [f'[{p1[0]}] = {dfmt(Q[p1[0]])}, [{p1[1]}] = {dfmt(Q[p1[1]])} → I is {"true" if s1 else "false"}.', f'[{p2[0]}] = {dfmt(Q[p2[0]])}, [{p2[1]}] = {dfmt(Q[p2[1]])} → II is {"true" if s2 else "false"}.']
        return dict(q=q, o=o, a=a, sol=sol, p=dict(t='dst', p1=p1, p2=p2), ans=right)
    sames = rng.sample([p for p in PAIRS_SAME if p[0] != p[1]], 3); diff = rng.choice(PAIRS_DIFF)
    fmt = lambda p: f'{p[0][0].upper() + p[0][1:]} and {p[1]}'
    q = 'The pair of physical quantities NOT having the same dimensions is :'
    o, a = mcq(rng, fmt(diff), [fmt(p) for p in sames])
    sol = [f'{fmt(diff)}: {dfmt(Q[diff[0]])} vs {dfmt(Q[diff[1]])} — different.'] + [f'{fmt(p)}: both {dfmt(Q[p[0]])}.' for p in sames]
    return dict(q=q, o=o, a=a, sol=sol, p=dict(t='dodd', diff=diff, sames=sames), ans=fmt(diff))

CONS = [  # equation text, {constant: dims}, quantity names used
    ('x = At + Bt^{2}', {'A': Q['speed'], 'B': Q['acceleration']}),
    ('v = At^{2} + \\f{Bt}{C + t}', {'A': Q['speed'] / Q['time'] ** 2, 'B': Q['speed'], 'C': Q['time']}),
    ('F = ax^{2} + bt^{1/2} (x distance, t time)', {'a': Q['force'] / Q['area'], 'b': Q['force'] / Q['time'] ** F(1, 2)}),
    ('x = A sin(ωt) + Bt^{3} + C (x in m, t in s)', {'A': Q['length'], 'B': Q['length'] / Q['time'] ** 3, 'C': Q['length']}),
    ('E = \\f{B − x^{2}}{At} (E energy, x length, t time)', {'A': Q['area'] / (Q['energy'] * Q['time']), 'B': Q['area']}),
    ('V = \\f{A√{x}}{x + B} (V energy, x length)', {'A': Q['energy'] * Q['length'] ** F(1, 2), 'B': Q['length']}),
    ('P = \\f{a − t^{2}}{bx} (P pressure, x distance, t time)', {'a': Q['time'] ** 2, 'b': Q['time'] ** 2 / (Q['pressure'] * Q['length'])}),
    ('y = A sin(Bt − Cx) (y, x in m; t in s)', {'A': Q['length'], 'B': Q['frequency'], 'C': ONE / Q['length']}),
    ('F = αv + βv^{2} (F force, v speed)', {'α': Q['force'] / Q['speed'], 'β': Q['force'] / Q['speed'] ** 2}),
    ('U = \\f{a}{x^{2}} − \\f{b}{x} (U energy, x distance)', {'a': Q['energy'] * Q['area'], 'b': Q['energy'] * Q['length']}),
    ('(P + \\f{a}{V^{2}})(V − b) = RT', {'a': Q['pressure'] * Q['volume'] ** 2, 'b': Q['volume']}),
    ('P = \\f{A}{Bt^{2}} + ρgBt (P pressure, t time)', {'A': Q['pressure'] * Q['speed'] * Q['time'] ** 2, 'B': Q['speed']}),
]
def g_cons(rng):
    eq, ks = rng.choice(CONS); names = list(ks)
    if len(names) >= 2 and rng.random() < 0.7:
        x, y = rng.sample(names, 2); op = rng.choice(['xy', 'x/y', 'x^2/y', 'xy^2'])
        d = {'xy': ks[x] * ks[y], 'x/y': ks[x] / ks[y], 'x^2/y': ks[x] ** 2 / ks[y], 'xy^2': ks[x] * ks[y] ** 2}[op]
        lab = {'xy': f'{x}{y}', 'x/y': f'\\f{{{x}}}{{{y}}}', 'x^2/y': f'\\f{{{x}^{{2}}}}{{{y}}}', 'xy^2': f'{x}{y}^{{2}}'}[op]
    else:
        x = rng.choice(names); d = ks[x]; lab = x; op = 'x'; y = None
    q = f'In the relation {eq}, the dimensions of {lab} are :'
    o, a = mcq(rng, dfmt(d), [dfmt(w) for w in wrong_dims(rng, d)])
    sol = ['Only quantities with the same dimensions can be added or subtracted, and arguments of sin/exp are pure numbers.'] + [f'[{k}] = {dfmt(v)}' for k, v in ks.items()] + [f'[{lab}] = {dfmt(d)}.']
    return dict(q=q, o=o, a=a, sol=sol, p=dict(t='cons', eq=eq, op=op, x=x, y=y), ans=dfmt(d))

GAS = [('(P + \\f{a}{V^{2}})(V − b) = RT', 'van der Waals', Q['pressure'] * Q['volume'] ** 2, 'a/V^{2} is added to P → [a] = [P][V^{2}] = ML^{5}T^{−2}.'),
       ('(P + \\f{a}{TV^{2}})(V − b) = RT', 'Berthelot', Q['pressure'] * Q['volume'] ** 2 * Q['temperature'], 'a/(TV^{2}) is added to P → [a] = [P][V^{2}][T] = ML^{5}T^{−2}K.'),
       ('P(V − b) = RT e^{−a/(RTV)}', 'Dieterici', Q['energy'] * Q['volume'], 'An exponent is a pure number → [a] = [RT][V] = (energy)(volume) = ML^{5}T^{−2} (per mole).')]
def g_gas(rng):
    eq, nm, a_, why = rng.choice(GAS); b_ = Q['volume']
    combos = [('ab', a_ * b_), ('\\f{a}{b}', a_ / b_), ('\\f{a}{b^{2}}', a_ / b_ ** 2), ('ab^{2}', a_ * b_ ** 2), ('\\f{b^{2}}{a}', b_ ** 2 / a_), ('a', a_), ('b', b_), ('\\f{a}{b^{3}}', a_ / b_ ** 3)]
    lab, d = rng.choice(combos)
    named = [n for n in NAMES if Q[n] == d]
    if named and rng.random() < 0.6:
        others = []
        for n in NAMES:
            if Q[n] != d and Q[n] not in [Q[o_] for o_ in others]: others.append(n)
        rng.shuffle(others); right = named[0]
        q = f'In the {nm} equation {eq}, the quantity {lab} has the same dimensions as :'
        o, a = mcq(rng, right, others)
    else:
        q = f'In the {nm} equation {eq}, the dimensional formula of {lab} is :'
        o, a = mcq(rng, dfmt(d), [dfmt(w) for w in wrong_dims(rng, d)]); right = dfmt(d)
    sol = [why, 'b is subtracted from V → [b] = L^{3}.', f'[{lab}] = {dfmt(d)}' + (f' — same as {named[0]}.' if named else '.')]
    return dict(q=q, o=o, a=a, sol=sol, p=dict(t='gas', lab=lab, eq=nm), ans=right)

# (what, LHS quantity, [(text, RHS factors)]) — the FIRST formula is the true one; every other one is checked to be dimensionally wrong
HOMO = [
 ('time period of a simple pendulum', 'time', [('T = 2π√{\\f{l}{g}}', [('length', F(1, 2)), ('acceleration', F(-1, 2))]), ('T = 2π√{\\f{g}{l}}', [('acceleration', F(1, 2)), ('length', F(-1, 2))]), ('T = 2π\\f{l}{g}', [('length', 1), ('acceleration', -1)]), ('T = 2π√{lg}', [('length', F(1, 2)), ('acceleration', F(1, 2))])]),
 ('square of the orbital period', 'time', [('T^{2} = \\f{4π^{2}r^{3}}{GM}', [('length', F(3, 2)), ('gravitational constant G', F(-1, 2)), ('mass', F(-1, 2))]), ('T^{2} = \\f{4π^{2}r^{2}}{GM}', [('length', 1), ('gravitational constant G', F(-1, 2)), ('mass', F(-1, 2))]), ('T^{2} = 4π^{2}r^{3}', [('length', F(3, 2))]), ('T^{2} = \\f{4π^{2}r}{GM^{2}}', [('length', F(1, 2)), ('gravitational constant G', F(-1, 2)), ('mass', -1)])]),
 ('escape speed', 'speed', [('v = √{\\f{2GM}{R}}', [('gravitational constant G', F(1, 2)), ('mass', F(1, 2)), ('length', F(-1, 2))]), ('v = √{\\f{2GM}{R^{2}}}', [('gravitational constant G', F(1, 2)), ('mass', F(1, 2)), ('length', -1)]), ('v = \\f{2GM}{R}', [('gravitational constant G', 1), ('mass', 1), ('length', -1)]), ('v = √{2GMR}', [('gravitational constant G', F(1, 2)), ('mass', F(1, 2)), ('length', F(1, 2))])]),
 ('frequency of a stretched string (T tension, μ mass per length)', 'frequency', [('f = \\f{1}{2l}√{\\f{T}{μ}}', [('length', -1), ('force', F(1, 2)), ('linear mass density', F(-1, 2))]), ('f = \\f{1}{2l}√{\\f{μ}{T}}', [('length', -1), ('force', F(-1, 2)), ('linear mass density', F(1, 2))]), ('f = 2l√{\\f{T}{μ}}', [('length', 1), ('force', F(1, 2)), ('linear mass density', F(-1, 2))]), ('f = \\f{1}{2l}\\f{T}{μ}', [('length', -1), ('force', 1), ('linear mass density', -1)])]),
 ('viscous drag on a sphere', 'force', [('F = 6πηrv', [('coefficient of viscosity', 1), ('length', 1), ('speed', 1)]), ('F = 6πηr^{2}v', [('coefficient of viscosity', 1), ('length', 2), ('speed', 1)]), ('F = 6π\\f{ηv}{r}', [('coefficient of viscosity', 1), ('length', -1), ('speed', 1)]), ('F = 6πηrv^{2}', [('coefficient of viscosity', 1), ('length', 1), ('speed', 2)])]),
 ('capillary rise (T surface tension)', 'length', [('h = \\f{2T cosθ}{rρg}', [('surface tension', 1), ('length', -1), ('density', -1), ('acceleration', -1)]), ('h = \\f{2T cosθ}{r^{2}ρg}', [('surface tension', 1), ('length', -2), ('density', -1), ('acceleration', -1)]), ('h = \\f{2Tr cosθ}{ρg}', [('surface tension', 1), ('length', 1), ('density', -1), ('acceleration', -1)]), ('h = 2T cosθ·rρg', [('surface tension', 1), ('length', 1), ('density', 1), ('acceleration', 1)])]),
 ('speed of sound in a gas', 'speed', [('v = √{\\f{γP}{ρ}}', [('pressure', F(1, 2)), ('density', F(-1, 2))]), ('v = √{\\f{ρ}{γP}}', [('pressure', F(-1, 2)), ('density', F(1, 2))]), ('v = \\f{γP}{ρ}', [('pressure', 1), ('density', -1)]), ('v = √{γPρ}', [('pressure', F(1, 2)), ('density', F(1, 2))])]),
 ('energy stored in a capacitor', 'energy', [('U = \\f{q^{2}}{2C}', [('charge', 2), ('capacitance', -1)]), ('U = \\f{q}{2C}', [('charge', 1), ('capacitance', -1)]), ('U = \\f{q^{2}C}{2}', [('charge', 2), ('capacitance', 1)]), ('U = \\f{qC^{2}}{2}', [('charge', 1), ('capacitance', 2)])]),
 ('centripetal force', 'force', [('F = \\f{mv^{2}}{r}', [('mass', 1), ('speed', 2), ('length', -1)]), ('F = mv^{2}r', [('mass', 1), ('speed', 2), ('length', 1)]), ('F = \\f{mv}{r}', [('mass', 1), ('speed', 1), ('length', -1)]), ('F = \\f{mv^{2}}{r^{2}}', [('mass', 1), ('speed', 2), ('length', -2)])]),
 ('force on a current-carrying wire in a field', 'force', [('F = BIl', [('magnetic field', 1), ('current', 1), ('length', 1)]), ('F = \\f{BI}{l}', [('magnetic field', 1), ('current', 1), ('length', -1)]), ('F = BIl^{2}', [('magnetic field', 1), ('current', 1), ('length', 2)]), ('F = B^{2}Il', [('magnetic field', 2), ('current', 1), ('length', 1)])]),
 ('de Broglie wavelength of a particle of energy E', 'length', [('λ = \\f{h}{√{2mE}}', [("Planck's constant", 1), ('mass', F(-1, 2)), ('energy', F(-1, 2))]), ('λ = h√{2mE}', [("Planck's constant", 1), ('mass', F(1, 2)), ('energy', F(1, 2))]), ('λ = \\f{h}{2mE}', [("Planck's constant", 1), ('mass', -1), ('energy', -1)]), ('λ = √{\\f{h}{2mE}}', [("Planck's constant", F(1, 2)), ('mass', F(-1, 2)), ('energy', F(-1, 2))])]),
 ('radius of a charge circling in a magnetic field', 'length', [('r = \\f{mv}{qB}', [('mass', 1), ('speed', 1), ('charge', -1), ('magnetic field', -1)]), ('r = \\f{qB}{mv}', [('mass', -1), ('speed', -1), ('charge', 1), ('magnetic field', 1)]), ('r = mvqB', [('mass', 1), ('speed', 1), ('charge', 1), ('magnetic field', 1)]), ('r = \\f{mv^{2}}{qB}', [('mass', 1), ('speed', 2), ('charge', -1), ('magnetic field', -1)])]),
 ('terminal speed of a sphere in a liquid', 'speed', [('v = \\f{2r^{2}(ρ − σ)g}{9η}', [('length', 2), ('density', 1), ('acceleration', 1), ('coefficient of viscosity', -1)]), ('v = \\f{2r(ρ − σ)g}{9η}', [('length', 1), ('density', 1), ('acceleration', 1), ('coefficient of viscosity', -1)]), ('v = \\f{2r^{2}(ρ − σ)gη}{9}', [('length', 2), ('density', 1), ('acceleration', 1), ('coefficient of viscosity', 1)]), ('v = \\f{9η}{2r^{2}(ρ − σ)g}', [('length', -2), ('density', -1), ('acceleration', -1), ('coefficient of viscosity', 1)])]),
]
def g_homo(rng):
    what, lhs, forms = rng.choice(HOMO)
    assert evald(forms[0][1]) == Q[lhs] and all(evald(f[1]) != Q[lhs] for f in forms[1:]), what
    q = f'Using the principle of homogeneity of dimensions, the correct relation for the {what} is : (symbols have their usual meanings)'
    o, a = mcq(rng, forms[0][0], [f[0] for f in forms[1:]])
    sol = ['Every term of a correct equation has the same dimensions. (This test can reject a formula, but cannot prove one right.)', f'Left side: {dfmt(Q[lhs])}.'] + [f'{f[0]} → right side {dfmt(evald(f[1]))}' + (' ✓' if k == 0 else ' ✗') for k, f in enumerate(forms)]
    return dict(q=q, o=o, a=a, sol=sol, p=dict(t='homo', what=what), ans=forms[0][0])

EXPO = [  # target, base quantities, label, latex template
    ('mass', ["Planck's constant", 'speed', 'gravitational constant G'], 'm ∝ h^{x}c^{y}G^{z}', 'Planck mass'),
    ('length', ["Planck's constant", 'speed', 'gravitational constant G'], 'l ∝ h^{x}c^{y}G^{z}', 'Planck length'),
    ('time', ["Planck's constant", 'speed', 'gravitational constant G'], 't ∝ h^{x}c^{y}G^{z}', 'Planck time'),
    ('time', ['mass', 'spring constant'], 'T ∝ m^{x}k^{y}', 'spring–mass period'),
    ('speed', ['force', 'linear mass density'], 'v ∝ T^{x}μ^{y} (T tension)', 'wave on a string'),
    ('force', ['coefficient of viscosity', 'length', 'speed'], 'F ∝ η^{x}r^{y}v^{z}', 'Stokes drag'),
    ('speed', ['wavelength', 'acceleration', 'density'], 'v ∝ λ^{x}g^{y}ρ^{z}', 'deep-water waves'),
    ('frequency', ['surface tension', 'mass'], 'f ∝ S^{x}m^{y} (drop oscillation)', 'drop frequency'),
    ('speed', ['pressure', 'density'], 'v ∝ P^{x}ρ^{y}', 'speed of sound'),
    ('energy', ['mass', 'speed'], 'E ∝ m^{x}c^{y}', 'mass–energy'),
]
import itertools
def solve_expo(target, bases, table=Q):
    rng_ = [F(n, 2) for n in range(-8, 9)]
    sols = [c for c in itertools.product(rng_, repeat=len(bases)) if evald(list(zip(bases, c)), table) == table[target]]
    return sols
def g_expo(rng):
    target, bases, lab, name = rng.choice(EXPO)
    s = solve_expo(target, bases); assert len(s) == 1, (lab, s); s = s[0]
    vars_ = ['x', 'y', 'z'][:len(bases)]; ask = rng.choice(vars_ + (['sum'] if len(bases) > 1 else []))
    val = sum(s) if ask == 'sum' else s[vars_.index(ask)]
    lbl = 'x + y' + (' + z' if len(bases) == 3 else '') if ask == 'sum' else ask
    q = f'By dimensional analysis, {lab}. The value of {lbl} is :'
    def fr(v): return (str(v.numerator) if v.denominator == 1 else f'{v.numerator}/{v.denominator}').replace('-', '−')
    o, a = mcq(rng, fr(val), [fr(val + F(1, 2)), fr(val - F(1, 2)), fr(-val) if val else '1', fr(val + 1), fr(val * 2) if val else '−1'])
    sol = ['Write each quantity in M, L, T and equate powers on both sides.'] + [f'[{b}] = {dfmt(Q[b])}' for b in bases] + [', '.join(f'{v} = {fr(c)}' for v, c in zip(vars_, s)) + f' ({name}).', f'{lbl} = {fr(val)}.']
    return dict(q=q, o=o, a=a, sol=sol, p=dict(t='expo', target=target, bases=bases, ask=ask), ans=fr(val))

GEN = dict(vlc=g_vlc, vze=g_vze, vrd=g_vrd, sgr=g_sgr, sgz=g_sgz, sglc=g_sglc, perr=g_perr, aerr=g_aerr, sfc=g_sfc, sfa=g_sfa, mean=g_mean, lcr=g_lcr,
           dimq=g_dimq, dimst=g_dimst, cons=g_cons, gas=g_gas, homo=g_homo, expo=g_expo, units=g_dimq)
