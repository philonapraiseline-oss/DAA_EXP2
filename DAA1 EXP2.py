import random
import string

# Generate random text
def generate_text(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

# Naive String Matching
def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)
    comparisons = 0

    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1

    return comparisons

# KMP String Matching
def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m

    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)

    lps = compute_lps(pattern)

    i = 0
    j = 0
    comparisons = 0

    while i < n:
        comparisons += 1

        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == m:
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return comparisons

# Rabin-Karp String Matching
def rabin_karp(text, pattern):
    n = len(text)
    m = len(pattern)

    d = 256
    q = 101

    comparisons = 0

    h = 1
    for i in range(m - 1):
        h = (h * d) % q

    p_hash = 0
    t_hash = 0

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for i in range(n - m + 1):

        if p_hash == t_hash:
            for j in range(m):
                comparisons += 1
                if text[i + j] != pattern[j]:
                    break

        if i < n - m:
            t_hash = (d * (t_hash - ord(text[i]) * h) +
                      ord(text[i + m])) % q

            if t_hash < 0:
                t_hash += q

    return comparisons

# Main Program
text_length = 12000
pattern_lengths = [6, 12, 24, 48]

text = generate_text(text_length)

print("\nTEXT LENGTH =", text_length)
print("-" * 75)
print("{:<15}{:<20}{:<20}{:<20}".format(
    "Pattern", "Naive", "KMP", "Rabin-Karp"))
print("-" * 75)

for m in pattern_lengths:
    start = random.randint(0, text_length - m)
    pattern = text[start:start + m]

    print("{:<15}{:<20}{:<20}{:<20}".format(
        m,
        naive_search(text, pattern),
        kmp_search(text, pattern),
        rabin_karp(text, pattern)
    ))
