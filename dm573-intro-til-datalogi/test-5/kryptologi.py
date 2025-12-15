# 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97


"""
RSA Cryptography Exam Helper Functions
========================================
Based on DM573 course materials for cryptography exam preparation.
"""

import math
from typing import Tuple, List, Optional

# ============================================================================
# BASIC NUMBER THEORY FUNCTIONS
# ============================================================================

def gcd(a: int, b: int) -> int:
    """
    Calculate Greatest Common Divisor using Euclidean Algorithm.

    Parameters:
    - a (int): First integer
    - b (int): Second integer

    Returns:
    - int: Greatest common divisor of a and b

    Used for:
    - Checking if gcd(e, N') = 1 when selecting RSA keys
    - Exercise I.2: Finding multiplicative inverses
    - Verifying RSA key validity (Exercise I.3)

    Similar to: Slide 30 - Euclidean Algorithm example with gcd(75, 42)

    Example: gcd(75, 42) returns 3
    """
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean Algorithm - finds gcd and coefficients s, t.

    Parameters:
    - a (int): First integer
    - b (int): Second integer

    Returns:
    - Tuple[int, int, int]: (gcd, s, t) where s*a + t*b = gcd

    Used for:
    - Finding multiplicative inverse d in RSA (Exercise I.5b, I.9a)
    - Solving e*d ≡ 1 (mod N')

    Similar to: Slide 30 - Extended Euclidean Algorithm example
    Example from slides: gcd(75,42) = 3 = -5*75 + 9*42
                        returns (3, -5, 9)
    """
    if b == 0:
        return a, 1, 0

    gcd_val, s1, t1 = extended_gcd(b, a % b)
    s = t1
    t = s1 - (a // b) * t1

    return gcd_val, s, t


def mod_inverse(e: int, n: int) -> Optional[int]:
    """
    Find multiplicative inverse of e modulo n.

    Parameters:
    - e (int): The number to find the inverse of
    - n (int): The modulus

    Returns:
    - int: d such that (e * d) mod n = 1
    - None: if inverse doesn't exist (when gcd(e,n) ≠ 1)

    Used for:
    - Finding secret key d from public key e (Exercise I.5b, I.9a)
    - Exercise I.2: "Is one of these the multiplicative inverse of 49 mod 221?"

    Similar to: Slide 29 - Finding d such that e*d mod N' = 1

    Example: mod_inverse(3, 40) returns 27 because (3 * 27) mod 40 = 1
    """
    gcd_val, s, t = extended_gcd(e, n)

    if gcd_val != 1:
        return None  # Inverse doesn't exist

    # s*e + t*n = 1, so s*e ≡ 1 (mod n)
    return s % n


# ============================================================================
# MODULAR EXPONENTIATION
# ============================================================================

def fast_mod_exp(a: int, k: int, n: int, count_ops: bool = False) -> Tuple[int, int, int]:
    """
    Fast Modular Exponentiation: compute a^k mod n efficiently.

    Parameters:
    - a (int): Base
    - k (int): Exponent
    - n (int): Modulus
    - count_ops (bool): If True, counts odd/even cases during recursion

    Returns:
    - Tuple[int, int, int]: (result, odd_count, even_count)
      * result: a^k mod n
      * odd_count: number of times "k is odd" case encountered (0 if count_ops=False)
      * even_count: number of times "k is even" case encountered (0 if count_ops=False)

    Note: Does NOT count base cases k=0 and k=1 as per exercise instructions

    Used for:
    - RSA encryption: m^e mod N (Exercise I.1b, I.5a, I.9b)
    - RSA decryption: c^d mod N (Exercise I.9c)
    - Counting odd/even cases in recursion (Exercise I.5a, I.9b, I.9c)

    Similar to: Slide 27 - Exp(a, k, n) algorithm

    Example: fast_mod_exp(8, 3, 55, count_ops=True)
             returns (17, 2, 0) meaning 8^3 mod 55 = 17 with 2 odd cases
    """
    if count_ops:
        return _fast_mod_exp_with_count(a, k, n)
    else:
        return pow(a, k, n), 0, 0


def _fast_mod_exp_with_count(a: int, k: int, n: int) -> Tuple[int, int, int]:
    """Helper function that counts odd/even cases during recursion."""
    odd_count = 0
    even_count = 0

    def exp_recursive(base: int, exp: int) -> int:
        nonlocal odd_count, even_count

        # Base cases (don't count these)
        if exp == 0:
            return 1
        if exp == 1:
            return base % n

        # Recursive cases (count these)
        if exp % 2 == 1:  # Odd case
            odd_count += 1
            return (base * exp_recursive(base, exp - 1)) % n
        else:  # Even case
            even_count += 1
            c = exp_recursive(base, exp // 2)
            return (c * c) % n

    result = exp_recursive(a, k)
    return result, odd_count, even_count


# ============================================================================
# RSA KEY GENERATION
# ============================================================================

def factor_n(N: int) -> Optional[Tuple[int, int]]:
    """
    Factor N into two primes p and q (naive approach).
    Only practical for small N used in exercises.

    Parameters:
    - N (int): The number to factor (should be product of two primes)

    Returns:
    - Tuple[int, int]: (p, q) where N = p * q
    - None: if N cannot be factored into two factors

    Used for:
    - Exercise I.5b: "you would know that p=37 and q=41"
    - Finding p and q to compute secret key d

    Similar to: Slide 20 - Factor(N) algorithm
    Warning: This is exponential time, only use for exam-sized numbers!

    Example: factor_n(1517) returns (37, 41) because 1517 = 37 * 41
    """
    for i in range(2, int(math.sqrt(N)) + 1):
        if N % i == 0:
            return i, N // i
    return None


def find_rsa_secret_key(N: int, e: int, p: int, q: int) -> Optional[int]:
    """
    Find RSA secret key d given N, e, p, and q.

    Parameters:
    - N (int): RSA modulus (should equal p * q)
    - e (int): Public exponent
    - p (int): First prime factor of N
    - q (int): Second prime factor of N

    Returns:
    - int: Secret key d such that (e * d) mod (p-1)(q-1) = 1
    - None: if gcd(e, (p-1)(q-1)) ≠ 1 (invalid e)

    Used for:
    - Exercise I.5b: Find d given N=1517, e=13, p=37, q=41
    - Exercise I.9a: Find d given N=1517, e=17, p=37, q=41

    Similar to: Slide 13 - RSA key generation
    Computes N' = (p-1)*(q-1), then finds d such that e*d ≡ 1 (mod N')

    Example: find_rsa_secret_key(1517, 13, 37, 41) returns 937
    """
    N_prime = (p - 1) * (q - 1)

    # Check requirement: gcd(e, N') = 1
    if gcd(e, N_prime) != 1:
        return None

    # Find d such that e*d ≡ 1 (mod N')
    d = mod_inverse(e, N_prime)
    return d


def verify_rsa_keys(N: int, e: int, d: int) -> bool:
    """
    Verify if (N,e) and (N,d) form valid RSA key pair.

    Parameters:
    - N (int): RSA modulus
    - e (int): Public exponent
    - d (int): Secret exponent

    Returns:
    - bool: True if keys are valid, False otherwise

    Used for:
    - Exercise I.3: "Which set of PK and SK is valid?"

    Similar to: Slide 13 - RSA requirements
    Checks:
    1. N = p*q for primes p, q
    2. gcd(e, (p-1)*(q-1)) = 1
    3. e*d ≡ 1 (mod (p-1)*(q-1))

    Example: verify_rsa_keys(55, 3, 27) returns True (valid RSA keys)
             verify_rsa_keys(91, 37, 23) returns False (invalid)
    """
    # Try to factor N
    factors = factor_n(N)
    if not factors:
        return False

    p, q = factors

    # Check if p and q are prime (basic check)
    if not is_prime_trial(p) or not is_prime_trial(q):
        return False

    N_prime = (p - 1) * (q - 1)

    # Check gcd(e, N') = 1
    if gcd(e, N_prime) != 1:
        return False

    # Check e*d ≡ 1 (mod N')
    if (e * d) % N_prime != 1:
        return False

    return True


# ============================================================================
# RSA ENCRYPTION/DECRYPTION
# ============================================================================

def rsa_encrypt(m: int, N: int, e: int, count_ops: bool = False) -> Tuple[int, int, int]:
    """
    RSA Encryption: Encrypt message m with public key (N, e).

    Parameters:
    - m (int): Message to encrypt (must be 0 ≤ m < N)
    - N (int): RSA modulus (part of public key)
    - e (int): Public exponent (part of public key)
    - count_ops (bool): If True, counts odd/even cases during exponentiation

    Returns:
    - Tuple[int, int, int]: (ciphertext, odd_count, even_count)
      * ciphertext: encrypted message c = m^e mod N
      * odd_count: number of odd cases (0 if count_ops=False)
      * even_count: number of even cases (0 if count_ops=False)

    Used for:
    - Exercise I.1: "Which is the RSA encryption of message 43?"
    - Exercise I.5a: "Encrypt the message m=43"
    - Exercise I.9b: "Try encrypting 423"

    Similar to: Slide 13 - Encrypt(m, PK) = m^e mod N

    Example: rsa_encrypt(43, 1517, 13, count_ops=True)
             returns (1056, ..., ...) for ciphertext with operation counts
    """
    return fast_mod_exp(m, e, N, count_ops)


def rsa_decrypt(c: int, N: int, d: int, count_ops: bool = False) -> Tuple[int, int, int]:
    """
    RSA Decryption: Decrypt ciphertext c with secret key (N, d).

    Parameters:
    - c (int): Ciphertext to decrypt
    - N (int): RSA modulus (part of secret key)
    - d (int): Secret exponent (part of secret key)
    - count_ops (bool): If True, counts odd/even cases during exponentiation

    Returns:
    - Tuple[int, int, int]: (plaintext, odd_count, even_count)
      * plaintext: decrypted message m = c^d mod N
      * odd_count: number of odd cases (0 if count_ops=False)
      * even_count: number of even cases (0 if count_ops=False)

    Used for:
    - Exercise I.9c: "Decrypt the number obtained above"
    - Verifying encryption/decryption works correctly

    Similar to: Slide 13 - Decrypt(c, SK) = c^d mod N

    Example: rsa_decrypt(1056, 1517, 937, count_ops=True)
             returns (43, ..., ...) for original message with operation counts
    """
    return fast_mod_exp(c, d, N, count_ops)


# ============================================================================
# PRIMALITY TESTING
# ============================================================================

def is_prime_trial(n: int) -> bool:
    """
    Simple trial division primality test.
    Only use for small numbers in exercises.

    Parameters:
    - n (int): Number to test for primality

    Returns:
    - bool: True if n is prime, False if composite

    Used for:
    - Verifying small primes in exercises
    - Exercise II.3: Identifying prime/composite numbers

    Similar to: Slide 34 - CheckPrime(n) algorithm

    Example: is_prime_trial(11) returns True
             is_prime_trial(15) returns False
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False

    return True


