"""
Epicurious Recipes Analysis
---------------------------
This script loads the Epicurious recipe dataset (previously downloaded),
categorizes recipes by diet type, and generates multiple nutrition graphs.

Graphs generated (each saved as a separate file):
1. Pie chart of recipe categories
2. Protein box-and-whisker plot by category
3. Calories box-and-whisker plot by category
4. Fat box-and-whisker plot by category
"""

# =========================
# Imports & Dependencies
# =========================
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub

# =========================
# Load Dataset
# =========================
print("Loading Epicurious dataset...")
try:
    # Download/retrieve the dataset path using kagglehub
    path = kagglehub.dataset_download("hugodarwood/epirecipes")
    print(f"Dataset path: {path}")
    
    # Find the CSV file
    csv_file = None
    for file in os.listdir(path):
        if file.endswith('.csv'):
            csv_file = os.path.join(path, file)
            break
    
    if csv_file is None:
        raise FileNotFoundError("No CSV file found in the dataset")
    
    df = pd.read_csv(csv_file)
    print(f"Dataset loaded successfully! Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")

except Exception as e:
    print(f"Error loading dataset: {e}")
    exit(1)

# =========================
# Clean Data
# =========================
print("Cleaning data...")

# Define nutrition columns - check which ones exist
nutrition_cols = []
possible_cols = {
    "protein": ["protein"],
    "calories": ["calories", "calorie", "cal"],
    "fat": ["fat", "sodium"]
}

# Map the actual column names
actual_cols = {}
for key, possible_names in possible_cols.items():
    for col_name in possible_names:
        if col_name in df.columns:
            actual_cols[key] = col_name
            nutrition_cols.append(col_name)
            break

if len(nutrition_cols) < 3:
    print(f"Warning: Could only find {len(nutrition_cols)} out of 3 nutrition columns")
    print(f"Found: {nutrition_cols}")
    print(f"All available columns: {df.columns.tolist()}")

# Keep only rows with relevant nutrition data
df = df.dropna(subset=nutrition_cols)

# =========================
# Recipe Categorization
# =========================
def categorize_recipe(row):
    """Categorize recipe based on dietary attributes."""
    if row.get("vegan", 0) == 1:
        return "Vegan"
    elif row.get("vegetarian", 0) == 1:
        return "Vegetarian"
    elif row.get("fish", 0) == 1:
        return "Fish"
    else:
        return "Meat/Poultry"

df["category"] = df.apply(categorize_recipe, axis=1)

# Filter to only include our categories
categories = ["Vegan", "Vegetarian", "Fish", "Meat/Poultry"]
df = df[df["category"].isin(categories)]

print(f"Total recipes after filtering: {len(df)}")
print(f"Category distribution:\n{df['category'].value_counts()}\n")

# Get actual column names for the nutrition data
protein_col = actual_cols.get("protein", "protein")
calories_col = actual_cols.get("calories", "calories")
fat_col = actual_cols.get("fat", "fat")

# =========================
# Graph 1: Pie Chart
# =========================
print("Generating Graph 1: Recipe Category Distribution...")
category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(
    category_counts,
    labels=category_counts.index,
    autopct="%1.1f%%",
    startangle=140
)
plt.title("Recipe Category Distribution (Epicurious)")
plt.savefig("graph_1_recipe_category_pie.png", dpi=150, bbox_inches='tight')
plt.close()

# =========================
# Graph 2: Protein Box Plot
# =========================
print("Generating Graph 2: Protein Content by Category...")
plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df,
    x="category",
    y=protein_col,
    order=categories,
    showfliers=True
)
sns.stripplot(
    data=df,
    x="category",
    y=protein_col,
    order=categories,
    color="black",
    alpha=0.3,
    jitter=True
)
plt.title("Protein Content by Recipe Category")
plt.ylabel("Protein (g)")
plt.xlabel("Recipe Category")
plt.savefig("graph_2_protein_boxplot.png", dpi=150, bbox_inches='tight')
plt.close()

# =========================
# Graph 3: Calories Box Plot
# =========================
print("Generating Graph 3: Calories by Category...")
plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df,
    x="category",
    y=calories_col,
    order=categories,
    showfliers=True
)
sns.stripplot(
    data=df,
    x="category",
    y=calories_col,
    order=categories,
    color="black",
    alpha=0.3,
    jitter=True
)
plt.title("Calories by Recipe Category")
plt.ylabel("Calories")
plt.xlabel("Recipe Category")
plt.savefig("graph_3_calories_boxplot.png", dpi=150, bbox_inches='tight')
plt.close()

# =========================
# Graph 4: Fat Box Plot
# =========================
print("Generating Graph 4: Fat Content by Category...")
plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df,
    x="category",
    y=fat_col,
    order=categories,
    showfliers=True
)
sns.stripplot(
    data=df,
    x="category",
    y=fat_col,
    order=categories,
    color="black",
    alpha=0.3,
    jitter=True
)
plt.title("Fat Content by Recipe Category")
plt.ylabel("Fat (g)")
plt.xlabel("Recipe Category")
plt.savefig("graph_4_fat_boxplot.png", dpi=150, bbox_inches='tight')
plt.close()

print("\nAll graphs generated successfully!")
print("Output files:")
print("  - graph_1_recipe_category_pie.png")
print("  - graph_2_protein_boxplot.png")
print("  - graph_3_calories_boxplot.png")
print("  - graph_4_fat_boxplot.png")