interface ErrorMessageProps {
  message: string
}

function ErrorMessage({ message }: ErrorMessageProps) {
  return (
    <div style={{ 
      color: '#d32f2f', 
      marginBottom: '10px', 
      backgroundColor: '#ffebee', 
      padding: '10px', 
      borderRadius: '4px',
      fontSize: '14px'
    }}>
      {message}
    </div>
  )
}

export default ErrorMessage
