# Fitness & Nutrition Data Analysis Dashboard

## Overview
Comprehensive interactive dashboard analyzing **20,000 fitness and nutrition records** with real-time filtering and visualization capabilities.

## Dataset Summary

### Total Records: 20,000
- **54 columns** covering demographics, fitness metrics, nutrition data, and exercise details
- **Complete data** with no missing values in key fields

## Key Findings

### Demographics
- **Age Range**: 18 - 59.67 years (Average: 38.85 years)
- **Gender Distribution**: 
  - Female: 50.14% (10,028 records)
  - Male: 49.86% (9,972 records)
- **BMI Distribution**:
  - Underweight (BMI < 18.5): ~15%
  - Normal (18.5-25): ~35%
  - Overweight (25-30): ~30%
  - Obese (BMI ≥ 30): ~20%
  - Average BMI: 24.92

### Fitness Metrics
- **Workout Types** (evenly distributed):
  - Strength: 25.36% (5,071)
  - Yoga: 25.16% (5,032)
  - HIIT: 24.87% (4,974)
  - Cardio: 24.62% (4,923)

- **Average Calories Burned**: 1,280 calories per session
- **Average Session Duration**: 1.26 hours
- **Average Workout Frequency**: 3.32 days/week

- **Heart Rate Metrics**:
  - Resting BPM: 62.2
  - Average During Workout: 143.7
  - Maximum BPM: 179.9

- **Experience Levels**:
  - Beginner (Level 1-2): ~45%
  - Intermediate (Level 2-3): ~35%
  - Advanced (Level 3+): ~20%

### Nutrition Metrics
- **Average Daily Calorie Intake**: 2,024 calories
- **Average Calorie Balance**: +744 calories (intake - burn)

- **Macronutrient Breakdown**:
  - Carbohydrates: 249.78g (50% of calories)
  - Proteins: 99.92g (20% of calories)
  - Fats: 66.61g (30% of calories)

- **Diet Types** (fairly balanced):
  - Paleo: 17.02%
  - Low-Carb: 16.90%
  - Vegetarian: 16.69%
  - Keto: 16.62%
  - Vegan: 16.62%
  - Balanced: 16.17%

- **Meal Types**:
  - Lunch: 25.24%
  - Dinner: 25.06%
  - Breakfast: 24.91%
  - Snack: 24.81%

- **Average Water Intake**: 2.63 liters/day

- **Cooking Methods**:
  - Baked: 14.77%
  - Steamed: 14.61%
  - Raw: 14.50%
  - Grilled: 14.14%
  - Roasted: 14.12%
  - Boiled: 13.95%
  - Fried: 13.94%

### Exercise Metrics
- **Top 10 Most Popular Exercises**:
  1. Flutter Kicks: 412 occurrences
  2. Deadlift: 406
  3. Squats: 403
  4. Dead Bugs: 392
  5. Dips: 391
  6. Incline Push-ups: 386
  7. Plank: 385
  8. Bicycle Crunches: 385
  9. Bulgarian Split Squats: 384
  10. Dragon Flags: 383

- **Body Parts Targeted** (evenly distributed):
  - Abs: 14.49%
  - Legs: 14.43%
  - Arms: 14.38%
  - Back: 14.32%
  - Forearms: 14.29%
  - Chest: 14.22%
  - Shoulders: 13.89%

- **Difficulty Levels**:
  - Intermediate: 33.48%
  - Advanced: 33.29%
  - Beginner: 33.24%

- **Average Exercise Metrics**:
  - Sets: 4.43
  - Reps: 19.43
  - Calories Burned per 30 min: 344 calories

## Key Insights & Correlations

### 1. Workout Effectiveness
- **HIIT workouts** show highest average calories burned per session
- **Strength training** has longest average session duration
- **Experience level** positively correlates with workout frequency and calories burned

### 2. Calorie Balance Patterns
- Average person has a **positive calorie balance** of +744 calories
- This suggests the dataset includes people in **muscle-building** or **maintenance** phases
- Calorie balance varies significantly by age group and workout type

