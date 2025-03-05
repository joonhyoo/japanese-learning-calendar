import CalendarHeatmap from 'react-calendar-heatmap';
import './styles.css';
import learningData from './data.json';
import { Tooltip } from 'react-tooltip';

function App() {
  const getOrdinalSuffix = (day) => {
    if (day > 3 && day < 21) return 'th'; // Covers 11-19
    switch (day % 10) {
      case 1:
        return 'st';
      case 2:
        return 'nd';
      case 3:
        return 'rd';
      default:
        return 'th';
    }
  };
  return (
    <div>
      <h1 style={{ textAlign: 'center' }}>Japanese Learning Calendar 2025</h1>
      <CalendarHeatmap
        startDate={new Date('2024-12-31')}
        endDate={new Date('2025-12-31')}
        showWeekdayLabels
        classForValue={(value) => {
          if (!value) {
            return 'color-empty';
          }
          return `color-${value.count}`;
        }}
        tooltipDataAttrs={(value) => {
          const date = new Date(value.date);
          const day = date.getDate();
          const month = date.toLocaleString('en-us', { month: 'long' }); // Full month name
          const content = `${value.count} point${
            value.count !== 1 ? 's' : ''
          } on ${month} ${day}${getOrdinalSuffix(day)}`;
          return {
            'data-tooltip-id': 'calendar-tooltip',
            'data-tooltip-content': content,
          };
        }}
        values={learningData ? learningData : []}
      />
      <Tooltip id="calendar-tooltip" />
    </div>
  );
}

export default App;
