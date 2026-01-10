from werkzeug.exceptions import ServiceUnavailable

class WeatherProviderUnavailable(ServiceUnavailable):
    description = "Weather provider unavailable"

