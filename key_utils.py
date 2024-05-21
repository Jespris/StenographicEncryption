import sympy


def get_primes_summing_to_x(x):
    primes = list(sympy.primerange(1, x))
    primes = sorted(primes, reverse=True)
    prime_sum = 0
    prime_list = []

    for prime in primes:
        if prime_sum + prime <= x:
            prime_sum += prime
            prime_list.append(prime)
        if prime_sum == x:
            break

    return prime_list


def calculate_prime_sum_component(x):
    prime_list = get_primes_summing_to_x(x)
    sum_of_squares = sum(p**2 for p in prime_list)
    result = 3 * sum_of_squares
    return result


def generate_unique_key(pixels_start: int, pixels_end: int, msg_length: int):
    pixels_range = (pixels_end - pixels_start)
    start_upper_bound = (pixels_range - msg_length) // 2
    end_lower_bound = start_upper_bound + msg_length

    # Digits 1-8: Midpoint of range [start, start_upper_bound]
    start_index = ((pixels_start + start_upper_bound) // 2)
    start_index_str = f"{start_index:08d}"

    # Digits 9-16: Transformation of msg_length
    middle_number = (msg_length * 7 + 13)
    middle_number_str = f"{middle_number:08d}"

    # Digits 17-24: Sum of squares of primes summing to msg_length, multiplied by 3
    prime_component = calculate_prime_sum_component(msg_length)
    prime_component_str = f"{prime_component:08d}"

    # Digits 25-32: Midpoint of range [end_lower_bound, pixels_end]
    end_index = ((end_lower_bound + pixels_end) // 2)
    end_index_str = f"{end_index:08d}"

    # Combine all parts into a 32-digit number
    key_str = f"{start_index_str}{middle_number_str}{prime_component_str}{end_index_str}"
    key_int = int(key_str)

    # Convert the 32-digit number to a hexadecimal string
    key_hex = f"{key_int:032x}"
    # Delete leading zeroes
    key_hex = key_hex.lstrip('0')

    print(f"Generated key: {key_hex}")
    return key_hex


