import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("dark_background")

df = pd.read_csv("Data/Laliga 1-2.csv")
df.columns = [" ".join(str(c).strip().split()) for c in df.columns]

ga_col = "Goals against At LaLiga"
pts_col = "Points At LaLiga"

df[ga_col] = pd.to_numeric(df[ga_col], errors="coerce")
df[pts_col] = pd.to_numeric(df[pts_col], errors="coerce")
df = df.dropna(subset=[ga_col, pts_col]).copy()

df["Survival"] = df[pts_col] >= 40

colors = {True: "#6fdc8c", False: "#ee538b"}

plt.figure(figsize=(9, 5))

plt.scatter(
    df[ga_col],
    df[pts_col],
    c=df["Survival"].map(colors),
    s=90,
    alpha=0.95
)

plt.axhline(40, linestyle="--", linewidth=1.5, color="#6fdc8c", alpha=0.9)

worst = df.sort_values(ga_col, ascending=False).head(3)
best = df.sort_values(ga_col, ascending=True).head(3)
label_df = pd.concat([worst, best])

for _, r in label_df.iterrows():
    plt.text(r[ga_col] + 0.6, r[pts_col] + 0.6, f'{r["Team"]} {r["Season"]}', fontsize=9, alpha=0.95)

plt.title(
    "From LaLiga 2 to LaLiga: Defense Decides Survival",
    fontsize=14,
    fontweight="bold"
)
plt.xlabel("Goals Conceded in LaLiga (Promoted Teams)")
plt.ylabel("LaLiga Points")

plt.tight_layout()
plt.savefig("Outputs/04_goals_against_vs_points.png", dpi=220, facecolor="black")
plt.show()
