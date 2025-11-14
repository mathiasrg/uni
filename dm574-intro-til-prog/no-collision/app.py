def noColloision(n,k):
    s = 1.0
    i = 1
    while i < n:
        s = s* (k-i) / k
        i += 1
    return s


n = 4
k = 13
# Elementer foerst, pladser efter
print("Chance of no collision:",  noColloision(n, k))
print("Chance of collision:",  1 - noColloision(n, k))
