import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { HeadingLarge, HeadingMedium } from 'baseui/typography'
import { Button } from 'baseui/button'
import { Card } from 'baseui/card'
import { useAuth } from '../contexts/AuthContext'
import { useApiClient } from '../api/client'
import { getErrorMessage } from '../util'
import CitySearch from '../components/CitySearch'
import ZoneList from '../components/ZoneList'
import ErrorMessage from '../components/ErrorMessage'
import type { Zone } from '../types/api'

function DashboardPage() {
  const { logout } = useAuth()
  const navigate = useNavigate()
  const apiClient = useApiClient()
  const [zones, setZones] = useState<Zone[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchZones = async () => {
    setLoading(true)
    setError('')
    try {
      const zonesData = await apiClient.listZones()
      setZones(zonesData)
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchZones()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []) // TODO: Currently only fetch on mount, think if we should add a condition to refetch

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
        <HeadingLarge>Dashboard</HeadingLarge>
        <Button onClick={handleLogout}>
          Logout
        </Button>
      </div>

      {/* Main content area */}
      <div style={{ display: 'flex', gap: '24px', alignItems: 'flex-start' }}>
        {/* Left column: Zones list */}
        <div style={{ flex: 1, minWidth: 0 }}>
          <Card>
            {loading && <p>Loading zones...</p>}
            
            {error && <ErrorMessage message={error} />}

            {!loading && !error && <ZoneList zones={zones} />}
          </Card>
        </div>

        {/* Right column: Add Zone panel */}
        <div style={{ width: '380px', flexShrink: 0 }}>
          <Card>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <HeadingMedium style={{ margin: 0 }}>Add Zone</HeadingMedium>
            </div>
            <div>
              <CitySearch onZoneCreated={fetchZones} />
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default DashboardPage
