// Behavioural Config
export const REDIRECT_TO_LOGINMILLIS = 1500
export const CITY_SEARCH_RESULTS_LIMIT = 5
export const WEATHER_TEMPERATURE_THRESHOLDS_IN_CELCIUS = {
    cold: 0,
    warm: 20,
    hot: 30,
} as const
export const WEATHER_EMOJIS = {
    cold: '❄️',
    warm: '☁️',
    hot: '☀️',
} as const


// Standard Values
export const STANDARD_GENERAL_ERROR_MSG = 'Something went wrong'
export const MILLISECONDS_IN_MINUTE = 1000 * 60