def miller_rabin_test(n: int, a: int) -> Tuple[bool, str]:
    """
    Miller-Rabin primality test for a single witness a.

    Parameters:
    - n (int): Number to test for primality
    - a (int): Witness value (usually 1 ≤ a ≤ n-1)

    Returns:
    - Tuple[bool, str]: (is_probably_prime, message)
      * is_probably_prime: True if n is probably prime for this witness
      * message: Description of what happened during the test

    Used for:
    - Exercise II.3: "Run Miller-Rabin test on 11, 15, and 561"
    - Understanding Fermat test vs. full Miller-Rabin

    Similar to: Slides 36-38 - Miller-Rabin algorithm

    Example from slides:
    - miller_rabin_test(561, 2) returns (False, "Found square root...")
    - miller_rabin_test(561, 50) returns (True, "Passed...") [false negative]

    Note: If False is returned, message tells which line detected composite.
          If True is returned, n is probably prime for this witness a.
    """
    if n < 2:
        return False, "n < 2"
    if n == 2:
        return True, "n = 2 is prime"
    if n % 2 == 0:
        return False, "n is even"

    # Write n-1 as 2^s * m where m is odd
    s = 0
    m = n - 1
    while m % 2 == 0:
        s += 1
        m //= 2

    # First check: Fermat test a^(n-1) mod n = 1
    x = pow(a, n - 1, n)
    if x != 1:
        return False, f"Fermat test failed: {a}^{n-1} mod {n} = {x} ≠ 1"

    # Now check the sequence: a^m, a^(2m), a^(4m), ..., a^(n-1)
    # Looking for square roots of 1 that aren't ±1
    x = pow(a, m, n)

    if x == 1 or x == n - 1:
        return True, f"Passed: {a}^{m} mod {n} = {x}"

    for i in range(s - 1):
        x = pow(x, 2, n)

        if x == n - 1:
            return True, f"Passed: found {n-1} at iteration {i+1}"

        if x == 1:
            return False, f"Found square root of 1 that isn't ±1 at iteration {i+1}"

    return False, f"Never found {n-1}, ended with {x}"


