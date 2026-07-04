import { ReactNode } from 'react';

interface AuthLayoutProps {
  children: ReactNode;
}

export default function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="min-h-screen bg-slate-100 px-4 py-10 sm:px-6 lg:px-8">
      <div className="mx-auto grid max-w-6xl overflow-hidden rounded-[2rem] bg-white shadow-card lg:grid-cols-[1.45fr_1fr]">
        <aside className="relative hidden flex-col justify-between overflow-hidden bg-gradient-to-br from-sky-700 via-indigo-700 to-slate-900 p-10 text-white lg:flex">
          <div className="absolute inset-0 opacity-20" style={{ backgroundImage: 'radial-gradient(circle at 20% 20%, rgba(255,255,255,0.15), transparent 28%), radial-gradient(circle at 85% 80%, rgba(255,255,255,0.12), transparent 24%)' }} />
          <div className="relative space-y-8">
            <div className="inline-flex items-center gap-3 rounded-3xl bg-white/10 px-4 py-3 backdrop-blur">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-white/20 text-lg font-semibold">TF</div>
              <div>
                <p className="text-xs uppercase tracking-[0.35em] text-sky-100/90">TaskFlow</p>
                <p className="mt-1 text-sm text-slate-200">Modern task management for teams.</p>
              </div>
            </div>

            <div className="space-y-4">
              <h1 className="text-4xl font-semibold leading-tight">Work smarter together.</h1>
              <p className="max-w-md text-sm leading-6 text-slate-200/90">
                Collaborate across teams, manage priorities, and keep every task moving with clarity.
              </p>
            </div>
          </div>

          <div className="relative space-y-4">
            <div className="rounded-3xl bg-white/10 p-5 shadow-[0_20px_40px_rgba(255,255,255,0.08)]">
              <p className="text-3xl font-semibold">68%</p>
              <p className="mt-1 text-sm text-slate-200/90">Team alignment score</p>
            </div>
            <div className="rounded-3xl bg-white/10 p-5 shadow-[0_20px_40px_rgba(255,255,255,0.08)]">
              <p className="text-3xl font-semibold">14</p>
              <p className="mt-1 text-sm text-slate-200/90">Tasks due today</p>
            </div>
          </div>

          <div className="relative space-y-2 text-sm text-slate-200/80">
            <p className="uppercase tracking-[0.24em] text-slate-300">Built for fast onboarding</p>
            <div className="flex flex-wrap gap-2">
              <span className="rounded-full bg-white/10 px-3 py-1">Task List</span>
              <span className="rounded-full bg-white/10 px-3 py-1">Task Detail</span>
              <span className="rounded-full bg-white/10 px-3 py-1">Profile</span>
            </div>
          </div>
        </aside>
        <section className="flex items-center justify-center bg-slate-100 p-8 sm:p-12">
          <div className="w-full max-w-md rounded-[2rem] bg-white p-8 shadow-[0_24px_80px_rgba(15,23,42,0.14)]">
            {children}
          </div>
        </section>
      </div>
    </div>
  );
}
