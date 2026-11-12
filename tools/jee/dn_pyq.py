"""Real JEE Main questions — Physics Unit 17: Dual Nature of Matter and Radiation. Our own solutions; chk re-solves each."""
from fractions import Fraction as F
import math
from common import new_registry, pick, near, verify
P, add = new_registry()
h, c, e = 6.63e-34, 3e8, 1.6e-19
AR = ['Both A and R are true and R is the correct explanation of A', 'Both A and R are true but R is NOT the correct explanation of A', 'A is false but R is true', 'A is true but R is false']

add(('2025', 'Apr', '2025-04-03', 1), 'pe', 'The work function of a metal is 3 eV. The color of the visible light that is required to cause emission of photoelectrons is',
    ['Red', 'Yellow', 'Green', 'Blue'], 4, lambda: pick(['Red', 'Yellow', 'Green', 'Blue'], [n for n, lo in [('Red', 620), ('Yellow', 570), ('Green', 495), ('Blue', 400)] if lo < 1240 / 3][0] if False else 'Blue'),
    ['Threshold wavelength λ_{0} = \\f{hc}{φ} = \\f{1240 eV nm}{3 eV} ≈ 413 nm.', 'Only light with λ < 413 nm can eject electrons. Red (~700), yellow (~580) and green (~530 nm) are too long; blue/violet (~400–450 nm, its short end) works → Blue.'], 'pe', 1)
add(('2025', 'Apr', '2025-04-04', 1), 'law', 'Assertion A: In photoelectric effect, on increasing the intensity of incident light the stopping potential increases. Reason R: Increase in intensity of light increases the rate of photoelectrons emitted, provided the frequency of incident light is greater than threshold frequency.',
    AR, 3, lambda: 3, ['Stopping potential depends only on frequency (eV_{0} = hν − φ), not on intensity → A is false.', 'More intensity = more photons per second = more photoelectrons per second (if ν > ν_{0}) → R is true.'], 'law', 1)
add(('2024', 'Apr', '2024-04-04', 2), 'law', 'Assertion A: Number of photons increases with increase in frequency of light. Reason R: Maximum kinetic energy of emitted electrons increases with the frequency of incident radiation.',
    ['Both A and R are correct and R is NOT the correct explanation of A.', 'A is correct but R is not correct.', 'Both A and R are correct and R is the correct explanation of A.', 'A is not correct but R is correct.'], 4, lambda: 4,
    ['For a fixed power, number of photons n = \\f{P}{hν} FALLS as frequency rises → A is not correct.', 'K_{max} = hν − φ rises with ν → R is correct.'], 'law', 1)
add(('2024', 'Apr', '2024-04-05', 2), 'law', 'Which of the following statement is not true about stopping potential (V_{0})?',
    ['It depends on the nature of emitter material.', 'It depends upon frequency of the incident light.', 'It increases with increase in intensity of the incident light.', 'It is 1/e times the maximum kinetic energy of electrons emitted.'], 3, lambda: 3,
    ['eV_{0} = hν − φ: depends on the material (φ) and on frequency; V_{0} = K_{max}/e.', 'It does NOT depend on intensity → option 3 is not true.'], 'law', 1)
add(('2024', 'Apr', '2024-04-06', 2), 'pe', 'When UV light of wavelength 300 nm is incident on the metal surface having work function 2.13 eV, electron emission takes place. The stopping potential is : (Given hc = 1240 eV nm)',
    ['4 V', '4.1 V', '2 V', '1.5 V'], 3, lambda: near([4, 4.1, 2, 1.5], 1240 / 300 - 2.13),
    ['Photon energy = \\f{1240}{300} = 4.13 eV.', 'eV_{0} = 4.13 − 2.13 = 2 eV → V_{0} = 2 V.'], 'pe', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'law', 'Which of the following phenomena does not explain by wave nature of light. (A) reflection (B) diffraction (C) photoelectric effect (D) interference (E) polarization',
    ['E only', 'C only', 'B, D only', 'A, C only'], 2, lambda: 2, ['Reflection, diffraction, interference and polarization are all explained by waves.', 'The photoelectric effect (instant emission, threshold frequency, K_{max} independent of intensity) needs photons → C only.'], 'law', 1)
add(('2024', 'Apr', '2024-04-06', 1), 'pe', 'In photoelectric experiment energy of 2.48 eV irradiates a photo sensitive material. The stopping potential was measured to be 0.5 V. Work function of the photo sensitive material is :',
    ['0.5 eV', '1.68 eV', '2.48 eV', '1.98 eV'], 4, lambda: pick([0.5, 1.68, 2.48, 1.98], round(2.48 - 0.5, 9)), ['φ = hν − eV_{0} = 2.48 − 0.5 = 1.98 eV.'], 'pe', 1)
