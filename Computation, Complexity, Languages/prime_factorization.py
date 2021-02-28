def prime_factors(n):
    i = 2
    factors = {}
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors[i] = factors[i] + 1 if factors.get(i) else 1
    if n > 1:
        factors[n] = factors[n] + 1 if factors.get(n) else 1
    return factors


def get_instructions(prog_num):
    godel_num = prog_num+1
    pr_facs = prime_factors(godel_num)



print(prime_factors(576))