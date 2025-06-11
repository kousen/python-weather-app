# CLAUDE.md - AI Assistant Context

This file contains important context and development information for AI assistants working on this Weather App project.

## 🎯 Project Overview

**Purpose**: A Flask-based weather web application that provides comprehensive weather forecasts for cities worldwide.

**Target Users**: General public seeking current weather and 5-day forecasts with professional-quality UX.

**Key Value Proposition**: Clean, responsive interface with smart city disambiguation and comprehensive weather details.

## 🏗️ Architecture & Design Decisions

### Backend Architecture
- **Framework**: Flask 2.3.2 (chosen for simplicity and rapid development)
- **API Integration**: OpenWeather API (current weather + 5-day forecast + geocoding)
- **Data Flow**: Request → Input Sanitization → API Call → Data Processing → Template Rendering

### Key Design Decisions

1. **Single Unit System Approach**
   - **Decision**: Use OpenWeather API's native unit parameters (`metric`/`imperial`) instead of manual conversion
   - **Rationale**: Ensures all units (temperature, wind speed, pressure) are correctly converted by the API
   - **Implementation**: Query parameter `?units=metric|imperial` triggers page reload with correct units

2. **City Disambiguation Strategy**
   - **Problem**: API often returns duplicate or multiple cities with same name
   - **Solution**: Coordinate-based deduplication + user selection interface
   - **Implementation**: Round coordinates to 4 decimal places for duplicate detection

3. **Error Handling Philosophy**
   - **Approach**: Graceful degradation with user-friendly error pages
   - **Strategy**: Catch all `requests.exceptions.RequestException` and redirect to error page
   - **Timeouts**: 5-second timeout on all API calls to prevent hanging

4. **Security Approach**
   - **Input Sanitization**: Regex pattern `[^a-zA-Z\s-]` removes potentially harmful characters
   - **API Security**: HTTPS endpoints, environment variable storage for API keys
   - **XSS Prevention**: Flask's automatic template escaping

### Data Processing Pipeline

```
User Input → Sanitization → Geocoding API → City Selection (if needed) → Weather API → Template Rendering
```

## 📁 Code Organization

### File Structure
```
/
├── main.py                 # Main Flask application with all routes
├── templates/              # Jinja2 templates
│   ├── index.html         # Home page with search
│   ├── city.html          # Weather display page
│   ├── select_city.html   # City selection for duplicates
│   └── error.html         # Error page
├── static/
│   ├── css/main.css       # All styles (responsive design)
│   └── assets/            # Images and icons
├── test_main.py           # Integration tests
├── requirements.txt       # Python dependencies
└── README.md              # User documentation
```

### Route Structure
- `/` - Home page (GET/POST for search)
- `/<city>` - Weather display (handles ?units= parameter)
- `/weather` - POST endpoint for coordinate-based weather
- `/error` - Error page

### Function Organization
- `get_weather_data(lat, lon, units)` - API interaction helper
- Route handlers - Request processing and template rendering
- All business logic is in the routes (simple enough to not need separate services)

## 🧪 Testing Strategy

### Test Architecture
- **Framework**: pytest with unittest.mock
- **Approach**: Integration tests with mocked API responses
- **Coverage**: 11 tests covering all major workflows

### Test Categories
1. **TestHomePage**: Search functionality, input validation
2. **TestCityWeather**: Weather display, city selection, coordinate handling
3. **TestErrorHandling**: API failures, invalid cities, missing data

### Mocking Strategy
- Mock `get_weather_data()` helper function instead of raw `requests.get()`
- Provides realistic API response structures
- Tests both metric and imperial data flows

### Running Tests
```bash
pytest test_main.py -v                    # All tests
pytest test_main.py::TestCityWeather -v   # Weather functionality
```

## 🔧 Development Workflow

### Environment Setup
1. Virtual environment with `python3 -m venv venv`
2. Requirements from `requirements.txt` (minimal dependencies)
3. Environment variable: `OPENWEATHERMAP_API_KEY`

### API Integration Notes
- **OpenWeather API Limits**: 1000 calls/day on free tier
- **Rate Limiting**: Implemented request optimization to stay under limits
- **API Endpoints Used**:
  - Geocoding: `https://api.openweathermap.org/geo/1.0/direct`
  - Current Weather: `https://api.openweathermap.org/data/2.5/weather`
  - 5-Day Forecast: `https://api.openweathermap.org/data/2.5/forecast`