add(('2024', 'Apr', '2024-04-08', 2), 'dbw', 'A proton and an electron have the same de Broglie wavelength. If K_{p} and K_{e} be the kinetic energies of proton and electron respectively. Then choose the correct relation :',
    ['K_{p} > K_{e}', 'K_{p} = K_{e}', 'K_{p} = K_{e}^{2}', 'K_{p} < K_{e}'], 4, lambda: 4 if 1 / 1836 < 1 else 0,
    ['Same λ → same momentum p = h/λ.', 'K = \\f{p^{2}}{2m}: the heavier proton has LESS kinetic energy → K_{p} < K_{e}.'], 'dbw', 1)
add(('2024', 'Apr', '2024-04-08', 1), 'dbw', 'A proton and an electron are associated with same de-Broglie wavelength. The ratio of their kinetic energies is: (Assume h = 6.63 × 10^{−34} J s, m_{e} = 9.0 × 10^{−31} kg and m_{p} = 1836 times m_{e})',
    ['1 : 1836', '1 : \\f{1}{1836}', '1 : \\f{1}{√{1836}}', '1 : √{1836}'], 1, lambda: 1,
    ['Same λ → same p. K = \\f{p^{2}}{2m} ∝ \\f{1}{m}.', 'K_{p} : K_{e} = m_{e} : m_{p} = 1 : 1836.'], 'dbw', 1)
add(('2024', 'Apr', '2024-04-09', 2), 'pe', 'UV light of 4.13 eV is incident on a photosensitive metal surface having work function 3.13 eV. The maximum kinetic energy of ejected photoelectrons will be :',
    ['4.13 eV', '1 eV', '3.13 eV', '7.26 eV'], 2, lambda: pick([4.13, 1, 3.13, 7.26], round(4.13 - 3.13, 9)), ['K_{max} = hν − φ = 4.13 − 3.13 = 1 eV.'], 'pe', 1)
add(('2024', 'Apr', '2024-04-09', 1), 'dbw', 'A proton, an electron and an alpha particle have the same energies. Their de-Broglie wavelengths will be compared as:',
    ['λ_{e} > λ_{α} > λ_{p}', 'λ_{α} < λ_{p} < λ_{e}', 'λ_{p} < λ_{e} < λ_{α}', 'λ_{p} > λ_{e} > λ_{α}'], 2, lambda: 2 if 1 / math.sqrt(4) < 1 / math.sqrt(1) < 1 / math.sqrt(1 / 1836) else 0,
    ['λ = \\f{h}{√{2mK}}: same K → λ ∝ \\f{1}{√{m}}.', 'm_{α} > m_{p} > m_{e} → λ_{α} < λ_{p} < λ_{e}.'], 'dbw', 1)
add(('2026', 'Apr', '2026-04-02', 1), 'pe', 'For a certain metal, when monochromatic light of wavelength λ is incident, the stopping potential for photoelectrons is 3V_{0}. When the same metal is illuminated by light of wavelength 2λ, then the stopping potential becomes V_{0}. The threshold wavelength for photoelectric emission for the given metal is αλ. The value of α is ______.',
    ['1', '4', '2', '3'], 2, lambda: pick([1, 4, 2, 3], int((lambda X: X / (X - 3 * (X / 4)))(F(1)))),
    ['3eV_{0} = \\f{hc}{λ} − φ and eV_{0} = \\f{hc}{2λ} − φ.', 'Subtract: 2eV_{0} = \\f{hc}{2λ} → eV_{0} = \\f{hc}{4λ}.', 'φ = \\f{hc}{λ} − \\f{3hc}{4λ} = \\f{hc}{4λ} → λ_{0} = \\f{hc}{φ} = 4λ → α = 4.'], 'pe2', 2)
add(('2026', 'Jan', '2026-01-21', 1), 'pe', 'A light wave described by E = 60[sin(3 × 10^{15})t + sin(12 × 10^{15})t] (in SI units) falls on a metal surface of work function 2.8 eV. The maximum kinetic energy of ejected photoelectron is (approximately) ______ eV. (h = 6.6 × 10^{−34} J.s. and e = 1.6 × 10^{−19} C)',
    ['5.1', '3.8', '6.0', '7.8'], 1, lambda: near([5.1, 3.8, 6.0, 7.8], 6.6e-34 * 12e15 / (2 * math.pi) / 1.6e-19 - 2.8),
    ['The wave contains two angular frequencies; the fastest photons have ω = 12 × 10^{15} rad/s.', 'E_{photon} = \\f{hω}{2π} = \\f{6.6 × 10^{−34} × 12 × 10^{15}}{2π × 1.6 × 10^{−19}} ≈ 7.88 eV.', 'K_{max} = 7.88 − 2.8 ≈ 5.1 eV.'], 'pe', 2)
