import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("dark_background")

df = pd.read_csv("Data/Laliga 1-2.csv")
df.columns = [" ".join(str(c).strip().split()) for c in df.columns]

prev_pos_col = "Position prevoius at Laliga2"
points_laliga_col = "Points At LaLiga"

df[prev_pos_col] = pd.to_numeric(df[prev_pos_col], errors="coerce")
df[points_laliga_col] = pd.to_numeric(df[points_laliga_col], errors="coerce")

df["Promotion_Type"] = df[prev_pos_col].apply(
    lambda x: "1st" if x == 1 else ("2nd" if x == 2 else "Playoff")
)

trend = (
    df.groupby(["Season", "Promotion_Type"])[points_laliga_col]
    .mean()
    .reset_index()
)

colors = {"1st": "#08bdba", "2nd": "#8a3ffc", "Playoff": "#ee538b"}

plt.figure(figsize=(9, 5))

for ptype in ["1st", "2nd", "Playoff"]:
    tmp = trend[trend["Promotion_Type"] == ptype]
    plt.plot(
        tmp["Season"],
        tmp[points_laliga_col],
        marker="o",
        linewidth=2.5,
        markersize=6,
        color=colors[ptype],
        label=ptype,
    )

plt.axhline(40, linestyle="--", linewidth=1.5, color="#6fdc8c", alpha=0.9)

plt.title("Average LaLiga points by promotion route (1st, 2nd, Playoff)", fontsize=14, fontweight="bold")
plt.xlabel("Season")
plt.ylabel("LaLiga Points")

leg = plt.legend(frameon=True)
leg.get_frame().set_alpha(0.15)

plt.tight_layout()
plt.savefig("Outputs/01_points_trend_by_promotion_type.png", dpi=220, facecolor="black")
plt.show()
