import sympy


def get_primes_summing_to_x(x):
    primes = list(sympy.primerange(1, x))
    primes = sorted(primes, reverse=True)
    prime_sum = 0
    prime_list = []

    for prime in primes:
        while prime_sum + prime**2 <= x:
            prime_sum += prime**2
            prime_list.append(prime)
            if prime_sum == x:
                return prime_list
    while prime_sum != x:
        prime_list.append(1)
        prime_sum += 1

    return prime_list


def calculate_prime_sum_component(x):
    prime_list = get_primes_summing_to_x(x)
    sum_of_squares = sum(p for p in prime_list)
    # if len(prime_list) > 3:
    """
    print("_________________________")
    print(f"{x=}")
    print(f"{prime_list=}")
    print(f"{sum_of_squares=}")
    print("_________________________")
    """
    return sum_of_squares, prime_list


def generate_unique_key(pixels_start: int, pixels_end: int, msg_length: int):
    pixels_range = (pixels_end - pixels_start)
    start_upper_bound = (pixels_range - msg_length) // 2
    end_lower_bound = start_upper_bound + msg_length

    # Digits 1-8: Midpoint of range [start, start_upper_bound]
    start_index = ((pixels_start + start_upper_bound) // 2)
    start_index_str = f"{start_index:08d}"

    # Digits 9-16: Sum of squares of primes summing to msg_length
    prime_component, primes_list = calculate_prime_sum_component(msg_length)
    print(f"{prime_component=} for {msg_length=}")
    prime_component_str = f"{prime_component:08d}"

    # Digits 17-24: Midpoint of range [end_lower_bound, pixels_end]
    end_index = ((end_lower_bound + pixels_end) // 2)
    end_index_str = f"{end_index:08d}"

    # Combine all parts into a 24-digit number
    key_str = f"{start_index_str}{prime_component_str}{end_index_str}"
    # Delete leading zeroes
    key_hex = key_str.lstrip('0')

    # print(f"Generated key: {key_hex}")
    return key_hex, primes_list


def parse_key(key_hex):
    # Add leading zeroes back if necessary
    key_hex = key_hex.zfill(24)

    # Extract each part of the key
    start_index_str = key_hex[:8]
    print(f"{start_index_str}")
    prime_component_str = key_hex[8:16]
    print(f"{prime_component_str}")
    end_index_str = key_hex[16:]
    print(f"{end_index_str}")

    # Convert each part back to its original form
    start_index = int(start_index_str, 16)
    prime_component = int(prime_component_str, 16)
    end_index = int(end_index_str, 16)

    prime_sum_possibilities = reverse_primes_sum(prime_component)
    if len(prime_sum_possibilities) == 1:
        msg_length = prime_sum_possibilities[0]
    else:
        print("ERROR")
        msg_length = prime_sum_possibilities

    # Calculate pixels_start, pixels_end
    pixels_range = end_index * 2 - start_index
    pixels_end = end_index + pixels_range // 2
    pixels_start = pixels_end - pixels_range

    # Return the parsed information as a dictionary
    parsed_info = {
        "start": pixels_start,
        "end": pixels_end,
        "msg_length": msg_length
    }

    return parsed_info


# Reverse engineer the primes sum function to calculate msg_length
def reverse_primes_sum(prime_sum):
    print(f"Trying to reverse {prime_sum=}")
    try_n_primes = 100
    prime_list = []
    for i in range(try_n_primes):
        prime_list.append(sympy.prime(1 + i))
    # print(f"List of primes: {prime_list}")
    # Step 1: Which prime has the largest square that is still smaller or equal to prime_sum

    x_possibilities = []

    # Test really low prime sums for ones
    for i in range(0, 4):
        if i == prime_sum:
            x_possibilities.append(i)

    largest_square_prime = 0
    k = 0
    # Get the largest prime possible
    while prime_list[k] ** 2 <= prime_sum:
        largest_square_prime = prime_list[k]
        for i in range(4):
            if largest_square_prime ** 2 + i == prime_sum:
                x_possibilities.append(largest_square_prime + i)
        k += 1
    print(f"Largest square prime found: {largest_square_prime} for y = {prime_sum}")
    current_prime_sum = largest_square_prime ** 2

    tested_primes = [largest_square_prime]
    b = k - 1
    while b >= 0:
        if prime_list[b] ** 2 + current_prime_sum <= prime_sum:
            current_prime_sum += prime_list[b] ** 2
            tested_primes.append(prime_list[b])
            for i in range(4):
                if current_prime_sum + i == prime_sum:
                    x_possibilities.append(sum(p for p in tested_primes) + i)
        else:
            b -= 1

    return x_possibilities

