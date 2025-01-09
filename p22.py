from collections import defaultdict


def read_input():
    with open("p22.input.txt", "r") as f:
        return [int(l.strip()) for l in f.readlines()]


def mix(i: int, j: int) -> int:
    return i ^ j


def prune(i: int) -> int:
    return i % 16777216


def next_secret(s: int) -> int:
    s = prune(mix(s, s * 64))
    s = prune(mix(s, s // 32))
    return prune(mix(s, s * 2048))


def update_changes(
    changes: (int, int, int, int), new_change: int
) -> (int, int, int, int):
    _, a, b, c = changes
    return a, b, c, new_change


if __name__ == "__main__":
    total = 0
    change_prices = defaultdict(int)  # { (change_val_tuple): total_price }
    for seller, secret in enumerate(read_input()):
        changes = (0, 0, 0, 0)
        seen = set()
        for i in range(2000):
            prev_price = secret % 10
            secret = next_secret(secret)
            price = secret % 10
            change = price - prev_price
            changes = update_changes(changes, change)
            if i < 4 or changes in seen:
                continue
            seen.add(changes)
            change_prices[changes] += price
        total += secret
    print(total)
    print(max(change_prices.values()))
