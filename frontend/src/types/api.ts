// API Response Types - mirroring backend DTOs

export interface AuthResponse {
  access_token: string
  token_type: string
  expires_in: number
}

export interface UserRegister {
  username: string
  password: string
}

export interface UserLogin {
  username: string
  password: string
}

export interface CitySearchResult {
  name: string
  country_code: string | null
  latitude: number
  longitude: number
}

export interface CitySearchResponse {
  results: CitySearchResult[]
}

export type WeatherStatus = 'never_fetched' | 'cached' | 'fresh'

export interface Zone {
  id: number
  name: string
  latitude: number
  longitude: number
  temperature: number | null
  last_fetched_at: string | null
  weather_status: WeatherStatus
}
