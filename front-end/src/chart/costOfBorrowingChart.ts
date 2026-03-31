import { type TooltipItem } from 'chart.js'
import { format } from 'date-fns'

import type { Observation } from '../hooks/useObservations'
import './setupChartJs'

export const CHART_OPTIONS = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    title: { display: false },
    tooltip: {
      mode: 'index' as const,
      intersect: false,
      displayColors: false,
      callbacks: {
        title: (items: TooltipItem<'line'>[]) => {
          const x = items[0]?.parsed?.x
          if (!x) return ''
          return format(new Date(x), 'MMM yyyy')
        },
        label: (item: TooltipItem<'line'>) => {
          const y = item.parsed?.y
          if (typeof y !== 'number' || Number.isNaN(y)) return ''
          return `${y.toFixed(2)}%`
        },
      },
    },
  },
  scales: {
    x: {
      type: 'time' as const,
      time: {
        unit: 'year' as const,
        displayFormats: { year: 'yyyy' },
      },
      ticks: { maxTicksLimit: 12 },
      grid: { display: false },
    },
    y: {
      title: { display: true },
    },
  },
}

export function buildChartData(data: Observation[] | null) {
  return {
    datasets: [
      {
        label: 'Percent per annum',
        data: (data ?? []).map((d) => ({
          x: d.period_date,
          y: Number.parseFloat(d.value),
        })),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.15)',
        pointRadius: 0,
        borderWidth: 2,
        tension: 0.2,
        fill: true,
      },
    ],
  }
}

