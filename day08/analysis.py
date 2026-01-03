"""
Epicurious Recipes Analysis
---------------------------
This script downloads the Epicurious recipe dataset from Kaggle,
categorizes recipes by diet type, and generates multiple nutrition graphs.

Graphs generated (each saved as a separate file):
1. Pie chart of recipe categories
2. Protein box-and-whisker plot by category
3. Fiber box-and-whisker plot by category
4. Carbohydrate box-and-whisker plot by category
"""

# =========================
# Imports & Dependencies
# =========================
import os
import zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from kaggle.api.kaggle_api_extended import KaggleApi

# =========================
# Kaggle Dataset Download
# =========================
DATA_DIR = "data"
ZIP_PATH = os.path.join(DATA_DIR, "epirecipes.zip")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

api = KaggleApi()
api.authenticate()

# Epicurious dataset (epi_r.csv)
api.dataset_download_files(
    "hugomathien/epirecipes",
    path=DATA_DIR,
    zip=True
)

# Unzip dataset
with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
    zip_ref.extractall(DATA_DIR)

# =========================
# Load & Clean Data
# =========================
df = pd.read_csv(os.path.join(DATA_DIR, "epi_r.csv"))

# Keep only rows with relevant nutrition data
nutrition_cols = ["protein", "fiber", "carbs"]
df = df.dropna(subset=nutrition_cols)

# =========================
# Recipe Categorization
# =========================
def categorize_recipe(row):
    if row.get("vegan", 0) == 1:
        return "Vegan"
    elif row.get("vegetarian", 0) == 1:
        return "Vegetarian"
    elif row.get("fish", 0) == 1:
        return "Fish"
    else:
        return "Meat/Poultry"

df["category"] = df.apply(categorize_recipe, axis=1)

categories = ["Vegan", "Vegetarian", "Fish", "Meat/Poultry"]
df = df[df["category"].isin(categories)]

# =========================
# Graph 1: Pie Chart
# =========================
# This graph shows the proportion of recipes that are
# Vegan, Vegetarian, Fish-based, or Meat/Poultry-based.

category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(
    category_counts,
    labels=category_counts.index,
    autopct="%1.1f%%",
    startangle=140
)
plt.title("Recipe Category Distribution (Epicurious)")
plt.savefig("graph_1_recipe_category_pie.png")
plt.close()

# =========================
# Graph 2: Protein Box Plot
# =========================
# This graph shows the distribution of protein content
# for each recipe category. Each dot represents one recipe.

plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df,
    x="category",
    y="protein",
    showfliers=True
)
sns.stripplot(
    data=df,
    x="category",
    y="protein",
    color="black",
    alpha=0.3,
    jitter=True
)
plt.title("Protein Content by Recipe Category")
plt.ylabel("Protein (g)")
plt.xlabel("Recipe Category")
plt.savefig("graph_2_protein_boxplot.png")
plt.close()

# =========================
# Graph 3: Fiber Box Plot
# =========================
# This graph shows the distribution of fiber content
# for each recipe category. Each dot represents one recipe.

plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df,
    x="category",
    y="fiber",
    showfliers=True
)
sns.stripplot(
    data=df,
    x="category",
    y="fiber",
    color="black",
    alpha=0.3,
    jitter=True
)
plt.title("Fiber Content by Recipe Category")
plt.ylabel("Fiber (g)")
plt.xlabel("Recipe Category")
plt.savefig("graph_3_fiber_boxplot.png")
plt.close()

# =========================
# Graph 4: Carbohydrate Box Plot
# =========================
# This graph shows the distribution of carbohydrate content
# for each recipe category. Each dot represents one recipe.

plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df,
    x="category",
    y="carbs",
    showfliers=True
)
sns.stripplot(
    data=df,
    x="category",
    y="carbs",
    color="black",
    alpha=0.3,
    jitter=True
)
plt.title("Carbohydrate Content by Recipe Category")
plt.ylabel("Carbohydrates (g)")
plt.xlabel("Recipe Category")
plt.savefig("graph_4_carbs_boxplot.png")
plt.close()

print("All graphs generated successfully.")
