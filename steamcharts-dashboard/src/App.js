import React, { useState, useEffect, useMemo } from 'react';
import { BarChart, Bar, Line, PieChart, Pie, Cell, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import Papa from 'papaparse';

function App() {
  const [data, setData] = useState([]);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedGame, setSelectedGame] = useState(null);
  const [darkMode, setDarkMode] = useState(true);

  useEffect(() => {
    console.log('Starting data load...');
    // Load insights JSON
    fetch('/steamcharts_insights.json')
      .then(r => r.json())
      .then(insightsData => {
        console.log('Insights loaded:', insightsData);
        setInsights(insightsData);
      })
      .catch(err => console.error('Insights error:', err));

    // Load CSV data (using sample for performance)
    fetch('/steamcharts_sample.csv')
      .then(r => r.text())
      .then(text => {
        Papa.parse(text, {
          header: true,
          dynamicTyping: true,
          complete: (results) => {
            const cleanData = results.data.filter(row => row.name && row.steam_appid);
            console.log('Loaded data:', cleanData.length, 'rows');
            setData(cleanData);
            setLoading(false);
          },
          error: (error) => {
            console.error('Parse error:', error);
            setLoading(false);
          }
        });
      })
      .catch(err => {
        console.error('Fetch error:', err);
        setLoading(false);
      });
  }, []);

  const stats = useMemo(() => {
    if (!data.length || !insights) return null;

    const latestMonth = data[0]?.month;
    const latestData = data.filter(d => d.month === latestMonth);
    
    return {
      totalGames: new Set(data.map(d => d.steam_appid)).size,
      totalRecords: data.length,
      avgPlayers: latestData.reduce((sum, d) => sum + (d.avg_players || 0), 0) / latestData.length,
      topGame: latestData.sort((a, b) => b.avg_players - a.avg_players)[0]
    };
  }, [data, insights]);

  const topGamesData = useMemo(() => {
    if (!insights?.latest_month?.top_10_games) return [];
    return insights.latest_month.top_10_games.map(g => ({
      name: g.name.length > 20 ? g.name.substring(0, 20) + '...' : g.name,
      players: Math.round(g.avg_players),
      peak: g.peak_players
    }));
  }, [insights]);

  const marketSegmentData = useMemo(() => {
    if (!insights?.market_segments) return [];
    return Object.entries(insights.market_segments).map(([name, data]) => ({
      name,
      count: data.count,
      growth: data.avg_growth_percent.toFixed(2)
    }));
  }, [insights]);

  const growthDeclineData = useMemo(() => {
    if (!insights?.latest_month) return { growth: [], decline: [] };
    return {
      growth: insights.latest_month.fastest_growing.slice(0, 10).map(g => ({
        name: g.name.length > 15 ? g.name.substring(0, 15) + '...' : g.name,
        growth: g.gain_percent.toFixed(2)
      })),
      decline: insights.latest_month.biggest_declines.slice(0, 10).map(g => ({
        name: g.name.length > 15 ? g.name.substring(0, 15) + '...' : g.name,
        decline: Math.abs(g.gain_percent).toFixed(2)
      }))
    };
  }, [insights]);

  const gameTimeSeries = useMemo(() => {
    if (!selectedGame || !data.length) return [];
    
    const gameData = data
      .filter(d => d.steam_appid === selectedGame)
      .sort((a, b) => {
        const parseMonth = (m) => {
          const [month, year] = m.split('-');
          return new Date(`20${year}`, ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'].indexOf(month));
        };
        return parseMonth(a.month) - parseMonth(b.month);
      })
      .slice(-24); // Last 24 months
    
    return gameData.map(d => ({
      month: d.month,
      players: Math.round(d.avg_players),
      peak: d.peak_players
    }));
  }, [selectedGame, data]);

  const allTimePeaksData = useMemo(() => {
    if (!insights?.all_time_peaks) return [];
    return Object.entries(insights.all_time_peaks)
      .slice(0, 15)
      .map(([name, peak]) => ({
        name: name.length > 20 ? name.substring(0, 20) + '...' : name,
        peak
      }));
  }, [insights]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-2xl">Loading Steam Charts Data...</div>
      </div>
    );
  }

  if (!data.length || !insights) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-2xl">No data loaded. Check console for errors.</div>
      </div>
    );
  }

  const bgClass = darkMode ? 'bg-gradient-to-br from-gray-900 to-gray-800' : 'bg-gradient-to-br from-gray-50 to-gray-100';
  const cardClass = darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200';
  const textClass = darkMode ? 'text-white' : 'text-gray-900';
  const textSecondaryClass = darkMode ? 'text-gray-400' : 'text-gray-600';

  return (
    <div className={`min-h-screen ${bgClass} p-6`}>
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="flex justify-between items-center">
          <div>
            <h1 className={`text-4xl font-bold ${textClass} mb-2`}>Steam Charts Analytics Dashboard</h1>
            <p className={textSecondaryClass}>Comprehensive analysis of {stats?.totalGames.toLocaleString()} games across {insights?.dataset_overview?.months_covered} months</p>
          </div>
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition"
          >
            {darkMode ? '☀️ Light' : '🌙 Dark'}
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className={`${cardClass} border rounded-lg p-6 shadow-lg`}>
          <div className={`text-sm ${textSecondaryClass} mb-2`}>Total Games</div>
          <div className={`text-3xl font-bold ${textClass}`}>{stats?.totalGames.toLocaleString()}</div>
          <div className="text-xs text-blue-500 mt-2">Tracked on Steam</div>
        </div>
        
        <div className={`${cardClass} border rounded-lg p-6 shadow-lg`}>
          <div className={`text-sm ${textSecondaryClass} mb-2`}>Data Points</div>
          <div className={`text-3xl font-bold ${textClass}`}>{stats?.totalRecords.toLocaleString()}</div>
          <div className="text-xs text-green-500 mt-2">Monthly records</div>
        </div>
        
        <div className={`${cardClass} border rounded-lg p-6 shadow-lg`}>
          <div className={`text-sm ${textSecondaryClass} mb-2`}>Avg Players/Game</div>
          <div className={`text-3xl font-bold ${textClass}`}>{Math.round(stats?.avgPlayers).toLocaleString()}</div>
          <div className="text-xs text-purple-500 mt-2">Latest month</div>
        </div>
        
        <div className={`${cardClass} border rounded-lg p-6 shadow-lg`}>
          <div className={`text-sm ${textSecondaryClass} mb-2`}>Top Game</div>
          <div className={`text-xl font-bold ${textClass} truncate`}>{stats?.topGame?.name}</div>
          <div className="text-xs text-orange-500 mt-2">{Math.round(stats?.topGame?.avg_players).toLocaleString()} players</div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Top Games Chart */}
        <div className={`${cardClass} border rounded-lg p-6 shadow-lg`}>
          <h2 className={`text-xl font-bold ${textClass} mb-4`}>Top 10 Games by Player Count</h2>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={topGamesData}>
              <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? "#374151" : "#e5e7eb"} />
              <XAxis dataKey="name" stroke={darkMode ? "#9ca3af" : "#6b7280"} angle={-45} textAnchor="end" height={100} />
              <YAxis stroke={darkMode ? "#9ca3af" : "#6b7280"} />
              <Tooltip 
                contentStyle={{ backgroundColor: darkMode ? '#1f2937' : '#ffffff', border: '1px solid #374151' }}
                labelStyle={{ color: darkMode ? '#ffffff' : '#000000' }}
              />
              <Legend />
              <Bar dataKey="players" fill="#3b82f6" name="Avg Players" />
              <Bar dataKey="peak" fill="#8b5cf6" name="Peak Players" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Market Segments */}
        <div className={`${cardClass} border rounded-lg p-6 shadow-lg`}>
          <h2 className={`text-xl font-bold ${textClass} mb-4`}>Market Segments Distribution</h2>
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={marketSegmentData}
                dataKey="count"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={120}
                label={(entry) => `${entry.name}: ${entry.count}`}
              >
                {marketSegmentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444'][index % 5]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ backgroundColor: darkMode ? '#1f2937' : '#ffffff', border: '1px solid #374151' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Fastest Growing Games */}
        <div className={`${cardClass} border rounded-lg p-6 shadow-lg`}>
          <h2 className={`text-xl font-bold ${textClass} mb-4`}>Fastest Growing Games</h2>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={growthDeclineData.growth} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? "#374151" : "#e5e7eb"} />
              <XAxis type="number" stroke={darkMode ? "#9ca3af" : "#6b7280"} />
              <YAxis dataKey="name" type="category" stroke={darkMode ? "#9ca3af" : "#6b7280"} width={120} />
              <Tooltip 
                contentStyle={{ backgroundColor: darkMode ? '#1f2937' : '#ffffff', border: '1px solid #374151' }}
              />
              <Bar dataKey="growth" fill="#10b981" name="Growth %" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Biggest Declines */}
        <div className={`${cardClass} border rounded-lg p-6 shadow-lg`}>
          <h2 className={`text-xl font-bold ${textClass} mb-4`}>Biggest Declines</h2>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={growthDeclineData.decline} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? "#374151" : "#e5e7eb"} />
              <XAxis type="number" stroke={darkMode ? "#9ca3af" : "#6b7280"} />
              <YAxis dataKey="name" type="category" stroke={darkMode ? "#9ca3af" : "#6b7280"} width={120} />
              <Tooltip 
                contentStyle={{ backgroundColor: darkMode ? '#1f2937' : '#ffffff', border: '1px solid #374151' }}
              />
              <Bar dataKey="decline" fill="#ef4444" name="Decline %" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* All-Time Peak Players */}
        <div className={`${cardClass} border rounded-lg p-6 shadow-lg lg:col-span-2`}>
          <h2 className={`text-xl font-bold ${textClass} mb-4`}>All-Time Peak Players</h2>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={allTimePeaksData}>
              <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? "#374151" : "#e5e7eb"} />
              <XAxis dataKey="name" stroke={darkMode ? "#9ca3af" : "#6b7280"} angle={-45} textAnchor="end" height={100} />
              <YAxis stroke={darkMode ? "#9ca3af" : "#6b7280"} />
              <Tooltip 
                contentStyle={{ backgroundColor: darkMode ? '#1f2937' : '#ffffff', border: '1px solid #374151' }}
              />
              <Bar dataKey="peak" fill="#f59e0b" name="Peak Players" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Game Selector and Time Series */}
        <div className={`${cardClass} border rounded-lg p-6 shadow-lg lg:col-span-2`}>
          <h2 className={`text-xl font-bold ${textClass} mb-4`}>Game Time Series Analysis</h2>
          <select
            className={`w-full p-2 mb-4 rounded border ${darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-900'}`}
            onChange={(e) => setSelectedGame(parseInt(e.target.value))}
            value={selectedGame || ''}
          >
            <option value="">Select a game...</option>
            {topGamesData.map((game, idx) => (
              <option key={idx} value={insights.latest_month.top_10_games[idx].steam_appid}>
                {insights.latest_month.top_10_games[idx].name}
              </option>
            ))}
          </select>
          
          {selectedGame && gameTimeSeries.length > 0 ? (
            <ResponsiveContainer width="100%" height={350}>
              <AreaChart data={gameTimeSeries}>
                <defs>
                  <linearGradient id="colorPlayers" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? "#374151" : "#e5e7eb"} />
                <XAxis dataKey="month" stroke={darkMode ? "#9ca3af" : "#6b7280"} />
                <YAxis stroke={darkMode ? "#9ca3af" : "#6b7280"} />
                <Tooltip 
                  contentStyle={{ backgroundColor: darkMode ? '#1f2937' : '#ffffff', border: '1px solid #374151' }}
                />
                <Legend />
                <Area type="monotone" dataKey="players" stroke="#3b82f6" fillOpacity={1} fill="url(#colorPlayers)" name="Avg Players" />
                <Line type="monotone" dataKey="peak" stroke="#8b5cf6" name="Peak Players" />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className={`h-[350px] flex items-center justify-center ${textSecondaryClass}`}>
              Select a game to view its historical data
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="max-w-7xl mx-auto mt-8 text-center">
        <p className={textSecondaryClass}>
          Data spans from {insights?.dataset_overview?.date_range?.start} to {insights?.dataset_overview?.date_range?.end}
        </p>
        <p className={`${textSecondaryClass} text-sm mt-2`}>
          Analyzing {stats?.totalRecords.toLocaleString()} data points across {stats?.totalGames.toLocaleString()} games
        </p>
      </div>
    </div>
  );
}

export default App;
