# One-pass concept validation brief

## Purpose

Generate twelve complete banknote images in one pass per image: one recto and one verso for each denomination.

Do not create variants, alternate compositions, or extra exploratory images. Generate exactly the twelve files listed below.

## 1. Output list and exact dimensions

Use a base height of 1000 pixels. Vary the width according to the current euro denomination proportions.

| File               | Side       |           Size |
| ------------------ | ---------- | -------------: |
| `EUR005_recto.png` | €5 recto   | 1935 × 1000 px |
| `EUR005_verso.png` | €5 verso   | 1935 × 1000 px |
| `EUR010_recto.png` | €10 recto  | 1896 × 1000 px |
| `EUR010_verso.png` | €10 verso  | 1896 × 1000 px |
| `EUR020_recto.png` | €20 recto  | 1847 × 1000 px |
| `EUR020_verso.png` | €20 verso  | 1847 × 1000 px |
| `EUR050_recto.png` | €50 recto  | 1818 × 1000 px |
| `EUR050_verso.png` | €50 verso  | 1818 × 1000 px |
| `EUR100_recto.png` | €100 recto | 1909 × 1000 px |
| `EUR100_verso.png` | €100 verso | 1909 × 1000 px |
| `EUR200_recto.png` | €200 recto | 1987 × 1000 px |
| `EUR200_verso.png` | €200 verso | 1987 × 1000 px |

Every note fills its canvas exactly. Use straight edges, no outer paper margin, no rotation, no perspective distortion, no drop shadow, and no surrounding background.