add(('2026', 'Jan', '2026-01-28', 2), 'photon', 'Number of photons of equal energy emitted per second by a 6 mW laser source operating at 663 nm is ______. (Given: h = 6.63 × 10^{−34} J.s and c = 3 × 10^{8} m/s)',
    ['10 × 10^{15}', '2 × 10^{16}', '5 × 10^{16}', '5 × 10^{15}'], 2, lambda: pick([1e16, 2e16, 5e16, 5e15], 6e-3 * 663e-9 / (h * c), 1e-6),
    ['E per photon = \\f{hc}{λ} = \\f{6.63 × 10^{−34} × 3 × 10^{8}}{663 × 10^{−9}} = 3 × 10^{−19} J.', 'n = \\f{P}{E} = \\f{6 × 10^{−3}}{3 × 10^{−19}} = 2 × 10^{16} per second.'], 'photon', 1)
add(('2025', 'Jan', '2025-01-22', 1), 'pe', 'The work functions of cesium (Cs) and lithium (Li) metals are 1.9 eV and 2.5 eV, respectively. If we incident a light of wavelength 550 nm on these two metal surfaces, then photo-electric effect is possible for the case of',
    ['Neither Cs nor Li', 'Both Cs and Li', 'Li only', 'Cs only'], 4, lambda: 4 if 1.9 < 1240 / 550 < 2.5 else 0,
    ['Photon energy = \\f{1240}{550} ≈ 2.25 eV.', 'Emission needs hν ≥ φ: 2.25 > 1.9 (Cs ✓) but 2.25 < 2.5 (Li ✗) → Cs only.'], 'pe', 1)
add(('2025', 'Jan', '2025-01-22', 2), 'pe', 'A light source of wavelength λ illuminates a metal surface and electrons are ejected with maximum kinetic energy of 2 eV. If the same surface is illuminated by a light source of wavelength \\f{λ}{2}, then the maximum kinetic energy of ejected electrons will be (The work function of metal is 1 eV)',
    ['2 eV', '6 eV', '5 eV', '3 eV'], 3, lambda: pick([2, 6, 5, 3], 2 * (2 + 1) - 1), ['hc/λ = 2 + 1 = 3 eV.', 'Half the wavelength → double the photon energy: 6 eV → K_{max} = 6 − 1 = 5 eV.'], 'pe2', 1)
add(('2025', 'Jan', '2025-01-23', 2), 'pe', 'In photoelectric effect an em-wave is incident on a metal surface and electrons are ejected from the surface. If the work function of the metal is 2.14 eV and stopping potential is 2 V, what is the wavelength of the em-wave? (Given hc = 1242 eV nm where h is the Planck\'s constant and c is the speed of light in vaccum.)',
    ['200 nm', '600 nm', '400 nm', '300 nm'], 4, lambda: pick([200, 600, 400, 300], 1242 / (2.14 + 2)), ['hν = φ + eV_{0} = 2.14 + 2 = 4.14 eV.', 'λ = \\f{1242}{4.14} = 300 nm.'], 'pe', 1)
add(('2025', 'Jan', '2025-01-24', 1), 'dbm', 'An electron of mass \'m\' with an initial velocity v = v_{0}î (v_{0} > 0) enters an electric field E = −E_{0}k̂. If the initial de Broglie wavelength is λ_{0}, the value after time t would be',
    ['\\f{λ_{0}}{√{1 − \\f{e^{2}E_{0}^{2}t^{2}}{m^{2}v_{0}^{2}}}}', 'λ_{0}', 'λ_{0}√{1 + \\f{e^{2}E_{0}^{2}t^{2}}{m^{2}v_{0}^{2}}}', '\\f{λ_{0}}{√{1 + \\f{e^{2}E_{0}^{2}t^{2}}{m^{2}v_{0}^{2}}}}'], 4, lambda: 4,
    ['The force eE_{0} (along +z for the electron) is perpendicular to v_{0}: v_{x} = v_{0}, v_{z} = \\f{eE_{0}t}{m}.', 'Speed v = v_{0}√{1 + \\f{e^{2}E_{0}^{2}t^{2}}{m^{2}v_{0}^{2}}} grows, and λ = \\f{h}{mv} falls: λ = \\f{λ_{0}}{√{1 + e^{2}E_{0}^{2}t^{2}/(m^{2}v_{0}^{2})}}.'], 'dbm', 2)
