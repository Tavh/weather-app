import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { HeadingLarge } from 'baseui/typography'
import { Button } from 'baseui/button'
import { useAuth } from '../contexts/AuthContext'
import { useApiClient } from '../api/client'
import { getErrorMessage } from '../util'
import type { Zone } from '../types/api'

function DashboardPage() {
  const { logout } = useAuth()
  const navigate = useNavigate()
  const apiClient = useApiClient()
  const [zones, setZones] = useState<Zone[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchZones = async () => {
      console.log('fetchZones')
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

    fetchZones()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []) // TODO: Currently only fetch on mount, think if we should add a condition to refetch

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const isOkAndEmptyZones = !loading && !error && zones.length === 0
  const isOkAndHasZones = !loading && !error && zones.length > 0
  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <HeadingLarge>Dashboard</HeadingLarge>
      <p>You are logged in.</p>

      {loading && <p>Loading zones...</p>}
      
      {error && (
        <div style={{ color: 'red', marginBottom: '10px', backgroundColor: 'lightpink', padding: '10px', borderRadius: '4px' }}>
          {error}
        </div>
      )}

      {isOkAndEmptyZones && (
        <p>No zones yet</p>
      )}

      {isOkAndHasZones && (
        <div style={{ marginTop: '20px' }}>
          <h2>Zones</h2>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {zones.map((zone) => (
              <li>
                Zone Placeholder
              </li>
            ))}
          </ul>
        </div>
      )}

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
