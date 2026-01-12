import { STANDARD_GENERAL_ERROR_MSG } from '../constants'
import { useAuth } from '../contexts/AuthContext'
import type { AuthResponse, UserLogin, UserRegister, CitySearchResponse, Zone } from '../types/api'

// In Docker: use relative path (nginx proxies /api to backend)
// In local dev: use relative path (vite proxy handles it)
// Only use absolute URL if explicitly set via env var
const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1'

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
    '/zones/{id}/refresh': 'Failed to refresh zone',
  },
}

class ApiClient {
  private token: string | null

  constructor(token: string | null) {
    this.token = token
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE}${endpoint}`
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(this.token && { Authorization: `Bearer ${this.token}` }),
      ...options.headers,
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      })

      if (!response.ok) {
        let errorDetail: string | undefined
        try {
          const body = await response.json()
          errorDetail = body.detail
        } catch {
          // Error response is not valid JSON, use default error message
        }

        const errorMessageToEndpoint = ResponseStatusToErrorMessage[response.status]
        const errorMessage = errorMessageToEndpoint?.[endpoint]
          ?? errorMessageToEndpoint?.['default']
          ?? errorDetail
          ?? STANDARD_GENERAL_ERROR_MSG
        throw new Error(errorMessage)
      }

      if (response.status === 204) {
        return null as T
      }

      return await response.json() as T
    } catch (err) {
      // Handle network errors and other fetch failures
      if (err instanceof Error) {
        console.error(`API Call failed: ${endpoint}`, err.message)
        // If it's already our normalized error, re-throw it
        throw err
      }
      // Network failure or other unexpected errors
      throw new Error('Server unavailable, please try again')
    }
  }

  async login(username: string, password: string): Promise<AuthResponse> {
    const data: UserLogin = { username, password }
    return this.request<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async register(username: string, password: string): Promise<void> {
    const data: UserRegister = { username, password }
    return this.request<void>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async searchCities(query: string): Promise<CitySearchResponse> {
    return this.request<CitySearchResponse>(`/cities/search?q=${encodeURIComponent(query)}`)
  }

  async listZones(): Promise<Zone[]> {
    return this.request<Zone[]>('/zones')
  }

  async createZone(name: string, latitude: number, longitude: number, countryCode: string | null = null): Promise<Zone> {
    return this.request<Zone>('/zones', {
      method: 'POST',
      body: JSON.stringify({ name, country_code: countryCode, latitude, longitude }),
    })
  }

  async refreshZone(zoneId: number): Promise<Zone> {
    return this.request<Zone>(`/zones/${zoneId}/refresh`, {
      method: 'POST',
    })
  }

  async deleteZone(zoneId: number): Promise<void> {
    return this.request<void>(`/zones/${zoneId}`, {
      method: 'DELETE',
    })
  }

  async updateZone(zoneId: number, name: string, latitude: number, longitude: number, countryCode: string | null = null): Promise<Zone> {
    return this.request<Zone>(`/zones/${zoneId}`, {
      method: 'PUT',
      body: JSON.stringify({ name, country_code: countryCode, latitude, longitude }),
    })
  }
}

export function useApiClient(): ApiClient {
  const { token } = useAuth()
  return new ApiClient(token)
}
