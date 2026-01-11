import React from 'react'
import ReactDOM from 'react-dom/client'
import { Provider as StyletronProvider } from 'styletron-react'
import { Client as Styletron } from 'styletron-engine-atomic'
import { BaseProvider, LightTheme } from 'baseui'
import { AuthProvider } from './contexts/AuthContext'
import App from './App'
import './index.css'

const engine = new Styletron()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <StyletronProvider value={engine}>
      <BaseProvider theme={LightTheme}>
        <AuthProvider>
          <App />
        </AuthProvider>
      </BaseProvider>
    </StyletronProvider>
  </React.StrictMode>,
)
