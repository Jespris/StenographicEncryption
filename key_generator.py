import random
import sympy


class KeyUtils:
    def __init__(self, start_index: int, end_index: int, msg_length: int):
        self.pixels_start: int = start_index
        self.pixels_end: int = end_index
        self.msg_length: int = msg_length

        self.pixels_range = (self.pixels_end - self.pixels_start)
        self.start_upper_bound = (self.pixels_range - self.msg_length) // 2
        self.end_lower_bound = self.start_upper_bound + self.msg_length

    @staticmethod
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

    def calculate_prime_sum_component(self, x):
        prime_list = self.get_primes_summing_to_x(x)
        sum_of_squares = sum(p**2 for p in prime_list)
        result = 3 * sum_of_squares
        return result

    def generate_unique_key(self):
        # Digits 1-2: Midpoint of range [a, b], modulo 100
        start_index = ((self.pixels_start + self.start_upper_bound) // 2) % 100
        start_index_str = f"{start_index:02d}"

        # Digits 3-4: Transformation of x, modulo 100
        middle_number = (self.msg_length * 7 + 13) % 100  # Example transformation
        middle_number_str = f"{middle_number:02d}"

        # Digits 5-6: Sum of squares of primes summing to x, multiplied by 3, modulo 100
        prime_component = self.calculate_prime_sum_component(self.msg_length)
        prime_component_str = f"{prime_component:02d}"[-2:]  # Take the last two digits

        # Digits 7-8: Midpoint of range [c, d], modulo 100
        end_index = ((self.end_lower_bound + self.pixels_end) // 2) % 100
        end_index_str = f"{end_index:02d}"

        # Combine all parts into an 8-digit number
        key_str = f"{start_index_str}{middle_number_str}{prime_component_str}{end_index_str}"
        key_int = int(key_str)

        # Convert the 8-digit number to a hexadecimal string
        key_hex = f"{key_int:x}"

        print(f"Generated key: {key_hex}")
        return key_hex