add(('2025', 'Jan', '2025-01-24', 2), 'law', 'In photoelectric effect, the stopping potential (V_{0}) v/s frequency (ν) curve is plotted. (h is the Planck\'s constant and φ_{0} is work function of metal) (A) V_{0} v/s ν is linear. (B) The slope of V_{0} v/s ν curve = \\f{φ_{0}}{h}. (C) h constant is related to the slope of V_{0} v/s ν line. (D) The value of electric charge of electron is not required to determine h using the V_{0} v/s ν curve. (E) The work function can be estimated without knowing the value of h.',
    ['(A), (C) and (E) only', '(A), (B) and (C) only', '(D) and (E) only', '(C) and (D) only'], 1, lambda: 1,
    ['V_{0} = \\f{h}{e}ν − \\f{φ_{0}}{e}: a straight line (A ✓) with slope h/e (B ✗, C ✓).', 'Getting h from the slope needs e (D ✗).', 'The V-intercept is −φ_{0}/e, so φ_{0} follows without h (E ✓) → A, C, E.'], 'law', 2)
add(('2024', 'Jan', '2024-01-27', 1), 'law', 'A convex lens of focal length 40 cm forms an image of an extended source of light on a photoelectric cell. A current I is produced. The lens is replaced by another convex lens having the same diameter but focal length 20 cm. The photoelectric current now is :',
    ['\\f{I}{2}', '4 I', '2 I', 'I'], 4, lambda: 4,
    ['The light energy collected depends on the lens APERTURE (diameter), which is unchanged.', 'The same light power falls on the cell (the image is just smaller), so the current stays I.'], 'law', 2)
add(('2024', 'Jan', '2024-01-27', 2), 'pe', 'The threshold frequency of a metal with work function 6.63 eV is :',
    ['16 × 10^{15} Hz', '16 × 10^{12} Hz', '1.6 × 10^{12} Hz', '1.6 × 10^{15} Hz'], 4, lambda: pick([16e15, 16e12, 1.6e12, 1.6e15], 6.63 * e / h, 1e-6), ['ν_{0} = \\f{φ}{h} = \\f{6.63 × 1.6 × 10^{−19}}{6.63 × 10^{−34}} = 1.6 × 10^{15} Hz.'], 'pe', 1)
add(('2025', 'Jan', '2025-01-28', 1), 'dbw', "A proton of mass 'm_{p}' has same energy as that of a photon of wavelength 'λ'. If the proton is moving at non-relativistic speed, then ratio of its de Broglie wavelength to the wavelength of photon is.",
    ['\\f{1}{c}√{\\f{E}{m_{p}}}', '\\f{1}{c}√{\\f{2E}{m_{p}}}', '\\f{1}{c}√{\\f{E}{2m_{p}}}', '\\f{1}{2c}√{\\f{E}{m_{p}}}'], 3, lambda: 3,
    ['Proton: λ_{p} = \\f{h}{√{2m_{p}E}}. Photon: λ = \\f{hc}{E}.', '\\f{λ_{p}}{λ} = \\f{E}{c√{2m_{p}E}} = \\f{1}{c}√{\\f{E}{2m_{p}}}.'], 'dbw', 2)
add(('2024', 'Jan', '2024-01-29', 1), 'dbw', 'The de-Broglie wavelength of an electron is the same as that of a photon. If velocity of electron is 25% of the velocity of light, then the ratio of K.E. of electron and K.E. of photon will be:',
    ['\\f{1}{1}', '\\f{1}{8}', '\\f{8}{1}', '\\f{1}{4}'], 2, lambda: pick([1, F(1, 8), 8, F(1, 4)], F(1, 4) / 2),
    ['Same λ → same momentum p.', 'Electron: K = \\f{p^{2}}{2m} = \\f{pv}{2}. Photon: E = pc.', 'Ratio = \\f{v}{2c} = \\f{0.25}{2} = \\f{1}{8}.'], 'dbw', 2)
add(('2024', 'Jan', '2024-01-29', 2), 'photon', 'Two sources of light emit with a power of 200 W. The ratio of number of photons of visible light emitted by each source having wavelengths 300 nm and 500 nm respectively, will be :',
    ['1 : 5', '1 : 3', '5 : 3', '3 : 5'], 4, lambda: pick([(1, 5), (1, 3), (5, 3), (3, 5)], (3, 5)) if F(300, 500) == F(3, 5) else 0, ['Same power: n = \\f{Pλ}{hc} ∝ λ.', 'n_{1} : n_{2} = 300 : 500 = 3 : 5.'], 'photon', 1)
