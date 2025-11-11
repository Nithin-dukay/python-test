import pandas as pd
import numpy as np
import json

# Read the complete dataset
print("Loading complete dataset...")
df = pd.read_csv('/vercel/sandbox/Final_data (1).csv')

print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")

# Phase 1: Structure Discovery
print("\n=== PHASE 1: STRUCTURE DISCOVERY ===")
print("\nColumn Data Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nBasic Statistics:")
print(df.describe())

# Phase 2: Deep Analysis
print("\n=== PHASE 2: DEEP ANALYSIS ===")

analysis = {
    "total_records": len(df),
    "demographics": {},
    "fitness_metrics": {},
    "nutrition_metrics": {},
    "exercise_metrics": {},
    "correlations": {},
    "insights": []
}

# Demographics Analysis
print("\nAnalyzing Demographics...")
analysis["demographics"] = {
    "age_distribution": {
        "min": float(df['Age'].min()),
        "max": float(df['Age'].max()),
        "mean": float(df['Age'].mean()),
        "median": float(df['Age'].median())
    },
    "gender_distribution": df['Gender'].value_counts().to_dict(),
    "bmi_categories": {
        "underweight": int((df['BMI'] < 18.5).sum()),
        "normal": int(((df['BMI'] >= 18.5) & (df['BMI'] < 25)).sum()),
        "overweight": int(((df['BMI'] >= 25) & (df['BMI'] < 30)).sum()),
        "obese": int((df['BMI'] >= 30).sum())
    }
}

# Fitness Metrics Analysis
print("Analyzing Fitness Metrics...")
analysis["fitness_metrics"] = {
    "workout_types": df['Workout_Type'].value_counts().to_dict(),
    "experience_levels": {
        "beginner": int((df['Experience_Level'] < 2).sum()),
        "intermediate": int(((df['Experience_Level'] >= 2) & (df['Experience_Level'] < 3)).sum()),
        "advanced": int((df['Experience_Level'] >= 3).sum())
    },
    "avg_calories_burned": float(df['Calories_Burned'].mean()),
    "avg_session_duration": float(df['Session_Duration (hours)'].mean()),
    "avg_workout_frequency": float(df['Workout_Frequency (days/week)'].mean()),
    "heart_rate": {
        "avg_resting": float(df['Resting_BPM'].mean()),
        "avg_during_workout": float(df['Avg_BPM'].mean()),
        "avg_max": float(df['Max_BPM'].mean())
    }
}

# Nutrition Metrics Analysis
print("Analyzing Nutrition Metrics...")
analysis["nutrition_metrics"] = {
    "diet_types": df['diet_type'].value_counts().to_dict(),
    "meal_types": df['meal_type'].value_counts().to_dict(),
    "avg_daily_calories": float(df['Calories'].mean()),
    "macros": {
        "avg_carbs": float(df['Carbs'].mean()),
        "avg_proteins": float(df['Proteins'].mean()),
        "avg_fats": float(df['Fats'].mean())
    },
    "avg_water_intake": float(df['Water_Intake (liters)'].mean()),
    "cooking_methods": df['cooking_method'].value_counts().to_dict()
}

# Exercise Metrics Analysis
print("Analyzing Exercise Metrics...")
analysis["exercise_metrics"] = {
    "top_exercises": df['Name of Exercise'].value_counts().head(10).to_dict(),
    "body_parts": df['Body Part'].value_counts().to_dict(),
    "difficulty_levels": df['Difficulty Level'].value_counts().to_dict(),
    "equipment_needed": df['Equipment Needed'].value_counts().head(10).to_dict(),
    "avg_sets": float(df['Sets'].mean()),
    "avg_reps": float(df['Reps'].mean()),
    "avg_calories_per_30min": float(df['Burns Calories (per 30 min)'].mean())
}

# Phase 3: Correlations and Patterns
print("\n=== PHASE 3: CORRELATIONS AND PATTERNS ===")

# Key correlations
numeric_cols = ['Age', 'Weight (kg)', 'BMI', 'Calories_Burned', 'Session_Duration (hours)', 
                'Workout_Frequency (days/week)', 'Experience_Level', 'Calories', 'Water_Intake (liters)']

corr_matrix = df[numeric_cols].corr()

