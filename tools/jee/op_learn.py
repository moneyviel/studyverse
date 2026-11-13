"""Concept cards for Physics Unit 16 — Optics (written for StudyVerse)."""
TOPICS = {'mirror': 'Mirrors', 'lens': 'Lenses & optical instruments', 'refr': 'Refraction, TIR & prisms', 'wave': 'Wave optics: interference, diffraction, polarisation'}
CARDS = [
 dict(id='c1', t='Mirrors', e='🪞', lvl='f', topic='mirror',
  body=['<div class="jx-f">\\f{1}{v} + \\f{1}{u} = \\f{1}{f},  f = \\f{R}{2},  m = −\\f{v}{u}</div>', 'Sign rule: distances against the incoming light are negative. Concave f < 0, convex f > 0.',
        'Concave: object beyond F → real, inverted; inside F → virtual, erect, magnified. Convex: always virtual, erect, smaller.', 'Mirror focal length does not change in a liquid — reflection ignores the medium.'],
  check=dict(q='An erect, diminished image is formed by a', o=['convex mirror', 'concave mirror (object beyond C)', 'plane mirror', 'concave mirror (object at F)'], a=0, why='Convex mirrors always give m between 0 and 1.')),
 dict(id='c2', t='Refraction & TIR', e='💧', lvl='f', topic='refr',
  body=['<div class="jx-f">n_{1} sin i = n_{2} sin r,  λ_{medium} = \\f{λ_{0}}{n},  sin C = \\f{n_{2}}{n_{1}}</div>', 'Apparent depth = \\f{real depth}{n}; for layers add \\f{t}{n} for each.',
        'Slab: emerges parallel, shifted sideways by \\f{t sin(i − r)}{cos r}.', 'Spherical surface: \\f{n_{2}}{v} − \\f{n_{1}}{u} = \\f{n_{2} − n_{1}}{R}, m = \\f{n_{1}v}{n_{2}u}.'],
  check=dict(q='Total internal reflection needs light going from', o=['denser to rarer, i > C', 'rarer to denser', 'denser to rarer, i < C', 'any medium at 45°'], a=0, why='Only then can sin r exceed 1.')),
 dict(id='c3', t='Prisms', e='🔺', lvl='m', topic='refr',
  body=['<div class="jx-f">A = r_{1} + r_{2},  δ = i + e − A,  n = \\f{sin((A + δ_{m})/2)}{sin(A/2)}</div>', 'At minimum deviation i = e and r = \\f{A}{2}; the ray inside runs parallel to the base.',
        'Thin prism: δ = (n − 1)A. No deviation (with dispersion): (n_{1} − 1)A_{1} = (n_{2} − 1)A_{2}.', 'Violet (larger n) bends most, red least.'],
  check=dict(q='Larger prism angle (same glass) makes δ_min', o=['larger', 'smaller', 'unchanged', 'zero'], a=0, why='δ grows with A.')),
 dict(id='c4', t='Lenses', e='🔍', lvl='m', topic='lens',
  body=['<div class="jx-f">\\f{1}{v} − \\f{1}{u} = \\f{1}{f},  \\f{1}{f} = (\\f{n}{n_{m}} − 1)(\\f{1}{R_{1}} − \\f{1}{R_{2}}),  P = \\f{1}{f}</div>', 'Contact: P = P_{1} + P_{2}; separated by d: P = P_{1} + P_{2} − dP_{1}P_{2}.',
        'In a denser liquid a glass lens can even become diverging. Cutting along the lens plane makes plano-convex halves of double focal length.', 'Silvered lens = mirror with P = 2P_{lens} + P_{mirror}.'],
  check=dict(q='A convex lens (n = 1.5) in a liquid of n = 1.5 has focal length', o=['infinite', 'unchanged', 'halved', 'negative'], a=0, why='n/n_m − 1 = 0.')),
 dict(id='c5', t='Instruments', e='🔭', lvl='m', topic='lens',
  body=['<div class="jx-f">Microscope: m = \\f{L}{f_{o}} × \\f{D}{f_{e}};  Telescope: m = \\f{f_{o}}{f_{e}};  resolution θ = \\f{1.22λ}{D}</div>', 'Microscope: short focal lengths for both lenses. Telescope: long objective, short eyepiece, large aperture for brightness and resolution.',
        'Beam expander: two lenses sharing a focus widen a beam by \\f{f_{2}}{f_{1}}.'],
  check=dict(q='Doubling a telescope objective\'s diameter changes its limit of resolution by', o=['½ (better)', '×2', 'none', '×4'], a=0, why='θ ∝ 1/D.')),
 dict(id='c6', t='Interference (YDSE)', e='🌊', lvl='m', topic='wave',
  body=['<div class="jx-f">β = \\f{λD}{d},  I = I_{1} + I_{2} + 2√{I_{1}I_{2}} cos φ,  φ = \\f{2π}{λ}Δx</div>', '\\f{I_{max}}{I_{min}} = (\\f{√{I_{1}} + √{I_{2}}}{√{I_{1}} − √{I_{2}}})^{2}. Equal slits: I = I_{max} cos^{2}\\f{φ}{2}.',
        'A sheet (μ, t) on one slit shifts the pattern by \\f{(μ − 1)tD}{d}. In a liquid, β → \\f{β}{n}.', 'Coincidence of two colours: n_{1}λ_{1} = n_{2}λ_{2}. Different colours from the two slits: no fringes.'],
  check=dict(q='Angular fringe width depends on', o=['λ and d only', 'D only', 'λ, d and D', 'intensity'], a=0, why='θ = λ/d.')),
 dict(id='c7', t='Diffraction & polarisation', e='🕶️', lvl='m', topic='wave',
  body=['<div class="jx-f">Single slit minima: a sin θ = nλ,  central width \\f{2λD}{a};  Malus: I = I_{0} cos^{2} θ;  Brewster: tan i_{B} = \\f{n_{2}}{n_{1}}</div>', 'Narrower slit or longer wavelength → wider central maximum.',
        'Unpolarised light through one polaroid: I_{0}/2. At Brewster\'s angle the reflected and refracted rays are at 90° and the reflected light is fully polarised.', 'Thin films: watch for a π flip at each reflection off a denser medium.'],
  check=dict(q='Unpolarised I₀ through polaroids at 0° then 60° gives', o=['I₀/8', 'I₀/4', 'I₀/2', '3I₀/8'], a=0, why='½ × cos² 60°.')),
]
FORMULAS = [('Mirror', '\\f{1}{v} + \\f{1}{u} = \\f{1}{f}'), ('Lens', '\\f{1}{v} − \\f{1}{u} = \\f{1}{f}'), ('Lens maker', '\\f{1}{f} = (n − 1)(\\f{1}{R_{1}} − \\f{1}{R_{2}})'), ('Surface', '\\f{n_{2}}{v} − \\f{n_{1}}{u} = \\f{n_{2} − n_{1}}{R}'),
            ('Prism', 'n = \\f{sin((A + δ_{m})/2)}{sin(A/2)}'), ('Critical', 'sin C = \\f{n_{2}}{n_{1}}'), ('Fringe', 'β = \\f{λD}{d}'), ('Intensity', 'I = 4I_{0} cos^{2}\\f{φ}{2}'),
            ('Single slit', 'a sin θ = nλ'), ('Malus', 'I = I_{0} cos^{2} θ'), ('Brewster', 'tan i_{B} = n'), ('Resolution', 'θ = \\f{1.22λ}{D}')]
