import { useState } from 'react'
import { Input } from 'baseui/input'
import { Button } from 'baseui/button'
import { useApiClient } from '../api/client'
import { getErrorMessage } from '../util'
import ErrorMessage from './ErrorMessage'
import type { CitySearchResult } from '../types/api'
import { CITY_SEARCH_RESULTS_LIMIT } from '../constants'

interface CitySearchProps {
  onZoneCreated: () => void
}

function CitySearch({ onZoneCreated }: CitySearchProps) {
  const apiClient = useApiClient()
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<CitySearchResult[]>([])
  const [searchLoading, setSearchLoading] = useState(false)
  const [searchError, setSearchError] = useState('')
  const [lastSearchedQuery, setLastSearchedQuery] = useState<string | null>(null) // used to display the last searched query in the UI. Might've been a bit of an overkill but it looks nice.

  const handleSearch = async () => {
    if (!searchQuery.trim()) return
    
    const queryToSearch = searchQuery.trim()
    setSearchLoading(true)
    setSearchError('')
    setSearchResults([])
    setLastSearchedQuery(queryToSearch)
    
    try {
      const response = await apiClient.searchCities(queryToSearch)
      const limitedResults = response.results.slice(0, CITY_SEARCH_RESULTS_LIMIT)
      setSearchResults(limitedResults)
    } catch (err) {
      setSearchError(getErrorMessage(err))
    } finally {
      setSearchLoading(false)
    }
  }

  const handleAddZone = async (city: CitySearchResult) => {
    setSearchLoading(true)
    setSearchError('')
    
    try {
      await apiClient.createZone(city.name, city.latitude, city.longitude, city.country_code)
      // Clear search
      setSearchQuery('')
      setSearchResults([])
      setLastSearchedQuery(null)
      // Notify parent to refetch zones
      onZoneCreated()
    } catch (err) {
      setSearchError(getErrorMessage(err))
    } finally {
      setSearchLoading(false)
    }
  }

  const lastSearchedQuerySpan = <span style={{ fontWeight: 'bold' }}>'{lastSearchedQuery}'</span>
  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <div style={{ display: 'flex', gap: '10px' }}>
          {/* @ts-expect-error Base Web type compatibility issue */}
          <Input
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.currentTarget.value)}
            placeholder="Enter city name"
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                handleSearch()
              }
            }}
            disabled={searchLoading}
            overrides={{
              Input: {
                style: {
                  flex: 1,
                },
              },
            }}
          />
          <Button
            onClick={handleSearch}
            disabled={searchLoading || !searchQuery.trim()}
          >
            {searchLoading ? 'Searching...' : 'Search'}
          </Button>
        </div>
        {searchQuery.trim().length === 1 && (
          <p style={{ fontSize: '12px', color: '#999', marginTop: '5px', marginBottom: 0 }}>
            Please enter at least 2 characters to search.
          </p>
        )}
      </div>

      {searchError && <ErrorMessage message={searchError} />}

     {searchLoading && <p>Loading...</p>}

     {!searchLoading && lastSearchedQuery !== null && searchResults.length === 0 && (
       <p style={{ marginTop: '15px', color: '#666' }}>
        No results found for: {lastSearchedQuerySpan}
       </p>
     )}

    {!searchLoading && searchResults.length > 0 && (
      <div style={{ marginTop: '15px' }}>
        <p>Found {searchResults.length} results for: {lastSearchedQuerySpan}</p>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {searchResults.map((city, index) => (
            <li
              key={index}
              style={{
                border: '1px solid #ccc',
                borderRadius: '4px',
                padding: '10px',
                marginBottom: '8px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
              }}
            >
                <div>
                  <div style={{ fontWeight: 'bold' }}>{city.name}</div>
                  {city.country_code && (
                    <div style={{ fontSize: '14px', color: '#666' }}>{city.country_code}</div>
                  )}
                </div>
                <Button
                  onClick={() => handleAddZone(city)}
                  disabled={searchLoading}
                  size="compact"
                >
                  Add
                </Button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default CitySearch
