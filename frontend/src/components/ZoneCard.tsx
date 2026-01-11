import { useState } from 'react'
import { Card } from 'baseui/card'
import { HeadingSmall, LabelMedium, LabelSmall } from 'baseui/typography'
import { Button } from 'baseui/button'
import { Input } from 'baseui/input'
import { useApiClient } from '../api/client'
import { getErrorMessage } from '../util'
import ErrorMessage from './ErrorMessage'
import type { Zone } from '../types/api'
import { WEATHER_TEMPERATURE_THRESHOLDS_IN_CELCIUS, WEATHER_EMOJIS, MILLISECONDS_IN_MINUTE } from '../constants'

interface ZoneCardProps {
  zone: Zone
  onZoneUpdated: (updatedZone: Zone) => void
  onDelete: (zoneId: number) => void
}

function ZoneCard({ zone, onZoneUpdated, onDelete }: ZoneCardProps) {
  const apiClient = useApiClient()
  const [refreshing, setRefreshing] = useState(false)
  const [deleting, setDeleting] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [editedName, setEditedName] = useState(zone.name)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [showUpdateMessage, setShowUpdateMessage] = useState(false)

  const handleRefresh = async () => {
    setRefreshing(true)
    setError('')
    setShowUpdateMessage(false) // Clear update message after refresh
    
    try {
      const updatedZone = await apiClient.refreshZone(zone.id)
      onZoneUpdated(updatedZone)
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setRefreshing(false)
    }
  }

  const handleDelete = async () => {
    const confirmed = window.confirm(`Are you sure you want to delete "${zone.name}"?`)
    if (!confirmed) return

    setDeleting(true)
    setError('')
    
    try {
      await apiClient.deleteZone(zone.id)
      onDelete(zone.id)
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setDeleting(false)
    }
  }

  const handleEdit = () => {
    setIsEditing(true)
    setEditedName(zone.name)
    setError('')
  }

  const handleCancel = () => {
    setIsEditing(false)
    setEditedName(zone.name)
    setError('')
  }

  const handleSave = async () => {
    if (!editedName.trim()) {
      setError('Zone name cannot be empty')
      return
    }

    setSaving(true)
    setError('')
    
    try {
      const updatedZone = await apiClient.updateZone(
        zone.id,
        editedName.trim(),
        zone.latitude,
        zone.longitude,
        zone.country_code
      )
      setIsEditing(false)
      setShowUpdateMessage(true) // Show message after successful update
      onZoneUpdated(updatedZone)
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setSaving(false)
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
      {/* Header: City name + country code and action buttons */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
        <div style={{ flex: 1, marginRight: '16px' }}>
          {isEditing ? (
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
              {/* @ts-expect-error Base Web type compatibility issue */}
              <Input
                value={editedName}
                onChange={(e) => setEditedName(e.currentTarget.value)}
                placeholder="Zone name"
                disabled={saving}
                overrides={{
                  Input: {
                    style: {
                      flex: 1,
                    },
                  },
                }}
              />
              <Button
                size="compact"
                onClick={handleSave}
                disabled={saving || !editedName.trim()}
              >
                {saving ? 'Saving...' : 'Save'}
              </Button>
              <Button
                size="compact"
                onClick={handleCancel}
                disabled={saving}
              >
                Cancel
              </Button>
            </div>
          ) : (
            <HeadingSmall style={{ margin: 0, marginBottom: '4px' }}>
              {zone.name}
              {zone.country_code && (
                <span style={{ marginLeft: '8px', fontSize: '14px', fontWeight: 400, color: '#666' }}>
                  {zone.country_code}
                </span>
              )}
            </HeadingSmall>
          )}
        </div>
        {!isEditing && (
          <div style={{ display: 'flex', gap: '8px' }}>
            <Button
              size="compact"
              onClick={handleEdit}
              disabled={refreshing || deleting}
            >
              Edit
            </Button>
            <Button
              size="compact"
              onClick={handleRefresh}
              disabled={refreshing || deleting}
            >
              {refreshing ? 'Refreshing...' : 'Refresh Weather'}
            </Button>
            <Button
              size="compact"
              onClick={handleDelete}
              disabled={refreshing || deleting}
            >
              {deleting ? 'Deleting...' : 'Delete'}
            </Button>
          </div>
        )}
      </div>

      {error && <ErrorMessage message={error} />}

      {showUpdateMessage && (
        <div style={{ 
          marginBottom: '8px', 
          padding: '6px 10px', 
          backgroundColor: '#f5f5f5', 
          borderRadius: '4px',
          fontSize: '12px',
          color: '#666'
        }}>
          Zone updated. Weather data was reset — please refresh.
        </div>
      )}

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
