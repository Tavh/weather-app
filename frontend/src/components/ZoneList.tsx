import { HeadingMedium } from 'baseui/typography'
import ZoneCard from './ZoneCard'
import type { Zone } from '../types/api'

interface ZoneListProps {
  zones: Zone[]
}

function ZoneList({ zones }: ZoneListProps) {
  if (zones.length === 0) {
    return <p>No zones yet</p>
  }

  return (
    <div>
      <HeadingMedium style={{ margin: 0, marginBottom: '20px' }}>Zones</HeadingMedium>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {zones.map((zone) => (
          <ZoneCard key={zone.id} zone={zone} />
        ))}
      </div>
    </div>
  )
}

export default ZoneList
