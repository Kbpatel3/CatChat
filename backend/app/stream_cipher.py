######################################
# CS466 Project 3: Secure Communication
# Authors: Kaushal Patel and Zach Eanes
#
# Description:
#   This file that performs the encryption and decryption of a message using
#   a stream cipher done for bytes.
######################################


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