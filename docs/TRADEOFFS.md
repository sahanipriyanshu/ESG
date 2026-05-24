# Trade-offs & Simplifications

As a 4-day prototype, several conscious engineering trade-offs were made to prioritize core architecture, UX, and auditability over absolute completeness.

## 1. Synchronous vs. Asynchronous File Parsing
- **Implementation**: CSV files are parsed synchronously inside the Django API view using `pandas`.
- **Trade-off**: This blocks the HTTP request thread. In production, uploading a 50MB CSV would cause a timeout.
- **Production Path**: Implement Celery + Redis. The API would immediately return a `task_id` and process the `DataSource` in the background.

## 2. Mock Emission Factors
- **Implementation**: Emission calculations rely on hardcoded constants (e.g., 0.4 kg CO2e / kWh) within the `UtilityService`.
- **Trade-off**: Real ESG platforms integrate with APIs like Climatiq or EPA databases for accurate, localized factor matching. 
- **Production Path**: Introduce an `EmissionFactor` database model or third-party integration that resolves factors based on region, date, and grid mix.

## 3. Lack of Authentication
- **Implementation**: The system operates with a hardcoded `organization_id` and passes mock actor names (e.g., "Analyst Alice") from the frontend.
- **Trade-off**: No real security or tenant isolation enforcement at the HTTP layer.
- **Production Path**: Implement JWT authentication (e.g., Auth0 or Django SimpleJWT), attach a `User` model, and infer the `Organization` from the authenticated user's token.

## 4. SQLite for Development
- **Implementation**: Defaulting to `sqlite3` locally, while supporting PostgreSQL via `.env`.
- **Trade-off**: SQLite handles JSONFields well enough for prototyping, but lacks concurrent write performance and advanced JSONB indexing.
- **Production Path**: Enforce PostgreSQL in all environments (local docker-compose and production).

## 5. Mock Travel Distances
- **Implementation**: Used a hardcoded dictionary for airport distances via Haversine simulation.
- **Trade-off**: Limited to a few test routes.
- **Production Path**: Integrate with a Geocoding/Aviation API to dynamically calculate flight path distances.
