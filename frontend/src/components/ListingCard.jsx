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
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow duration-300 flex flex-col h-full group">
            {/* Image Area with Badges */}
            <div className="relative">
                <div className="w-full h-56 bg-gradient-to-br from-gray-100 to-gray-200 flex flex-col items-center justify-center text-gray-400 font-medium text-sm text-center px-4">
                    <svg className="w-10 h-10 mb-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                    No Image Provided
                </div>
                
                {/* Top Badges */}
                <div className="absolute top-3 left-3 flex gap-2">
                    {item.is_verified && (
                        <span className="bg-green-500 text-white text-xs font-bold px-2 py-1 rounded shadow-sm flex items-center gap-1">
                            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"></path></svg>
                            Verified
                        </span>
                    )}
                    <span className="bg-white/90 backdrop-blur text-gray-800 text-xs font-bold px-2 py-1 rounded shadow-sm capitalize">
                        {item.property_type || item.project_status}
                    </span>
                </div>
                
                {/* Save Button */}
                <button 
                    onClick={handleSave} 
                    className="absolute top-3 right-3 p-2 rounded-full bg-white/90 backdrop-blur shadow-sm hover:scale-110 transition-transform"
                >
                    <svg className={`w-5 h-5 ${saved ? 'text-red-500 fill-current' : 'text-gray-400'}`} fill={saved ? "currentColor" : "none"} stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                    </svg>
                </button>
            </div>
            
            {/* Content Area */}
            <div className="p-5 flex flex-col flex-grow">
                <div className="flex justify-between items-start mb-1">
                    <h3 className="font-bold text-lg text-gray-900 leading-tight line-clamp-1">
                        {item.apartment_name || item.title || item.developer_name}
                    </h3>
                </div>
                
                <p className="text-gray-500 capitalize text-sm mb-4 flex items-center gap-1">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                    {item.locality}
                </p>
                
                <div className="mt-auto">
                    {isProject ? (
                        <div className="text-blue-600 font-extrabold text-2xl mb-3">
                            {item.price_max < 15 ? `₹${item.price_max} Cr` : `₹${item.price_max} L`}
                            <span className="text-sm font-normal text-gray-500 ml-2">(Max)</span>
                        </div>
                    ) : (
                        <div className="text-blue-600 font-extrabold text-2xl mb-3">
                            ₹{item.price?.toLocaleString('en-IN')}
                        </div>
                    )}
                    
                    {!isProject && (
                        <div className="flex gap-3 border-t border-gray-100 pt-3">
                            <div className="flex flex-col">
                                <span className="text-xs text-gray-400 font-medium uppercase tracking-wider">Bedrooms</span>
                                <span className="font-semibold text-gray-700">{item.bedroom} BHK</span>
                            </div>
                            <div className="w-px bg-gray-200"></div>
                            <div className="flex flex-col">
                                <span className="text-xs text-gray-400 font-medium uppercase tracking-wider">Area</span>
                                <span className="font-semibold text-gray-700">{item.carpet_area} sqft</span>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
