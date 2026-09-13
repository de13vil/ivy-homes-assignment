# Ivy Homes - Software Engineering Internship Assignment

## How to Run the Frontend
1. Open a terminal and navigate to the `frontend` folder: `cd frontend`
2. Install the dependencies: `npm install`
3. Start the development server: `npm run dev`
4. Open your browser to `http://localhost:5173`

The app is built using **React, Vite, and Tailwind CSS**.

## Design Decisions & How I Handled the "Lies"
While building the frontend and analyzing the data, I discovered several severe discrepancies between the `API_REFERENCE.md` and the actual API behavior. Here is how I handled them:

### 1. The Pagination Trap
The documentation claims that `GET /v1/listings` accepts a `page` parameter. However, testing the API revealed that it completely ignores `page` and instead expects an `offset` parameter. Furthermore, it strictly caps the response limit at 50 records per page, even if `limit=200` is requested. 
**Solution:** I built a custom fetch handler in `src/api.js` that tracks the `offset` and increments by 50 when the user clicks "Load More", totally bypassing the broken `page` parameter.

### 2. The Authentication Refresh
The docs claim tokens are valid for 24 hours. The API response actually issues a token valid for 15 minutes and requires a refresh flow.
**Solution:** I implemented a robust `fetchWithAuth` wrapper in the API client that intercepts `401 Unauthorized` responses, automatically calls the `/auth/refresh` endpoint, and retries the original request seamlessly.

### 3. Active Listings Bug
The docs state that inactive listings are excluded server-side. However, pulling the raw dataset showed hundreds of listings with `is_live: false`.
**Solution:** I added strict client-side filtering to strip out any records where `is_live` is false before they reach the UI, ensuring users don't see withdrawn properties.

### 4. Fake Prices & Units
The documentation states that money is strictly represented in Indian Rupees as an integer. I found out that projects actually return decimal values representing Lakhs and Crores (e.g. `3.22` Crores or `80.0` Lakhs). Furthermore, some listings are completely fake "bait" listings posing as sales but using monthly rent values (~10k INR).
**Solution:** I added a price formatter in the `ListingCard.jsx` component that correctly parses the Project max prices into Crores and Lakhs so they display properly in the UI.

## What I Checked That Turned Out to Be Fine
- **Duplicates:** I hypothesized that the API was returning massive amounts of duplicates because `page` wasn't working. After fixing pagination, I checked if any properties were exactly duplicated. Grouping by physical traits (floor, apartment, area, facing), I found exactly 9 cross-posted properties out of 3800. The API's claim that `listing_id` is unique holds up perfectly.
- **Sorting:** I checked if the default sort order was arbitrary, but it actually seems to respect the basic query structure.
- **Data Completeness:** I expected missing fields in the JSON objects, but the API response bodies were remarkably clean and consistent with the schema provided.

## If I Had Another Two Days...
1. **Robust Client-Side Caching & Search:** Since the server-side filters are unreliable (e.g., `project_id` filter is completely ignored), I would implement a background synchronizer that pulls the entire dataset into an IndexedDB cache on login, allowing for instant, zero-latency filtering and text search across the entire city's database.
2. **Interactive Map:** I would use the `latitude` and `longitude` fields to plot properties on a Mapbox/Leaflet interface.
3. **Advanced Security:** I would move the refresh token logic to use secure HttpOnly cookies rather than localStorage.
