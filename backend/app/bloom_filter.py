"""
Bloom filter for checking if an item is in a set. It can also add items to the set.

Note: We researched and found that using random prime numbers for the default hash values is a good practice.
      We also found that multiplying the hash by a random prime number is a good practice.

Sources:
https://www.baeldung.com/cs/bloom-filter

"""

# Constants
ZERO = 0
ONE = 1


class BloomFilter:
    """
    Bloom filter class that uses three different hash functions to check if an item is in a set. It can also add items
    to the set.
    """

    def __init__(self, size, hash_funcs):
        """
        Initializes the bloom filter.
        :param size: The size of the bloom filter
        :param hash_funcs: The hash functions to be used
        """
        self.size = size
        self.bit_array = [ZERO] * size
        self.hash_funcs = hash_funcs

    def add(self, item):
        """
        Adds an item to the set.
        :param item: The item to be added
        :return: None
        """
        for hash_func in self.hash_funcs:
            position = hash_func(item) % self.size
            self.bit_array[position] = ONE

    def check(self, item):
        """
        Checks if an item is in the set.
        :param item: The item to be checked
        :return: True if the item is in the set, False otherwise
        """
        return all(self.bit_array[hash_func(item) % self.size] == ONE for hash_func in self.hash_funcs)


# Three hash functions to use for the bloom filter
def hash1(s):
    """
    Hash function 1. It is used for the bloom filter.
    :param s: The string to be hashed
    :return: The hash of the string
    """
    # The default value of the hash (Random prime number)
    hash = 0

    # Loop through each character in the string
    for character in s:
        # Update the hash
        hash = (hash << 5) - hash + ord(character)

    # Return the hash
    return abs(hash)


def hash2(s):
    """
    Hash function 2. It is used for the bloom filter.
    :param s: The string to be hashed
    :return: The hash of the string
    """
    # The default value of the hash (Random prime number)
    hash = 5381

    # Loop through each character in the string
    for character in s:
        # Update the hash
        hash = (hash * 33) ^ ord(character)

    # Return the hash
    return abs(hash)


def hash3(s):
    """
    Hash function 3. It is used for the bloom filter.
    :param s: The string to be hashed
    :return: The hash of the string
    """

    # The default value of the hash (Random prime number)
    hash = 7

    # Loop through each character in the string
    for character in s:
        # Update the hash
        hash = hash * 31 + ord(character)

    # Return the hash
    return abs(hash)


def username_bloom_filter():
    """
    This function creates a bloom filter for the usernames that are blacklisted.
    :return: The bloom filter
    """
    # Create a bloom filter with the three hash functions and the size of the bits to be 100
    # Function to find optimal size of bit array (m = -(n * lg(p)) / (lg(2)^2) where n is the number of items and p is the
    # probability of false positives)
    bloom_filter = BloomFilter(100, [hash1, hash2, hash3])

    # Add blacklisted usernames
    with open("bannedWords.txt") as f:
        for line in f:
            bloom_filter.add(line.strip())

    # Return the bloom filter with the blacklisted usernames
    return bloom_filter