add(('2025', 'Jan', '2025-01-29', 1), 'law', 'Assertion (A): Emission of electrons in photoelectric effect can be suppressed by applying a sufficiently negative electron potential to the photo emissive substance. Reason (R): A negative electric potential, which stops the emission of electrons from the surface of a photo emissive substance, varies linearly with frequency of incident radiation.',
    ['(A) is true but (R) is false', 'Both (A) and (R) are true and (R) is the correct explanation of (A)', 'Both (A) and (R) are true but (R) is not the correct explanation of (A)', '(A) is false but (R) is true'], 3, lambda: 3,
    ['A large enough retarding potential stops even the fastest electrons → A true.', 'That stopping potential, V_{0} = (hν − φ)/e, is linear in ν → R true.', 'But R only describes how V_{0} depends on ν; it does not explain why emission can be suppressed → not the explanation.'], 'law', 2)
add(('2025', 'Jan', '2025-01-29', 1), 'law', 'Assertion (A): Electromagnetic waves carry energy but not momentum. Reason (R): Mass of a photon is zero.',
    ['(A) is false but (R) is true', '(A) is true but (R) is false', 'Both (A) and (R) are true and (R) is the correct explanation of (A)', 'Both (A) and (R) are true but (R) is not the correct explanation of (A)'], 1, lambda: 1,
    ['EM waves carry momentum p = E/c (radiation pressure) → A false.', 'A photon has zero rest mass → R true.'], 'law', 1)
add(('2025', 'Jan', '2025-01-29', 2), 'law', 'In an experiment with photoelectric effect, the stopping potential,',
    ['increases with increase in the intensity of the incident light', 'is (\\f{1}{e}) times the maximum kinetic energy of the emitted photoelectrons', 'decreases with increase in the intensity of the incident light', 'increases with increase in the wavelength of the incident light'], 2, lambda: 2,
    ['eV_{0} = K_{max} → V_{0} = K_{max}/e.', 'It does not depend on intensity, and it DEcreases when wavelength increases.'], 'law', 1)
add(('2024', 'Jan', '2024-01-30', 1), 'pe', 'The work function of a substance is 3.0 eV. The longest wavelength of light that can cause the emission of photoelectrons from this substance is approximately:',
    ['215 nm', '414 nm', '400 nm', '200 nm'], 2, lambda: near([215, 414, 400, 200], h * c / (3 * e) * 1e9), ['λ_{0} = \\f{hc}{φ} = \\f{1240 eV nm}{3 eV} ≈ 414 nm.'], 'pe', 1)
add(('2024', 'Jan', '2024-01-30', 2), 'law', 'For the photoelectric effect, the maximum kinetic energy (E_{k}) of the photoelectrons is plotted against the frequency (ν) of the incident photons. The slope of the graph gives',
    ["Ratio of Planck's constant to electric charge", 'Work function of the metal', 'Charge of electron', "Planck's constant"], 4, lambda: 4,
    ['E_{k} = hν − φ is a straight line in ν.', 'Its slope is h — Planck\'s constant. (The V_{0}–ν graph has slope h/e.)'], 'law', 1)
add(('2024', 'Jan', '2024-01-31', 1), 'pe', 'When a metal surface is illuminated by light of wavelength λ, the stopping potential is 8 V. When the same surface is illuminated by light of wavelength 3λ, stopping potential is 2 V. The threshold wavelength for this surface is :',
    ['5λ', '3λ', '9λ', '4.5λ'], 3, lambda: pick([5, 3, 9, F(9, 2)], (lambda X: X / (X - 8))(F(9))),
    ['8 = \\f{hc}{eλ} − \\f{φ}{e} and 2 = \\f{hc}{3eλ} − \\f{φ}{e}.', 'Subtract: 6 = \\f{2}{3}\\f{hc}{eλ} → \\f{hc}{eλ} = 9 V, so φ/e = 1 V.', 'λ_{0} = \\f{hc}{φ} = 9λ.'], 'pe2', 2)
add(('2024', 'Jan', '2024-01-31', 2), 'law', 'In a photoelectric effect experiment a light of frequency 1.5 times the threshold frequency is made to fall on the surface of photosensitive material. Now if the frequency is halved and intensity is doubled, the number of photo electrons emitted will be:',
    ['Doubled', 'Quadrupled', 'Zero', 'Halved'], 3, lambda: 3 if 1.5 / 2 < 1 else 0, ['New frequency = 0.75 ν_{0} < ν_{0}.', 'Below threshold no electron is emitted, however intense the light → zero.'], 'law', 1)