TRAPS = ['Use the sign convention: distances measured against the light are negative.', 'Mirror focal length is the same in any medium; a lens\'s is not.', 'Magnification of a refracting surface includes the refractive indices: m = n_{1}v/(n_{2}u).',
         'YDSE angular fringe width does not depend on D.', 'First polaroid always halves unpolarised light.', 'Wider slit → narrower diffraction pattern (less bending).']
STEPS = [dict(k='s1', t='Mirrors', e='🪞', cards=['c1'], need=['mirror'], note='Images by reflection'),
         dict(k='s2', t='Refraction', e='💧', cards=['c2', 'c3'], need=['refr'], note='Snell, TIR, slabs and prisms'),
         dict(k='s3', t='Lenses', e='🔍', cards=['c4', 'c5'], need=['lens'], note='Lenses and instruments'),
         dict(k='s4', t='Waves', e='🌊', cards=['c6', 'c7'], need=['wave'], note='Interference, diffraction, polarisation')]
META = dict(unit='phy-u16', subject='phy', n=16, title='Optics', cls=12, labs=['optbench'],
            syllabus='Reflection of light, spherical mirrors, mirror formula. Refraction of light at plane and spherical surfaces, thin lens formula and lens maker formula. Total internal reflection and its applications. Magnification. Power of a lens. Combination of thin lenses in contact. Refraction of light through a prism. Microscope and astronomical telescope (reflecting and refracting) and their magnifying powers. Wave optics: wavefront and Huygens\' principle. Laws of reflection and refraction using Huygens principle. Interference, Young\'s double-slit experiment and expression for fringe width, coherent sources and sustained interference of light. Diffraction due to a single slit, width of central maximum. Polarisation, plane-polarised light: Brewster\'s law, uses of plane-polarised light and Polaroid.')
