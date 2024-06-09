from sympy import nextprime

# New encoded sequence from next_output.txt
new_encoded_sequence = [205, 217, 198, 210, 250, 248, 104, 112, 192, 246, 104, 192, 216, 223, 101, 246, 192, 114, 211, 105, 114, 192, 114, 211, 104, 241, 104, 192, 105, 241, 104, 192, 222, 101, 241, 104, 192, 217, 102, 223, 104, 112, 192, 199, 244, 114, 192, 114, 211, 104, 192, 102, 222, 225, 101, 241, 114, 112, 192, 201, 101, 223, 80, 114, 192, 200, 101, 244, 223, 114, 192, 200, 116, 198, 198, 103, 103, 102, 101, 252]

# Function to decode the sequence
def decode_sequence(encoded_sequence):
    decoded_chars = []
    for num in encoded_sequence:
        # Find the original number by trying to subtract primes until it matches an ASCII value
        original_num = None
        for x in range(256):  # ASCII values range from 0 to 255
            if num == x + nextprime(x):
                original_num = x
                break
        if original_num is not None:
            decoded_chars.append(chr(original_num))
    return ''.join(decoded_chars)

# Decode the new sequence
new_decoded_flag = decode_sequence(new_encoded_sequence)
print(new_decoded_flag)
