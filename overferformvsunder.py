import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("dark_background")

df = pd.read_csv("Data/Laliga 1-2.csv")
df.columns = [" ".join(str(c).strip().split()) for c in df.columns]

x_col = "xPT LaLiga"
y_col = "Points At LaLiga"

df[x_col] = pd.to_numeric(df[x_col], errors="coerce")
df[y_col] = pd.to_numeric(df[y_col], errors="coerce")

df = df.dropna(subset=[x_col, y_col]).copy()
df["Delta"] = df[y_col] - df[x_col]
df["Status"] = df["Delta"].apply(lambda d: "Overperform" if d >= 0 else "Underperform")

colors = {"Overperform": "#6fdc8c", "Underperform": "#ee538b"}

size = (df["Delta"].abs() * 18 + 60).clip(60, 260)

plt.figure(figsize=(9, 5))

for status in ["Overperform", "Underperform"]:
    tmp = df[df["Status"] == status]
    plt.scatter(
        tmp[x_col],
        tmp[y_col],
        s=size.loc[tmp.index],
        alpha=0.92,
        color=colors[status],
        edgecolors="none",
        label=status
    )

mn = min(df[x_col].min(), df[y_col].min()) - 2
mx = max(df[x_col].max(), df[y_col].max()) + 2
plt.plot([mn, mx], [mn, mx], linestyle="--", linewidth=1.6, color="#08bdba", alpha=0.8)

plt.axhline(40, linestyle="--", linewidth=1.2, color="#6fdc8c", alpha=0.85)
plt.axvline(40, linestyle="--", linewidth=1.2, color="#6fdc8c", alpha=0.85)

top_over = df.sort_values("Delta", ascending=False).head(3)
top_under = df.sort_values("Delta", ascending=True).head(3)
label_df = pd.concat([top_over, top_under])

for _, r in label_df.iterrows():
    dx = 0.6 if r["Delta"] >= 0 else 0.6
    dy = 0.6 if r["Delta"] >= 0 else -1.2
    plt.text(r[x_col] + dx, r[y_col] + dy, f'{r["Team"]} {r["Season"]}', fontsize=9, alpha=0.95)

plt.xlim(mn, mx)
plt.ylim(mn, mx)

plt.title("From LaLiga 2 to LaLiga: xPT vs Reality (Promoted Teams)", fontsize=14, fontweight="bold")
plt.xlabel("xPT (Expected Points) in LaLiga")
plt.ylabel("Actual Points in LaLiga")

leg = plt.legend(frameon=True)
leg.get_frame().set_alpha(0.15)

plt.tight_layout()
plt.savefig("Outputs/02_xpt_vs_actual_points.png", dpi=220, facecolor="black")
plt.show()
