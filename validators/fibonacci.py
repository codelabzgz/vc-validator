from typing import List


def is_fibonacci_sequence(sequence: List[int]) -> bool:
    if len(sequence) < 3:
        return False  # Una secuencia de Fibonacci válida necesita al menos 3 números

    for i in range(2, len(sequence)):
        if sequence[i] != sequence[i-1] + sequence[i-2]:
            return False

    return True
