import { useNavigate } from 'react-router-dom'
import { HeadingLarge } from 'baseui/typography'
import { Button } from 'baseui/button'
import { useAuth } from '../contexts/AuthContext'

function DashboardPage() {
  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <HeadingLarge>Dashboard</HeadingLarge>
      <p>You are logged in.</p>
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
