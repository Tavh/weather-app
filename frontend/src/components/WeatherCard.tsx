import { useState } from 'react';
import TemperatureDisplay from './TemperatureDisplay';

// Exercise 2: Create an interactive Weather Card
//
// Requirements:
// 1. Define a 'WeatherCondition' type which can be 'Sunny', 'Rainy', 'Cloudy', or 'Snowy'.
// 2. Define props interface 'WeatherCardProps' containing:
//    - city: string
//    - temperature: number (in Celsius)
//    - condition: WeatherCondition
// 3. Implement the component:
//    - Display the city name bolded.
//    - Display the temperature.
//    - Add a button "Switch to °F" / "Switch to °C" that toggles the unit.
//      - Formula: (C * 9/5) + 32 = F
//    - Change the background color or add an emoji based on the 'condition'.
//      - Sunny: ☀️ (yellow bg?)
//      - Rainy: 🌧️ (blue bg?)
//      - Cloudy: ☁️ (gray bg?)
//      - Snowy: ❄️ (white/light blue bg?)


export type WeatherCondition = 'Sunny' | 'Rainy' | 'Cloudy' | 'Snowy';

export interface WeatherCardProps { // Not good to export, but this is an exercise
    city: string;
    temperature: number;
    condition: WeatherCondition;
}

const WeatherCard = ({ city, temperature, condition }: WeatherCardProps) => {
    const [unit, setUnit] = useState<'C' | 'F'>('C');

    const toggleUnit = () => {
        setUnit(unit === 'C' ? 'F' : 'C');
    };

    const displayTemperature = unit === 'C' ? temperature : (temperature * 9 / 5) + 32;


    const conditionToColor = {
        "Sunny": "yellow",
        "Rainy": "blue",
        "Cloudy": "gray",
        "Snowy": "white"
    }

    return (
        <div style={{
            border: '1px solid #ccc',
            padding: '20px',
            borderRadius: '8px',
            width: '200px',
            margin: '10px',
            backgroundColor: condition !== null ? conditionToColor[condition] : "white"
        }}>
            <h2>{city}</h2>
            <TemperatureDisplay temperature={displayTemperature} unit={unit} />
            <button onClick={toggleUnit}>
                Switch to {unit === 'C' ? '°F' : '°C'}
            </button>
        </div>
    );
};

export default WeatherCard;
