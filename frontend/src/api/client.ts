import { STANDARD_GENERAL_ERROR_MSG, ResponseStatusToErrorMessage } from '../constants'
import { useAuth } from '../contexts/AuthContext'
import type { AuthResponse, UserLogin, UserRegister, CitySearchResponse, Zone } from '../types/api'

// In Docker: use relative path (nginx proxies /api to backend)
// In local dev: use relative path (vite proxy handles it)
// Only use absolute URL if explicitly set via env var
const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1'

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
        const errorMessage = ResponseStatusToErrorMessage[response.status] ?? STANDARD_GENERAL_ERROR_MSG 
        throw new Error(errorMessage)
      }

      if (response.status === 204) {
        return null as T
      }

      return await response.json() as T
    } catch (err) {
      // Handle network errors and other fetch failures
      if (err instanceof Error) {
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

  async createZone(name: string, latitude: number, longitude: number): Promise<Zone> {
    return this.request<Zone>('/zones', {
      method: 'POST',
      body: JSON.stringify({ name, latitude, longitude }),
    })
  }
}

export function useApiClient(): ApiClient {
  const { token } = useAuth()
  return new ApiClient(token)
}
