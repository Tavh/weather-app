export const CITY_SEARCH_RESULTS_LIMIT = 5
export const STANDARD_GENERAL_ERROR_MSG = 'Something went wrong'

export const ResponseStatusToErrorMessage: Record<number, Record<string, string>> = {
    400: {
        'default': 'Invalid input',
    },
    401: {
        'default': 'session expired, please log in again.',
        '/auth/login': 'Invalid username or password',
    },
    500: {
        'default': 'Server unavailable, please try again',
    },
}