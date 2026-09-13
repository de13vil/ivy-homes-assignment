import os

files = {
    'tailwind.config.js': '''/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}''',
    
    'postcss.config.js': '''export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}''',

    'src/index.css': '''@tailwind base;
@tailwind components;
@tailwind utilities;
body { background-color: #f3f4f6; }
''',

    'src/api.js': '''
const BASE_URL = 'https://solve.ivy.homes';
const API_KEY = 'IVY26-B367969111EC';

export const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token');
    return {
        'X-API-Key': API_KEY,
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
};

export const login = async (email, password) => {
    const res = await fetch(`${BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'X-API-Key': API_KEY, 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    if (!res.ok) throw new Error('Login failed');
    const data = await res.json();
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
};

export const refreshToken = async () => {
    const refresh = localStorage.getItem('refresh_token');
    if (!refresh) throw new Error('No refresh token');
    const res = await fetch(`${BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: { 'X-API-Key': API_KEY, 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refresh })
    });
    if (!res.ok) {
        localStorage.clear();
        throw new Error('Refresh failed');
    }
    const data = await res.json();
    localStorage.setItem('access_token', data.access_token);
    return data.access_token;
};

const fetchWithAuth = async (url, options = {}) => {
    let res = await fetch(url, { ...options, headers: getAuthHeaders() });
    if (res.status === 401) {
        await refreshToken();
        res = await fetch(url, { ...options, headers: getAuthHeaders() });
    }
    if (!res.ok) throw new Error(`API Error: ${res.status}`);
    return res.json();
};

export const getListings = async (endpoint, filters, offset = 0, limit = 50) => {
    const params = new URLSearchParams({ offset, limit });
    for (const [key, val] of Object.entries(filters)) {
        if (val) params.append(key, val);
    }
    return fetchWithAuth(`${BASE_URL}/v1/${endpoint}?${params.toString()}`);
};

export const getAnalytics = async () => fetchWithAuth(`${BASE_URL}/v1/analytics/summary`);
export const getSaved = async () => fetchWithAuth(`${BASE_URL}/v1/saved`);
export const addSaved = async (id) => fetchWithAuth(`${BASE_URL}/v1/saved`, { method: 'POST', body: JSON.stringify({ listing_id: id }) });
export const removeSaved = async (id) => fetchWithAuth(`${BASE_URL}/v1/saved/${id}`, { method: 'DELETE' });
''',

    'src/AuthContext.jsx': '''
import React, { createContext, useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(() => JSON.parse(localStorage.getItem('user')));
    const navigate = useNavigate();

    const logout = () => {
        localStorage.clear();
        setUser(null);
        navigate('/login');
    };

    return (
        <AuthContext.Provider value={{ user, setUser, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
export const useAuth = () => useContext(AuthContext);
''',

    'src/App.jsx': '''
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Listings from './pages/Listings';
import Saved from './pages/Saved';
import Insights from './pages/Insights';

const Protected = ({ children }) => {
    const { user } = useAuth();
    if (!user) return <Navigate to="/login" />;
    return <><Navbar /><div className="max-w-7xl mx-auto p-4">{children}</div></>;
};

function App() {
    return (
        <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<Protected><Listings endpoint="listings" /></Protected>} />
            <Route path="/rentals" element={<Protected><Listings endpoint="rentals" /></Protected>} />
            <Route path="/projects" element={<Protected><Listings endpoint="projects" isProjects={true} /></Protected>} />
            <Route path="/saved" element={<Protected><Saved /></Protected>} />
            <Route path="/insights" element={<Protected><Insights /></Protected>} />
        </Routes>
    );
}
export default App;
''',

    'src/main.jsx': '''
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';
import { AuthProvider } from './AuthContext';

ReactDOM.createRoot(document.getElementById('root')).render(
    <BrowserRouter>
        <AuthProvider>
            <App />
        </AuthProvider>
    </BrowserRouter>
);
''',

    'src/components/Navbar.jsx': '''
import { Link } from 'react-router-dom';
import { useAuth } from '../AuthContext';

export default function Navbar() {
    const { user, logout } = useAuth();
    return (
        <nav className="bg-white shadow p-4 flex justify-between items-center mb-6">
            <div className="font-bold text-xl text-blue-600">Ivy Homes</div>
            <div className="flex gap-4 items-center">
                <Link to="/" className="hover:text-blue-500">Buy</Link>
                <Link to="/rentals" className="hover:text-blue-500">Rent</Link>
                <Link to="/projects" className="hover:text-blue-500">Projects</Link>
                <Link to="/saved" className="hover:text-blue-500">Saved</Link>
                <Link to="/insights" className="hover:text-blue-500">Insights</Link>
                <span className="text-gray-500 ml-4">{user?.email}</span>
                <button onClick={logout} className="text-sm bg-red-100 text-red-600 px-3 py-1 rounded">Logout</button>
            </div>
        </nav>
    );
}
''',

    'src/components/ListingCard.jsx': '''
import { useState } from 'react';
import { addSaved, removeSaved } from '../api';

export default function ListingCard({ item, isProject, isSavedList, onRemove }) {
    const [saved, setSaved] = useState(isSavedList);
    const id = item.listing_id || item.project_id;
    
    const handleSave = async () => {
        if (saved) {
            await removeSaved(id);
            setSaved(false);
            if (onRemove) onRemove(id);
        } else {
            await addSaved(id);
            setSaved(true);
        }
    };

    return (
        <div className="bg-white p-4 rounded shadow">
            <img src="https://placehold.co/600x400?text=Property" className="w-full h-48 object-cover rounded mb-4" />
            <div className="flex justify-between items-start">
                <h3 className="font-bold text-lg">{item.apartment_name || item.title || item.developer_name}</h3>
                <button onClick={handleSave} className={saved ? "text-red-500" : "text-gray-400"}>
                    {saved ? '♥ Saved' : '♡ Save'}
                </button>
            </div>
            <p className="text-gray-500 capitalize">{item.locality} • {item.property_type || item.project_status}</p>
            
            {isProject ? (
                <div className="mt-2 text-blue-600 font-bold">
                    Max: {item.price_max < 15 ? `${item.price_max} Cr` : `${item.price_max} L`}
                </div>
            ) : (
                <div className="mt-2 text-blue-600 font-bold">₹ {item.price?.toLocaleString()}</div>
            )}
            
            {!isProject && <p className="text-sm mt-1">{item.bedroom} BHK • {item.carpet_area} sqft</p>}
        </div>
    );
}
''',

    'src/pages/Login.jsx': '''
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api';
import { useAuth } from '../AuthContext';

export default function Login() {
    const [email, setEmail] = useState('demo1@ivy.homes');
    const [password, setPassword] = useState('ceb39868a2');
    const [err, setErr] = useState('');
    const { setUser } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = await login(email, password);
            setUser(data.user);
            navigate('/');
        } catch (error) {
            setErr('Login failed. Check credentials.');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <form onSubmit={handleSubmit} className="bg-white p-8 rounded shadow-md w-96">
                <h2 className="text-2xl font-bold mb-6 text-center text-blue-600">Ivy Homes</h2>
                {err && <div className="bg-red-100 text-red-600 p-2 rounded mb-4 text-sm">{err}</div>}
                <input type="email" value={email} onChange={e=>setEmail(e.target.value)} className="w-full border p-2 mb-4 rounded" />
                <input type="password" value={password} onChange={e=>setPassword(e.target.value)} className="w-full border p-2 mb-6 rounded" />
                <button className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">Login</button>
            </form>
        </div>
    );
}
''',

    'src/pages/Listings.jsx': '''
import { useState, useEffect } from 'react';
import { getListings } from '../api';
import ListingCard from '../components/ListingCard';

export default function Listings({ endpoint, isProjects = false }) {
    const [data, setData] = useState([]);
    const [offset, setOffset] = useState(0);
    const [total, setTotal] = useState(0);
    const [filters, setFilters] = useState({ locality: '', bhk: '' });

    useEffect(() => {
        setOffset(0);
        fetchData(0, true);
    }, [endpoint, filters]);

    const fetchData = async (currentOffset, reset = false) => {
        try {
            const res = await getListings(endpoint, filters, currentOffset, 50);
            
            // Client side filtering for is_live because API returns inactive listings!
            let results = res.results;
            if (!isProjects) {
                results = results.filter(r => r.is_live);
            }
            
            setData(reset ? results : [...data, ...results]);
            setTotal(res.total);
        } catch (e) {
            console.error(e);
        }
    };

    const loadMore = () => {
        const next = offset + 50;
        setOffset(next);
        fetchData(next);
    };

    return (
        <div className="flex gap-6">
            <div className="w-64 bg-white p-4 rounded shadow h-fit">
                <h3 className="font-bold mb-4">Filters</h3>
                <label className="block text-sm mb-1">Locality</label>
                <input type="text" placeholder="e.g. balewadi" className="w-full border p-2 rounded mb-4" 
                       value={filters.locality} onChange={e => setFilters({...filters, locality: e.target.value})} />
                
                {!isProjects && (
                    <>
                        <label className="block text-sm mb-1">Bedrooms</label>
                        <input type="number" placeholder="e.g. 2" className="w-full border p-2 rounded mb-4"
                               value={filters.bhk} onChange={e => setFilters({...filters, bhk: e.target.value})} />
                    </>
                )}
            </div>
            <div className="flex-1">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {data.map((item, i) => <ListingCard key={i} item={item} isProject={isProjects} />)}
                </div>
                {data.length > 0 && data.length < total && (
                    <button onClick={loadMore} className="mt-8 w-full bg-blue-100 text-blue-700 py-3 rounded font-bold hover:bg-blue-200">
                        Load More (Offset: {offset+50})
                    </button>
                )}
            </div>
        </div>
    );
}
''',

    'src/pages/Saved.jsx': '''
import { useState, useEffect } from 'react';
import { getSaved } from '../api';
import ListingCard from '../components/ListingCard';

export default function Saved() {
    const [data, setData] = useState([]);

    useEffect(() => {
        getSaved().then(res => setData(res.results)).catch(console.error);
    }, []);

    const handleRemove = (id) => {
        setData(data.filter(item => item.listing_id !== id && item.project_id !== id));
    };

    return (
        <div>
            <h2 className="text-2xl font-bold mb-6">Saved Properties</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {data.map(item => (
                    <ListingCard key={item.listing_id || item.project_id} item={item} isSavedList={true} onRemove={handleRemove} />
                ))}
            </div>
            {data.length === 0 && <p className="text-gray-500">No saved properties yet.</p>}
        </div>
    );
}
''',

    'src/pages/Insights.jsx': '''
import { useState, useEffect } from 'react';
import { getAnalytics } from '../api';

export default function Insights() {
    const [data, setData] = useState(null);

    useEffect(() => {
        getAnalytics().then(setData).catch(console.error);
    }, []);

    if (!data) return <div>Loading...</div>;

    return (
        <div>
            <h2 className="text-2xl font-bold mb-6">City Insights: {data.city}</h2>
            <div className="grid grid-cols-3 gap-4 mb-8">
                <div className="bg-white p-6 rounded shadow text-center">
                    <div className="text-gray-500">Total Listings</div>
                    <div className="text-3xl font-bold text-blue-600">{data.total_listings}</div>
                </div>
                <div className="bg-white p-6 rounded shadow text-center">
                    <div className="text-gray-500">Median Price</div>
                    <div className="text-3xl font-bold text-blue-600">₹ {(data.median_price/100000).toFixed(2)} L</div>
                </div>
                <div className="bg-white p-6 rounded shadow text-center">
                    <div className="text-gray-500">Median Price / sqft</div>
                    <div className="text-3xl font-bold text-blue-600">₹ {data.median_price_per_sqft}</div>
                </div>
            </div>
            
            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-8">
                <h3 className="font-bold text-yellow-800">Developer Notes (Discovered Lies)</h3>
                <ul className="list-disc pl-5 mt-2 text-yellow-700">
                    <li>The API claims projects are priced in raw INR, but they actually return decimals in Crores/Lakhs!</li>
                    <li>Pagination claims to use 'page', but silently ignores it and expects 'offset'.</li>
                    <li>The API claims to filter out inactive listings, but it doesn't! We built client-side filtering to fix it.</li>
                </ul>
            </div>
        </div>
    );
}
'''
}

for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("React app structure generated successfully.")
