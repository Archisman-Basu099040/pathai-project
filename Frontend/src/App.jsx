import React, { useEffect, useState } from 'react';
import './App.css';

const featureCards = [
  {
    title: 'AI study path builder',
    text: 'The system turns a single confusing topic into a clear, step-by-step learning roadmap.',
    icon: '🧭'
  },
  {
    title: 'Mentor matching',
    text: 'Every learner gets guidance shaped around their grade, subject, and language preference.',
    icon: '👨‍🏫'
  },
  {
    title: 'Fast concept diagnosis',
    text: 'Instead of generic advice, PathAI reads your question and identifies the real learning gap.',
    icon: '⚡'
  }
];

const stats = [
  { label: 'Syllabus topics', value: '9' },
  { label: 'Mock mentors', value: '15' },
  { label: 'AI Engine', value: 'Llama 3.3' }
];

const subjectIcon = {
  math: '📘',
  science: '🧪',
  english: '📝'
};

export default function App() {
  const [formData, setFormData] = useState({
    name: '',
    grade: '',
    language: '',
    subject: '',
    topic: '',
    query: ''
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const [progressHistory, setProgressHistory] = useState([]);

  const isDark = true;
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  // Pick a random default mentor for the preview card on load
  const [previewMentor] = useState(() => {
    const sampleMentors = ["Dr. Ananya Sharma", "Mr. Rohan Chatterjee", "Ms. Priya Rao", "Dr. Tariq Iqbal", "Ms. Sunita Devi"];
    return sampleMentors[Math.floor(Math.random() * sampleMentors.length)];
  });

  useEffect(() => {
    const elements = document.querySelectorAll('.reveal');

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
          }
        });
      },
      { threshold: 0.15 }
    );

    elements.forEach((element) => observer.observe(element));

    return () => observer.disconnect();
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/api/intake`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error(`Server returned status ${response.status}`);
      }

      const data = await response.json();
      setResult(data);

      setProgressHistory((prev) => [
        ...prev,
        {
          topic: data.topic || formData.topic,
          subject: data.subject || formData.subject,
          level: data.level,
          mentor: data.assigned_mentor,
          confidence: data.confidence,
          timestamp: Date.now()
        }
      ]);
    } catch (err) {
      setError(err.message || 'Failed to connect to PathAI backend server.');
    } finally {
      setLoading(false);
    }
  };

  const sessionsCompleted = progressHistory.length;
  const averageConfidence = sessionsCompleted
    ? Math.round(progressHistory.reduce((sum, item) => sum + item.confidence, 0) / sessionsCompleted)
    : null;

  const currentTopicDisplay = result ? `${result.level.replace('_', ' ')}: ${formData.topic || 'General'}` : 'No active gaps analyzed yet';
  const currentIcon = result ? subjectIcon[formData.subject] || '📘' : '📘';
  const currentConfidence = result ? `${result.confidence}%` : '--';
  const currentMentor = result ? result.assigned_mentor : previewMentor;
  const currentReadiness = result ? `${result.confidence}%` : '0%';

  return (
    <div className={`min-h-screen ${isDark ? 'bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-900'} relative overflow-hidden selection:bg-emerald-400/30`}>
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(16,185,129,0.2),_transparent_30%),radial-gradient(circle_at_bottom_right,_rgba(34,211,238,0.18),_transparent_28%)]" />
      <div className="absolute top-[-150px] left-[-120px] h-80 w-80 rounded-full bg-emerald-500/20 blur-3xl" />
      <div className="absolute bottom-[-120px] right-[-80px] h-96 w-96 rounded-full bg-cyan-500/20 blur-3xl" />

      <div className="relative z-10 max-w-7xl mx-auto px-5 sm:px-6 lg:px-8 py-6">
        <header className="sticky top-4 z-50 mb-10 flex items-center justify-between rounded-full border border-white/10 bg-white/5 px-4 py-3 backdrop-blur-xl relative">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-emerald-400 to-cyan-400 text-lg font-bold text-slate-950">P</div>
            <div>
              <p className="text-sm font-semibold tracking-[0.22em] text-emerald-300 uppercase">PathAI</p>
              <p className="text-xs text-slate-400">Adaptive learning mentor</p>
            </div>
          </div>

          <nav className="hidden md:flex items-center gap-6 text-sm text-slate-300 absolute left-1/2 -translate-x-1/2">
            <a href="#features" className="hover:text-white transition">Features</a>
            <a href="#generator" className="hover:text-white transition">Generator</a>
          </nav>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setMenuOpen(!menuOpen)}
              className="rounded-full border border-white/15 bg-white/5 px-3 py-2 text-sm font-semibold text-white md:hidden"
            >
              {menuOpen ? 'Close' : 'Menu'}
            </button>
          </div>
        </header>

        {menuOpen && (
          <nav className="mb-6 rounded-[24px] border border-white/10 bg-white/5 p-4 md:hidden">
            <div className="flex flex-col gap-3 text-sm text-slate-200">
              <a href="#features" onClick={() => setMenuOpen(false)}>Features</a>
              <a href="#generator" onClick={() => setMenuOpen(false)}>Generator</a>
            </div>
          </nav>
        )}

        <section className="reveal grid items-center gap-10 lg:grid-cols-[1.1fr_0.9fr] py-6 lg:py-12">
          <div>
            <div className="mb-5 inline-flex rounded-full border border-emerald-400/30 bg-emerald-500/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-emerald-300">
              Powered by intelligent learning routing
            </div>

            <h1 className={`max-w-3xl text-4xl font-black tracking-[-0.04em] sm:text-5xl lg:text-7xl ${isDark ? 'text-white' : 'text-slate-900'}`}>
              Turn confusion into a clear learning path.
            </h1>

            <p className={`mt-5 max-w-2xl text-base leading-7 sm:text-lg ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
              PathAI helps students understand what they are missing, connect the dots fast, and start learning with a mentor-shaped roadmap designed just for them.
            </p>

            <div className="mt-7 flex flex-wrap gap-3">
              <a
                href="#generator"
                className="rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400 px-5 py-3 text-sm font-bold text-slate-950 shadow-lg shadow-emerald-500/20 transition hover:-translate-y-0.5"
              >
                Start learning path
              </a>
              <a
                href="#features"
                className="rounded-full border border-white/15 bg-white/5 px-5 py-3 text-sm font-semibold text-slate-100 transition hover:border-cyan-300/50 hover:bg-white/10"
              >
                See how it works
              </a>
            </div>

            <div className="mt-8 grid gap-3 sm:grid-cols-3">
              {stats.map((stat) => (
                <div key={stat.label} className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur-xl">
                  <p className="text-2xl font-black text-white">{stat.value}</p>
                  <p className="mt-1 text-sm text-slate-400">{stat.label}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-[28px] border border-white/10 bg-white/5 p-4 shadow-2xl shadow-cyan-950/30 backdrop-blur-2xl">
            <div className="rounded-[24px] border border-white/10 bg-slate-950/70 p-5">
              <div className="flex items-center justify-between pb-4">
                <div>
                  <p className="text-xs uppercase tracking-[0.24em] text-cyan-300">Learning pulse</p>
                  <p className="mt-1 text-lg font-semibold text-white">Student progress preview</p>
                </div>
                <div
                  className={`rounded-full px-3 py-1 text-xs font-semibold ${result ? 'bg-emerald-500/15 text-emerald-300' : 'bg-slate-500/15 text-slate-300'}`}
                >
                  {result ? 'Live' : 'Preview'}
                </div>
              </div>

              <div className="space-y-3">
                <div className="rounded-2xl bg-gradient-to-r from-emerald-400/20 to-cyan-400/20 p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-slate-300">Current gap</p>
                      <p className="text-xl font-bold text-white">{currentTopicDisplay}</p>
                    </div>
                    <span className="text-2xl">{currentIcon}</span>
                  </div>
                </div>

                <div className="grid gap-3 sm:grid-cols-2">
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Confidence</p>
                    <p className="mt-2 text-3xl font-black text-white">{currentConfidence}</p>
                  </div>
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Mentor</p>
                    <p className="mt-2 text-lg font-bold text-white truncate">{currentMentor}</p>
                  </div>
                </div>

                <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                  <div className="mb-2 flex items-center justify-between text-sm text-slate-300">
                    <span>Learning path readiness</span>
                    <span>{currentReadiness}</span>
                  </div>
                  <div className="h-2 rounded-full bg-slate-800">
                    <div
                      className="h-2 rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400 transition-all duration-700"
                      style={{ width: currentReadiness }}
                    />
                  </div>
                </div>

                <div className="grid gap-3 sm:grid-cols-2">
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Sessions completed</p>
                    <p className="mt-2 text-2xl font-black text-white">{sessionsCompleted}</p>
                  </div>
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Avg. confidence</p>
                    <p className="mt-2 text-2xl font-black text-white">{averageConfidence !== null ? `${averageConfidence}%` : '—'}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="features" className="reveal py-10 lg:py-14 scroll-mt-32">
          <div className="mb-8 max-w-2xl">
            <p className="text-sm font-semibold uppercase tracking-[0.25em] text-emerald-300">Why students love it</p>
            <h2 className="mt-2 text-3xl font-bold text-white sm:text-4xl">A landing page built around clarity, trust, and momentum.</h2>
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            {featureCards.map((feature) => (
              <article key={feature.title} className="floating-card rounded-[24px] border border-white/10 bg-white/5 p-5 backdrop-blur-xl transition hover:-translate-y-1 hover:border-emerald-300/40">
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-white/10 text-2xl">{feature.icon}</div>
                <h3 className="text-lg font-semibold text-white">{feature.title}</h3>
                <p className="mt-2 text-sm leading-6 text-slate-300">{feature.text}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="reveal py-10 lg:py-14">
          <div className="cta-banner rounded-[32px] border border-emerald-300/20 bg-gradient-to-r from-emerald-400/15 via-cyan-400/10 to-sky-400/15 p-8 text-center backdrop-blur-xl">
            <p className="text-sm font-semibold uppercase tracking-[0.28em] text-emerald-300">Start now</p>
            <h2 className="mt-3 text-3xl font-black text-white sm:text-4xl">Make learning more focused, faster, and calmer.</h2>
            <p className="mx-auto mt-3 max-w-2xl text-slate-200">Turn confusing topics into guided steps, better mentor matching, and a better student experience from the first click.</p>
            <a href="#generator" className="mt-6 inline-flex rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400 px-5 py-3 text-sm font-bold text-slate-950 shadow-lg shadow-emerald-500/20 transition hover:-translate-y-0.5">
              Try PathAI today
            </a>
          </div>
        </section>

        <section id="generator" className="reveal py-8 lg:py-12 scroll-mt-32">
          <div className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
            <div className="rounded-[28px] border border-white/10 bg-white/5 p-6 backdrop-blur-2xl">
              <p className="text-sm font-semibold uppercase tracking-[0.24em] text-cyan-300">Launch the journey</p>
              <h2 className="mt-2 text-3xl font-bold text-white">Enter the topic your student is stuck on.</h2>
              <p className="mt-3 text-slate-300">This intake form collects the exact signals PathAI needs to classify the gap and create a learning pathway.</p>

              <form onSubmit={handleSubmit} className="mt-6 space-y-4">
                <div>
                  <label className="mb-2 block text-xs font-bold uppercase tracking-[0.24em] text-slate-400">Student name</label>
                  <input required type="text" name="name" value={formData.name} onChange={handleChange} placeholder="Enter student name" className="pathai-input" />
                </div>

                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label className="mb-2 block text-xs font-bold uppercase tracking-[0.24em] text-slate-400">Grade</label>
                    <select required name="grade" value={formData.grade} onChange={handleChange} className="pathai-input">
                      <option value="" disabled>Select grade</option>
                      {/* Updated to match curriculum map grades [6, 8, 10] */}
                      {[6, 8, 10].map((g) => (
                        <option key={g} value={g}>Grade {g}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="mb-2 block text-xs font-bold uppercase tracking-[0.24em] text-slate-400">Language</label>
                    <select required name="language" value={formData.language} onChange={handleChange} className="pathai-input">
                      <option value="" disabled>Select language</option>
                      <option value="English">English</option>
                      <option value="Hindi">Hindi</option>
                      <option value="Bengali">Bengali</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="mb-2 block text-xs font-bold uppercase tracking-[0.24em] text-slate-400">Subject</label>
                  <select required name="subject" value={formData.subject} onChange={handleChange} className="pathai-input">
                    <option value="" disabled>Select subject</option>
                    <option value="math">Mathematics</option>
                    <option value="science">Science</option>
                    <option value="english">English</option>
                  </select>
                </div>

                <div>
                  <label className="mb-2 block text-xs font-bold uppercase tracking-[0.24em] text-slate-400">Topic</label>
                  <input required type="text" name="topic" value={formData.topic} onChange={handleChange} placeholder="Fractions, photosynthesis, algebra..." className="pathai-input" />
                </div>

                <div>
                  <label className="mb-2 block text-xs font-bold uppercase tracking-[0.24em] text-slate-400">What is confusing?</label>
                  <textarea required rows="4" name="query" value={formData.query} onChange={handleChange} placeholder="Describe the exact misconception or difficulty." className="pathai-input min-h-[120px] resize-none" />
                </div>

                <button type="submit" disabled={loading} className="pathai-button">
                  {loading ? 'Generating path...' : 'Generate learning path'}
                </button>
              </form>
            </div>

            <div id="results" className="rounded-[28px] border border-white/10 bg-slate-950/60 p-5 backdrop-blur-2xl">
              {error && (
                <div className="rounded-2xl border border-rose-500/30 bg-rose-500/10 p-5 text-sm text-rose-200">
                  <p className="font-semibold">Connection Error</p>
                  <p className="mt-1">{error}</p>
                </div>
              )}

              {!result && !loading && !error && (
                <div className="flex min-h-[500px] flex-col items-center justify-center rounded-[24px] border border-dashed border-white/10 bg-white/5 p-8 text-center">
                  <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-white/10 text-3xl">🧠</div>
                  <h3 className="text-xl font-semibold text-white">Awaiting analysis</h3>
                  <p className="mt-2 max-w-md text-sm leading-6 text-slate-400">
                    Your personalized learning pathway will appear here with the concept breakdown, mentor assignment, and a quick quiz.
                  </p>
                </div>
              )}

              {loading && (
                <div className="flex min-h-[500px] flex-col items-center justify-center rounded-[24px] border border-white/10 bg-white/5 p-8 text-center">
                  <div className="loader-ring mb-5" />
                  <p className="text-lg font-semibold text-white">Analyzing learning gap</p>
                  <p className="mt-2 text-sm text-slate-400">Routing through the best mentor logic for {formData.language || 'selected language'}.</p>
                </div>
              )}

              {result && !loading && (
                <div className="space-y-4">
                  <div className="rounded-[24px] border border-white/10 bg-white/5 p-5">
                    <div className="flex flex-wrap items-center justify-between gap-4">
                      <div>
                        <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Classified level</p>
                        <span className="mt-2 inline-flex rounded-full px-3 py-1 text-xs font-bold uppercase tracking-[0.2em] text-slate-950 bg-emerald-300">
                          {result.level.replace('_', ' ')}
                        </span>
                      </div>
                      <div>
                        <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Assigned mentor</p>
                        <span className="mt-2 inline-flex rounded-full bg-cyan-400/15 px-3 py-1 text-sm font-semibold text-cyan-300">
                          {result.assigned_mentor}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="rounded-[24px] border border-white/10 bg-white/5 p-5">
                    <p className="mb-3 text-xs uppercase tracking-[0.24em] text-emerald-300">Adaptive breakdown</p>
                    <p className="whitespace-pre-line text-sm leading-7 text-slate-200">{result.explanation}</p>
                  </div>

                  <div className="rounded-[24px] border border-white/10 bg-white/5 p-5">
                    <p className="mb-3 text-xs uppercase tracking-[0.24em] text-cyan-300">Knowledge check</p>
                    <div className="rounded-2xl bg-slate-900 p-4 text-sm leading-7 text-slate-200 whitespace-pre-line font-mono">
                      {result.quiz}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>

        <footer className="mt-8 border-t border-white/10 py-8 text-sm text-slate-400">
          <div className="grid gap-6 md:grid-cols-[1.2fr_0.8fr_0.8fr]">
            <div>
              <p className="font-semibold uppercase tracking-[0.24em] text-emerald-300">PathAI</p>
              <p className="mt-2 max-w-md">Adaptive learning mentorship for every student, built to turn confusion into a confident next step.</p>
            </div>

            <div>
              <p className="font-semibold text-white">Company</p>
              <div className="mt-2 space-y-2">
                <a href="#features" className="block hover:text-white">Features</a>
                <a href="#generator" className="block hover:text-white">Generator</a>
              </div>
            </div>

            <div>
              <p className="font-semibold text-white">Connect</p>
              <div className="mt-2 flex gap-3 text-lg">
                <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" className="hover:text-white">LinkedIn</a>
                <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="hover:text-white">Twitter</a>
                <a href="mailto:hello@pathai.com" className="hover:text-white">Email</a>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}