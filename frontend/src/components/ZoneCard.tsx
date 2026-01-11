import { Card } from 'baseui/card'
import { HeadingSmall } from 'baseui/typography'
import type { Zone } from '../types/api'

interface ZoneCardProps {
  zone: Zone
}

function ZoneCard({ zone }: ZoneCardProps) {
  return (
    <Card>
      <HeadingSmall>{zone.name}</HeadingSmall>
      <div style={{ marginTop: '10px', fontSize: '14px', color: '#666' }}>
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
