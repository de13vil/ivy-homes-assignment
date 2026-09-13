
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
