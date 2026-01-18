import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plt.style.use("dark_background")

df = pd.read_csv("Data/Laliga 1-2.csv")
df.columns = [" ".join(str(c).strip().split()) for c in df.columns]

season_col = "Season"
team_col = "Team"
xg_col = "Xg At LaLiga"
g_col = "Goals for At LaLiga"
pts_col = "Points At LaLiga"

for c in [xg_col, g_col, pts_col]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df = df.dropna(subset=[season_col, team_col, xg_col, g_col, pts_col]).copy()
df["Survival"] = df[pts_col] >= 40

def season_key(s):
    s = str(s).strip()
    a = s.split("-")[0]
    a = "".join([ch for ch in a if ch.isdigit()])
    return int(a) if a else 0

seasons_sorted = sorted(df[season_col].unique(), key=season_key)
last3 = seasons_sorted[-3:]

df3 = df[df[season_col].isin(last3)].copy()

surv_color = "#6fdc8c"
fail_color = "#ee538b"

fig, axes = plt.subplots(1, 3, figsize=(16, 6), sharex=True)

for ax, s in zip(axes, last3):
    tmp = df3[df3[season_col] == s].copy()
    tmp = tmp.sort_values(g_col, ascending=True)

    y = range(len(tmp))
    bar_colors = tmp["Survival"].map({True: surv_color, False: fail_color}).tolist()

    ax.barh(y, tmp[xg_col], color=bar_colors, alpha=0.85, height=0.6)
    ax.scatter(tmp[g_col], y, s=65, color="white", edgecolors="black", linewidths=0.6, zorder=3)

    ax.set_yticks(list(y))
    ax.set_yticklabels(tmp[team_col])
    ax.set_title(f"{s}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Goals / xG")

    ax.grid(False)

axes[0].set_ylabel("Promoted teams")

fig.suptitle(
    "From LaLiga 2 to LaLiga: xG vs Goals (Last 3 Seasons) Survival Context",
    fontsize=16,
    fontweight="bold"
)

legend_items = [
    Line2D([0], [0], marker="o", color="none", markerfacecolor="white", markersize=8, label="Goals (Actual)"),
    Line2D([0], [0], color=surv_color, lw=8, label="Survived (>=40 pts)"),
    Line2D([0], [0], color=fail_color, lw=8, label="Failed (<40 pts)"),
]
leg = fig.legend(handles=legend_items, loc="lower center", ncol=3, frameon=True)
leg.get_frame().set_alpha(0.15)

plt.tight_layout(rect=[0, 0.06, 1, 0.92])
plt.savefig("Outputs/06_last3_xg_vs_goals_survival.png", dpi=220, facecolor="black")
plt.show()
