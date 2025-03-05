import CalendarHeatmap from 'react-calendar-heatmap';
import './styles.css';
import learningData from './data.json';
import { Tooltip } from 'react-tooltip';
import { useState } from 'react';

function App() {
  const [selected, setSelected] = useState(null);

  const sumValues = (obj) =>
    Object.values(obj)
      .map((num) => Number(num))
      .reduce((a, b) => a + b, 0);

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
          return `color-${
            sumValues(value['additional']) + value['studied'].length
          }`;
        }}
        tooltipDataAttrs={(value) => {
          const date = new Date(value.date);
          const day = date.getDate();
          const month = date.toLocaleString('en-us', { month: 'long' }); // Full month name
          const points =
            sumValues(value['additional']) + value['studied'].length;

          const content = `${points} point${
            points !== 1 ? 's' : ''
          } on ${month} ${day}${getOrdinalSuffix(day)}`;
          return {
            'data-tooltip-id': 'calendar-tooltip',
            'data-tooltip-content': content,
          };
        }}
        values={learningData ? learningData : []}
        onMouseOver={(e, selected_date) => setSelected(selected_date)}
      />
      <Tooltip id="calendar-tooltip" />
      {selected && (
        <>
          {selected.date} {selected.count}
          <div>
            Bunpro lessons:
            {selected.studied
              .filter((item) => item === 'b')
              .map(() => '✅')
              .join('') || '❌'}
          </div>
          <div>
            WaniKani lessons:
            {selected.studied
              .filter((item) => item === 'w')
              .map(() => '✅')
              .join('') || '❌'}
          </div>
          <div>
            Review sessions:
            {selected.studied
              .filter((item) => item === 'r')
              .map(() => '✅')
              .join('') || '❌'}
          </div>
          <div>
            Additional study:
            {Object.entries(selected.additional)
              .map(([key, value]) => `${key} for ${value} hrs`)
              .join('') || '❌'}
          </div>
          <div>WaniKani lessons: ❌</div>
        </>
      )}
    </div>
  );
}

export default App;
