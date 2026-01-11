interface TemperatureDisplayProps {
  temperature: number | null
  unit: 'C' | 'F'
}

function TemperatureDisplay({ temperature, unit }: TemperatureDisplayProps) {
  return (
    <div >
      <span style={{ fontSize: '58px', color: temperature !== null ? 'black' : 'red' }}>
        {temperature !== null ? `${temperature} ${unit}` : 'N/A'}
      </span>
    </div>
  )
}

export default TemperatureDisplay
