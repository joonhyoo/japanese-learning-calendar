import CalendarHeatmap from 'react-calendar-heatmap';
import './styles.css';
import learningData from './data.json';
import { Tooltip } from 'react-tooltip';
import { useEffect, useState } from 'react';

function App() {
  const [selected, setSelected] = useState(null);
  const [maxStudied, setMaxStudied] = useState(null);

  useEffect(() => {
    const max = Math.max(...learningData.map((data) => data.studied.length));
    setMaxStudied(max);
  }, []);

  const sumValues = (obj) =>
    Object.values(obj)
      .map((num) => Number(num))
      .reduce((a, b) => a + b, 0);

  const lessonTypes = [
    { label: 'Bunpro lessons', key: 'b' },
    { label: 'WaniKani lessons', key: 'w' },
    { label: 'Review sessions', key: 'r' },
  ];

  const generateStudyCompletion = (studiedList, studyType) => {
    return (
      studiedList
        .filter((item) => item === studyType)
        .map(() => '✅')
        .join('') || '❌'
    );
  };

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
        classForValue={(givenDate) => {
          if (Object.keys(givenDate['additional']).length) return 'color-bonus';
          const totalStudied = givenDate['studied'].length / maxStudied;
          if (totalStudied === 0) return 'color-0';
          if (totalStudied < 0.25) return 'color-1';
          if (totalStudied < 0.5) return 'color-2';
          if (totalStudied < 0.75) return 'color-3';
          if (totalStudied < 1) return 'color-4';
          if (totalStudied === 1) return 'color-5';
          return `color-${totalStudied}`;
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
        <div>
          {selected.date} {selected.count}
          {lessonTypes.map(({ label, key }) => (
            <div key={key}>
              {label}: {generateStudyCompletion(selected.studied, key)}
            </div>
          ))}
          <div>
            Additional study:
            {Object.entries(selected.additional)
              .map(([key, value]) => `${key} for ${value} hrs`)
              .join('') || '❌'}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
