# health_data_demo.py
# Demo script for Health Data Science course

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats

# ── 1. Basic variable types ────────────────────────────────────────────────────
patient_id = "PT-001"          # str
age = 45                       # int
bmi = 27.3                     # float
hypertensive = True            # bool
blood_group = "A+"             # str (categorical-like)

print("=== Basic Variables ===")
print(f"Patient: {patient_id}, Age: {age}, BMI: {bmi}, Hypertension: {hypertensive}")

# ── 2. Synthetic dataset ───────────────────────────────────────────────────────
np.random.seed(42)
n = 200

df = pd.DataFrame({
    "age":         np.random.randint(18, 80, n),
    "sex":         np.random.choice(["Male", "Female"], n),
    "bmi":         np.round(np.random.normal(26, 4, n), 1),
    "systolic_bp": np.round(np.random.normal(120, 15, n), 0),
    "diastolic_bp":np.round(np.random.normal(80, 10, n), 0),
    "glucose":     np.round(np.random.normal(95, 20, n), 1),
    "smoker":      np.random.choice([0, 1], n, p=[0.7, 0.3]),
})

# Introduce a realistic correlation: smokers tend to have higher BP
df.loc[df["smoker"] == 1, "systolic_bp"] += np.random.normal(10, 3, df["smoker"].sum())

print("\n=== Dataset head ===")
print(df.head())

print("\n=== Descriptive Statistics ===")
print(df.describe().round(2))

print("\n=== Value counts: sex ===")
print(df["sex"].value_counts())

# ── 3. Plots ───────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(10, 7))
fig.suptitle("Health Data Science — Variable Explorer", fontsize=13, fontweight="bold")
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

# 3a. Histogram — BMI
ax1 = fig.add_subplot(gs[0, 0])
ax1.hist(df["bmi"], bins=20, color="steelblue", edgecolor="white")
ax1.set_title("BMI Distribution")
ax1.set_xlabel("BMI")
ax1.set_ylabel("Count")

# 3b. Boxplot — Systolic BP by sex
ax2 = fig.add_subplot(gs[0, 1])
males   = df.loc[df["sex"] == "Male",   "systolic_bp"]
females = df.loc[df["sex"] == "Female", "systolic_bp"]
ax2.boxplot([males, females], labels=["Male", "Female"], patch_artist=True,
            boxprops=dict(facecolor="lightblue"))
ax2.set_title("Systolic BP by Sex")
ax2.set_ylabel("mmHg")

# 3c. Scatter — Age vs Systolic BP
ax3 = fig.add_subplot(gs[0, 2])
colors = df["smoker"].map({0: "steelblue", 1: "tomato"})
ax3.scatter(df["age"], df["systolic_bp"], c=colors, alpha=0.5, s=20)
ax3.set_title("Age vs Systolic BP")
ax3.set_xlabel("Age")
ax3.set_ylabel("Systolic BP (mmHg)")
# Legend
from matplotlib.patches import Patch  # noqa: E402
ax3.legend(handles=[Patch(color="steelblue", label="Non-smoker"),
                    Patch(color="tomato",    label="Smoker")], fontsize=8)

# 3d. Bar chart — Smoker prevalence by sex
ax4 = fig.add_subplot(gs[1, 0])
smoker_rate = df.groupby("sex")["smoker"].mean() * 100
smoker_rate.plot(kind="bar", ax=ax4, color=["salmon", "steelblue"], edgecolor="white", rot=0)
ax4.set_title("Smoking Prevalence by Sex")
ax4.set_ylabel("% Smokers")
ax4.set_ylim(0, 50)

# 3e. Correlation heatmap (manual)
ax5 = fig.add_subplot(gs[1, 1])
num_cols = ["age", "bmi", "systolic_bp", "diastolic_bp", "glucose"]
corr = df[num_cols].corr()
im = ax5.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
ax5.set_xticks(range(len(num_cols))) 
ax5.set_xticklabels(num_cols, rotation=45, ha="right", fontsize=7)
ax5.set_yticks(range(len(num_cols))) 
ax5.set_yticklabels(num_cols, fontsize=7)
ax5.set_title("Correlation Matrix")
plt.colorbar(im, ax=ax5, fraction=0.046)

# 3f. Simple linear regression — BMI vs Glucose
ax6 = fig.add_subplot(gs[1, 2])
slope, intercept, r, p, se = stats.linregress(df["bmi"], df["glucose"])
x_line = np.linspace(df["bmi"].min(), df["bmi"].max(), 100)
ax6.scatter(df["bmi"], df["glucose"], alpha=0.4, s=15, color="steelblue")
ax6.plot(x_line, intercept + slope * x_line, color="red", linewidth=2)
ax6.set_title(f"BMI vs Glucose\nr={r:.2f}, p={p:.3f}")
ax6.set_xlabel("BMI")
ax6.set_ylabel("Glucose (mg/dL)")

plt.savefig("health_demo.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nPlot saved to health_demo.png")