def miller_rabin_multiple(n: int, witnesses: List[int]) -> dict:
    """
    Run Miller-Rabin test with multiple witnesses.

    Parameters:
    - n (int): Number to test for primality
    - witnesses (List[int]): List of witness values to test

    Returns:
    - dict: Results for each witness, structured as:
            {witness_a: {'probably_prime': bool, 'message': str}, ...}

    Used for:
    - Exercise II.3: Testing with multiple values of a
    - Understanding which witnesses detect compositeness

    Example: miller_rabin_multiple(561, [2, 3, 50])
             returns results showing which witnesses detect 561 as composite
    """
    results = {}
    for a in witnesses:
        is_probably_prime, message = miller_rabin_test(n, a)
        results[a] = {
            'probably_prime': is_probably_prime,
            'message': message
        }
    return results


# ============================================================================
# ADDITIONAL HELPERS
# ============================================================================

def find_square_roots_of_1(n: int) -> List[int]:
    """
    Find all square roots of 1 modulo n.
    (Numbers x where x^2 ≡ 1 (mod n) and 0 ≤ x < n)

    Parameters:
    - n (int): The modulus

    Returns:
    - List[int]: All values x where 0 ≤ x < n and x^2 mod n = 1

    Used for:
    - Exercise II.2: "Find four different square roots of 1 modulo 143"

    Similar to: Slide 36 - Theorem about square roots of 1
    "If n is composite with two distinct factors, x^2 mod n = 1
     implies at least four different values for x mod n"

    Example from slides: find_square_roots_of_1(15) returns [1, 4, 11, 14]
                        find_square_roots_of_1(143) returns 4 values
    """
    roots = []
    for x in range(n):
        if (x * x) % n == 1:
            roots.append(x)
    return roots


