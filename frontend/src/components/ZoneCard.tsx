import { useState } from 'react'
import { Card } from 'baseui/card'
import { HeadingSmall } from 'baseui/typography'
import { Button } from 'baseui/button'
import { useApiClient } from '../api/client'
import { getErrorMessage } from '../util'
import ErrorMessage from './ErrorMessage'
import type { Zone } from '../types/api'

interface ZoneCardProps {
  zone: Zone
  onZoneUpdated: () => void
}

function ZoneCard({ zone, onZoneUpdated }: ZoneCardProps) {
  const apiClient = useApiClient()
  const [refreshing, setRefreshing] = useState(false)
  const [error, setError] = useState('')

  const handleRefresh = async () => {
    setRefreshing(true)
    setError('')
    
    try {
      await apiClient.refreshZone(zone.id)
      onZoneUpdated()
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setRefreshing(false)
    }
  }

  return (
    <Card>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
        <HeadingSmall style={{ margin: 0 }}>{zone.name}</HeadingSmall>
        <Button
          size="compact"
          onClick={handleRefresh}
          disabled={refreshing}
        >
          {refreshing ? 'Refreshing...' : 'Refresh Weather'}
        </Button>
      </div>
      
      {error && <ErrorMessage message={error} />}
      
      <div style={{ fontSize: '14px', color: '#666' }}>
        <div>Coordinates: {zone.latitude.toFixed(4)}, {zone.longitude.toFixed(4)}</div>
        {zone.temperature !== null && (
          <div style={{ marginTop: '5px' }}>
            Temperature: {zone.temperature}°C
          </div>
        )}
        <div style={{ marginTop: '5px', textTransform: 'capitalize' }}>
          Status: {zone.weather_status.replace('_', ' ')}
        </div>
      </div>
    </Card>
  )
}

export default ZoneCard