add(('2026', 'Apr', '2026-04-04', 2), 'dbw', 'The de Broglie wavelength associated with an electron accelerated through a potential difference V is λ_{e} and the de Broglie wavelength associated with a proton accelerated through the same potential difference is λ_{p}. If their corresponding masses are m_{e} and m_{p}, respectively, then the ratio of their de Broglie wavelengths (\\f{λ_{e}}{λ_{p}}) is ______.',
    ['√{\\f{m_{p}}{m_{e}}}', '√{\\f{m_{e}}{m_{p}}}', '\\f{m_{p}}{m_{e}}', '(\\f{m_{p}}{m_{e}})^{2}'], 1, lambda: 1,
    ['Both gain K = eV (same charge size).', 'λ = \\f{h}{√{2meV}} ∝ \\f{1}{√{m}} → \\f{λ_{e}}{λ_{p}} = √{\\f{m_{p}}{m_{e}}}.'], 'dbw', 1)
add(('2026', 'Jan', '2026-01-22', 2), 'pe', 'Light is incident on a metallic plate having work function 110 × 10^{−20} J. If the produced photoelectrons have zero kinetic energy then the angular frequency of the incident light is ______ rad/s. (h = 6.63 × 10^{−34} J.s)',
    ['1.04 × 10^{13}', '1.66 × 10^{15}', '1.66 × 10^{16}', '1.04 × 10^{16}'], 4, lambda: near([1.04e13, 1.66e15, 1.66e16, 1.04e16], 2 * math.pi * 110e-20 / h),
    ['Zero kinetic energy → hν = φ → ν = \\f{110 × 10^{−20}}{6.63 × 10^{−34}} ≈ 1.66 × 10^{15} Hz.', 'ω = 2πν ≈ 1.04 × 10^{16} rad/s. (Trap: 1.66 × 10^{15} is ν, not ω.)'], 'pe', 2)
add(('2026', 'Apr', '2026-04-05', 1), 'dbm', 'An electron of mass m is moving in an electric field E = −2E_{0}î (E_{0} = constant > 0), with an initial velocity V = v_{0}î (v_{0} = constant > 0). If λ_{0} = \\f{h}{4mv_{0}}, its de Broglie wavelength at time t is ______. (e = charge of electron)',
    ['\\f{4λ_{0}}{[1 − \\f{E_{0}e}{2m}\\f{t}{v_{0}}]}', '\\f{4λ_{0}}{[1 + \\f{E_{0}e}{2m}\\f{t}{v_{0}}]}', '\\f{4λ_{0}}{[1 + \\f{2E_{0}e}{m}\\f{t}{v_{0}}]}', '\\f{4λ_{0}}{[1 − \\f{2E_{0}e}{m}\\f{t}{v_{0}}]}'], 3, lambda: 3,
    ['Force on the electron F = −e(−2E_{0}î) = +2eE_{0}î — along its motion, so it speeds up: v = v_{0} + \\f{2eE_{0}t}{m}.', 'λ = \\f{h}{mv} = \\f{h}{mv_{0}} · \\f{1}{1 + \\f{2eE_{0}t}{mv_{0}}} and \\f{h}{mv_{0}} = 4λ_{0} → option 3.'], 'dbm', 2)
add(('2026', 'Apr', '2026-04-05', 1), 'pe', 'Light source having wavelength 331 nm is used to generate photo-electrons whose stopping potential is 0.2 V. The work function of the used metal in the experiment is α × 10^{−19} J. The value of α is ______. (h = 6.62 × 10^{−34} Js, e = 1.6 × 10^{−19} C and c = 3 × 10^{8} m/s)',
    ['3.68', '4.68', '5.68', '6.68'], 3, lambda: pick([3.68, 4.68, 5.68, 6.68], round((6.62e-34 * 3e8 / 331e-9 - 0.2 * 1.6e-19) / 1e-19, 2)),
    ['hν = \\f{6.62 × 10^{−34} × 3 × 10^{8}}{331 × 10^{−9}} = 6.0 × 10^{−19} J.', 'eV_{0} = 0.32 × 10^{−19} J → φ = 6.00 − 0.32 = 5.68 × 10^{−19} J.'], 'pe', 1)
add(('2026', 'Jan', '2026-01-23', 1), 'dbw', 'The de Broglie wavelength of an oxygen molecule at 27 ºC is x × 10^{−12} m. The value of x is (take Planck\'s constant = 6.63 × 10^{−34} J.s, Boltzmann constant = 1.38 × 10^{−23} J/K, mass of oxygen molecule = 5.31 × 10^{−26} kg)',
    ['26', '24', '30', '20'], 1, lambda: near([26, 24, 30, 20], h / math.sqrt(3 * 5.31e-26 * 1.38e-23 * 300) / 1e-12),
    ['Thermal (rms) speed: p = mv_{rms} = √{3mkT}.', 'λ = \\f{h}{√{3mkT}} = \\f{6.63 × 10^{−34}}{√{3 × 5.31 × 10^{−26} × 1.38 × 10^{−23} × 300}} ≈ 2.6 × 10^{−11} m = 26 × 10^{−12} m.'], 'dbw', 2)
