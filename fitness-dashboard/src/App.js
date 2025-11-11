import React, { useState, useEffect, useMemo } from 'react';
import Papa from 'papaparse';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  ScatterChart, Scatter, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis
} from 'recharts';

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const [selectedWorkout, setSelectedWorkout] = useState('All');
  const [selectedDiet, setSelectedDiet] = useState('All');

  useEffect(() => {
    fetch('/data.csv')
      .then(response => response.text())
      .then(text => {
        Papa.parse(text, {
          header: true,
          dynamicTyping: true,
          skipEmptyLines: true,
          complete: (results) => {
            setData(results.data);
            setLoading(false);
          }
        });
      });
  }, []);

  const stats = useMemo(() => {
    if (data.length === 0) return null;

    const filteredData = data.filter(row => 
      (selectedWorkout === 'All' || row.Workout_Type === selectedWorkout) &&
      (selectedDiet === 'All' || row.diet_type === selectedDiet)
    );

    return {
      totalRecords: filteredData.length,
      avgAge: (filteredData.reduce((sum, row) => sum + (row.Age || 0), 0) / filteredData.length).toFixed(1),
      avgBMI: (filteredData.reduce((sum, row) => sum + (row.BMI || 0), 0) / filteredData.length).toFixed(2),
      avgCaloriesBurned: (filteredData.reduce((sum, row) => sum + (row.Calories_Burned || 0), 0) / filteredData.length).toFixed(0),
      avgCaloriesIntake: (filteredData.reduce((sum, row) => sum + (row.Calories || 0), 0) / filteredData.length).toFixed(0),
      avgCalorieBalance: (filteredData.reduce((sum, row) => sum + (row.cal_balance || 0), 0) / filteredData.length).toFixed(0),
      avgWorkoutDuration: (filteredData.reduce((sum, row) => sum + (row['Session_Duration (hours)'] || 0), 0) / filteredData.length).toFixed(2),
      avgWaterIntake: (filteredData.reduce((sum, row) => sum + (row['Water_Intake (liters)'] || 0), 0) / filteredData.length).toFixed(2)
    };
  }, [data, selectedWorkout, selectedDiet]);

  const genderDistribution = useMemo(() => {
    if (data.length === 0) return [];
    const counts = {};
    data.forEach(row => {
      counts[row.Gender] = (counts[row.Gender] || 0) + 1;
    });
    return Object.entries(counts).map(([name, value]) => ({ name, value }));
  }, [data]);

  const workoutTypeData = useMemo(() => {
    if (data.length === 0) return [];
    const workoutStats = {};
    data.forEach(row => {
      const type = row.Workout_Type;
      if (!workoutStats[type]) {
        workoutStats[type] = { type, totalCalories: 0, count: 0, totalDuration: 0 };
      }
      workoutStats[type].totalCalories += row.Calories_Burned || 0;
      workoutStats[type].totalDuration += row['Session_Duration (hours)'] || 0;
      workoutStats[type].count += 1;
    });
    return Object.values(workoutStats).map(stat => ({
      type: stat.type,
      avgCalories: Math.round(stat.totalCalories / stat.count),
      avgDuration: (stat.totalDuration / stat.count).toFixed(2),
      count: stat.count
    }));
  }, [data]);

  const dietTypeData = useMemo(() => {
    if (data.length === 0) return [];
    const dietStats = {};
    data.forEach(row => {
      const diet = row.diet_type;
      if (!dietStats[diet]) {
        dietStats[diet] = { diet, totalBMI: 0, totalCalories: 0, count: 0 };
      }
      dietStats[diet].totalBMI += row.BMI || 0;
      dietStats[diet].totalCalories += row.Calories || 0;
      dietStats[diet].count += 1;
    });
    return Object.values(dietStats).map(stat => ({
      diet: stat.diet,
      avgBMI: (stat.totalBMI / stat.count).toFixed(2),
      avgCalories: Math.round(stat.totalCalories / stat.count),
      count: stat.count
    }));
  }, [data]);

  const bmiCategories = useMemo(() => {
    if (data.length === 0) return [];
    const categories = {
      'Underweight': 0,
      'Normal': 0,
      'Overweight': 0,
      'Obese': 0
    };
    data.forEach(row => {
      const bmi = row.BMI;
      if (bmi < 18.5) categories['Underweight']++;
      else if (bmi < 25) categories['Normal']++;
      else if (bmi < 30) categories['Overweight']++;
      else categories['Obese']++;
    });
    return Object.entries(categories).map(([name, value]) => ({ name, value }));
  }, [data]);

  const experienceLevelData = useMemo(() => {
    if (data.length === 0) return [];
    const levels = {};
    data.forEach(row => {
      const level = row.Experience_Level < 2 ? 'Beginner' : 
                    row.Experience_Level < 3 ? 'Intermediate' : 'Advanced';
      if (!levels[level]) {
        levels[level] = { level, totalCalories: 0, count: 0 };
      }
      levels[level].totalCalories += row.Calories_Burned || 0;
      levels[level].count += 1;
    });
    return Object.values(levels).map(stat => ({
      level: stat.level,
      avgCalories: Math.round(stat.totalCalories / stat.count),
      count: stat.count
    }));
  }, [data]);

  const topExercises = useMemo(() => {
    if (data.length === 0) return [];
    const exercises = {};
    data.forEach(row => {
      const name = row['Name of Exercise'];
      exercises[name] = (exercises[name] || 0) + 1;
    });
    return Object.entries(exercises)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([name, count]) => ({ name, count }));
  }, [data]);

  const bodyPartData = useMemo(() => {
    if (data.length === 0) return [];
    const parts = {};
    data.forEach(row => {
      const part = row['Body Part'];
      parts[part] = (parts[part] || 0) + 1;
    });
    return Object.entries(parts).map(([name, value]) => ({ name, value }));
  }, [data]);

  const ageVsBMI = useMemo(() => {
    if (data.length === 0) return [];
    return data.slice(0, 500).map(row => ({
      age: row.Age,
      bmi: row.BMI,
      gender: row.Gender
    }));
  }, [data]);

  const calorieBalanceTrend = useMemo(() => {
    if (data.length === 0) return [];
    const ageGroups = {};
    data.forEach(row => {
      const ageGroup = Math.floor(row.Age / 10) * 10;
      if (!ageGroups[ageGroup]) {
        ageGroups[ageGroup] = { ageGroup: `${ageGroup}s`, totalBalance: 0, count: 0 };
      }
      ageGroups[ageGroup].totalBalance += row.cal_balance || 0;
      ageGroups[ageGroup].count += 1;
    });
    return Object.values(ageGroups)
      .map(group => ({
        ageGroup: group.ageGroup,
        avgBalance: Math.round(group.totalBalance / group.count)
      }))
      .sort((a, b) => parseInt(a.ageGroup) - parseInt(b.ageGroup));
  }, [data]);

  const macroDistribution = useMemo(() => {
    if (data.length === 0) return [];
    const avgCarbs = data.reduce((sum, row) => sum + (row.Carbs || 0), 0) / data.length;
    const avgProteins = data.reduce((sum, row) => sum + (row.Proteins || 0), 0) / data.length;
    const avgFats = data.reduce((sum, row) => sum + (row.Fats || 0), 0) / data.length;
    return [
      { name: 'Carbs', value: Math.round(avgCarbs) },
      { name: 'Proteins', value: Math.round(avgProteins) },
      { name: 'Fats', value: Math.round(avgFats) }
    ];
  }, [data]);

  const COLORS = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444', '#06b6d4', '#ec4899'];

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600 text-lg">Loading fitness data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={darkMode ? 'dark' : ''}>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 p-6">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-2">
                Fitness & Nutrition Analytics Dashboard
              </h1>
              <p className="text-gray-600 dark:text-gray-300">
                Comprehensive analysis of {data.length.toLocaleString()} fitness records
              </p>
            </div>
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="px-4 py-2 bg-gray-800 dark:bg-gray-200 text-white dark:text-gray-800 rounded-lg hover:opacity-80 transition"
            >
              {darkMode ? '☀️ Light' : '🌙 Dark'}
            </button>
          </div>

          {/* Filters */}
          <div className="mt-6 flex gap-4">
            <select
              value={selectedWorkout}
              onChange={(e) => setSelectedWorkout(e.target.value)}
              className="px-4 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-800 dark:text-white"
            >
              <option value="All">All Workouts</option>
              <option value="Cardio">Cardio</option>
              <option value="Strength">Strength</option>
              <option value="HIIT">HIIT</option>
              <option value="Yoga">Yoga</option>
            </select>
            <select
              value={selectedDiet}
              onChange={(e) => setSelectedDiet(e.target.value)}
              className="px-4 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-800 dark:text-white"
            >
              <option value="All">All Diets</option>
              <option value="Balanced">Balanced</option>
              <option value="Keto">Keto</option>
              <option value="Paleo">Paleo</option>
              <option value="Vegan">Vegan</option>
              <option value="Vegetarian">Vegetarian</option>
              <option value="Low-Carb">Low-Carb</option>
            </select>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 border-l-4 border-blue-500">
            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Records</div>
            <div className="text-3xl font-bold text-gray-800 dark:text-white">{stats.totalRecords.toLocaleString()}</div>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 border-l-4 border-purple-500">
            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Avg Age</div>
            <div className="text-3xl font-bold text-gray-800 dark:text-white">{stats.avgAge} years</div>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 border-l-4 border-green-500">
            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Avg BMI</div>
            <div className="text-3xl font-bold text-gray-800 dark:text-white">{stats.avgBMI}</div>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 border-l-4 border-orange-500">
            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Avg Calories Burned</div>
            <div className="text-3xl font-bold text-gray-800 dark:text-white">{stats.avgCaloriesBurned}</div>
          </div>
        </div>

        {/* Secondary Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Avg Calorie Intake</div>
            <div className="text-2xl font-bold text-gray-800 dark:text-white">{stats.avgCaloriesIntake} cal</div>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Avg Calorie Balance</div>
            <div className="text-2xl font-bold text-gray-800 dark:text-white">{stats.avgCalorieBalance} cal</div>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Avg Workout Duration</div>
            <div className="text-2xl font-bold text-gray-800 dark:text-white">{stats.avgWorkoutDuration} hrs</div>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Avg Water Intake</div>
            <div className="text-2xl font-bold text-gray-800 dark:text-white">{stats.avgWaterIntake} L</div>
          </div>
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Workout Type Analysis */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">Workout Type Performance</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={workoutTypeData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="type" stroke="#6b7280" />
                <YAxis stroke="#6b7280" />
                <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }} />
                <Legend />
                <Bar dataKey="avgCalories" fill="#3b82f6" name="Avg Calories Burned" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Gender Distribution */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">Gender Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={genderDistribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {genderDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* BMI Categories */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">BMI Categories</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={bmiCategories}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="name" stroke="#6b7280" />
                <YAxis stroke="#6b7280" />
                <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }} />
                <Bar dataKey="value" fill="#10b981" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Diet Type Analysis */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">Diet Type vs BMI</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={dietTypeData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="diet" stroke="#6b7280" />
                <YAxis stroke="#6b7280" />
                <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }} />
                <Legend />
                <Bar dataKey="avgBMI" fill="#8b5cf6" name="Avg BMI" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Experience Level */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">Experience Level Impact</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={experienceLevelData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="level" stroke="#6b7280" />
                <YAxis stroke="#6b7280" />
                <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }} />
                <Bar dataKey="avgCalories" fill="#f59e0b" name="Avg Calories Burned" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Top Exercises */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">Top 10 Exercises</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={topExercises} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis type="number" stroke="#6b7280" />
                <YAxis dataKey="name" type="category" stroke="#6b7280" width={120} />
                <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }} />
                <Bar dataKey="count" fill="#ef4444" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Body Part Distribution */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">Body Part Focus</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={bodyPartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {bodyPartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Calorie Balance Trend */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">Calorie Balance by Age Group</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={calorieBalanceTrend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="ageGroup" stroke="#6b7280" />
                <YAxis stroke="#6b7280" />
                <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }} />
                <Legend />
                <Line type="monotone" dataKey="avgBalance" stroke="#06b6d4" strokeWidth={2} name="Avg Calorie Balance" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Full Width Charts */}
        <div className="grid grid-cols-1 gap-6 mb-8">
          {/* Age vs BMI Scatter */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">Age vs BMI Correlation (Sample)</h3>
            <ResponsiveContainer width="100%" height={400}>
              <ScatterChart>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="age" name="Age" stroke="#6b7280" />
                <YAxis dataKey="bmi" name="BMI" stroke="#6b7280" />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }} />
                <Legend />
                <Scatter name="Male" data={ageVsBMI.filter(d => d.gender === 'Male')} fill="#3b82f6" />
                <Scatter name="Female" data={ageVsBMI.filter(d => d.gender === 'Female')} fill="#ec4899" />
              </ScatterChart>
            </ResponsiveContainer>
          </div>

          {/* Macro Distribution */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">Average Macronutrient Distribution</h3>
            <ResponsiveContainer width="100%" height={400}>
              <PieChart>
                <Pie
                  data={macroDistribution}
                  cx="50%"
                  cy="50%"
                  labelLine={true}
                  label={({ name, value }) => `${name}: ${value}g`}
                  outerRadius={150}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {macroDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-gray-600 dark:text-gray-400 mt-8">
          <p>Dashboard analyzing {data.length.toLocaleString()} complete fitness and nutrition records</p>
          <p className="text-sm mt-2">Data includes demographics, workout metrics, nutrition data, and exercise details</p>
        </div>
      </div>
    </div>
  );
}

export default App;
