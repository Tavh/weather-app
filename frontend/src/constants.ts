export const STANDARD_GENERAL_ERROR_MSG = 'Something went wrong'

export const ResponseStatusToErrorMessage: Record<number, string> = {
    400: 'Invalid input',
    401: 'Invalid username or password',
    500: 'Server unavailable, please try again',
}