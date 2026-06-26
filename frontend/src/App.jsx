import { useState } from 'react'
import './App.css'

function App() {
  const [task, setTask] = useState('')
  const [tests, setTests] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  async function handleRun() {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch("https://patchwork-9lfw.onrender.com/solve", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task, tests }),
      })

      if (!response.ok) {
        throw new Error(`Request failed (${response.status})`)
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  const passed = result?.result === 'passed'

  return (
    <div className="app">
      <header className="header">
        <div className="agent-orbit" aria-hidden="true">
          <div className="orbit-node">
            <span className="orbit-dot" />
            <span className="orbit-label">write</span>
          </div>
          <div className="orbit-line" />
          <div className="orbit-node">
            <span className="orbit-dot" />
            <span className="orbit-label">test</span>
          </div>
          <div className="orbit-line" />
          <div className="orbit-node">
            <span className="orbit-dot" />
            <span className="orbit-label">fix</span>
          </div>
        </div>

        <h1 className="title">
          <span className="title-prefix" aria-hidden="true">
            &gt;
          </span>
          Patch<span className="title-accent">work</span>
          <span className="title-cursor" aria-hidden="true" />
        </h1>

        <p className="tagline">
          Self-correcting code generation — it writes, tests, and fixes its own
          code.
        </p>
      </header>

      <form
        className="form"
        onSubmit={(e) => {
          e.preventDefault()
          if (!loading) handleRun()
        }}
      >
        <label className="field">
          <span className="label">Task</span>
          <textarea
            className="textarea"
            value={task}
            onChange={(e) => setTask(e.target.value)}
            placeholder="Describe what the code should do…"
            rows={4}
          />
        </label>

        <label className="field">
          <span className="label">Test Cases</span>
          <span className="helper">
            Python assert statements, one per line (e.g. assert add(2,3) == 5)
          </span>
          <textarea
            className="textarea textarea--mono"
            value={tests}
            onChange={(e) => setTests(e.target.value)}
            placeholder="assert add(2, 3) == 5"
            rows={4}
          />
        </label>

        <button
          type="submit"
          className={`run-btn${loading ? ' run-btn--loading' : ''}`}
          disabled={loading}
        >
          {loading ? (
            <>
              Running
              <span className="loading-dots" aria-hidden="true">
                <span>.</span>
                <span>.</span>
                <span>.</span>
              </span>
            </>
          ) : (
            'Run'
          )}
        </button>

        {loading && <div className="loading-bar" aria-hidden="true" />}
      </form>

      {error && (
        <div className="error-banner" role="alert">
          {error}
        </div>
      )}

      {result && (
        <section className="results">
          <div className="results-header">
            <span
              className={`badge ${passed ? 'badge--passed' : 'badge--failed'}`}
            >
              {passed
                ? 'Passed'
                : `Failed after ${result.attempts} attempt${result.attempts === 1 ? '' : 's'}`}
            </span>
            <span className="attempts">
              {result.attempts} fix attempt{result.attempts === 1 ? '' : 's'}
            </span>
          </div>

          <pre className="code-block">
            <code>{result.code}</code>
          </pre>
        </section>
      )}
    </div>
  )
}

export default App