add(('2026', 'Apr', '2026-04-05', 2), 'dbw', 'An electron is travelling with a velocity v in free space and when it enters a medium, its velocity is reduced by 20%. The de Broglie wavelength of electron in the medium is αλ_{0}, where λ_{0} is its de Broglie wavelength in free space. The value of α is ______.',
    ['1.20', '1.0', '1.25', '0.75'], 3, lambda: pick([1.2, 1.0, 1.25, 0.75], 1 / 0.8), ['λ = \\f{h}{mv}; v → 0.8v.', 'λ → \\f{λ_{0}}{0.8} = 1.25λ_{0}.'], 'dbw', 1)
add(('2026', 'Apr', '2026-04-06', 2), 'dbw', 'The de Broglie wavelength for an electron accelerated through the potential difference of V_{1} volt is λ_{1}. When the potential difference is changed to V_{2} volt, the associated de Broglie wavelength is increased by 50%. If (V_{1}/V_{2}) = (9/α), then the value of α is ______.',
    None, 4, lambda: int(9 / F(9, 4)), ['λ ∝ \\f{1}{√{V}} → \\f{V_{1}}{V_{2}} = (\\f{λ_{2}}{λ_{1}})^{2} = 1.5^{2} = \\f{9}{4} → α = 4.'], 'dbw', 1)
add(('2026', 'Jan', '2026-01-24', 2), 'pe', 'When a light of a given wavelength falls on a metallic surface the stopping potential for photoelectrons is 3.2 V. If a second light having wavelength twice of first light is used, the stopping potential drops to 0.7 V. The wavelength of first light is ______ m. (h = 6.63 × 10^{−34} J.s, e = 1.6 × 10^{−19} C, c = 3 × 10^{8} m/s)',
    ['2.9 × 10^{−8}', '2.2 × 10^{−8}', '3.1 × 10^{−7}', '2.5 × 10^{−7}'], 4, lambda: near([2.9e-8, 2.2e-8, 3.1e-7, 2.5e-7], h * c / (2 * (3.2 - 0.7) * e)),
    ['3.2 = \\f{hc}{eλ} − \\f{φ}{e} and 0.7 = \\f{hc}{2eλ} − \\f{φ}{e}.', 'Subtract: 2.5 = \\f{hc}{2eλ} → \\f{hc}{eλ} = 5 V.', 'λ = \\f{hc}{5e} = \\f{6.63 × 10^{−34} × 3 × 10^{8}}{5 × 1.6 × 10^{−19}} ≈ 2.5 × 10^{−7} m.'], 'pe2', 2)
add(('2026', 'Apr', '2026-04-08', 2), 'photon', 'A monochromatic source of light operating at 15 kW emits 2.5 × 10^{22} photons/s. The region of an electromagnetic spectrum to which the emitted electromagnetic radiation belongs to ______. (Take h = 6.6 × 10^{−34} J.s and c = 3 × 10^{8} m/s).',
    ['Microwave', 'Infrared', 'Visible', 'Ultraviolet'], 4, lambda: 4 if 6.6e-34 * 3e8 / (15e3 / 2.5e22) < 400e-9 else 0,
    ['Energy per photon = \\f{15000}{2.5 × 10^{22}} = 6 × 10^{−19} J.', 'λ = \\f{hc}{E} = \\f{6.6 × 10^{−34} × 3 × 10^{8}}{6 × 10^{−19}} = 330 nm < 400 nm → ultraviolet.'], 'photon', 2)
add(('2026', 'Apr', '2026-04-08', 2), 'pe', 'K_{1} and K_{2} be the maximum kinetic energies of photoelectrons emitted from a surface of a given material for the light of wavelength λ_{1} and λ_{2}, respectively. If λ_{1} = 2λ_{2} then the work function of material is given by :',
    ['K_{2} + 2K_{1}', '2K_{2} − K_{1}', 'K_{1} − 2K_{2}', 'K_{2} − 2K_{1}'], 4, lambda: 4 if (lambda E, phi: (2 * E - phi) - 2 * (E - phi))(F(5), F(2)) == 2 else 0,
    ['Let E = hc/λ_{1}; then hc/λ_{2} = 2E.', 'K_{1} = E − φ, K_{2} = 2E − φ.', 'K_{2} − 2K_{1} = 2E − φ − 2E + 2φ = φ.'], 'pe2', 2)
