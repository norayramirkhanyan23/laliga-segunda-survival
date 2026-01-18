import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("dark_background")

df = pd.read_csv("Data/Laliga 1-2.csv")
df.columns = [" ".join(str(c).strip().split()) for c in df.columns]

points_col = "Points At LaLiga"

df[points_col] = pd.to_numeric(df[points_col], errors="coerce")
df = df.dropna(subset=[points_col])

df["Survival"] = df[points_col] >= 40

colors = {True: "#6fdc8c", False: "#ee538b"}

plt.figure(figsize=(9, 5))

plt.scatter(
    df["Season"],
    df[points_col],
    c=df["Survival"].map(colors),
    s=90,
    alpha=0.95
)

plt.axhline(40, linestyle="--", linewidth=1.5, color="#6fdc8c", alpha=0.9)

plt.title(
    "From LaLiga 2 to LaLiga: The 40-Point Survival Test",
    fontsize=14,
    fontweight="bold"
)
plt.xlabel("Season")
plt.ylabel("LaLiga Points")

plt.tight_layout()
plt.savefig("Outputs/03_survival_40_point_rule.png", dpi=220, facecolor="black")
plt.show()
