
stream = [3, 1, 4, 1, 5, 9, 2, 6, 5]

hash_funcs = {
    'h1': lambda x: (2 * x + 1) % 32,
    'h2': lambda x: (3 * x + 7) % 32,
    'h3': lambda x: (4 * x) % 32
}

results = {}

for name, func in hash_funcs.items():
    values = [func(x) for x in stream]
    max_zeros = 0
    for val in values:
        count = 0
        for bit in bin(val)[::-1]:
            if bit == '1':
                break
            if bit == '0':
                count += 1
        if count > max_zeros:
            max_zeros = count
    estimate = 2 ** max_zeros
    results[name] = {
        'hashed': values,
        'max_zeros': max_zeros,
        'estimate': estimate
    }

for name in results:
    print(name)
    print("Hashed values:", results[name]['hashed'])
    print("Max trailing zeros:", results[name]['max_zeros'])
    print("Estimate:", results[name]['estimate'], "\n")

mean_estimate = sum(r['estimate'] for r in results.values()) / 3
print(f"Combined mean estimate: {mean_estimate:.2f}")











import random
import statistics

stream_8 = [1, 2, 3, 4, 5, 6, 7, 8] * 12 + [1, 2, 3, 4]
stream_3 = [10, 20, 30] * 33 + [10]

params = [(random.randint(1, 31), random.randint(0, 31)) for _ in range(50)]
hash_functions = [lambda x, a=a, b=b: (a * x + b) % 32 for a, b in params]

def run_estimate(stream, hash_functions):
    estimates = []
    for h in hash_functions:
        hashed_values = [h(x) for x in stream]
        max_trailing_zeros = 0
        for value in hashed_values:
            if value == 0:
                zeros = 5
            else:
                zeros = 0
                for bit in bin(value)[2:][::-1]:
                    if bit == '1':
                        break
                    if bit == '0':
                        zeros += 1
            if zeros > max_trailing_zeros:
                max_trailing_zeros = zeros
        estimates.append(2 ** max_trailing_zeros)
    return estimates

estimates_8 = run_estimate(stream_8, hash_functions)
estimates_3 = run_estimate(stream_3, hash_functions)

groups_8 = [sum(estimates_8[i:i+10]) / 10 for i in range(0, 50, 10)]
groups_3 = [sum(estimates_3[i:i+10]) / 10 for i in range(0, 50, 10)]

print("Stream with 8 distinct values:")
print("Mean:", round(sum(estimates_8) / 50, 2))
print("Median:", round(statistics.median(estimates_8), 2))
print("Group median:", round(statistics.median(groups_8), 2))

print("\nStream with 3 distinct values:")
print("Mean:", round(sum(estimates_3) / 50, 2))
print("Median:", round(statistics.median(estimates_3), 2))
print("Group median:", round(statistics.median(groups_3), 2))