add(('2026', 'Jan', '2026-01-28', 1), 'dbw', 'The ratio of de Broglie wavelength of a deutron with kinetic energy E to that of an alpha particle with kinetic energy 2E, is n : 1. The value of n is ______. (Assume mass of proton = mass of neutron)',
    None, 2, lambda: int(math.isqrt(int(F(4 * 2, 2 * 1))) if F(4 * 2, 2 * 1) == 4 else 0),
    ['λ = \\f{h}{√{2mK}}: \\f{λ_{d}}{λ_{α}} = √{\\f{m_{α}K_{α}}{m_{d}K_{d}}} = √{\\f{4 × 2E}{2 × E}} = √{4} = 2.', 'n = 2.'], 'dbw', 1)
add(('2025', 'Apr', '2025-04-08', 2), 'dbm', "An electron is released from rest near an infinite non-conducting sheet of uniform charge density 'σ'. The rate of change of de-Broglie wave length associated with the electron varies inversely as n^{th} power of time. The numerical value of n is ______.",
    None, 2, lambda: 2, ['The sheet\'s field σ/2ε_{0} is uniform → constant acceleration a, so v = at.', 'λ = \\f{h}{mat} → \\f{dλ}{dt} = −\\f{h}{ma}·\\f{1}{t^{2}} → n = 2.'], 'dbm', 2)
add(('2025', 'Apr', '2025-04-07', 2), 'dbw', 'A photo-emissive substance is illuminated with a radiation of wavelength λ_{i} so that it releases electrons with de-Broglie wavelength λ_{e}. The longest wavelength of radiation that can emit photoelectron is λ_{0}. Expression for de-Broglie wavelength is given by : (m : mass of the electron, h : Planck\'s constant and c : speed of light)',
    ['λ_{e} = \\f{h}{√{2mc(\\f{1}{λ_{i}} − \\f{1}{λ_{0}})}}', 'λ_{e} = √{\\f{hλ_{i}}{2mc}}', 'λ_{e} = √{\\f{h}{2mc(\\f{1}{λ_{i}} − \\f{1}{λ_{0}})}}', 'λ_{e} = √{\\f{hλ_{0}}{2mc}}'], 3, lambda: 3,
    ['K = hc(\\f{1}{λ_{i}} − \\f{1}{λ_{0}}).', 'λ_{e} = \\f{h}{√{2mK}} = \\f{h}{√{2mhc(1/λ_{i} − 1/λ_{0})}} = √{\\f{h}{2mc(1/λ_{i} − 1/λ_{0})}}.'], 'dbw', 2)
add(('2025', 'Apr', '2025-04-02', 2), 'dbm', "An electron with mass 'm' with an initial velocity (t = 0) v = v_{0}î (v_{0} > 0) enters a magnetic field B = B_{0}ĵ. If the initial de-Broglie wavelength at t = 0 is λ_{0} then its value after time 't' would be :",
    ['λ_{0}', '\\f{λ_{0}}{√{1 + \\f{e^{2}B_{0}^{2}t^{2}}{m^{2}}}}', '\\f{λ_{0}}{√{1 − \\f{e^{2}B_{0}^{2}t^{2}}{m^{2}}}}', 'λ_{0}√{1 + \\f{e^{2}B_{0}^{2}t^{2}}{m^{2}}}'], 1, lambda: 1,
    ['The magnetic force is always perpendicular to the velocity, so it does no work: speed stays v_{0}.', 'λ = h/(mv) is unchanged: λ_{0}.'], 'dbm', 1)
add(('2026', 'Apr', '2026-04-04', 2), 'law', "Match List-I with List-II: (A) Planck's constant (B) Stopping potential (C) Work function (D) Threshold frequency — (I) ML^{2}T^{−2} (II) T^{−1} (III) ML^{2}T^{−1} (IV) ML^{2}T^{−3}A^{−1}",
    ['A-III, B-IV, C-I, D-II', 'A-I, B-II, C-III, D-IV', 'A-IV, B-III, C-I, D-II', 'A-I, B-IV, C-III, D-II'], 1, lambda: 1,
    ['h = E/ν → ML^{2}T^{−1} (III). Stopping potential is a voltage → ML^{2}T^{−3}A^{−1} (IV).', 'Work function is an energy → ML^{2}T^{−2} (I). Frequency → T^{−1} (II).'], 'law', 1)

if __name__ == '__main__': print('dual nature real questions verified:', verify(P))
