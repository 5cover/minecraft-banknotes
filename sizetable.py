baseheight = 938

notes = (
    (5, 60, 31),
    (10, 127, 67),
    (20, 133, 72),
    (50, 20, 11),
    (100, 147, 82),
    (200, 153, 82)
)

print(f"""
Scaling aspect ratios to a maximum height of {baseheight} pixels.

| File               | Side       | Aspect ratio | Scale by |           Size |
| ------------------ | ---------- | ------------ | -------- | -------------: |""")

for (value, width, height) in notes:
    scale = int(baseheight / height)
    size = (width * scale, height * scale)

    def row(side: str): return f"| {' | '.join([f'`EUR{value:0>3}_{side}.png`', f'€{value} {side}',
                                                f'{width}:{height}', str(scale), ' × '.join(map(str, size)) + ' px'])} |"
    print(row('recto'))
    print(row('verso'))

"""
| `EUR005_recto.png` | €5 recto   | 60:31        | 32       | 1920 × 992 px |
| `EUR005_verso.png` | €5 verso   | 60:31        | 32       | 1920 × 992 px |
| `EUR010_recto.png` | €10 recto  | 127:67       | 14       | 1778 × 938 px |
| `EUR010_verso.png` | €10 verso  | 127:67       | 14       | 1896 × 100 px |
| `EUR020_recto.png` | €20 recto  | 133:72       | 13       | 1847 × 100 px |
| `EUR020_verso.png` | €20 verso  | 133:72       | 13       | 1847 × 100 px |
| `EUR050_recto.png` | €50 recto  | 20:11        | 90       | 1818 × 100 px |
| `EUR050_verso.png` | €50 verso  | 20:11        | 90       | 1818 × 100 px |
| `EUR100_recto.png` | €100 recto | 147:82       | 12       | 1909 × 100 px |
| `EUR100_verso.png` | €100 verso | 147:82       | 12       | 1909 × 100 px |
| `EUR200_recto.png` | €200 recto | 153:82       | 12       | 1987 × 100 px |
| `EUR200_verso.png` | €200 verso | 153:82       | 12       | 1987 × 100 px |
"""