### Frontend Technologies
- **CSS Framework**: Custom CSS Grid + Flexbox (no external frameworks)
- **JavaScript**: Vanilla JS for minimal interactivity (loading states, form submission)
- **Icons**: Icons8 for weather conditions and UI elements
- **Responsive**: Mobile-first design with breakpoint at 768px

## 🚨 Known Issues & Considerations

### Current Limitations
1. **API Rate Limits**: Free tier limits could be hit with heavy usage
2. **iPad Layout**: Some spacing issues on tablet devices (noted in README)
3. **Icon Fallbacks**: Limited fallback handling for unusual weather conditions
4. **No Caching**: Each request hits the API (could benefit from Redis/memory cache)

### Security Considerations
- **Input Validation**: Currently regex-based, could be enhanced with more sophisticated validation
- **Rate Limiting**: No application-level rate limiting (relies on API limits)
- **CSRF**: Not implemented (could be added for production)

### Performance Considerations
- **API Calls**: Currently 2 calls per weather request (optimized from original 4)
- **Static Assets**: Could benefit from CDN in production
- **Caching**: No application-level caching implemented

## 🛠️ Development Patterns

### Error Handling Pattern
```python
try:
    # API call with timeout
    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException:
    return redirect(url_for("error"))
```

### Template Data Pattern
- Pass minimal data to templates
- Use template logic for formatting
- Include unit information for proper display

### Input Sanitization Pattern
```python
city = re.sub(r'[^a-zA-Z\s-]', '', request.form.get("search", "").strip())
if not city:
    return redirect(url_for("error"))
```

## 🔄 Recent Development History

### Major Refactoring Events
1. **Security Hardening** - Added input sanitization, HTTPS enforcement, error handling
2. **UX Enhancement** - Added loading states, enhanced weather details, temperature toggle
3. **City Disambiguation** - Implemented smart duplicate removal and user choice interface
4. **Unit System Optimization** - Refactored from manual conversion to API-native units
5. **Test Coverage** - Added comprehensive integration test suite

### API Usage Evolution
- **Original**: Manual Fahrenheit conversion (incomplete - missed wind speed)
- **Intermediate**: Dual API calls for metric + imperial (caused rate limiting)
- **Current**: Single API call with unit parameter + page reload for unit switching

## 💡 Future Development Guidelines

### Recommended Improvements
1. **Caching Layer**: Redis or memory cache for API responses (15-minute TTL)
2. **Search History**: localStorage-based recent searches
3. **Favorite Cities**: User preference storage
4. **Progressive Enhancement**: Service worker for offline functionality
5. **Accessibility**: ARIA labels, keyboard navigation improvements

### Architecture Considerations
- Keep the single-file Flask structure until complexity demands separation
- Consider moving to Flask-RESTful for API endpoints if adding mobile app
- Database integration only needed if adding user accounts/preferences

### Performance Optimization Opportunities
1. **Bundle CSS/JS**: Currently separate files
2. **Image Optimization**: Weather icons could be optimized/vectorized
3. **API Response Caching**: Significant potential for improvement
4. **Lazy Loading**: For forecast data or non-critical elements

## 🔍 Debugging & Troubleshooting

### Common Issues
1. **Hanging Requests**: Usually API timeout or rate limiting
   - Check console for network errors
   - Verify API key is valid
   - Check API usage limits

2. **City Not Found**: Geocoding API returned empty results
   - Verify city name spelling
   - Try with state/country qualifier

3. **JavaScript Errors**: Usually form submission issues
   - Check browser console for errors
   - Verify form action URLs are correct

### Development Server Issues
- **Port 5000 Conflicts**: Kill existing processes with `lsof -ti:5000 | xargs kill -9`
- **API Key Issues**: Verify environment variable is set correctly
- **Dependency Conflicts**: Use virtual environment, update requirements.txt

### Testing Issues
- **Mock Failures**: Ensure mock data structure matches current API responses
- **Timeout Errors**: Check if real API calls are happening instead of mocks

## 📊 Metrics & Monitoring

### Key Performance Indicators
- **API Response Times**: Should be < 2 seconds for weather data
- **Error Rates**: Track 4xx/5xx responses and redirect to error page
- **User Flow Completion**: Search → City Selection → Weather Display

### Monitoring Recommendations
- **API Usage**: Track daily API call counts vs. limits
- **Error Tracking**: Log API failures and error page visits
- **Performance**: Monitor page load times and API response times

---

*This document should be updated as the project evolves. Last updated: June 2025*