import { useId, useMemo, useState } from 'react';

/*
  Recommended palette tokens
  --bg-0: #040814
  --bg-1: #08111f
  --bg-2: #0d1a2c
  --line-soft: rgba(173, 208, 255, 0.14)
  --line-strong: rgba(186, 220, 255, 0.24)
  --text-main: rgba(245, 248, 255, 0.96)
  --text-body: rgba(221, 231, 246, 0.84)
  --text-muted: rgba(179, 196, 220, 0.7)
  --text-helper: rgba(191, 208, 232, 0.78)
  --glow-blue: rgba(101, 159, 255, 0.24)
  --glow-cyan: rgba(123, 208, 255, 0.16)
  --cta-surface: #f2eee8
  --cta-text: #102033
*/

const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

const currentYear = new Date().getFullYear();
const YEARS = Array.from({ length: currentYear - 1919 }, (_, i) => String(currentYear - i));
const DAYS = Array.from({ length: 31 }, (_, i) => String(i + 1));
const HOURS = Array.from({ length: 12 }, (_, i) => String(i + 1));
const MINUTES = Array.from({ length: 60 }, (_, i) => String(i).padStart(2, '0'));

const SAMPLE_FORM = {
  name: '',
  month: '',
  day: '',
  year: '',
  hour: '12',
  minute: '00',
  ampm: 'PM',
  birthLocation: '',
  currentLocation: '',
};

function FieldLabel({ children, htmlFor }) {
  return (
    <label
      htmlFor={htmlFor}
      className="mb-2 block text-[10px] font-semibold uppercase tracking-[0.22em] text-slate-300/82"
    >
      {children}
    </label>
  );
}

function FieldHint({ children }) {
  return (
    <p className="mt-2 text-[12px] leading-5 text-slate-300/75">
      {children}
    </p>
  );
}

function SurfaceInput({ className = '', ...props }) {
  return (
    <input
      {...props}
      className={[
        'h-13 w-full rounded-2xl border border-slate-200/10 bg-white/[0.055] px-4 text-[15px] text-slate-50 outline-none',
        'placeholder:text-slate-300/48',
        'shadow-[inset_0_1px_0_rgba(255,255,255,0.06),0_8px_24px_rgba(0,0,0,0.18)] backdrop-blur-md',
        'transition-all duration-200',
        'focus:border-sky-200/28 focus:bg-white/[0.075] focus:shadow-[inset_0_1px_0_rgba(255,255,255,0.08),0_0_0_1px_rgba(125,182,255,0.18),0_14px_30px_rgba(7,18,40,0.26)]',
        className,
      ].join(' ')}
    />
  );
}

function SurfaceSelect({ className = '', children, ...props }) {
  return (
    <div className="relative">
      <select
        {...props}
        className={[
          'h-13 w-full appearance-none rounded-2xl border border-slate-200/10 bg-white/[0.055] px-4 pr-11 text-[15px] text-slate-50 outline-none',
          'shadow-[inset_0_1px_0_rgba(255,255,255,0.06),0_8px_24px_rgba(0,0,0,0.18)] backdrop-blur-md',
          'transition-all duration-200',
          'focus:border-sky-200/28 focus:bg-white/[0.075] focus:shadow-[inset_0_1px_0_rgba(255,255,255,0.08),0_0_0_1px_rgba(125,182,255,0.18),0_14px_30px_rgba(7,18,40,0.26)]',
          className,
        ].join(' ')}
      >
        {children}
      </select>

      <div className="pointer-events-none absolute inset-y-0 right-4 flex items-center text-slate-300/56">
        <svg viewBox="0 0 20 20" fill="none" className="h-4 w-4">
          <path
            d="M5.5 7.75L10 12.25L14.5 7.75"
            stroke="currentColor"
            strokeWidth="1.6"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
    </div>
  );
}

