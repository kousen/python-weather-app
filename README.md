# Weather App

A modern Flask-based weather web application that provides comprehensive weather forecasts for any city worldwide. Built with a focus on user experience, security, and responsive design.

> **Note**: This is an enhanced fork of the original project with additional features including temperature unit conversion, improved city selection, comprehensive testing, and performance optimizations.

## ✨ Features

### Core Functionality
- **Real-time weather data** for any city using OpenWeather API
- **5-day weather forecast** with detailed conditions
- **Multiple city disambiguation** - when searching for cities like "Springfield", choose from available options
- **Smart duplicate removal** - eliminates duplicate city entries from API responses

### Enhanced User Experience
- **Temperature unit toggle** - Switch between Celsius and Fahrenheit via page reload (ensures proper unit conversion for temperature AND wind speed: m/s ↔ mph)
- **Comprehensive weather details**:
  - Current temperature with "feels like" temperature
  - Min/max temperatures for the day
  - Humidity percentage
  - Wind speed (properly converted based on unit preference)
  - Sunrise and sunset times
- **Loading indicators** during API calls for better user feedback
- **Responsive design** optimized for both desktop and mobile devices

### Technical Improvements
- **Input sanitization** to prevent security vulnerabilities
- **Robust error handling** with graceful fallbacks
- **API timeout protection** (5-second timeouts)
- **Comprehensive test suite** with 11 integration tests
- **Rate limiting protection** through optimized API usage

## 🛠️ Tech Stack

- **Backend**: Flask 2.3.2 (Python web framework)
- **API**: OpenWeather API (weather data and geocoding)
- **Frontend**: HTML5, CSS3 (Grid & Flexbox), Vanilla JavaScript
- **Testing**: pytest with mocking for API calls
- **Environment**: python-dotenv for configuration
- **Deployment**: Gunicorn-ready for production deployment

## 📋 Setup Instructions

### Prerequisites
- Python 3.11+ 
- OpenWeather API key (free at [openweathermap.org](https://openweathermap.org/api))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd python-weather-app
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create .env file or set environment variable
   export OPENWEATHERMAP_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the app**
   - Open browser to `http://localhost:5000`

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest test_main.py -v

# Run specific test categories
pytest test_main.py::TestCityWeather -v        # Weather functionality
pytest test_main.py::TestErrorHandling -v      # Error handling
pytest test_main.py::TestHomePage -v           # Home page features
```

### Test Coverage
- ✅ Home page rendering and search functionality
- ✅ Input sanitization and validation
- ✅ Single city weather display
- ✅ Multiple city selection workflow
- ✅ Weather display by coordinates
- ✅ Comprehensive error handling scenarios
- ✅ API failure resilience

## 🏗️ Architecture

### Security Features
- **Input sanitization** - Removes potentially harmful characters
- **HTTPS API endpoints** - Secure communication with OpenWeather
- **Environment variable storage** - API keys never committed to code
- **Request timeouts** - Prevents hanging on slow API responses
- **Error handling** - Graceful degradation on failures

### Performance Optimizations
- **Efficient API usage** - Minimal requests to avoid rate limiting
- **Coordinate-based deduplication** - Removes duplicate city entries
- **Responsive caching** - Browser-level caching for static assets
- **Optimized CSS** - Mobile-first design with media queries

## 📱 User Interface

### Pages
1. **Home Page** - Clean search interface with loading indicators
2. **City Selection** - When multiple cities match, users can choose the specific location
3. **Weather Display** - Comprehensive weather information with unit toggle
4. **Error Page** - User-friendly error messaging

### Mobile Responsiveness
- Adaptive layouts using CSS Grid and Flexbox
- Touch-friendly buttons and controls
- Optimized font sizes and spacing
- Responsive images and icons

## 🔄 Recent Improvements

### Version 2.0 Updates
- **Smart city disambiguation** - Handles cities with identical names
- **Enhanced weather details** - Added humidity, feels-like temp, sunrise/sunset
- **Temperature unit toggle** - Complete implementation using API unit parameters with proper wind speed conversion
- **Loading states** - Visual feedback during API calls
- **Mobile optimization** - Improved responsive design
- **Security hardening** - Input validation and HTTPS enforcement
- **Test coverage** - Comprehensive integration test suite

## 🚀 Deployment

### Local Development
```bash
# Set up virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py  # Runs on localhost:5000 with debug mode
```

### Production Deployment
The app is configured for production deployment with Gunicorn:

```bash
gunicorn main:app
```

Environment variables required in production:
- `OPENWEATHERMAP_API_KEY` - Your OpenWeather API key

## 🛣️ Future Enhancements

- **Search history** - Remember recent city searches
- **Favorite cities** - Save frequently accessed locations  
- **Weather alerts** - Display severe weather warnings
- **Extended forecast** - 7-day forecast option
- **Location detection** - GPS-based weather for current location
- **Dark mode** - Theme toggle for better accessibility

## 🐛 Known Issues

- iPad layout could be further optimized (spacing improvements needed)  
- Weather icons could have better fallbacks for unusual weather conditions

## 📸 Screenshots

### Desktop
<img src="/screenshots/weather_app_desktop_home_page_screenshot.png" alt="Desktop Home Page">
<img src="/screenshots/weather_app_desktop_forecast_page_screenshot.png" alt="Desktop Weather Page">
<img src="/screenshots/weather_app_desktop_error_page_screenshot.png" alt="Desktop Error Page">

### Mobile  
<img src="/screenshots/weather_app_iphone_forecast_page_screenshot.png" style="width:400px;" alt="Mobile Weather Page"> <img src="/screenshots/weather_app_iphone_home_page_screenshot.png" style="width:400px;" alt="Mobile Home Page">

## 📚 Resources & References

### APIs & Documentation
- [OpenWeather API Documentation](https://openweathermap.org/api/one-call-3)
- [Flask Documentation](https://flask.palletsprojects.com/)

### Development Resources
- [CSS Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [Responsive Design Patterns](https://web.dev/responsive-web-design-basics/)

### Testing & Security
- [pytest Documentation](https://docs.pytest.org/)
- [Flask Testing](https://flask.palletsprojects.com/en/2.3.x/testing/)
- [OWASP Security Guidelines](https://owasp.org/www-project-top-ten/)

## 🎨 Design Credits

### Images
- [Home page background](https://unsplash.com/photos/2KXEb_8G5vo) - Unsplash
- [Error page background](https://unsplash.com/photos/U-Kty6HxcQc) - Unsplash

### Icons
All weather and UI icons provided by [Icons8](https://icons8.com):
- Weather condition icons (sun, rain, clouds, snow, etc.)
- UI elements (search, navigation, thermometer)
- Interactive buttons and indicators

## 👨‍💻 Development

Built from scratch using modern web development practices:
- **Semantic HTML5** for accessibility
- **CSS Grid & Flexbox** for responsive layouts  
- **Progressive enhancement** for JavaScript functionality
- **RESTful API integration** with proper error handling
- **Test-driven development** with comprehensive coverage

---

*Original concept by Rachana Hegde • Enhanced with modern features and best practices*