import hashlib
import math
from array import array


class BloomFilter:
    def __init__(self, capacity: int, fp_rate: float):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if not 0 < fp_rate < 1:
            raise ValueError("fp_rate must be between 0 and 1")

        self._capacity = capacity
        self._fp_rate = fp_rate
        self._bit_array_size = max(
            1,
            math.ceil(-(capacity * math.log(fp_rate)) / (math.log(2) ** 2)),
        )
        self._num_hash_functions = max(
            2,
            round((self._bit_array_size / capacity) * math.log(2)),
        )
        self._bits = array("B", [0]) * ((self._bit_array_size + 7) // 8)

    @property
    def bit_array_size(self) -> int:
        return self._bit_array_size

    @property
    def num_hash_functions(self) -> int:
        return self._num_hash_functions

    def add(self, item: str) -> None:
        for index in self._hashes(item):
            self._set_bit(index)

    def contains(self, item: str) -> bool:
        return all(self._get_bit(index) for index in self._hashes(item))

    def _hashes(self, item: str):
        payload = item.encode("utf-8")
        hash1 = int.from_bytes(hashlib.md5(payload).digest(), "big")
        hash2 = int.from_bytes(hashlib.sha256(payload).digest(), "big")
        for i in range(self._num_hash_functions):
            yield (hash1 + i * hash2) % self._bit_array_size

    def _set_bit(self, index: int) -> None:
        byte_index, bit_index = divmod(index, 8)
        self._bits[byte_index] |= 1 << bit_index

    def _get_bit(self, index: int) -> bool:
        byte_index, bit_index = divmod(index, 8)
        return bool(self._bits[byte_index] & (1 << bit_index))


if __name__ == "__main__":
    bf = BloomFilter(capacity=1000, fp_rate=0.01)

    words = ["apple", "banana", "cherry", "date", "elderberry"]
    for word in words:
        bf.add(word)
    for word in words:
        assert bf.contains(word), f"False negative: {word}"

    import random
    import string

    random.seed(42)
    added = set()
    for _ in range(1000):
        word = "".join(random.choices(string.ascii_lowercase, k=8))
        bf.add(word)
        added.add(word)

    fp_count = 0
    checked = 0
    while checked < 1000:
        word = "".join(random.choices(string.ascii_lowercase, k=10))
        if word in added:
            continue
        checked += 1
        if bf.contains(word):
            fp_count += 1

    assert bf.bit_array_size > 0
    assert bf.num_hash_functions >= 2
    assert fp_count / checked < 0.05
    print("All tests passed")
