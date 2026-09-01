den = [31, 67, 72, 11, 82]

x = range(max(den), 1000)
error = [sum(height % d for d in den) for height in x]

if False:
    import matplotlib.pyplot as plt
    plt.xlabel("Height")
    plt.ylabel("Error")
    plt.plot(x, error)
    plt.show()

sortederror = sorted(zip(x, error, strict=True), key=lambda i: i[1] / i[0])
for e in sortederror[:10]:
    print(' | '.join(map(str, e)))
