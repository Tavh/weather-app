from werkzeug.exceptions import ServiceUnavailable


class WeatherProviderUnavailable(ServiceUnavailable):
    description = "Weather provider unavailable"

class CitySearchUnavailable(ServiceUnavailable):
    description = "City search temporarily unavailable"

