import numpy as np
import scipy.integrate as spi
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Функція та межі ──────────────────────────────────────────────────────────
def f(x):
    return x ** 2

A, B = 0, 2          # межі інтегрування
N_SAMPLES = 100_000  # кількість точок Монте-Карло

# ── 1. Метод Монте-Карло ──────────────────────────────────────────────────────
np.random.seed(42)

x_rand = np.random.uniform(A, B, N_SAMPLES)
y_max  = f(B)                                # максимум f(x) на [A, B]
y_rand = np.random.uniform(0, y_max, N_SAMPLES)

# Точки під кривою
under = y_rand <= f(x_rand)

# Площа прямокутника × частка точок під кривою
rect_area   = (B - A) * y_max
mc_result   = rect_area * under.sum() / N_SAMPLES

# ── 2. Аналітичний результат ─────────────────────────────────────────────────
# ∫₀² x² dx = [x³/3]₀² = 8/3
analytic_result = (B**3 - A**3) / 3

# ── 3. SciPy quad ────────────────────────────────────────────────────────────
quad_result, quad_error = spi.quad(f, A, B)

# ── 4. Виведення результатів ─────────────────────────────────────────────────
print("=" * 50)
print(f"Метод Монте-Карло ({N_SAMPLES:,} точок): {mc_result:.6f}")
print(f"Аналітично (x³/3):                    {analytic_result:.6f}")
print(f"SciPy quad:                            {quad_result:.6f}  (похибка: {quad_error:.2e})")
print("-" * 50)
print(f"Відхилення МК від аналітики:  {abs(mc_result - analytic_result):.6f}")
print(f"Відхилення МК від quad:       {abs(mc_result - quad_result):.6f}")
print(f"Відносна похибка МК:          {abs(mc_result - analytic_result)/analytic_result*100:.4f}%")
print("=" * 50)

# ── 5. Графік ────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Метод Монте-Карло: інтеграл f(x) = x²  від 0 до 2", fontsize=14)

# — Лівий: точки Монте-Карло —
ax = axes[0]
ax.scatter(x_rand[~under], y_rand[~under], s=0.3, color="steelblue", alpha=0.4, label="Поза кривою")
ax.scatter(x_rand[under],  y_rand[under],  s=0.3, color="tomato",    alpha=0.4, label="Під кривою")

xc = np.linspace(A, B, 400)
ax.plot(xc, f(xc), "k", linewidth=2)
ax.set_xlim(A, B)
ax.set_ylim(0, y_max)
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.set_title(f"Точки: {N_SAMPLES:,}   МК ≈ {mc_result:.5f}")
ax.legend(markerscale=8, fontsize=9)
ax.grid(True, alpha=0.3)

# — Правий: порівняння результатів —
ax2 = axes[1]
labels  = ["Монте-Карло", "Аналітично", "SciPy quad"]
values  = [mc_result, analytic_result, quad_result]
colors  = ["tomato", "seagreen", "steelblue"]
bars = ax2.bar(labels, values, color=colors, width=0.5, edgecolor="white")
for bar, val in zip(bars, values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
             f"{val:.5f}", ha="center", va="bottom", fontsize=10)
ax2.set_ylim(0, max(values) * 1.15)
ax2.set_ylabel("Значення інтеграла")
ax2.set_title("Порівняння методів")
ax2.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("monte_carlo_result.png", dpi=130, bbox_inches="tight")
plt.show()
print("Графік збережено: monte_carlo_result.png")