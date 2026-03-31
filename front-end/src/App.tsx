import { useState } from 'react'

import { format } from 'date-fns'
import { Line } from 'react-chartjs-2'

import { buildChartData, CHART_OPTIONS } from './chart/costOfBorrowingChart'
import { useObservations } from './hooks/useObservations'

function App() {
  const [range, setRange] = useState<{ start: string; end: string }>({
    start: '2022-01-01',
    end: format(new Date(), 'yyyy-MM-dd'),
  })

  const { data, error, isLoading } = useObservations({ start: range.start, end: range.end })

  const chartData = buildChartData(data)

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-5xl px-4 py-10">
        <h1 className="text-2xl font-semibold tracking-tight">
          Cost of borrowing for households for house purchase, Euro area, Monthly
        </h1>

        <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="mb-4 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
            <div className="text-sm text-slate-600">
              <div className="font-medium text-slate-900">Percent per annum</div>
              <div className="mt-0.5">Source: ECB Data Portal</div>
            </div>

            <div className="flex gap-3">
              <label className="flex flex-col gap-1 text-xs text-slate-600">
                Start date
                <input
                  className="w-40 rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900"
                  type="date"
                  value={range.start}
                  onChange={(e) => setRange((r) => ({ ...r, start: e.target.value }))}
                />
              </label>
              <label className="flex flex-col gap-1 text-xs text-slate-600">
                End date
                <input
                  className="w-40 rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900"
                  type="date"
                  value={range.end}
                  onChange={(e) => setRange((r) => ({ ...r, end: e.target.value }))}
                />
              </label>
            </div>
          </div>

          {error ? (
            <div className="rounded-lg bg-red-50 p-4 text-sm text-red-800">
              Failed to load observations: {error}
            </div>
          ) : null}

          {isLoading ? (
            <div className="p-8 text-sm text-slate-500">Loading…</div>
          ) : null}

          {data ? (
            <div className="h-[420px]">
              <Line data={chartData} options={CHART_OPTIONS} />
            </div>
          ) : null}
        </div>
      </div>
    </div>
  )
}

export default App
