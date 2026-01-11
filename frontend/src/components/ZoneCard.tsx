import { useState } from 'react'
import { Card } from 'baseui/card'
import { HeadingSmall, LabelMedium, LabelSmall } from 'baseui/typography'
import { Button } from 'baseui/button'
import { useApiClient } from '../api/client'
import { getErrorMessage } from '../util'
import ErrorMessage from './ErrorMessage'
import type { Zone } from '../types/api'
import { WEATHER_TEMPERATURE_THRESHOLDS_IN_CELCIUS, WEATHER_EMOJIS, MILLISECONDS_IN_MINUTE } from '../constants'

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

  // Format temperature display
  const formatTemperature = (temp: number | null): string => {
    if (temp === null) {
      return 'Not fetched yet'
    }
    return `${temp.toFixed(1)}°C`
  }

  // Get weather emoji based on temperature
  const getWeatherEmoji = (temp: number | null): string => {
    if (temp === null) return ''
    
    const { cold, warm, hot } = WEATHER_TEMPERATURE_THRESHOLDS_IN_CELCIUS
    
    if (temp < cold) return WEATHER_EMOJIS.cold
    if (temp <= warm) return WEATHER_EMOJIS.warm
    if (temp <= hot) return WEATHER_EMOJIS.warm
    return WEATHER_EMOJIS.hot
  }

  // Format "Last Updated" text
  const formatLastUpdated = (lastFetchedAt: string | null): string => {
    if (!lastFetchedAt) {
      return 'Never updated'
    }

    const fetchedDate = new Date(lastFetchedAt)
    const now = new Date()
    const diffMs = now.getTime() - fetchedDate.getTime()
    const diffMinutes = Math.floor(diffMs / MILLISECONDS_IN_MINUTE) // convert to minutes

    if (diffMinutes < 1) {
      return 'Updated just now'
    }

    return `Updated ${diffMinutes} minute${diffMinutes !== 1 ? 's' : ''} ago`
  }

  const weatherEmoji = getWeatherEmoji(zone.temperature)
  const temperatureText = formatTemperature(zone.temperature)
  const lastUpdatedText = formatLastUpdated(zone.last_fetched_at)

  return (
    <Card>
      {/* Header: City name + country code and Refresh button */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
        <div>
          <HeadingSmall style={{ margin: 0, marginBottom: '4px' }}>
            {zone.name}
            {zone.country_code && (
              <span style={{ marginLeft: '8px', fontSize: '14px', fontWeight: 400, color: '#666' }}>
                {zone.country_code}
              </span>
            )}
          </HeadingSmall>
        </div>
        <Button
          size="compact"
          onClick={handleRefresh}
          disabled={refreshing}
        >
          {refreshing ? 'Refreshing...' : 'Refresh Weather'}
        </Button>
      </div>

      {error && <ErrorMessage message={error} />}

      {/* Temperature - Second most prominent */}
      <div style={{ marginBottom: '8px' }}>
        <LabelMedium style={{ fontSize: '18px', fontWeight: 500 }}>
          {weatherEmoji} {temperatureText}
        </LabelMedium>
      </div>

      {/* Last Updated - Muted/secondary */}
      <div style={{ marginBottom: '12px' }}>
        <LabelSmall style={{ color: '#666', fontSize: '12px' }}>
          {lastUpdatedText}
        </LabelSmall>
      </div>
    </Card>
  )
}

export default ZoneCard
