import CalendarHeatmap from 'react-calendar-heatmap';
import './styles.css';
import learningData from '../data.json';
import { Tooltip } from 'react-tooltip';
import { useEffect, useState } from 'react';
import supabase from './utils/supabase';

function App() {
  const [selected, setSelected] = useState(null);
  const [selected2, setSelected2] = useState(null);
  const [maxStudied, setMaxStudied] = useState(null);
  const [maxStudied2, setMaxStudied2] = useState(null);
  const [test, setTest] = useState(null);

  useEffect(() => {
    const max = Math.max(...learningData.map((data) => data.studied.length));
    setMaxStudied(max);

    async function getData() {
      const { data, error } = await supabase
        .from('study_records')
        .select('study_date, study_material(title), studied_items(count)');
      const formattedData = data.map((item) => {
        item.date = item.study_date;
        delete item.study_date;
        item.points = item.studied_items.reduce(
          (a, b) => a + (b['count'] || 0),
          0
        );
        delete item.studied_items;
        return item;
      });
      setMaxStudied2(Math.max(formattedData.map((record) => record.points)));
      setTest(formattedData);
      return;
    }

    getData();
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
      {test && (
        <CalendarHeatmap
          startDate={new Date('2024-12-31')}
          endDate={new Date('2025-12-31')}
          showWeekdayLabels
          classForValue={(studyRecord) => {
            // if (Object.keys(givenDate['additional']).length) return 'color-bonus';
            if (!studyRecord) return 'color-0';
            const totalStudied = studyRecord['points'] / maxStudied2;
            if (totalStudied === 0) return 'color-0';
            if (totalStudied === 1) return 'color-5';
            return `color-${Math.ceil(totalStudied * 4)}`;
          }}
          tooltipDataAttrs={(value) => {
            const date = new Date(value['date']);
            const day = date.getDate();
            const month = date.toLocaleString('en-us', { month: 'long' }); // Full month name
            const points = value.points || 0;
            const content = `${points} point${
              points !== 1 ? 's' : ''
            } on ${month} ${day}${getOrdinalSuffix(day)}`;
            return {
              'data-tooltip-id': 'calendar-tooltip2',
              'data-tooltip-content': content,
            };
          }}
          values={test}
          onMouseOver={(e, selected_date) => setSelected2(selected_date)}
        />
      )}
      <Tooltip id="calendar-tooltip2" />
      {selected2 && (
        <div>
          {selected2.date} {selected2.user_id}
          {/* {lessonTypes.map(({ label, key }) => (
            <div key={key}>
              {label}: {generateStudyCompletion(selected2.studied, key)}
            </div>
          ))} */}
          {/* <div>
            Additional study:
            {Object.entries(selected2.additional)
              .map(([key, value]) => `${key} for ${value} hrs`)
              .join('') || '❌'}
          </div> */}
        </div>
      )}
    </div>
  );
}

export default App;