analysis["correlations"] = {
    "calories_burned_vs_session_duration": float(corr_matrix.loc['Calories_Burned', 'Session_Duration (hours)']),
    "calories_burned_vs_workout_frequency": float(corr_matrix.loc['Calories_Burned', 'Workout_Frequency (days/week)']),
    "bmi_vs_calories_intake": float(corr_matrix.loc['BMI', 'Calories']),
    "experience_vs_workout_frequency": float(corr_matrix.loc['Experience_Level', 'Workout_Frequency (days/week)'])
}

# Workout Type Analysis
print("\nAnalyzing Workout Type Patterns...")
workout_analysis = df.groupby('Workout_Type').agg({
    'Calories_Burned': 'mean',
    'Session_Duration (hours)': 'mean',
    'Avg_BPM': 'mean'
}).round(2).to_dict()

analysis["workout_type_analysis"] = workout_analysis

# Diet Type Analysis
print("Analyzing Diet Type Patterns...")
diet_analysis = df.groupby('diet_type').agg({
    'Calories': 'mean',
    'Carbs': 'mean',
    'Proteins': 'mean',
    'Fats': 'mean',
    'BMI': 'mean'
}).round(2).to_dict()

analysis["diet_type_analysis"] = diet_analysis

# Gender-based Analysis
print("Analyzing Gender Patterns...")
gender_analysis = df.groupby('Gender').agg({
    'Weight (kg)': 'mean',
    'Height (m)': 'mean',
    'BMI': 'mean',
    'Calories_Burned': 'mean',
    'Calories': 'mean'
}).round(2).to_dict()

analysis["gender_analysis"] = gender_analysis

# Phase 4: Key Insights
print("\n=== PHASE 4: KEY INSIGHTS ===")

insights = []

# Insight 1: Calorie Balance
avg_cal_balance = df['cal_balance'].mean()
insights.append(f"Average calorie balance: {avg_cal_balance:.2f} calories (intake - burn)")

# Insight 2: Most effective workout
best_workout = df.groupby('Workout_Type')['Calories_Burned'].mean().idxmax()
best_workout_cals = df.groupby('Workout_Type')['Calories_Burned'].mean().max()
insights.append(f"Most effective workout type: {best_workout} (avg {best_workout_cals:.2f} calories burned)")

# Insight 3: Experience level impact
exp_impact = df.groupby('Experience_Level')['Calories_Burned'].mean().to_dict()
insights.append(f"Experience level impact on calories burned: {exp_impact}")

# Insight 4: Diet effectiveness
diet_bmi = df.groupby('diet_type')['BMI'].mean().sort_values()
best_diet = diet_bmi.index[0]
insights.append(f"Diet type with lowest average BMI: {best_diet} ({diet_bmi.iloc[0]:.2f})")

# Insight 5: Workout frequency sweet spot
freq_groups = pd.cut(df['Workout_Frequency (days/week)'], bins=[0, 2, 4, 6])
freq_analysis = df.groupby(freq_groups)['Calories_Burned'].mean()
insights.append(f"Workout frequency impact: {freq_analysis.to_dict()}")

analysis["insights"] = insights

# Save analysis to JSON
print("\nSaving analysis to JSON...")
with open('/vercel/sandbox/data_analysis.json', 'w') as f:
    json.dump(analysis, f, indent=2)

print("\n=== ANALYSIS COMPLETE ===")
print(f"Total records analyzed: {len(df)}")
print(f"Analysis saved to: data_analysis.json")

# Print summary
print("\n=== SUMMARY ===")
print(f"Total Users: {len(df)}")
print(f"Gender Split: {analysis['demographics']['gender_distribution']}")
print(f"Average Age: {analysis['demographics']['age_distribution']['mean']:.1f} years")
print(f"Average BMI: {df['BMI'].mean():.2f}")
print(f"Average Calories Burned: {analysis['fitness_metrics']['avg_calories_burned']:.2f}")
print(f"Average Daily Calorie Intake: {analysis['nutrition_metrics']['avg_daily_calories']:.2f}")
print(f"Average Calorie Balance: {avg_cal_balance:.2f}")
print(f"\nTop 5 Exercises:")
for exercise, count in list(analysis['exercise_metrics']['top_exercises'].items())[:5]:
    print(f"  - {exercise}: {count}")
