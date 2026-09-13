
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
