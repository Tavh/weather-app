import { STANDARD_GENERAL_ERROR_MSG } from './constants'

export const getErrorMessage = (err: unknown) => {
    return err instanceof Error ? err.message : STANDARD_GENERAL_ERROR_MSG
}