import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { HeadingLarge } from 'baseui/typography'
import { Button } from 'baseui/button'
import { useAuth } from '../contexts/AuthContext'
import { useApiClient } from '../api/client'
import { getErrorMessage } from '../util'
import CitySearch from '../components/CitySearch'
import ZoneList from '../components/ZoneList'
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
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <HeadingLarge>Dashboard</HeadingLarge>
      <p>You are logged in.</p>

      <CitySearch onZoneCreated={fetchZones} />

      {loading && <p>Loading zones...</p>}
      
      {error && (
        <div style={{ color: 'red', marginBottom: '10px', backgroundColor: 'lightpink', padding: '10px', borderRadius: '4px' }}>
          {error}
        </div>
      )}

      {!loading && !error && <ZoneList zones={zones} />}

      <Button
        onClick={handleLogout}
        overrides={{
          BaseButton: {
            style: {
              marginTop: '20px',
            },
          },
        }}
      >
        Logout
      </Button>
    </div>
  )
}

export default DashboardPage
