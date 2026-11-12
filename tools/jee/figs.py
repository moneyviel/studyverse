"""Small SVG figures for questions that need a diagram (drawn by us, not copied)."""
def _r(x1, y, x2, label):   # zig-zag resistor between x1..x2 at height y
    m = (x1 + x2) / 2; z = ' '.join(f'{m - 18 + 6 * k},{y + (-6 if k % 2 else 6) if 0 < k < 6 else y}' for k in range(7))
    return f'<line x1="{x1}" y1="{y}" x2="{m - 18}" y2="{y}"/><polyline points="{z}" fill="none"/><line x1="{m + 18}" y1="{y}" x2="{x2}" y2="{y}"/><text x="{m}" y="{y - 12}" text-anchor="middle" stroke="none" fill="currentColor" font-size="13">{label}</text>'
def meter_bridge(left, right, a='P', b='R', cell=True):
    s = f'<svg viewBox="0 0 320 170" class="jx-fig" stroke="currentColor" stroke-width="1.8" fill="none" font-family="sans-serif">'
    s += _r(40, 30, 160, left) + _r(160, 30, 280, right)
    s += '<line x1="40" y1="30" x2="40" y2="110"/><line x1="280" y1="30" x2="280" y2="110"/><line x1="40" y1="110" x2="280" y2="110" stroke-width="3"/>'
    s += '<circle cx="160" cy="30" r="3" fill="currentColor"/><path d="M160 30 Q 175 70 140 108"/><circle cx="140" cy="110" r="3" fill="currentColor"/>'
    s += f'<text x="30" y="128" stroke="none" fill="currentColor" font-size="13">{a}</text><text x="282" y="128" stroke="none" fill="currentColor" font-size="13">{b}</text><text x="128" y="128" stroke="none" fill="currentColor" font-size="12">jockey</text>'
    if cell: s += '<line x1="40" y1="110" x2="40" y2="150"/><line x1="280" y1="110" x2="280" y2="150"/><line x1="40" y1="150" x2="150" y2="150"/><line x1="170" y1="150" x2="280" y2="150"/><line x1="150" y1="140" x2="150" y2="160"/><line x1="160" y1="145" x2="160" y2="155" stroke-width="3"/><line x1="160" y1="150" x2="170" y2="150"/>'
    return s + '</svg>'
def tetra_fig():
    A, B, T, C = (60, 150), (260, 150), (160, 20), (160, 105)
    s = '<svg viewBox="0 0 320 175" class="jx-fig" stroke="currentColor" stroke-width="1.8" fill="none" font-family="sans-serif">'
    for p, q in [(A, B), (B, T), (T, A), (A, C), (B, C), (T, C)]: s += f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}"/>'
    for p in (A, B, T, C): s += f'<circle cx="{p[0]}" cy="{p[1]}" r="4" fill="currentColor"/>'
    return s + '<text x="44" y="168" stroke="none" fill="currentColor" font-size="14">A</text><text x="264" y="168" stroke="none" fill="currentColor" font-size="14">B</text><text x="110" y="100" stroke="none" fill="currentColor" font-size="11">6 equal segments</text></svg>'