def check_gcd_requirement(e: int, p: int, q: int) -> bool:
    """
    Check if gcd(e, (p-1)(q-1)) = 1 for RSA.

    Parameters:
    - e (int): Proposed public exponent
    - p (int): First prime
    - q (int): Second prime

    Returns:
    - bool: True if gcd(e, (p-1)(q-1)) = 1, False otherwise

    Used for:
    - Exercise II.1: "Why is gcd(e, (p-1)(q-1)) = 1 necessary?"
    - Finding counterexamples where gcd ≠ 1

    Similar to: Slide 13 - RSA requirement

    Example: check_gcd_requirement(3, 5, 11) returns True (gcd(3, 40) = 1)
             check_gcd_requirement(10, 5, 11) returns False (gcd(10, 40) = 10)
    """
    N_prime = (p - 1) * (q - 1)
    return gcd(e, N_prime) == 1


def is_carmichael_number(n: int) -> bool:
    """
    Check if n is a Carmichael number.
    (Composite n where a^(n-1) ≡ 1 (mod n) for all a coprime to n)

    Parameters:
    - n (int): Number to check

    Returns:
    - bool: True if n is a Carmichael number, False otherwise

    Used for:
    - Exercise II.3: Understanding 561 (a Carmichael number)

    Similar to: Slide 36 - "561 = 3·11·17 is a Carmichael number"

    Note: This tests only a limited set of witnesses (up to 100),
          so it's a heuristic check, not a complete verification.

    Example: is_carmichael_number(561) returns True
             is_carmichael_number(15) returns False
    """
    if is_prime_trial(n):
        return False

    # Check Fermat's test for several values
    for a in range(2, min(n, 100)):
        if gcd(a, n) == 1:
            if pow(a, n - 1, n) != 1:
                return False

    return True
