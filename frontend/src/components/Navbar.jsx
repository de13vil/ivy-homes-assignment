import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../AuthContext';

export default function Navbar() {
    const { user, logout } = useAuth();
    const location = useLocation();

    const getLinkClass = (path) => {
        const base = "px-3 py-2 rounded-md text-sm font-medium transition-colors ";
        return location.pathname === path 
            ? base + "bg-blue-50 text-blue-700" 
            : base + "text-gray-600 hover:bg-gray-50 hover:text-blue-600";
    };

    return (
        <nav className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16 items-center">
                    <div className="flex items-center gap-8">
                        <Link to="/" className="flex items-center gap-2">
                            <div className="bg-blue-600 text-white p-2 rounded-lg font-bold text-xl leading-none shadow-sm">IH</div>
                            <span className="font-bold text-xl text-gray-900 tracking-tight">Ivy Homes</span>
                        </Link>
                        <div className="hidden md:flex gap-2">
                            <Link to="/" className={getLinkClass('/')}>Buy</Link>
                            <Link to="/rentals" className={getLinkClass('/rentals')}>Rent</Link>
                            <Link to="/projects" className={getLinkClass('/projects')}>Projects</Link>
                            <Link to="/saved" className={getLinkClass('/saved')}>Saved</Link>
                            <Link to="/insights" className={getLinkClass('/insights')}>Insights</Link>
                        </div>
                    </div>
                    <div className="flex items-center gap-4">
                        <div className="flex flex-col items-end hidden sm:flex">
                            <span className="text-sm font-medium text-gray-900">{user?.name || 'Demo User'}</span>
                            <span className="text-xs text-gray-500">{user?.email}</span>
                        </div>
                        <button 
                            onClick={logout} 
                            className="text-sm bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-50 hover:text-red-600 transition-colors shadow-sm font-medium"
                        >
                            Log out
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    );
}
