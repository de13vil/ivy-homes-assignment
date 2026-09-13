
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
