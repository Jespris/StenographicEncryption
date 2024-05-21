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
    sum_of_squares = sum(p for p in prime_list) * len(prime_list) * 31 * x
    # if len(prime_list) > 3:
    print("_________________________")
    print(f"{x=}")
    print(f"{prime_list=}")
    print(f"{sum_of_squares=}")
    print("_________________________")
    return sum_of_squares, prime_list


def generate_unique_key(pixels_start: int, pixels_end: int, msg_length: int):
    pixels_range = (pixels_end - pixels_start)
    start_upper_bound = (pixels_range - msg_length) // 2
    end_lower_bound = start_upper_bound + msg_length

    # Digits 1-8: Midpoint of range [start, start_upper_bound]
    start_index = ((pixels_start + start_upper_bound) // 2)
    start_index_str = f"{start_index:08d}"

    # Digits 9-16: Sum of squares of primes summing to msg_length, multiplied by 3
    prime_component, primes_list = calculate_prime_sum_component(msg_length)
    prime_component_str = f"{prime_component:08d}"

    # Digits 17-24: Midpoint of range [end_lower_bound, pixels_end]
    end_index = ((end_lower_bound + pixels_end) // 2)
    end_index_str = f"{end_index:08d}"

    # Combine all parts into a 24-digit number
    key_str = f"{start_index_str}{prime_component_str}{end_index_str}"
    key_int = int(key_str)

    # Convert the 24-digit number to a hexadecimal string
    key_hex = f"{key_int:024x}"
    # Delete leading zeroes
    key_hex = key_hex.lstrip('0')

    # print(f"Generated key: {key_hex}")
    return key_hex, primes_list


def parse_key(key_hex):
    # Add leading zeroes back if necessary
    key_hex = key_hex.zfill(24)

    # Extract each part of the key
    start_index_str = key_hex[:8]
    prime_component_str = key_hex[8:16]
    end_index_str = key_hex[16:]

    # Convert each part back to its original form
    start_index = int(start_index_str, 16)
    prime_component = int(prime_component_str, 16)
    end_index = int(end_index_str, 16)

    # Reverse engineer the primes sum function to calculate msg_length
    def reverse_primes_sum(prime_sum):
        try_n_primes = 1000
        prime_list = []
        for i in range(try_n_primes):
            prime_list.append(sympy.prime(1 + i))
        # Step 1: Which prime has the largest square that is still smaller or equal to prime_sum
        largest_square_prime = 0
        for k in range(try_n_primes - 1, -1, -1):
            if prime_list[k]**2 <= prime_sum:
                largest_square_prime = prime_list[k]
                if largest_square_prime ** 2 == prime_sum:
                    return largest_square_prime
                break
        # Step 2: Try all combinations of squared primes that are before index (try_n_primes - k) in prime_list
        # This step has time complexity n! Worst case up to n = 999 => 999! = 4.023872601*10^2564 which is nice lol.
        # In reality probably n < 10

    msg_length = reverse_primes_sum(prime_component // 3)

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


