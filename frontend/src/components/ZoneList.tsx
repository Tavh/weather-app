import type { Zone } from '../types/api'

interface ZoneListProps {
  zones: Zone[]
}

function ZoneList({ zones }: ZoneListProps) {
  if (zones.length === 0) {
    return <p>No zones yet</p>
  }

  return (
    <div style={{ marginTop: '20px' }}>
      <h2>Zones</h2>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {zones.map((zone) => (
          <li key={zone.id}>
            <div></div>
            <div>{zone.latitude}</div>
            <div>{zone.longitude}</div>
            <div>{zone.temperature}</div>
            <div>{zone.last_fetched_at}</div>
            <div>{zone.weather_status}</div>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default ZoneList
