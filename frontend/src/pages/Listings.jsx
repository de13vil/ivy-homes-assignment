import { useState, useEffect } from 'react';
import { getListings } from '../api';
import ListingCard from '../components/ListingCard';

const LOCALITIES = [
    '', 'balewadi', 'hinjewadi', 'kothrud', 
    'baner', 'magarpatta', 'kharadi', 'viman nagar'
];

export default function Listings({ endpoint, isProjects = false }) {
    const [data, setData] = useState([]);
    const [offset, setOffset] = useState(0);
    const [total, setTotal] = useState(0);
    const [filters, setFilters] = useState({ locality: '', bhk: '' });
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        setOffset(0);
        fetchData(0, true);
    }, [endpoint, filters]);

    const fetchData = async (currentOffset, reset = false) => {
        setLoading(true);
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
        } finally {
            setLoading(false);
        }
    };

    const loadMore = () => {
        const next = offset + 50;
        setOffset(next);
        fetchData(next);
    };

    return (
        <div className="flex gap-6">
            <div className="w-64 bg-white p-4 rounded shadow h-fit border border-gray-100">
                <h3 className="font-bold mb-4 text-blue-600">Filters</h3>
                
                <label className="block text-sm mb-1 font-medium">Locality</label>
                <select 
                    className="w-full border border-gray-300 p-2 rounded mb-4 bg-white" 
                    value={filters.locality} 
                    onChange={e => setFilters({...filters, locality: e.target.value})}
                >
                    <option value="">All Localities</option>
                    {LOCALITIES.filter(l => l !== '').map(loc => (
                        <option key={loc} value={loc} className="capitalize">{loc}</option>
                    ))}
                </select>
                
                {!isProjects && (
                    <>
                        <label className="block text-sm mb-1 font-medium">Bedrooms (BHK)</label>
                        <select 
                            className="w-full border border-gray-300 p-2 rounded mb-4 bg-white"
                            value={filters.bhk} 
                            onChange={e => setFilters({...filters, bhk: e.target.value})}
                        >
                            <option value="">Any</option>
                            <option value="1">1 BHK</option>
                            <option value="2">2 BHK</option>
                            <option value="3">3 BHK</option>
                            <option value="4">4+ BHK</option>
                        </select>
                    </>
                )}
            </div>
            
            <div className="flex-1">
                {data.length === 0 && !loading && (
                    <div className="text-gray-500 bg-white p-8 rounded text-center border border-gray-100">
                        No properties found matching these filters.
                    </div>
                )}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {data.map((item, i) => <ListingCard key={i} item={item} isProject={isProjects} />)}
                </div>
                {data.length > 0 && data.length < total && (
                    <button onClick={loadMore} className="mt-8 w-full bg-blue-50 text-blue-700 py-3 rounded font-bold hover:bg-blue-100 border border-blue-200 transition-colors">
                        {loading ? 'Loading...' : `Load More (Showing ${data.length} of ${total})`}
                    </button>
                )}
            </div>
        </div>
    );
}
