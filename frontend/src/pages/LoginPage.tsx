import { useState, FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { Input } from 'baseui/input'
import { Button } from 'baseui/button'
import { Link } from 'react-router-dom'
import { FormControl } from 'baseui/form-control'
import { HeadingLarge } from 'baseui/typography'
import { useAuth } from '../contexts/AuthContext'
import { useApiClient } from '../api/client'

function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()
  const apiClient = useApiClient()

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await apiClient.login(username, password)
      login(response.access_token)
      navigate('/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
      <HeadingLarge>Login</HeadingLarge>
      <form onSubmit={handleSubmit}>
        {/* @ts-expect-error Base Web type compatibility issue */}
        <FormControl label="Username">
          {/* @ts-expect-error Base Web type compatibility issue */}
          <Input
            value={username}
            onChange={(e) => setUsername(e.currentTarget.value)}
            placeholder="Enter username"
            required
            disabled={loading}
          />
        </FormControl>
        {/* @ts-expect-error Base Web type compatibility issue */}
        <FormControl label="Password">
          {/* @ts-expect-error Base Web type compatibility issue */}
          <Input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.currentTarget.value)}
            placeholder="Enter password"
            required
            disabled={loading}
          />
        </FormControl>
        {error && (
          <div style={{ color: 'red', marginBottom: '10px', backgroundColor: 'lightpink', padding: '2px', borderRadius: '4px' }}>{error}</div>
        )}
        <Button
          type="submit"
          disabled={loading}
          overrides={{
            BaseButton: {
              style: {
                width: '100%',
                marginTop: '10px',
              },
            },
          }}
        >
          {loading ? 'Logging in...' : 'Login'}
        </Button>
      </form>

      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <Link 
          to="/register" 
          style={{ 
            color: '#276EF1', 
            textDecoration: 'none',
            fontSize: '14px'
          }}
        >
          Don't have an account? Register here
        </Link>
      </div>
    </div>
  )
}

export default LoginPage
