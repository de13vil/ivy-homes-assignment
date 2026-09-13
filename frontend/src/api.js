
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
