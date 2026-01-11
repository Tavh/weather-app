import { useAuth } from '../contexts/AuthContext'
import type { AuthResponse, UserLogin, UserRegister, CitySearchResponse, Zone } from '../types/api'

const API_BASE = '/api/v1'

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

    const response = await fetch(url, {
      ...options,
      headers,
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    if (response.status === 204) {
      return null as T
    }

    return await response.json() as T
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
}

export function useApiClient(): ApiClient {
  const { token } = useAuth()
  return new ApiClient(token)
}