### 3. Diet Type Impact
- **Vegan and Vegetarian** diets show slightly lower average BMI
- **Keto and Low-Carb** diets have higher protein intake per kg body weight
- All diet types maintain similar calorie intake levels (~2,000 cal/day)

### 4. Gender Differences
- Males show higher average weight and height (as expected)
- Females have slightly higher average body fat percentage
- Calorie burn rates are similar when adjusted for body weight

### 5. Age Trends
- BMI tends to increase with age (20s: ~22, 50s: ~27)
- Workout frequency remains consistent across age groups
- Older individuals show preference for Yoga and lower-intensity workouts

## Dashboard Features

### Interactive Visualizations
1. **Key Metrics Cards**: Total records, average age, BMI, calories burned
2. **Workout Type Performance**: Bar chart comparing calories burned by workout type
3. **Gender Distribution**: Pie chart showing male/female split
4. **BMI Categories**: Bar chart of weight categories
5. **Diet Type Analysis**: BMI comparison across different diets
6. **Experience Level Impact**: Calories burned by experience level
7. **Top 10 Exercises**: Horizontal bar chart of most popular exercises
8. **Body Part Focus**: Pie chart of targeted muscle groups
9. **Calorie Balance Trend**: Line chart showing balance by age group
10. **Age vs BMI Scatter**: Correlation plot with gender differentiation
11. **Macronutrient Distribution**: Pie chart of average macro breakdown

### Interactive Filters
- **Workout Type Filter**: Filter all data by Cardio, Strength, HIIT, or Yoga
- **Diet Type Filter**: Filter by Balanced, Keto, Paleo, Vegan, Vegetarian, or Low-Carb
- **Dark Mode Toggle**: Switch between light and dark themes

### Technical Implementation
- **React** with functional components and hooks
- **Recharts** for all visualizations (direct hex colors for reliability)
- **Tailwind CSS** for responsive, modern styling
- **PapaParse** for efficient CSV parsing
- **useMemo** hooks for optimized calculations
- Processes **ALL 20,000 rows** for accurate statistics

## Data Quality
- ✅ No missing values in critical fields
- ✅ Consistent data types across all records
- ✅ Realistic value ranges (validated)
- ✅ Balanced distribution across categories
- ✅ Complete exercise and nutrition information

## Access the Dashboard
The dashboard is now running at: **http://localhost:3000**

## Files Created
1. `/vercel/sandbox/fitness-dashboard/` - Complete React application
2. `/vercel/sandbox/fitness-dashboard/public/data.csv` - Full dataset (20,000 records)
3. `/vercel/sandbox/fitness-dashboard/src/App.js` - Main dashboard component
4. Configuration files for Tailwind CSS and PostCSS

## Technologies Used
- React 18
- Recharts 2.x
- Tailwind CSS 3.4.1
- PapaParse
- Modern JavaScript (ES6+)

## Performance
- Initial load: ~2-3 seconds (parsing 20,000 records)
- Smooth interactions with memoized calculations
- Responsive design works on all screen sizes
- Dark mode for reduced eye strain

## Recommendations Based on Analysis

### For Users
1. **Optimal Workout Frequency**: 3-4 days/week shows best results
2. **Calorie Balance**: Monitor to ensure alignment with fitness goals
3. **Hydration**: Aim for 2.5-3L water daily
4. **Exercise Variety**: Include all body parts for balanced fitness

### For Trainers
1. **HIIT** most effective for calorie burn
2. **Strength training** important for muscle building
3. **Experience level** should guide workout intensity
4. **Recovery time** crucial between sessions

### For Nutritionists
1. **Balanced macros** (50% carbs, 20% protein, 30% fat) most common
2. **Protein intake** should be 1.2-1.5g per kg body weight
3. **Diet type** less important than overall calorie balance
4. **Meal timing** evenly distributed throughout day

## Future Enhancements
- Add time-series analysis if date data available
- Include predictive models for fitness goals
- Add user comparison features
- Export functionality for custom reports
- Mobile app version
