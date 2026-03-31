import { useEffect, useState } from 'react'

export type Observation = {
  period_date: string
  value: string
}

type State = {
  data: Observation[] | null
  error: string | null
  isLoading: boolean
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export function useObservations(params: { start: string; end: string }): State {
  const { start, end } = params

  const [state, setState] = useState<State>({
    data: null,
    error: null,
    isLoading: true,
  })

  useEffect(() => {
    const controller = new AbortController()

    async function load() {
      try {
        setState((s) => ({ ...s, isLoading: true, error: null }))
        const res = await fetch(
          `${API_BASE_URL}/observations?start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}`,
          { signal: controller.signal },
        )
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`)
        }
        const json = (await res.json()) as Observation[]
        setState({ data: json, error: null, isLoading: false })
      } catch (e) {
        if ((e as Error).name === 'AbortError') return
        setState({
          data: null,
          error: (e as Error).message ?? 'Failed to load data',
          isLoading: false,
        })
      }
    }

    load()
    return () => controller.abort()
  }, [start, end])

  return state
}

