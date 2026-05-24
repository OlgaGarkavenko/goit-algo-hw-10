import time
import random

COINS = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount: int) -> dict:
    """
    Жадібний алгоритм видачі решти.
    Складність: O(n), де n — кількість номіналів монет.
    """
    result = {}
    for coin in COINS:
        if amount >= coin:
            count = amount // coin
            result[coin] = count
            amount -= coin * count
    return result


def find_min_coins(amount: int) -> dict:
    """
    Алгоритм динамічного програмування для мінімальної кількості монет.
    Складність: O(amount * n), де n — кількість номіналів монет.
    """
    # dp[i] = мінімальна кількість монет для суми i
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    # coin_used[i] = остання монета, яку використали для суми i
    coin_used = [0] * (amount + 1)

    for i in range(1, amount + 1):
        for coin in COINS:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                coin_used[i] = coin

    # Відновлення результату
    result = {}
    current = amount
    while current > 0:
        coin = coin_used[current]
        result[coin] = result.get(coin, 0) + 1
        current -= coin

    return dict(sorted(result.items()))


def benchmark(amount: int):
    """Вимірює час виконання обох алгоритмів."""
    # Greedy
    start = time.perf_counter()
    greedy_result = find_coins_greedy(amount)
    greedy_time = time.perf_counter() - start

    # DP
    start = time.perf_counter()
    dp_result = find_min_coins(amount)
    dp_time = time.perf_counter() - start

    return greedy_result, greedy_time, dp_result, dp_time


if __name__ == "__main__":
    # Базовий приклад 
    print("=" * 55)
    print("Приклад для суми 113:")
    g = find_coins_greedy(113)
    d = find_min_coins(113)
    print(f"  Жадібний алгоритм : {g}")
    print(f"  Динамічне програм.: {d}")

    # Порівняння швидкості 
    print("\n" + "=" * 55)
    print(f"{'Сума':<12} {'Жадібний (мс)':<18} {'ДП (мс)':<15} {'Швидший'}")
    print("-" * 55)

    test_amounts = [113, 1_000, 10_000, 100_000, 500_000, 1_000_000]

    for amount in test_amounts:
        _, gt, _, dt = benchmark(amount)
        faster = "Жадібний" if gt < dt else "ДП"
        print(f"{amount:<12} {gt*1000:<18.4f} {dt*1000:<15.4f} {faster}")

    # Середній час по 50 запусках (для малих сум) 
    print("\n" + "=" * 55)
    print("Середній час (50 запусків, випадкові суми 1–10 000):")
    greedy_times, dp_times = [], []
    amounts = [random.randint(1, 10_000) for _ in range(50)]
    for a in amounts:
        _, gt, _, dt = benchmark(a)
        greedy_times.append(gt)
        dp_times.append(dt)

    print(f"  Жадібний : {sum(greedy_times)/len(greedy_times)*1000:.4f} мс")
    print(f"  ДП       : {sum(dp_times)/len(dp_times)*1000:.4f} мс")