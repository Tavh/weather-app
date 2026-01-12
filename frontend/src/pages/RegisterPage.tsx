import { useState, FormEvent } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Input } from 'baseui/input'
import { Button } from 'baseui/button'
import { FormControl } from 'baseui/form-control'
import { HeadingLarge } from 'baseui/typography'
import { useApiClient } from '../api/client'
import { getErrorMessage } from '../util'
import ErrorMessage from '../components/ErrorMessage'
import { REDIRECT_TO_LOGINMILLIS } from '../constants'

function RegisterPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const apiClient = useApiClient()

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError('')
    setSuccess(false)
    setLoading(true)

    try {
      await apiClient.register(username, password)
      setSuccess(true)
      // Redirect to login after showing success message
      setTimeout(() => {
        navigate('/login')
      }, REDIRECT_TO_LOGINMILLIS)
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
      <HeadingLarge>Register</HeadingLarge>
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
        {error && <ErrorMessage message={error} />}
        {success && (
          <div style={{ 
            marginBottom: '16px', 
            padding: '10px', 
            backgroundColor: '#e8f5e9', 
            borderRadius: '4px',
            color: '#2e7d32',
            fontSize: '14px'
          }}>
            Account created successfully! Redirecting to login...
          </div>
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
          {loading ? 'Registering...' : 'Register'}
        </Button>
      </form>

      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <Link 
          to="/login" 
          style={{ 
            color: '#276EF1', 
            textDecoration: 'none',
            fontSize: '14px'
          }}
        >
          Already have an account? Login here
        </Link>
      </div>
    </div>
  )
}

export default RegisterPage