function OnboardingAtmosphere() {
  return (
    <div aria-hidden="true" className="pointer-events-none absolute inset-0 overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(84,135,255,0.16)_0%,rgba(9,16,28,0.0)_34%),linear-gradient(180deg,#040814_0%,#07101c_46%,#050912_100%)]" />
      <div className="absolute -left-20 top-16 h-64 w-64 rounded-full bg-sky-400/12 blur-3xl" />
      <div className="absolute right-[-3.5rem] top-44 h-72 w-72 rounded-full bg-blue-500/10 blur-3xl" />
      <div className="absolute inset-x-0 top-[18%] h-64 bg-[radial-gradient(circle_at_center,rgba(130,196,255,0.12)_0%,transparent_60%)]" />
      <div className="absolute inset-0 bg-[linear-gradient(180deg,transparent_0%,rgba(4,8,16,0.08)_40%,rgba(2,4,8,0.32)_100%)]" />

      <div className="absolute inset-x-[8%] top-[10%] h-[46%] rounded-[40px] border border-slate-200/5 opacity-60" />
      <div className="absolute inset-x-[15%] top-[14%] h-[34%] rounded-[32px] border border-sky-100/5 opacity-40" />
      <div className="absolute left-1/2 top-[24%] h-52 w-52 -translate-x-1/2 rounded-full border border-slate-100/5 opacity-40" />
      <div className="absolute left-1/2 top-[24%] h-28 w-28 -translate-x-1/2 rounded-full border border-slate-100/5 opacity-50" />
      <div className="absolute left-1/2 top-[24%] h-[1px] w-72 -translate-x-1/2 bg-gradient-to-r from-transparent via-sky-100/10 to-transparent" />
      <div className="absolute left-1/2 top-[24%] h-72 w-[1px] -translate-x-1/2 bg-gradient-to-b from-transparent via-sky-100/10 to-transparent" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_58%,rgba(3,6,12,0.42)_100%)]" />
    </div>
  );
}

