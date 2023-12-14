import Crypto
from Crypto.Random import get_random_bytes


class StreamCipher:
    """
    This class is used to encrypt and decrypt messages using a stream cipher.
    """

    def __init__(self, key):
        """
        This function is the constructor for the StreamCipher class.
        Args:
            key: the key to be used for the stream cipher
        """
        self.key = key

    def generate_keystream(self, length):
        """
        This function generates a keystream of the given length.
        Args:
            length: the length of the keystream to be generated

        Returns:
            the keystream
        """
        keystream = bytearray()

        # loop until the keystream is the correct length
        while len(keystream) < length:
            keystream.extend(self.key)

        # return the key stream with only the specified length
        return keystream[:length]

    def encrypt(self, plaintext):
        """
        This function encrypts the given plaintext using the key.
        Args:
            plaintext: the text to be encrypted

        Returns:
            the ciphertext in byte representation
        """
        keystream = self.generate_keystream(len(plaintext))  # generate the keystream

        # XOR the plaintext and the keystream to get the ciphertext
        ciphertext = bytearray(p ^ k for p, k in zip(plaintext, keystream))

        # return the ciphertext in bytes
        return bytes(ciphertext)

    def decrypt(self, ciphertext):
        """
        This function decrypts the given ciphertext using the key.
        Args:
            ciphertext: the text to be decrypted

        Returns:
            the plaintext in byte representation
        """
        keystream = self.generate_keystream(len(ciphertext))  # generate the keystream

        # XOR the ciphertext and the keystream to get the plaintext
        plaintext = bytearray(c ^ k for c, k in zip(ciphertext, keystream))

        # return the plaintext in bytes
        return bytes(plaintext)

    def encrypt_string(self, plaintext):
        """
        Encrypts a string and returns the ciphertext in byte representation.
        Args:
            plaintext: the string to be encrypted
        Returns:
            the ciphertext in byte representation
        """
        plaintext_bytes = plaintext.encode('utf-8')  # Convert string to bytes
        return self.encrypt(plaintext_bytes)

    def decrypt_string(self, ciphertext):
        """
        Decrypts the given ciphertext and returns the plaintext as a string.
        Args:
            ciphertext: the ciphertext in byte representation to be decrypted
        Returns:
            the decrypted plaintext as a string
        """
        plaintext_bytes = self.decrypt(ciphertext)
        return plaintext_bytes.decode('utf-8')  # Convert bytes back to string


def test():
    key = Crypto.Random.get_random_bytes(32)
    cipher = StreamCipher(key)

    # Original message as a string
    message = "Hello, world!"
    encrypted_message = cipher.encrypt_string(message)
    decrypted_message = cipher.decrypt_string(encrypted_message)

    # Test output
    print("Original message:", message)
    print("Encrypted message:", encrypted_message)
    print("Decrypted message:", decrypted_message)


if __name__ == "__main__":
    test()
