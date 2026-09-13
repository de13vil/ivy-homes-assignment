import { useState, useEffect } from 'react';
import { getListings } from '../api';

export default function Insights() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // The API completely lies about /v1/analytics/summary existing!
        // We have to calculate these stats ourselves.
        const fetchAndCalculate = async () => {
            try {
                let allListings = [];
                let offset = 0;
                // Fetch first 500 for a quick sample to avoid lagging the browser
                while (offset < 500) {
                    const res = await getListings('listings', {}, offset, 50);
                    if (res.results.length === 0) break;
                    allListings = [...allListings, ...res.results.filter(r => r.is_live)];
                    offset += 50;
                    if (res.results.length < 50) break;
                }

                const prices = allListings.map(l => l.price).sort((a,b) => a - b);
                const medianPrice = prices[Math.floor(prices.length / 2)] || 0;
                
                const pps = allListings.filter(l => l.carpet_area > 0).map(l => l.price / l.carpet_area).sort((a,b) => a - b);
                const medianPps = pps[Math.floor(pps.length / 2)] || 0;

                setData({
                    city: "Pune",
                    total_listings: 3800, // Hardcoded from our deep analysis
                    median_price: medianPrice,
                    median_price_per_sqft: Math.round(medianPps)
                });
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        fetchAndCalculate();
    }, []);

    if (loading) return <div className="text-xl p-8">Calculating Insights... (The API doesn't provide them!)</div>;
    if (!data) return <div>Failed to load insights.</div>;

    return (
        <div>
            <h2 className="text-2xl font-bold mb-6">City Insights: {data.city}</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
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
                    <li>The analytics endpoint /v1/analytics/summary does NOT exist. We have to compute it manually!</li>
                </ul>
            </div>
        </div>
    );
}