export default function OnboardingScreenPremium() {
  const [form, setForm] = useState(SAMPLE_FORM);

  const ids = useMemo(
    () => ({
      name: useId(),
      month: useId(),
      day: useId(),
      year: useId(),
      hour: useId(),
      minute: useId(),
      ampm: useId(),
      birthLocation: useId(),
      currentLocation: useId(),
    }),
    []
  );

  function updateField(field, value) {
    setForm(prev => ({ ...prev, [field]: value }));
  }

  function handleSubmit(event) {
    event.preventDefault();
  }

  return (
    <main className="relative min-h-screen overflow-hidden bg-[#040814] text-slate-50">
      <OnboardingAtmosphere />

      <div className="relative z-[1] mx-auto flex min-h-screen w-full max-w-[440px] flex-col px-5 pb-10 pt-10 sm:px-6">
        <header className="pb-8 pt-3">
          <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-slate-200/10 bg-white/[0.04] px-3 py-1.5 text-[9px] font-semibold uppercase tracking-[0.18em] text-slate-300/76 shadow-[inset_0_1px_0_rgba(255,255,255,0.05)] backdrop-blur-md">
            <span className="h-1.5 w-1.5 rounded-full bg-sky-300/70 shadow-[0_0_10px_rgba(125,182,255,0.55)]" />
            Signal Setup
          </div>

          <div className="space-y-2">
            <p className="text-[17px] font-light tracking-[0.01em] text-slate-200/82">
              Your output isn&apos;t constant.
            </p>
            <p className="text-[17px] font-light tracking-[0.01em] text-slate-200/72">
              Neither is your day.
            </p>
          </div>

          <h1 className="mt-5 text-[42px] font-semibold leading-[0.95] tracking-[-0.04em] text-slate-50 [text-shadow:0_0_30px_rgba(110,170,255,0.16)]">
            Find your rhythm.
          </h1>

          <p className="mt-4 max-w-[22rem] text-[14px] leading-6 text-slate-300/82">
            Enter the same details you already use now. This redesign keeps the flow intact and makes every step clearer to scan.
          </p>
        </header>

        <section className="relative overflow-hidden rounded-[30px] border border-slate-200/10 bg-[linear-gradient(180deg,rgba(10,18,31,0.88)_0%,rgba(7,12,20,0.92)_100%)] px-4 pb-5 pt-4 shadow-[0_24px_80px_rgba(0,0,0,0.42),inset_0_1px_0_rgba(255,255,255,0.04)] backdrop-blur-xl sm:px-5 sm:pb-6 sm:pt-5">
          <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.03)_0%,rgba(255,255,255,0.0)_24%,rgba(255,255,255,0.015)_100%)]" />

          <form onSubmit={handleSubmit} className="relative z-[1] space-y-5">
            <div className="space-y-3">
              <FieldLabel htmlFor={ids.name}>&gt; Name</FieldLabel>
              <SurfaceInput
                id={ids.name}
                type="text"
                autoComplete="name"
                placeholder="What should we call you?"
                value={form.name}
                onChange={e => updateField('name', e.target.value)}
              />
              <FieldHint>
                Use your own name or any profile name you want to see in the app.
              </FieldHint>
            </div>

            <div className="space-y-3">
              <FieldLabel htmlFor={ids.month}>&gt; Birth Date</FieldLabel>
              <div className="grid grid-cols-[1.45fr_0.9fr_1.15fr] gap-2.5">
                <SurfaceSelect
                  id={ids.month}
                  value={form.month}
                  onChange={e => updateField('month', e.target.value)}
                >
                  <option value="">Month</option>
                  {MONTHS.map((month, index) => (
                    <option key={month} value={String(index + 1)}>
                      {month}
                    </option>
                  ))}
                </SurfaceSelect>

                <SurfaceSelect
                  id={ids.day}
                  value={form.day}
                  onChange={e => updateField('day', e.target.value)}
                >
                  <option value="">Day</option>
                  {DAYS.map(day => (
                    <option key={day} value={day}>
                      {day}
                    </option>
                  ))}
                </SurfaceSelect>

                <SurfaceSelect
                  id={ids.year}
                  value={form.year}
                  onChange={e => updateField('year', e.target.value)}
                >
                  <option value="">Year</option>
                  {YEARS.map(year => (
                    <option key={year} value={year}>
                      {year}
                    </option>
                  ))}
                </SurfaceSelect>
              </div>
            </div>

            <div className="space-y-3">
              <FieldLabel htmlFor={ids.hour}>&gt; Birth Time</FieldLabel>
              <div className="grid grid-cols-3 gap-2.5">
                <SurfaceSelect
                  id={ids.hour}
                  value={form.hour}
                  onChange={e => updateField('hour', e.target.value)}
                >
                  {HOURS.map(hour => (
                    <option key={hour} value={hour}>
                      {hour}
                    </option>
                  ))}
                </SurfaceSelect>

                <SurfaceSelect
                  id={ids.minute}
                  value={form.minute}
                  onChange={e => updateField('minute', e.target.value)}
                >
                  {MINUTES.map(minute => (
                    <option key={minute} value={minute}>
                      {minute}
                    </option>
                  ))}
                </SurfaceSelect>

                <SurfaceSelect
                  id={ids.ampm}
                  value={form.ampm}
                  onChange={e => updateField('ampm', e.target.value)}
                >
                  <option value="AM">AM</option>
                  <option value="PM">PM</option>
                </SurfaceSelect>
              </div>
              <FieldHint>No birth time? Leave at 12:00 PM</FieldHint>
            </div>

            <div className="space-y-3">
              <FieldLabel htmlFor={ids.birthLocation}>&gt; Birth Location</FieldLabel>
              <SurfaceInput
                id={ids.birthLocation}
                type="text"
                placeholder="Search city, country…"
                value={form.birthLocation}
                onChange={e => updateField('birthLocation', e.target.value)}
              />
              <FieldHint>
                City where you were born — sets birth timezone automatically
              </FieldHint>
            </div>

            <div className="space-y-3">
              <FieldLabel htmlFor={ids.currentLocation}>&gt; Current Location</FieldLabel>
              <SurfaceInput
                id={ids.currentLocation}
                type="text"
                placeholder="Search city, country…"
                value={form.currentLocation}
                onChange={e => updateField('currentLocation', e.target.value)}
              />
              <FieldHint>
                Where you are now — used for local timing calculations
              </FieldHint>
            </div>

            <button
              type="submit"
              className="group mt-2 flex h-14 w-full items-center justify-center rounded-2xl border border-[#f7f1e6]/60 bg-[linear-gradient(180deg,#f7f1e6_0%,#e7ddd0_100%)] px-5 text-[13px] font-semibold uppercase tracking-[0.18em] text-[#102033] shadow-[0_18px_40px_rgba(0,0,0,0.32),inset_0_1px_0_rgba(255,255,255,0.9)] transition-all duration-200 hover:translate-y-[-1px] hover:brightness-[1.02] focus:outline-none focus:ring-2 focus:ring-sky-200/50 focus:ring-offset-2 focus:ring-offset-[#07101b] active:translate-y-0"
            >
              Reveal Signal
            </button>
          </form>
        </section>
      </div>
    </main>
  );
}
