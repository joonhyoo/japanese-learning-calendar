import CalendarHeatmap from 'react-calendar-heatmap';
import './styles.css';
import learningData from './data.json';
import { Tooltip } from 'react-tooltip';

function App() {
  return (
    <div>
      <h1 style={{ textAlign: 'center' }}>Japanese Learning Calendar</h1>
      <CalendarHeatmap
        startDate={new Date('2025-01-01')}
        endDate={new Date('2025-12-31')}
        showWeekdayLabels
        showOutOfRangeDays
        classForValue={(value) => {
          if (!value) {
            return 'color-empty';
          }
          return `color-${value.count}`;
        }}
        tooltipDataAttrs={(value) => ({
          'data-tooltip-id': 'calendar-tooltip',
          'data-tooltip-content': `${value.date}: has count: ${value.count}`,
        })}
        values={learningData ? learningData : []}
      />
      <Tooltip id="calendar-tooltip" />
    </div>
  );
}

export default App;
