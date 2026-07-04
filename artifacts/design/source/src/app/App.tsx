import { useState } from "react";

// ─── Design tokens ─────────────────────────────────────────────────────────
const PRIMARY = "#2563EB";

// ─── Shared SVG Icons ──────────────────────────────────────────────────────

function IcoTask() {
  return <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-8.29 13.29L7 12.59 8.41 11.17l2.29 2.3 5.88-5.88L18 9l-7.29 7.29z" /></svg>;
}
function IcoGoogle() {
  return <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>;
}
function IcoEmail() { return <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" className="text-slate-400"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z"/></svg>; }
function IcoLock() { return <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" className="text-slate-400"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>; }
function IcoPerson() { return <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" className="text-slate-400"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>; }
function IcoEye({ off }: { off: boolean }) {
  return off
    ? <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78 3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"/></svg>
    : <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>;
}
function IcoCheck() { return <svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17 4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>; }
function IcoRight() { return <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M10 6 8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>; }
function IcoSearch() { return <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" className="text-slate-400"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>; }
function IcoHome() { return <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>; }
function IcoList() { return <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm0-8h2V7H3v2zm4 4h14v-2H7v2zm0 4h14v-2H7v2zM7 7v2h14V7H7z"/></svg>; }
function IcoCalendar() { return <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/></svg>; }
function IcoTeam() { return <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>; }
function IcoAnalytics() { return <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/></svg>; }
function IcoSettings() { return <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/></svg>; }
function IcoBell() { return <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.63-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.64 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/></svg>; }
function IcoPlus() { return <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>; }
function IcoFilter() { return <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M4.25 5.61C6.27 8.2 10 13 10 13v6c0 .55.45 1 1 1h2c.55 0 1-.45 1-1v-6s3.72-4.8 5.74-7.39A.998.998 0 0 0 18.95 4H5.04a1 1 0 0 0-.79 1.61z"/></svg>; }
function IcoSort() { return <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M3 18h6v-2H3v2zM3 6v2h18V6H3zm0 7h12v-2H3v2z"/></svg>; }
function IcoGrid() { return <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M3 3v8h8V3H3zm6 6H5V5h4v4zm-6 4v8h8v-8H3zm6 6H5v-4h4v4zm4-16v8h8V3h-8zm6 6h-4V5h4v4zm-6 4v8h8v-8h-8zm6 6h-4v-4h4v4z"/></svg>; }
function IcoRows() { return <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M3 5h2V3c-1.1 0-2 .9-2 2zm0 8h2v-2H3v2zm4 8h2v-2H7v2zM3 9h2V7H3v2zm10-6h-2v2h2V3zm6 0v2h2c0-1.1-.9-2-2-2zM5 21v-2H3c0 1.1.9 2 2 2zm-2-4h2v-2H3v2zM9 3H7v2h2V3zm2 18h2v-2h-2v2zm8-8h2v-2h-2v2zm0 8c1.1 0 2-.9 2-2h-2v2zm0-12h2V7h-2v2zm0 8h2v-2h-2v2zm-4 4h2v-2h-2v2zm0-16h2V3h-2v2z"/></svg>; }
function IcoMoreV() { return <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/></svg>; }
function IcoTrend() { return <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="m16 6 2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"/></svg>; }
function IcoChevron(){ return <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M10 6 8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>; }
function IcoChevronLeft(){ return <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M15.41 7.41 14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg>; }

// ─── Shared primitives ─────────────────────────────────────────────────────

function Avatar({ initials, color = "#2563EB", size = 32 }: { initials: string; color?: string; size?: number }) {
  return (
    <div className="rounded-full flex items-center justify-center flex-shrink-0 font-semibold text-white"
      style={{ width: size, height: size, background: color, fontSize: size * 0.36 }}>
      {initials}
    </div>
  );
}

function Badge({ label, variant }: { label: string; variant: "todo" | "inprogress" | "done" | "review" | "high" | "medium" | "low" | "overdue" }) {
  const map: Record<string, string> = {
    todo: "bg-slate-100 text-slate-600",
    inprogress: "bg-blue-50 text-blue-700",
    done: "bg-emerald-50 text-emerald-700",
    review: "bg-violet-50 text-violet-700",
    high: "bg-red-50 text-red-600",
    medium: "bg-amber-50 text-amber-700",
    low: "bg-slate-100 text-slate-500",
    overdue: "bg-red-100 text-red-700",
  };
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${map[variant]}`}>
      {label}
    </span>
  );
}

function Card({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`bg-white rounded-xl border border-slate-200 shadow-sm ${className}`}>
      {children}
    </div>
  );
}

function InputField({
  label, type = "text", placeholder, value, onChange, icon, rightIcon, onRightIconClick, error
}: {
  label: string; type?: string; placeholder: string; value: string;
  onChange: (v: string) => void; icon?: React.ReactNode; rightIcon?: React.ReactNode;
  onRightIconClick?: () => void; error?: string;
}) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-sm font-medium text-slate-700">{label}</label>
      <div className={`flex items-center gap-2.5 px-3.5 h-11 rounded-xl border transition-all ${
        error ? "border-red-400 ring-1 ring-red-200" : "border-slate-200 bg-white focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100"
      }`}>
        {icon && <span className="flex-shrink-0">{icon}</span>}
        <input
          type={type} placeholder={placeholder} value={value}
          onChange={e => onChange(e.target.value)}
          className="flex-1 bg-transparent text-sm text-slate-800 placeholder:text-slate-400 outline-none"
        />
        {rightIcon && (
          <button type="button" onClick={onRightIconClick} className="flex-shrink-0 text-slate-400 hover:text-slate-600 transition-colors">
            {rightIcon}
          </button>
        )}
      </div>
      {error && <p className="text-xs text-red-500">{error}</p>}
    </div>
  );
}

// ─── Auth Left Panel ───────────────────────────────────────────────────────

function AuthLeftPanel() {
  const tasks = [
    { label: "Design system audit", done: true, priority: "High", color: "#ef4444", initials: "KL", avatarColor: "#8b5cf6" },
    { label: "API integration review", done: false, priority: "Med", color: "#f59e0b", initials: "MR", avatarColor: "#10b981" },
    { label: "Q3 roadmap planning", done: false, priority: "High", color: "#ef4444", initials: "ST", avatarColor: "#f97316" },
    { label: "Onboarding flow update", done: true, priority: "Low", color: "#64748b", initials: "JW", avatarColor: "#2563eb" },
  ];

  return (
    <div className="relative flex-1 flex flex-col justify-between p-10 overflow-hidden"
      style={{ background: "linear-gradient(145deg, #1d4ed8 0%, #1e3a8a 55%, #172554 100%)" }}>
      <div className="absolute inset-0 opacity-[0.07]"
        style={{ backgroundImage: "radial-gradient(circle at 25% 25%, #60a5fa 0%, transparent 55%), radial-gradient(circle at 75% 75%, #a78bfa 0%, transparent 55%)" }} />
      <div className="absolute top-0 right-0 w-72 h-72 rounded-full opacity-10 -translate-y-1/3 translate-x-1/3"
        style={{ background: "radial-gradient(circle, #93c5fd, transparent)" }} />
      <div className="absolute bottom-0 left-0 w-80 h-80 rounded-full opacity-10 translate-y-1/3 -translate-x-1/3"
        style={{ background: "radial-gradient(circle, #c7d2fe, transparent)" }} />

      <div className="relative flex items-center gap-2.5">
        <div className="w-9 h-9 rounded-xl bg-white/20 flex items-center justify-center text-white"><IcoTask /></div>
        <span className="text-white font-bold text-xl" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>TaskFlow</span>
      </div>

      <div className="relative space-y-4 flex-1 flex flex-col justify-center py-8">
        <div className="grid grid-cols-3 gap-3">
          {[["142","Tasks"],["89%","On Track"],["12","Due Today"]].map(([v,l]) => (
            <div key={l} className="rounded-xl bg-white/10 p-3 text-center border border-white/10">
              <div className="text-white font-bold text-xl" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>{v}</div>
              <div className="text-blue-200 text-xs mt-0.5">{l}</div>
            </div>
          ))}
        </div>

        <div className="rounded-xl bg-white/10 border border-white/15 p-4 space-y-2.5">
          <p className="text-white/50 text-[11px] font-semibold uppercase tracking-wider">Active Sprint</p>
          {tasks.map(t => (
            <div key={t.label} className="flex items-center gap-2.5 p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors">
              <div className={`w-4.5 h-4.5 w-5 h-5 rounded-[5px] flex items-center justify-center flex-shrink-0 border ${t.done ? "bg-blue-400 border-blue-400 text-white" : "border-white/30"}`}>
                {t.done && <IcoCheck />}
              </div>
              <span className={`text-sm flex-1 ${t.done ? "line-through text-white/35" : "text-white/85"}`}>{t.label}</span>
              <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded-full" style={{ color: t.color, background: `${t.color}22` }}>{t.priority}</span>
              <Avatar initials={t.initials} color={t.avatarColor} size={22} />
            </div>
          ))}
        </div>

        <div>
          <div className="flex justify-between text-xs text-white/50 mb-1.5"><span>Sprint 12 progress</span><span>68%</span></div>
          <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
            <div className="h-full rounded-full" style={{ width: "68%", background: "linear-gradient(90deg,#93c5fd,#6ee7b7)" }} />
          </div>
        </div>
      </div>

      <div className="relative">
        <p className="text-blue-200 text-sm leading-relaxed italic">"TaskFlow cut our planning overhead by 40%. The team visibility is unmatched."</p>
        <div className="flex items-center gap-2 mt-3">
          <Avatar initials="SE" color="#3b82f6" size={28} />
          <div><p className="text-white text-xs font-semibold">Sarah Evans</p><p className="text-blue-300 text-xs">Engineering Lead · Stripe</p></div>
        </div>
      </div>
    </div>
  );
}

// ─── Auth Layout (shared wrapper) ─────────────────────���───────────────────

function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex w-full min-h-screen">
      <div className="hidden xl:flex w-[500px] flex-shrink-0"><AuthLeftPanel /></div>
      {/* Right panel: distinct patterned background */}
      <div className="flex-1 relative flex items-center justify-center overflow-hidden"
        style={{ background: "linear-gradient(150deg,#eef2ff 0%,#e0e7ff 40%,#dbeafe 100%)" }}>
        {/* Dot grid pattern */}
        <div className="absolute inset-0 opacity-40"
          style={{ backgroundImage: "radial-gradient(circle, #94a3b8 1px, transparent 1px)", backgroundSize: "28px 28px" }} />
        {/* Soft blobs */}
        <div className="absolute top-16 right-20 w-64 h-64 rounded-full opacity-30 blur-3xl" style={{ background: "#a5b4fc" }} />
        <div className="absolute bottom-20 left-16 w-56 h-56 rounded-full opacity-20 blur-3xl" style={{ background: "#93c5fd" }} />
        {/* Form card */}
        <div className="relative z-10 w-full max-w-md mx-auto px-4">
          <div className="bg-white rounded-2xl shadow-xl shadow-blue-900/10 border border-slate-200/80 px-8 py-9">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Login Screen ──────────────────────────────────────────────────────────

function LoginScreen({ onSwitch }: { onSwitch: () => void }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPw, setShowPw] = useState(false);
  const [remember, setRemember] = useState(false);
  const [loading, setLoading] = useState(false);

  return (
    <AuthLayout>
      <div className="flex items-center gap-2 mb-7 xl:hidden">
        <div className="w-8 h-8 rounded-lg flex items-center justify-center text-white" style={{ background: PRIMARY }}><IcoTask /></div>
        <span className="font-bold text-lg" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>TaskFlow</span>
      </div>
      <h1 className="text-[1.6rem] font-bold text-slate-900 mb-1" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>Welcome back</h1>
      <p className="text-sm text-slate-500 mb-7">Sign in to continue to your workspace</p>

      <form onSubmit={e => { e.preventDefault(); setLoading(true); setTimeout(() => setLoading(false), 1600); }} className="space-y-4">
        <InputField label="Email address" type="email" placeholder="you@company.com" value={email} onChange={setEmail} icon={<IcoEmail />} />
        <InputField label="Password" type={showPw ? "text" : "password"} placeholder="Enter your password" value={password} onChange={setPassword}
          icon={<IcoLock />} rightIcon={<IcoEye off={!showPw} />} onRightIconClick={() => setShowPw(p => !p)} />

        <div className="flex items-center justify-between pt-0.5">
          <label className="flex items-center gap-2 cursor-pointer" onClick={() => setRemember(r => !r)}>
            <div className={`w-4 h-4 rounded-[4px] border flex items-center justify-center transition-all ${remember ? "text-white border-blue-600" : "border-slate-300 bg-white"}`}
              style={remember ? { background: PRIMARY } : {}}>
              {remember && <IcoCheck />}
            </div>
            <span className="text-sm text-slate-500">Remember me</span>
          </label>
          <button type="button" className="text-sm font-medium text-blue-600 hover:underline">Forgot password?</button>
        </div>

        <button type="submit" disabled={loading}
          className="w-full h-11 rounded-xl text-white text-sm font-semibold flex items-center justify-center gap-1.5 hover:opacity-90 active:scale-[0.99] transition-all disabled:opacity-70 mt-1"
          style={{ background: PRIMARY }}>
          {loading ? <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/></svg>
            : <>Sign In <IcoRight /></>}
        </button>
      </form>

      <div className="mt-5 space-y-3.5">
        <div className="flex items-center gap-3"><div className="flex-1 h-px bg-slate-200"/><span className="text-xs text-slate-400 font-medium">OR</span><div className="flex-1 h-px bg-slate-200"/></div>
        <button className="w-full h-11 flex items-center justify-center gap-2.5 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 transition-colors text-sm font-medium text-slate-700">
          <IcoGoogle /> Continue with Google
        </button>
      </div>
      <p className="text-center text-sm text-slate-500 mt-7">
        Don&apos;t have an account?{" "}<button onClick={onSwitch} className="text-blue-600 font-semibold hover:underline">Create one free</button>
      </p>
    </AuthLayout>
  );
}

// ─── Register Screen ───────────────────────────────────────────────────────

function RegisterScreen({ onSwitch }: { onSwitch: () => void }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [showPw, setShowPw] = useState(false);
  const [showC, setShowC] = useState(false);
  const [terms, setTerms] = useState(false);
  const [loading, setLoading] = useState(false);
  const pwMatch = confirm.length > 0 && password !== confirm;
  const strength = password.length === 0 ? 0 : password.length < 6 ? 1 : password.length < 10 ? 2 : 3;
  const sLabel = ["","Weak","Fair","Strong"][strength];
  const sColor = ["","bg-red-400","bg-amber-400","bg-emerald-500"][strength];

  return (
    <AuthLayout>
      <div className="flex items-center gap-2 mb-6 xl:hidden">
        <div className="w-8 h-8 rounded-lg flex items-center justify-center text-white" style={{ background: PRIMARY }}><IcoTask /></div>
        <span className="font-bold text-lg" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>TaskFlow</span>
      </div>
      <h1 className="text-[1.6rem] font-bold text-slate-900 mb-1" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>Create your account</h1>
      <p className="text-sm text-slate-500 mb-6">14-day free trial · No credit card required</p>

      <form onSubmit={e => { e.preventDefault(); if (!terms || pwMatch) return; setLoading(true); setTimeout(() => setLoading(false), 1600); }} className="space-y-3.5">
        <InputField label="Full name" placeholder="Jane Smith" value={name} onChange={setName} icon={<IcoPerson />} />
        <InputField label="Work email" type="email" placeholder="jane@company.com" value={email} onChange={setEmail} icon={<IcoEmail />} />

        <div className="space-y-1.5">
          <InputField label="Password" type={showPw ? "text" : "password"} placeholder="At least 8 characters" value={password} onChange={setPassword}
            icon={<IcoLock />} rightIcon={<IcoEye off={!showPw} />} onRightIconClick={() => setShowPw(p => !p)} />
          {password.length > 0 && (
            <div className="flex items-center gap-2">
              <div className="flex gap-1 flex-1">
                {[1,2,3].map(i => <div key={i} className={`h-1 flex-1 rounded-full transition-all ${strength >= i ? sColor : "bg-slate-200"}`} />)}
              </div>
              <span className={`text-xs font-medium ${strength===1?"text-red-500":strength===2?"text-amber-500":"text-emerald-600"}`}>{sLabel}</span>
            </div>
          )}
        </div>

        <InputField label="Confirm password" type={showC ? "text" : "password"} placeholder="Re-enter password" value={confirm} onChange={setConfirm}
          icon={<IcoLock />} rightIcon={<IcoEye off={!showC} />} onRightIconClick={() => setShowC(p => !p)}
          error={pwMatch ? "Passwords do not match" : undefined} />

        <label className="flex items-start gap-2.5 cursor-pointer pt-0.5" onClick={() => setTerms(t => !t)}>
          <div className={`mt-0.5 w-4 h-4 rounded-[4px] border flex-shrink-0 flex items-center justify-center transition-all ${terms ? "text-white border-blue-600" : "border-slate-300 bg-white"}`}
            style={terms ? { background: PRIMARY } : {}}>
            {terms && <IcoCheck />}
          </div>
          <span className="text-sm text-slate-500 leading-relaxed">
            I agree to the <button type="button" className="text-blue-600 font-medium hover:underline">Terms</button> and <button type="button" className="text-blue-600 font-medium hover:underline">Privacy Policy</button>
          </span>
        </label>

        <button type="submit" disabled={loading || !terms}
          className="w-full h-11 rounded-xl text-white text-sm font-semibold flex items-center justify-center gap-1.5 hover:opacity-90 active:scale-[0.99] transition-all disabled:opacity-55 mt-1"
          style={{ background: PRIMARY }}>
          {loading ? <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/></svg>
            : <>Create Account <IcoRight /></>}
        </button>
      </form>

      <div className="mt-4 space-y-3.5">
        <div className="flex items-center gap-3"><div className="flex-1 h-px bg-slate-200"/><span className="text-xs text-slate-400 font-medium">OR</span><div className="flex-1 h-px bg-slate-200"/></div>
        <button className="w-full h-11 flex items-center justify-center gap-2.5 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 transition-colors text-sm font-medium text-slate-700">
          <IcoGoogle /> Continue with Google
        </button>
      </div>
      <p className="text-center text-sm text-slate-500 mt-5">
        Already have an account?{" "}<button onClick={onSwitch} className="text-blue-600 font-semibold hover:underline">Sign in</button>
      </p>
    </AuthLayout>
  );
}

// ─── Sidebar ───────────────────────────────────────────────────────────────

const navItems = [
  { icon: <IcoHome />, label: "Dashboard", id: "dashboard" },
  { icon: <IcoList />, label: "Task List", id: "tasklist" },
  { icon: <IcoCalendar />, label: "Calendar", id: "calendar" },
  { icon: <IcoTeam />, label: "Team", id: "team" },
  { icon: <IcoAnalytics />, label: "Analytics", id: "analytics" },
];

function Sidebar({ active, onNavigate }: { active: string; onNavigate: (s: string) => void }) {
  return (
    <aside className="w-60 flex-shrink-0 bg-white border-r border-slate-200 flex flex-col h-full">
      <div className="flex items-center gap-2.5 px-5 h-16 border-b border-slate-200 flex-shrink-0">
        <div className="w-8 h-8 rounded-lg flex items-center justify-center text-white" style={{ background: PRIMARY }}><IcoTask /></div>
        <span className="font-bold text-[17px] text-slate-800" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>TaskFlow</span>
      </div>

      <nav className="flex-1 py-4 px-3 space-y-0.5">
        {navItems.map(item => (
          <button key={item.id} onClick={() => onNavigate(item.id)}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
              active === item.id
                ? "text-blue-700 bg-blue-50"
                : "text-slate-500 hover:text-slate-800 hover:bg-slate-50"
            }`}>
            <span className={active === item.id ? "text-blue-600" : "text-slate-400"}>{item.icon}</span>
            {item.label}
            {active === item.id && <span className="ml-auto w-1.5 h-5 rounded-full" style={{ background: PRIMARY }} />}
          </button>
        ))}
      </nav>

      <div className="px-4 py-4 border-t border-slate-200 space-y-3">
        <div className="rounded-xl p-3.5" style={{ background: "#eff6ff" }}>
          <p className="text-xs font-semibold text-blue-800 mb-1">Sprint 12 Progress</p>
          <div className="h-1.5 bg-blue-100 rounded-full overflow-hidden mb-1.5">
            <div className="h-full rounded-full" style={{ width: "68%", background: PRIMARY }} />
          </div>
          <p className="text-xs text-blue-600">68% · 4 days left</p>
        </div>
        <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-500 hover:text-slate-800 hover:bg-slate-50 transition-all">
          <span className="text-slate-400"><IcoSettings /></span>Settings
        </button>
      </div>
    </aside>
  );
}

// ─── Top Nav ───────────────────────────────────────────────────────────────

function TopNav({ title, onNavigate }: { title: string; onNavigate?: (s: string) => void }) {
  const [profileOpen, setProfileOpen] = useState(false);

  return (
    <header className="h-16 flex-shrink-0 bg-white border-b border-slate-200 flex items-center px-6 gap-4 relative z-40">
      <div className="flex-1">
        <h2 className="text-lg font-bold text-slate-800" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>{title}</h2>
      </div>
      <div className="flex items-center gap-2 px-3 h-9 rounded-lg border border-slate-200 bg-slate-50 w-56">
        <IcoSearch />
        <input placeholder="Search tasks…" className="bg-transparent text-sm text-slate-700 placeholder:text-slate-400 outline-none flex-1" />
      </div>
      <button className="relative w-9 h-9 rounded-lg border border-slate-200 flex items-center justify-center text-slate-500 hover:bg-slate-50 transition-colors">
        <IcoBell />
        <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-red-500 border-2 border-white" />
      </button>

      {/* Profile button + dropdown */}
      <div className="relative pl-2 border-l border-slate-200">
        <button
          onClick={() => setProfileOpen(o => !o)}
          className="flex items-center gap-2.5 px-2 py-1.5 rounded-xl hover:bg-slate-50 transition-colors"
        >
          <Avatar initials="JW" color="#2563eb" size={34} />
          <div className="text-left">
            <p className="text-sm font-semibold text-slate-800 leading-none">James Wu</p>
            <p className="text-xs text-slate-400 mt-0.5">Product Lead</p>
          </div>
          <span className="text-slate-400 ml-1"><IcoDown /></span>
        </button>

        {profileOpen && (
          <>
            {/* Backdrop */}
            <div className="fixed inset-0 z-40" onClick={() => setProfileOpen(false)} />
            {/* Dropdown */}
            <div className="absolute right-0 top-full mt-2 w-64 bg-white border border-slate-200 rounded-2xl shadow-xl shadow-slate-200/60 z-50 overflow-hidden">
              {/* User card */}
              <div className="px-4 py-4 border-b border-slate-100 flex items-center gap-3"
                style={{ background: "linear-gradient(135deg,#eff6ff,#f5f3ff)" }}>
                <Avatar initials="JW" color="#2563eb" size={40} />
                <div>
                  <p className="text-sm font-bold text-slate-900">James Wu</p>
                  <p className="text-xs text-slate-500">james.wu@taskflow.io</p>
                  <span className="inline-flex items-center gap-1 mt-1 text-[10px] font-semibold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-full">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" /> Online
                  </span>
                </div>
              </div>
              {/* Menu items */}
              <div className="py-1.5">
                {[
                  { label: "Open Profile", icon: <IcoPerson />, action: "profile", highlight: true },
                  { label: "Account Settings", icon: <IcoSettings />, action: "settings" },
                  { label: "Keyboard Shortcuts", icon: <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20 5H4c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm-9 3h2v2h-2V8zm0 3h2v2h-2v-2zM8 8h2v2H8V8zm0 3h2v2H8v-2zm-1 5H5v-2h2v2zm10 0H9v-2h8v2zm0-3h-2v-2h2v2zm0-3h-2V8h2v2zm2 6h-2v-2h2v2z"/></svg>, action: null },
                ].map(item => (
                  <button key={item.label}
                    onClick={() => { if (item.action) { onNavigate?.(item.action); setProfileOpen(false); } }}
                    className={`w-full flex items-center gap-3 px-4 py-2.5 text-sm transition-colors text-left ${
                      item.highlight
                        ? "text-blue-700 font-semibold hover:bg-blue-50"
                        : "text-slate-600 font-medium hover:bg-slate-50"
                    }`}>
                    <span className={item.highlight ? "text-blue-500" : "text-slate-400"}>{item.icon}</span>
                    {item.label}
                    {item.highlight && <span className="ml-auto"><IcoChevron /></span>}
                  </button>
                ))}
              </div>
              <div className="border-t border-slate-100 py-1.5">
                <button className="w-full flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-red-500 hover:bg-red-50 transition-colors">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5-5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/></svg>
                  Sign out
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </header>
  );
}

// ─── Mini spark chart (pure CSS bars) ─────────────────────────────────────

function SparkBars({ data, color }: { data: number[]; color: string }) {
  const max = Math.max(...data);
  return (
    <div className="flex items-end gap-0.5 h-8">
      {data.map((v, i) => (
        <div key={i} className="flex-1 rounded-sm transition-all" style={{ height: `${(v / max) * 100}%`, background: color, opacity: 0.7 + (i / data.length) * 0.3 }} />
      ))}
    </div>
  );
}

// ─── Dashboard ────────────────────────────────────────────────────────────

const activityData = [
  { user: "KL", name: "Kiran Lal", color: "#8b5cf6", action: "Completed", task: "Design system audit", time: "2m ago" },
  { user: "MR", name: "Maya Reed", color: "#10b981", action: "Commented on", task: "API integration", time: "18m ago" },
  { user: "ST", name: "Sam Torres", color: "#f97316", action: "Created", task: "Q4 planning doc", time: "1h ago" },
  { user: "JW", name: "James Wu", color: "#2563eb", action: "Moved to review", task: "User research report", time: "3h ago" },
  { user: "AL", name: "Ava Lin", color: "#ec4899", action: "Assigned to you", task: "Dashboard redesign", time: "5h ago" },
];

const deadlines = [
  { title: "API integration review", due: "Today", priority: "high" as const, assignees: ["MR","KL"] },
  { title: "Stakeholder presentation", due: "Tomorrow", priority: "high" as const, assignees: ["JW"] },
  { title: "Sprint retrospective", due: "Jun 28", priority: "medium" as const, assignees: ["ST","MR","AL"] },
  { title: "Competitor analysis", due: "Jul 2", priority: "low" as const, assignees: ["AL"] },
];

const chartWeeks = ["W1","W2","W3","W4","W5","W6","W7"];
const chartCompleted = [12,19,14,22,18,26,21];
const chartCreated = [15,22,18,25,20,28,24];

function DashboardScreen() {
  return (
    <div className="flex-1 overflow-auto" style={{ background: "#f8fafc" }}>
      <div className="p-7 space-y-6">

        {/* Stat cards */}
        <div className="grid grid-cols-4 gap-5">
          {[
            { label: "Total Tasks", value: "142", delta: "+12", good: true, sub: "vs last sprint", color: PRIMARY, spark: [8,12,10,15,13,18,14] },
            { label: "Completed", value: "96", delta: "+8", good: true, sub: "this sprint", color: "#10b981", spark: [5,9,7,11,9,14,10] },
            { label: "Pending", value: "32", delta: "-3", good: true, sub: "vs last sprint", color: "#f59e0b", spark: [14,12,15,10,13,9,11] },
            { label: "Overdue", value: "14", delta: "+2", good: false, sub: "need attention", color: "#ef4444", spark: [3,5,4,6,5,8,7] },
          ].map(s => (
            <Card key={s.label} className="p-5">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{s.label}</p>
                  <p className="text-3xl font-bold text-slate-800 mt-1" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>{s.value}</p>
                </div>
                <span className={`flex items-center gap-0.5 text-xs font-semibold px-2 py-0.5 rounded-full ${s.good ? "bg-emerald-50 text-emerald-600" : "bg-red-50 text-red-600"}`}>
                  <IcoTrend />{s.delta}
                </span>
              </div>
              <SparkBars data={s.spark} color={s.color} />
              <p className="text-xs text-slate-400 mt-2">{s.sub}</p>
            </Card>
          ))}
        </div>

        <div className="grid grid-cols-3 gap-5">
          {/* Chart */}
          <Card className="col-span-2 p-5">
            <div className="flex items-center justify-between mb-5">
              <div>
                <h3 className="font-semibold text-slate-800" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>Productivity Overview</h3>
                <p className="text-xs text-slate-400 mt-0.5">Tasks created vs completed · Last 7 weeks</p>
              </div>
              <div className="flex items-center gap-4 text-xs">
                <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full inline-block" style={{ background: PRIMARY }}/> Created</span>
                <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full inline-block bg-emerald-400"/>  Completed</span>
              </div>
            </div>
            {/* Chart */}
            <div className="flex items-end gap-2 h-36">
              {chartWeeks.map((w, i) => (
                <div key={w} className="flex-1 flex flex-col items-center gap-1">
                  <div className="w-full flex items-end gap-0.5 justify-center" style={{ height: 112 }}>
                    <div className="flex-1 rounded-t-sm transition-all" style={{ height: `${(chartCreated[i]/30)*100}%`, background: `${PRIMARY}30` }} />
                    <div className="flex-1 rounded-t-sm transition-all" style={{ height: `${(chartCompleted[i]/30)*100}%`, background: PRIMARY }} />
                  </div>
                  <span className="text-[10px] text-slate-400">{w}</span>
                </div>
              ))}
            </div>
          </Card>

          {/* Quick actions */}
          <Card className="p-5">
            <h3 className="font-semibold text-slate-800 mb-4" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>Quick Actions</h3>
            <div className="space-y-2">
              {[
                { label: "Create new task", color: PRIMARY, bg: "#eff6ff" },
                { label: "Schedule meeting", color: "#8b5cf6", bg: "#f5f3ff" },
                { label: "Invite teammate", color: "#10b981", bg: "#f0fdf4" },
                { label: "Generate report", color: "#f59e0b", bg: "#fffbeb" },
                { label: "View calendar", color: "#ec4899", bg: "#fdf2f8" },
              ].map(a => (
                <button key={a.label} className="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all hover:scale-[1.02]"
                  style={{ color: a.color, background: a.bg }}>
                  <IcoPlus />
                  {a.label}
                </button>
              ))}
            </div>
          </Card>
        </div>

        <div className="grid grid-cols-2 gap-5">
          {/* Recent activity */}
          <Card className="p-5">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold text-slate-800" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>Recent Activity</h3>
              <button className="text-xs text-blue-600 font-medium hover:underline">View all</button>
            </div>
            <div className="space-y-3">
              {activityData.map((a, i) => (
                <div key={i} className="flex items-start gap-3">
                  <Avatar initials={a.user} color={a.color} size={32} />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-slate-700 leading-snug">
                      <span className="font-semibold">{a.name}</span>{" "}{a.action}{" "}
                      <span className="font-medium text-blue-600">"{a.task}"</span>
                    </p>
                    <p className="text-xs text-slate-400 mt-0.5">{a.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* Upcoming deadlines */}
          <Card className="p-5">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold text-slate-800" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>Upcoming Deadlines</h3>
              <button className="text-xs text-blue-600 font-medium hover:underline">View all</button>
            </div>
            <div className="space-y-2.5">
              {deadlines.map((d, i) => (
                <div key={i} className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-50 transition-colors">
                  <div className={`w-1.5 h-10 rounded-full flex-shrink-0 ${d.priority === "high" ? "bg-red-400" : d.priority === "medium" ? "bg-amber-400" : "bg-slate-300"}`} />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-slate-700 truncate">{d.title}</p>
                    <p className={`text-xs mt-0.5 font-medium ${d.due === "Today" ? "text-red-500" : d.due === "Tomorrow" ? "text-amber-600" : "text-slate-400"}`}>{d.due}</p>
                  </div>
                  <div className="flex -space-x-1.5">
                    {d.assignees.map((a, j) => (
                      <Avatar key={j} initials={a} color={["#8b5cf6","#10b981","#f97316","#2563eb","#ec4899"][j]} size={24} />
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

// ─── Task List Screen ──────────────────────────────────────────────────────

type Task = {
  id: number; title: string; status: "todo"|"inprogress"|"review"|"done";
  priority: "high"|"medium"|"low"; due: string; project: string;
  assignees: { initials: string; color: string }[];
};

const allTasks: Task[] = [
  { id: 1, title: "Design system component audit", status: "done", priority: "high", due: "Jun 20", project: "Platform", assignees: [{ initials: "KL", color: "#8b5cf6" }, { initials: "MR", color: "#10b981" }] },
  { id: 2, title: "API integration for notifications", status: "inprogress", priority: "high", due: "Jun 25", project: "Backend", assignees: [{ initials: "ST", color: "#f97316" }] },
  { id: 3, title: "User research synthesis report", status: "review", priority: "medium", due: "Jun 28", project: "Research", assignees: [{ initials: "AL", color: "#ec4899" }, { initials: "JW", color: "#2563eb" }] },
  { id: 4, title: "Onboarding email sequence", status: "todo", priority: "medium", due: "Jul 1", project: "Marketing", assignees: [{ initials: "MR", color: "#10b981" }] },
  { id: 5, title: "Mobile responsive breakpoints", status: "inprogress", priority: "high", due: "Jun 22", project: "Platform", assignees: [{ initials: "KL", color: "#8b5cf6" }] },
  { id: 6, title: "Q3 OKR documentation", status: "todo", priority: "low", due: "Jul 5", project: "Strategy", assignees: [{ initials: "JW", color: "#2563eb" }, { initials: "ST", color: "#f97316" }] },
  { id: 7, title: "Competitor analysis deck", status: "todo", priority: "medium", due: "Jul 3", project: "Research", assignees: [{ initials: "AL", color: "#ec4899" }] },
  { id: 8, title: "Accessibility audit pass", status: "review", priority: "high", due: "Jun 26", project: "Platform", assignees: [{ initials: "KL", color: "#8b5cf6" }, { initials: "MR", color: "#10b981" }, { initials: "ST", color: "#f97316" }] },
  { id: 9, title: "Payment gateway integration", status: "inprogress", priority: "high", due: "Jun 30", project: "Backend", assignees: [{ initials: "ST", color: "#f97316" }] },
  { id: 10, title: "Help center articles", status: "todo", priority: "low", due: "Jul 10", project: "Marketing", assignees: [{ initials: "MR", color: "#10b981" }] },
];

function TaskListScreen() {
  const [search, setSearch] = useState("");
  const [filterStatus, setFilterStatus] = useState<string>("all");
  const [filterPriority, setFilterPriority] = useState<string>("all");
  const [sortBy, setSortBy] = useState<"due"|"priority"|"status">("due");
  const [viewMode, setViewMode] = useState<"list"|"kanban">("list");
  const [page, setPage] = useState(1);
  const [selected, setSelected] = useState<number[]>([]);
  const perPage = 6;

  const filtered = allTasks.filter(t => {
    const matchSearch = t.title.toLowerCase().includes(search.toLowerCase()) || t.project.toLowerCase().includes(search.toLowerCase());
    const matchStatus = filterStatus === "all" || t.status === filterStatus;
    const matchPriority = filterPriority === "all" || t.priority === filterPriority;
    return matchSearch && matchStatus && matchPriority;
  });

  const sorted = [...filtered].sort((a, b) => {
    if (sortBy === "priority") { const o = { high:0, medium:1, low:2 }; return o[a.priority] - o[b.priority]; }
    if (sortBy === "status") { const o = { todo:0, inprogress:1, review:2, done:3 }; return o[a.status] - o[b.status]; }
    return a.due.localeCompare(b.due);
  });

  const totalPages = Math.ceil(sorted.length / perPage);
  const paged = sorted.slice((page - 1) * perPage, page * perPage);

  const toggleSelect = (id: number) => setSelected(s => s.includes(id) ? s.filter(x => x !== id) : [...s, id]);
  const allSelected = paged.every(t => selected.includes(t.id));

  const kanbanCols: Array<{ key: Task["status"]; label: string; color: string }> = [
    { key: "todo", label: "To Do", color: "#64748b" },
    { key: "inprogress", label: "In Progress", color: PRIMARY },
    { key: "review", label: "In Review", color: "#8b5cf6" },
    { key: "done", label: "Done", color: "#10b981" },
  ];

  return (
    <div className="flex-1 overflow-auto" style={{ background: "#f8fafc" }}>
      <div className="p-7 space-y-5">

        {/* Toolbar */}
        <div className="flex items-center gap-3 flex-wrap">
          <div className="flex items-center gap-2 px-3 h-9 rounded-lg border border-slate-200 bg-white flex-1 min-w-48 max-w-xs">
            <IcoSearch />
            <input placeholder="Search tasks or projects…" value={search} onChange={e => { setSearch(e.target.value); setPage(1); }}
              className="bg-transparent text-sm text-slate-700 placeholder:text-slate-400 outline-none flex-1" />
          </div>

          <div className="flex items-center gap-2 ml-auto">
            <div className="flex items-center gap-1.5 px-3 h-9 rounded-lg border border-slate-200 bg-white text-sm text-slate-600">
              <IcoFilter />
              <select value={filterStatus} onChange={e => { setFilterStatus(e.target.value); setPage(1); }}
                className="bg-transparent outline-none text-sm cursor-pointer pr-1">
                <option value="all">All Status</option>
                <option value="todo">To Do</option>
                <option value="inprogress">In Progress</option>
                <option value="review">In Review</option>
                <option value="done">Done</option>
              </select>
            </div>

            <div className="flex items-center gap-1.5 px-3 h-9 rounded-lg border border-slate-200 bg-white text-sm text-slate-600">
              <IcoFilter />
              <select value={filterPriority} onChange={e => { setFilterPriority(e.target.value); setPage(1); }}
                className="bg-transparent outline-none text-sm cursor-pointer pr-1">
                <option value="all">All Priority</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>

            <div className="flex items-center gap-1.5 px-3 h-9 rounded-lg border border-slate-200 bg-white text-sm text-slate-600">
              <IcoSort />
              <select value={sortBy} onChange={e => setSortBy(e.target.value as "due"|"priority"|"status")}
                className="bg-transparent outline-none text-sm cursor-pointer pr-1">
                <option value="due">Sort: Due Date</option>
                <option value="priority">Sort: Priority</option>
                <option value="status">Sort: Status</option>
              </select>
            </div>

            <div className="flex items-center bg-white border border-slate-200 rounded-lg overflow-hidden">
              {([["list","List"],["kanban","Kanban"]] as const).map(([v, l]) => (
                <button key={v} onClick={() => setViewMode(v)}
                  className={`flex items-center gap-1.5 px-3 h-9 text-sm font-medium transition-colors ${viewMode === v ? "text-white" : "text-slate-500 hover:text-slate-700"}`}
                  style={viewMode === v ? { background: PRIMARY } : {}}>
                  {v === "list" ? <IcoRows /> : <IcoGrid />} {l}
                </button>
              ))}
            </div>

            <button className="flex items-center gap-2 h-9 px-4 rounded-lg text-white text-sm font-semibold hover:opacity-90 transition-opacity"
              style={{ background: PRIMARY }}>
              <IcoPlus /> New Task
            </button>
          </div>
        </div>

        {/* Summary chips */}
        <div className="flex items-center gap-2">
          <span className="text-sm text-slate-500">{filtered.length} tasks</span>
          {selected.length > 0 && (
            <span className="text-xs font-medium px-2.5 py-1 rounded-full bg-blue-50 text-blue-700">{selected.length} selected</span>
          )}
          {filterStatus !== "all" && <span className="text-xs font-medium px-2.5 py-1 rounded-full bg-slate-100 text-slate-600 flex items-center gap-1">{statusLabel[filterStatus]} <button onClick={() => setFilterStatus("all")} className="ml-1 hover:text-slate-800">×</button></span>}
          {filterPriority !== "all" && <span className="text-xs font-medium px-2.5 py-1 rounded-full bg-slate-100 text-slate-600 flex items-center gap-1">{filterPriority} priority <button onClick={() => setFilterPriority("all")} className="ml-1 hover:text-slate-800">×</button></span>}
        </div>

        {/* Kanban view */}
        {viewMode === "kanban" ? (
          <div className="grid grid-cols-4 gap-4">
            {kanbanCols.map(col => {
              const colTasks = filtered.filter(t => t.status === col.key);
              return (
                <div key={col.key} className="flex flex-col gap-3">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full" style={{ background: col.color }} />
                    <span className="text-sm font-semibold text-slate-700">{col.label}</span>
                    <span className="ml-auto text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-500">{colTasks.length}</span>
                  </div>
                  <div className="space-y-2.5">
                    {colTasks.map(t => (
                      <div key={t.id} className="bg-white rounded-xl border border-slate-200 p-3.5 shadow-sm hover:shadow-md transition-shadow cursor-pointer">
                        <div className="flex items-start justify-between gap-2 mb-2">
                          <p className="text-sm font-medium text-slate-800 leading-snug">{t.title}</p>
                          <button className="text-slate-400 hover:text-slate-600 flex-shrink-0"><IcoMoreV /></button>
                        </div>
                        <div className="flex items-center gap-1.5 mb-3">
                          <Badge label={t.priority} variant={t.priority} />
                          <span className="text-xs text-slate-400 ml-auto">{t.project}</span>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-xs text-slate-400">{t.due}</span>
                          <div className="flex -space-x-1.5">
                            {t.assignees.map((a, j) => <Avatar key={j} initials={a.initials} color={a.color} size={22} />)}
                          </div>
                        </div>
                      </div>
                    ))}
                    <button className="w-full py-2 rounded-xl border-2 border-dashed border-slate-200 text-xs text-slate-400 hover:border-blue-300 hover:text-blue-500 transition-colors">
                      + Add task
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          /* List / Table view */
          <Card>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-100">
                    <th className="text-left px-5 py-3.5 w-10">
                      <div onClick={() => selected.length > 0 ? setSelected([]) : setSelected(paged.map(t => t.id))}
                        className={`w-4 h-4 rounded-[4px] border flex items-center justify-center cursor-pointer transition-all ${allSelected ? "text-white border-blue-600" : "border-slate-300"}`}
                        style={allSelected ? { background: PRIMARY } : {}}>
                        {allSelected && <IcoCheck />}
                      </div>
                    </th>
                    <th className="text-left px-4 py-3.5 text-xs font-semibold text-slate-400 uppercase tracking-wider">Task</th>
                    <th className="text-left px-4 py-3.5 text-xs font-semibold text-slate-400 uppercase tracking-wider">Project</th>
                    <th className="text-left px-4 py-3.5 text-xs font-semibold text-slate-400 uppercase tracking-wider">Status</th>
                    <th className="text-left px-4 py-3.5 text-xs font-semibold text-slate-400 uppercase tracking-wider">Priority</th>
                    <th className="text-left px-4 py-3.5 text-xs font-semibold text-slate-400 uppercase tracking-wider">Due Date</th>
                    <th className="text-left px-4 py-3.5 text-xs font-semibold text-slate-400 uppercase tracking-wider">Assignees</th>
                    <th className="px-4 py-3.5 w-10" />
                  </tr>
                </thead>
                <tbody>
                  {paged.map((t, i) => (
                    <tr key={t.id} className={`border-b border-slate-50 hover:bg-slate-50/70 transition-colors ${selected.includes(t.id) ? "bg-blue-50/40" : ""} ${i === paged.length - 1 ? "border-0" : ""}`}>
                      <td className="px-5 py-3.5">
                        <div onClick={() => toggleSelect(t.id)}
                          className={`w-4 h-4 rounded-[4px] border flex items-center justify-center cursor-pointer transition-all ${selected.includes(t.id) ? "text-white border-blue-600" : "border-slate-300"}`}
                          style={selected.includes(t.id) ? { background: PRIMARY } : {}}>
                          {selected.includes(t.id) && <IcoCheck />}
                        </div>
                      </td>
                      <td className="px-4 py-3.5">
                        <p className={`text-sm font-medium text-slate-800 ${t.status === "done" ? "line-through text-slate-400" : ""}`}>{t.title}</p>
                      </td>
                      <td className="px-4 py-3.5">
                        <span className="text-sm text-slate-500">{t.project}</span>
                      </td>
                      <td className="px-4 py-3.5">
                        <Badge label={statusLabel[t.status]} variant={t.status} />
                      </td>
                      <td className="px-4 py-3.5">
                        <Badge label={t.priority.charAt(0).toUpperCase() + t.priority.slice(1)} variant={t.priority} />
                      </td>
                      <td className="px-4 py-3.5">
                        <span className={`text-sm font-medium ${t.due === "Jun 22" || t.due === "Jun 20" ? "text-red-500" : "text-slate-600"}`}>{t.due}</span>
                      </td>
                      <td className="px-4 py-3.5">
                        <div className="flex -space-x-1.5">
                          {t.assignees.map((a, j) => <Avatar key={j} initials={a.initials} color={a.color} size={26} />)}
                        </div>
                      </td>
                      <td className="px-4 py-3.5">
                        <button className="text-slate-400 hover:text-slate-600 transition-colors"><IcoMoreV /></button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            <div className="flex items-center justify-between px-5 py-3.5 border-t border-slate-100">
              <span className="text-sm text-slate-400">
                Showing {Math.min((page-1)*perPage+1, filtered.length)}–{Math.min(page*perPage, filtered.length)} of {filtered.length} tasks
              </span>
              <div className="flex items-center gap-1">
                <button onClick={() => setPage(p => Math.max(1, p-1))} disabled={page === 1}
                  className="w-8 h-8 flex items-center justify-center rounded-lg border border-slate-200 text-slate-500 hover:bg-slate-50 disabled:opacity-40 transition-all">
                  <IcoChevronLeft />
                </button>
                {Array.from({ length: totalPages }, (_, i) => i+1).map(p => (
                  <button key={p} onClick={() => setPage(p)}
                    className="w-8 h-8 flex items-center justify-center rounded-lg text-sm font-medium transition-all"
                    style={page === p ? { background: PRIMARY, color: "#fff" } : { color: "#64748b" }}>
                    {p}
                  </button>
                ))}
                <button onClick={() => setPage(p => Math.min(totalPages, p+1))} disabled={page === totalPages}
                  className="w-8 h-8 flex items-center justify-center rounded-lg border border-slate-200 text-slate-500 hover:bg-slate-50 disabled:opacity-40 transition-all">
                  <IcoChevron />
                </button>
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}

// ─── Extra icons for new screens ──────────────────────────────────────────

function IcoAttach() { return <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="m16.5 6-8.5 8.5c-1.38 1.38-1.38 3.62 0 5 1.38 1.38 3.62 1.38 5 0l9.5-9.5c2.34-2.34 2.34-6.16 0-8.5-2.34-2.34-6.16-2.34-8.5 0l-10 10c-3.31 3.31-3.31 8.69 0 12 3.31 3.31 8.69 3.31 12 0l8.5-8.5-1.41-1.41-8.5 8.5c-2.54 2.54-6.65 2.54-9.19 0-2.54-2.54-2.54-6.65 0-9.19l10-10c1.56-1.56 4.14-1.56 5.7 0 1.56 1.56 1.56 4.14 0 5.7l-9.5 9.5a1.53 1.53 0 0 1-2.12 0 1.53 1.53 0 0 1 0-2.12l8.5-8.5-1.41-1.41z"/></svg>; }
function IcoComment() { return <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/></svg>; }
function IcoEdit() { return <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04a1 1 0 0 0 0-1.41l-2.34-2.34a1 1 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>; }
function IcoTrash() { return <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg>; }
function IcoLink() { return <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/></svg>; }
function IcoX() { return <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.41 17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>; }
function IcoDown() { return <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M7 10l5 5 5-5z"/></svg>; }
function IcoUpload() { return <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M19.35 10.04A7.49 7.49 0 0 0 12 4C9.11 4 6.6 5.64 5.35 8.04A5.994 5.994 0 0 0 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM14 13v4h-4v-4H7l5-5 5 5h-3z"/></svg>; }
function IcoFlag() { return <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M14.4 6 14 4H5v17h2v-7h5.6l.4 2h7V6z"/></svg>; }
function IcoHistory() { return <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M13 3a9 9 0 0 0-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42A8.954 8.954 0 0 0 13 21a9 9 0 0 0 0-18zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z"/></svg>; }
function IcoSend() { return <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M2.01 21 23 12 2.01 3 2 10l15 2-15 2z"/></svg>; }
function IcoCopy() { return <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>; }
function IcoLabel() { return <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M17.63 5.84C17.27 5.33 16.67 5 16 5L5 5.01C3.9 5.01 3 5.9 3 7v10c0 1.1.9 1.99 2 1.99L16 19c.67 0 1.27-.33 1.63-.84L22 12l-4.37-6.16z"/></svg>; }
function IcoClock() { return <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z"/></svg>; }

// ─── Reusable form primitives (new screens) ───────────────────────────────

function FormLabel({ children, required }: { children: React.ReactNode; required?: boolean }) {
  return (
    <label className="text-sm font-semibold text-slate-700 flex items-center gap-1">
      {children}
      {required && <span className="text-red-500 text-xs">*</span>}
    </label>
  );
}

function FormSelect({
  value, onChange, options, placeholder, error, icon
}: {
  value: string; onChange: (v: string) => void;
  options: { value: string; label: string }[];
  placeholder?: string; error?: string; icon?: React.ReactNode;
}) {
  return (
    <div>
      <div className={`flex items-center gap-2.5 px-3.5 h-11 rounded-xl border bg-white transition-all cursor-pointer ${
        error ? "border-red-400 ring-1 ring-red-200" : "border-slate-200 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100"
      }`}>
        {icon && <span className="text-slate-400 flex-shrink-0">{icon}</span>}
        <select value={value} onChange={e => onChange(e.target.value)}
          className="flex-1 bg-transparent text-sm text-slate-700 outline-none cursor-pointer appearance-none">
          {placeholder && <option value="">{placeholder}</option>}
          {options.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
        </select>
        <span className="text-slate-400 flex-shrink-0 pointer-events-none"><IcoDown /></span>
      </div>
      {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
    </div>
  );
}

function FormTextarea({
  value, onChange, placeholder, rows = 4, error
}: {
  value: string; onChange: (v: string) => void; placeholder?: string; rows?: number; error?: string;
}) {
  return (
    <div>
      <textarea value={value} onChange={e => onChange(e.target.value)} placeholder={placeholder} rows={rows}
        className={`w-full px-3.5 py-3 rounded-xl border bg-white text-sm text-slate-700 placeholder:text-slate-400 outline-none resize-none transition-all ${
          error ? "border-red-400 ring-1 ring-red-200" : "border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
        }`} />
      {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
    </div>
  );
}

function FormSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="space-y-3">
      <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest">{title}</h3>
      {children}
    </div>
  );
}

// ─── Task Details Screen ───────────────────────────────────────────────────

const TASK_DETAIL = {
  id: 2,
  title: "API integration for notifications",
  status: "inprogress" as const,
  priority: "high" as const,
  project: "Backend",
  due: "Jun 25, 2026",
  created: "Jun 10, 2026",
  description: `Integrate the backend notification service with the new event-driven architecture. This includes setting up WebSocket connections for real-time push notifications, fallback to polling for clients that don't support WebSocket, and ensuring message delivery guarantees (at-least-once semantics).\n\nThe integration should handle:\n• User preference filtering (do-not-disturb, digest mode)\n• Rate limiting to prevent notification spam\n• Delivery receipts and read state tracking\n• Graceful degradation when the notification service is unavailable`,
  assignees: [
    { initials: "ST", color: "#f97316", name: "Sam Torres", role: "Backend Lead" },
    { initials: "KL", color: "#8b5cf6", name: "Kiran Lal", role: "Senior Engineer" },
  ],
  labels: ["backend", "notifications", "websocket", "sprint-12"],
  attachments: [
    { name: "notification-spec-v2.pdf", size: "248 KB", type: "pdf" },
    { name: "architecture-diagram.png", size: "1.2 MB", type: "img" },
    { name: "api-contract.json", size: "32 KB", type: "json" },
  ],
  comments: [
    {
      initials: "KL", color: "#8b5cf6", name: "Kiran Lal", time: "2 hours ago",
      text: "The WebSocket handshake is working in staging. Still ironing out the reconnection logic — edge case where the client reconnects mid-message batch causes duplicate delivery."
    },
    {
      initials: "MR", color: "#10b981", name: "Maya Reed", time: "5 hours ago",
      text: "Reviewed the API contract. One concern: the `deliveredAt` timestamp is in local time, should be UTC. Also, can we add a `batchId` field to group related notifications?"
    },
    {
      initials: "JW", color: "#2563eb", name: "James Wu", time: "1 day ago",
      text: "Flagging this as high priority — the mobile team needs this done before the Jul 1 release freeze. Let me know if you need to pull in extra resources, Sam."
    },
  ],
  activity: [
    { text: "Sam Torres changed status to In Progress", time: "Jun 18" },
    { text: "Kiran Lal was assigned to this task", time: "Jun 15" },
    { text: "James Wu updated the due date to Jun 25", time: "Jun 12" },
    { text: "Task created by James Wu", time: "Jun 10" },
  ],
};

const statusLabel: Record<string, string> = { todo: "To Do", inprogress: "In Progress", review: "In Review", done: "Done" };

function TaskDetailScreen({ onEdit }: { onEdit: () => void }) {
  const t = TASK_DETAIL;
  const [comment, setComment] = useState("");
  const [showDelete, setShowDelete] = useState(false);
  const [localComments, setLocalComments] = useState(t.comments);

  const handleComment = () => {
    if (!comment.trim()) return;
    setLocalComments(c => [{ initials: "JW", color: "#2563eb", name: "James Wu", time: "Just now", text: comment }, ...c]);
    setComment("");
  };

  const fileIcon: Record<string, string> = { pdf: "📄", img: "🖼️", json: "📋" };

  return (
    <div className="flex-1 overflow-auto" style={{ background: "#f8fafc" }}>
      <div className="max-w-5xl mx-auto px-8 py-7 space-y-6">

        {/* Breadcrumb + actions */}
        <div className="flex items-center justify-between">
          <nav className="flex items-center gap-1.5 text-sm">
            <button className="text-slate-400 hover:text-blue-600 transition-colors">Task List</button>
            <span className="text-slate-300"><IcoChevron /></span>
            <button className="text-slate-400 hover:text-blue-600 transition-colors">{t.project}</button>
            <span className="text-slate-300"><IcoChevron /></span>
            <span className="text-slate-700 font-medium truncate max-w-xs">{t.title}</span>
          </nav>
          <div className="flex items-center gap-2">
            <button className="flex items-center gap-1.5 px-3.5 h-9 rounded-xl border border-slate-200 bg-white text-sm font-medium text-slate-600 hover:bg-slate-50 transition-colors">
              <IcoCopy /> Copy link
            </button>
            <button onClick={onEdit}
              className="flex items-center gap-1.5 px-3.5 h-9 rounded-xl text-white text-sm font-semibold hover:opacity-90 transition-opacity"
              style={{ background: PRIMARY }}>
              <IcoEdit /> Edit Task
            </button>
            <button onClick={() => setShowDelete(true)}
              className="flex items-center gap-1.5 px-3 h-9 rounded-xl border border-red-200 bg-red-50 text-sm font-medium text-red-600 hover:bg-red-100 transition-colors">
              <IcoTrash /> Delete
            </button>
          </div>
        </div>

        {/* Delete confirm */}
        {showDelete && (
          <div className="rounded-xl border border-red-200 bg-red-50 px-5 py-4 flex items-center gap-4">
            <div className="flex-1">
              <p className="text-sm font-semibold text-red-700">Delete this task?</p>
              <p className="text-xs text-red-500 mt-0.5">This action cannot be undone. All comments and attachments will be permanently removed.</p>
            </div>
            <button onClick={() => setShowDelete(false)} className="px-3.5 h-8 rounded-lg bg-white border border-slate-200 text-sm text-slate-600 hover:bg-slate-50">Cancel</button>
            <button className="px-3.5 h-8 rounded-lg bg-red-600 text-white text-sm font-semibold hover:bg-red-700">Yes, delete</button>
          </div>
        )}

        <div className="grid grid-cols-3 gap-6">
          {/* Main content */}
          <div className="col-span-2 space-y-5">

            {/* Title + badges */}
            <Card className="p-6">
              <div className="flex items-start gap-3 mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2.5">
                    <Badge label={statusLabel[t.status]} variant={t.status} />
                    <Badge label={t.priority.charAt(0).toUpperCase() + t.priority.slice(1)} variant={t.priority} />
                    <span className="text-xs text-slate-400 ml-1">#{t.id}</span>
                  </div>
                  <h1 className="text-xl font-bold text-slate-900 leading-snug" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>
                    {t.title}
                  </h1>
                </div>
              </div>
              <div className="flex items-center gap-4 text-xs text-slate-400 border-t border-slate-100 pt-4">
                <span className="flex items-center gap-1"><IcoClock /> Created {t.created}</span>
                <span className="flex items-center gap-1"><IcoCalendar /> Due {t.due}</span>
                <span className="flex items-center gap-1"><IcoComment /> {localComments.length} comments</span>
                <span className="flex items-center gap-1"><IcoAttach /> {t.attachments.length} files</span>
              </div>
            </Card>

            {/* Description */}
            <Card className="p-6">
              <h2 className="text-sm font-bold text-slate-700 mb-3 flex items-center gap-2">
                <span className="w-5 h-5 rounded-md bg-blue-50 flex items-center justify-center text-blue-600"><IcoList /></span>
                Description
              </h2>
              <div className="text-sm text-slate-600 leading-relaxed whitespace-pre-line">{t.description}</div>
            </Card>

            {/* Attachments */}
            <Card className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-bold text-slate-700 flex items-center gap-2">
                  <span className="w-5 h-5 rounded-md bg-slate-100 flex items-center justify-center text-slate-500"><IcoAttach /></span>
                  Attachments
                </h2>
                <button className="text-xs text-blue-600 font-medium hover:underline flex items-center gap-1"><IcoPlus /> Add file</button>
              </div>
              <div className="space-y-2">
                {t.attachments.map(f => (
                  <div key={f.name} className="flex items-center gap-3 px-3.5 py-2.5 rounded-lg border border-slate-200 hover:border-blue-200 hover:bg-blue-50/30 transition-all group">
                    <span className="text-lg">{fileIcon[f.type]}</span>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-slate-700 truncate">{f.name}</p>
                      <p className="text-xs text-slate-400">{f.size}</p>
                    </div>
                    <button className="opacity-0 group-hover:opacity-100 flex items-center gap-1 text-xs text-blue-600 font-medium transition-opacity">
                      <IcoLink /> Open
                    </button>
                  </div>
                ))}
              </div>
            </Card>

            {/* Comments */}
            <Card className="p-6">
              <h2 className="text-sm font-bold text-slate-700 mb-5 flex items-center gap-2">
                <span className="w-5 h-5 rounded-md bg-violet-50 flex items-center justify-center text-violet-600"><IcoComment /></span>
                Comments
                <span className="ml-1 text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-500">{localComments.length}</span>
              </h2>

              {/* Comment composer */}
              <div className="flex items-start gap-3 mb-6 pb-6 border-b border-slate-100">
                <Avatar initials="JW" color="#2563eb" size={34} />
                <div className="flex-1">
                  <textarea value={comment} onChange={e => setComment(e.target.value)}
                    placeholder="Add a comment… (supports markdown)"
                    rows={3}
                    className="w-full px-3.5 py-3 rounded-xl border border-slate-200 bg-white text-sm text-slate-700 placeholder:text-slate-400 outline-none resize-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-all" />
                  <div className="flex items-center justify-between mt-2">
                    <div className="flex items-center gap-2">
                      <button className="text-xs text-slate-400 hover:text-slate-600 transition-colors flex items-center gap-1"><IcoAttach /> Attach</button>
                      <button className="text-xs text-slate-400 hover:text-slate-600 transition-colors flex items-center gap-1"><IcoLabel /> Mention</button>
                    </div>
                    <button onClick={handleComment} disabled={!comment.trim()}
                      className="flex items-center gap-1.5 px-4 h-8 rounded-lg text-white text-sm font-semibold hover:opacity-90 disabled:opacity-50 transition-all"
                      style={{ background: PRIMARY }}>
                      <IcoSend /> Post
                    </button>
                  </div>
                </div>
              </div>

              {/* Comment list */}
              <div className="space-y-5">
                {localComments.map((c, i) => (
                  <div key={i} className="flex items-start gap-3">
                    <Avatar initials={c.initials} color={c.color} size={34} />
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1.5">
                        <span className="text-sm font-semibold text-slate-800">{c.name}</span>
                        <span className="text-xs text-slate-400">{c.time}</span>
                      </div>
                      <div className="bg-slate-50 rounded-xl px-4 py-3 text-sm text-slate-700 leading-relaxed">{c.text}</div>
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            {/* Activity history */}
            <Card className="p-6">
              <h2 className="text-sm font-bold text-slate-700 mb-5 flex items-center gap-2">
                <span className="w-5 h-5 rounded-md bg-emerald-50 flex items-center justify-center text-emerald-600"><IcoHistory /></span>
                Activity History
              </h2>
              <div className="relative pl-4">
                <div className="absolute left-0 top-0 bottom-0 w-px bg-slate-100" />
                <div className="space-y-4">
                  {t.activity.map((a, i) => (
                    <div key={i} className="flex items-start gap-3 relative">
                      <div className="absolute -left-[17px] w-2.5 h-2.5 rounded-full border-2 border-white bg-slate-300 mt-1 flex-shrink-0" />
                      <div>
                        <p className="text-sm text-slate-600">{a.text}</p>
                        <p className="text-xs text-slate-400 mt-0.5">{a.time}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </Card>
          </div>

          {/* Sidebar meta */}
          <div className="space-y-4">
            <Card className="p-5 space-y-5">
              <FormSection title="Status">
                <FormSelect value={t.status} onChange={() => {}} options={[
                  { value: "todo", label: "To Do" },
                  { value: "inprogress", label: "In Progress" },
                  { value: "review", label: "In Review" },
                  { value: "done", label: "Done" },
                ]} />
              </FormSection>

              <div className="h-px bg-slate-100" />

              <FormSection title="Priority">
                <FormSelect value={t.priority} onChange={() => {}} options={[
                  { value: "high", label: "🔴 High" },
                  { value: "medium", label: "🟡 Medium" },
                  { value: "low", label: "🟢 Low" },
                ]} icon={<IcoFlag />} />
              </FormSection>

              <div className="h-px bg-slate-100" />

              <FormSection title="Assignees">
                <div className="space-y-2">
                  {t.assignees.map(a => (
                    <div key={a.initials} className="flex items-center gap-2.5 px-3 py-2 rounded-lg bg-slate-50 border border-slate-100">
                      <Avatar initials={a.initials} color={a.color} size={28} />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-slate-800 truncate">{a.name}</p>
                        <p className="text-xs text-slate-400">{a.role}</p>
                      </div>
                    </div>
                  ))}
                  <button className="w-full flex items-center gap-2 px-3 py-2 rounded-lg border border-dashed border-slate-200 text-xs text-slate-400 hover:border-blue-300 hover:text-blue-500 transition-colors">
                    <IcoPlus /> Add assignee
                  </button>
                </div>
              </FormSection>

              <div className="h-px bg-slate-100" />

              <FormSection title="Due Date">
                <div className="flex items-center gap-2.5 px-3.5 h-10 rounded-xl border border-slate-200 bg-white text-sm text-slate-700">
                  <span className="text-slate-400"><IcoCalendar /></span>
                  {t.due}
                </div>
              </FormSection>

              <div className="h-px bg-slate-100" />

              <FormSection title="Project">
                <div className="flex items-center gap-2 px-3.5 h-10 rounded-xl border border-slate-200 bg-white text-sm text-slate-700">
                  <span className="w-2 h-2 rounded-full bg-blue-500" />
                  {t.project}
                </div>
              </FormSection>

              <div className="h-px bg-slate-100" />

              <FormSection title="Labels">
                <div className="flex flex-wrap gap-1.5">
                  {t.labels.map(l => (
                    <span key={l} className="flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-600 hover:bg-slate-200 transition-colors cursor-pointer">
                      <IcoLabel />{l}
                    </span>
                  ))}
                  <button className="flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium border border-dashed border-slate-200 text-slate-400 hover:border-blue-300 hover:text-blue-500 transition-colors">
                    <IcoPlus /> Add
                  </button>
                </div>
              </FormSection>
            </Card>

            {/* Related tasks */}
            <Card className="p-5">
              <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">Related Tasks</h3>
              <div className="space-y-2">
                {[
                  { title: "Design notification UI", status: "done" as const },
                  { title: "Write notification tests", status: "todo" as const },
                ].map(r => (
                  <div key={r.title} className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-slate-50 transition-colors cursor-pointer group">
                    <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: r.status === "done" ? "#10b981" : "#94a3b8" }} />
                    <p className="text-sm text-slate-600 flex-1 group-hover:text-blue-600 transition-colors">{r.title}</p>
                    <IcoChevron />
                  </div>
                ))}
                <button className="w-full flex items-center gap-2 px-3 py-2 rounded-lg border border-dashed border-slate-200 text-xs text-slate-400 hover:border-blue-300 hover:text-blue-500 transition-colors">
                  <IcoLink /> Link a task
                </button>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Create / Edit Task Screen ────────────────────────────────────────────

const TEAM = [
  { initials: "KL", color: "#8b5cf6", name: "Kiran Lal", role: "Backend Lead" },
  { initials: "MR", color: "#10b981", name: "Maya Reed", role: "Designer" },
  { initials: "ST", color: "#f97316", name: "Sam Torres", role: "Engineer" },
  { initials: "JW", color: "#2563eb", name: "James Wu", role: "Product Lead" },
  { initials: "AL", color: "#ec4899", name: "Ava Lin", role: "Researcher" },
];

const ALL_LABELS = ["backend","frontend","design","research","marketing","websocket","api","sprint-12","bug","feature","docs"];

function CreateTaskScreen({ onCancel, editMode = false }: { onCancel: () => void; editMode?: boolean }) {
  const [title, setTitle] = useState(editMode ? "API integration for notifications" : "");
  const [desc, setDesc] = useState(editMode ? "Integrate the backend notification service with the new event-driven architecture." : "");
  const [status, setStatus] = useState(editMode ? "inprogress" : "todo");
  const [priority, setPriority] = useState(editMode ? "high" : "medium");
  const [assignees, setAssignees] = useState<string[]>(editMode ? ["ST", "KL"] : []);
  const [dueDate, setDueDate] = useState(editMode ? "2026-06-25" : "");
  const [project, setProject] = useState(editMode ? "Backend" : "");
  const [labels, setLabels] = useState<string[]>(editMode ? ["backend","notifications","websocket"] : []);
  const [labelInput, setLabelInput] = useState("");
  const [showLabelDropdown, setShowLabelDropdown] = useState(false);
  const [attachments, setAttachments] = useState<string[]>(editMode ? ["notification-spec-v2.pdf", "architecture-diagram.png"] : []);
  const [saved, setSaved] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const toggleAssignee = (initials: string) =>
    setAssignees(a => a.includes(initials) ? a.filter(x => x !== initials) : [...a, initials]);
  const toggleLabel = (l: string) =>
    setLabels(ls => ls.includes(l) ? ls.filter(x => x !== l) : [...ls, l]);
  const addCustomLabel = () => {
    if (labelInput.trim() && !labels.includes(labelInput.trim())) {
      setLabels(ls => [...ls, labelInput.trim()]);
      setLabelInput("");
    }
  };

  const validate = () => {
    const e: Record<string, string> = {};
    if (!title.trim()) e.title = "Task title is required";
    if (!status) e.status = "Please select a status";
    if (!priority) e.priority = "Please select a priority";
    if (assignees.length === 0) e.assignees = "Assign at least one team member";
    if (!dueDate) e.due = "Due date is required";
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const handleSave = () => {
    if (!validate()) return;
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  const statusOpts = [
    { value: "todo", label: "📋 To Do" },
    { value: "inprogress", label: "🔵 In Progress" },
    { value: "review", label: "🟣 In Review" },
    { value: "done", label: "✅ Done" },
  ];
  const priorityOpts = [
    { value: "high", label: "🔴 High" },
    { value: "medium", label: "🟡 Medium" },
    { value: "low", label: "🟢 Low" },
  ];
  const projectOpts = [
    { value: "Platform", label: "Platform" },
    { value: "Backend", label: "Backend" },
    { value: "Research", label: "Research" },
    { value: "Marketing", label: "Marketing" },
    { value: "Strategy", label: "Strategy" },
  ];

  return (
    <div className="flex-1 overflow-auto" style={{ background: "#f8fafc" }}>
      <div className="max-w-4xl mx-auto px-8 py-7 space-y-6">

        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <nav className="flex items-center gap-1.5 text-sm mb-1">
              <button className="text-slate-400 hover:text-blue-600 transition-colors">Task List</button>
              <span className="text-slate-300"><IcoChevron /></span>
              <span className="text-slate-700 font-medium">{editMode ? "Edit Task" : "New Task"}</span>
            </nav>
            <h1 className="text-xl font-bold text-slate-900" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>
              {editMode ? "Edit Task" : "Create New Task"}
            </h1>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={onCancel}
              className="px-4 h-10 rounded-xl border border-slate-200 bg-white text-sm font-medium text-slate-600 hover:bg-slate-50 transition-colors">
              Cancel
            </button>
            <button onClick={handleSave}
              className={`flex items-center gap-2 px-5 h-10 rounded-xl text-white text-sm font-semibold transition-all ${saved ? "bg-emerald-500" : "hover:opacity-90"}`}
              style={saved ? {} : { background: PRIMARY }}>
              {saved ? <><IcoCheck /> Saved!</> : <>{editMode ? "Save Changes" : "Create Task"}</>}
            </button>
          </div>
        </div>

        {/* Validation summary */}
        {Object.keys(errors).length > 0 && (
          <div className="rounded-xl border border-red-200 bg-red-50 px-5 py-3.5 flex items-center gap-3">
            <span className="text-red-500 text-lg">⚠</span>
            <p className="text-sm text-red-700 font-medium">Please fix {Object.keys(errors).length} error{Object.keys(errors).length > 1 ? "s" : ""} before saving.</p>
          </div>
        )}

        <div className="grid grid-cols-3 gap-6">
          {/* Main form */}
          <div className="col-span-2 space-y-5">

            {/* Title */}
            <Card className="p-6">
              <FormSection title="Task Details">
                <div className="space-y-1.5">
                  <FormLabel required>Title</FormLabel>
                  <div className={`flex items-center px-3.5 h-12 rounded-xl border bg-white transition-all ${
                    errors.title ? "border-red-400 ring-1 ring-red-200" : "border-slate-200 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100"
                  }`}>
                    <input value={title} onChange={e => { setTitle(e.target.value); setErrors(er => ({ ...er, title: "" })); }}
                      placeholder="e.g. Implement OAuth2 token refresh"
                      className="flex-1 bg-transparent text-base font-medium text-slate-800 placeholder:text-slate-300 placeholder:font-normal outline-none" />
                    <span className="text-xs text-slate-300 flex-shrink-0">{title.length}/200</span>
                  </div>
                  {errors.title && <p className="text-xs text-red-500">{errors.title}</p>}
                </div>

                <div className="space-y-1.5 mt-4">
                  <FormLabel>Description</FormLabel>
                  <FormTextarea value={desc} onChange={setDesc} rows={5}
                    placeholder="Describe what needs to be done, acceptance criteria, edge cases…" />
                  <p className="text-xs text-slate-400">Supports markdown — **bold**, _italic_, `code`, - lists</p>
                </div>
              </FormSection>
            </Card>

            {/* Status & Priority */}
            <Card className="p-6">
              <FormSection title="Classification">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <FormLabel required>Status</FormLabel>
                    <FormSelect value={status} onChange={v => { setStatus(v); setErrors(er => ({ ...er, status: "" })); }}
                      options={statusOpts} error={errors.status} />
                  </div>
                  <div className="space-y-1.5">
                    <FormLabel required>Priority</FormLabel>
                    <FormSelect value={priority} onChange={v => { setPriority(v); setErrors(er => ({ ...er, priority: "" })); }}
                      options={priorityOpts} icon={<IcoFlag />} error={errors.priority} />
                  </div>
                </div>
                <div className="space-y-1.5 mt-4">
                  <FormLabel>Project</FormLabel>
                  <FormSelect value={project} onChange={setProject} placeholder="Select project…"
                    options={projectOpts} />
                </div>
              </FormSection>
            </Card>

            {/* Labels */}
            <Card className="p-6">
              <FormSection title="Labels">
                <div>
                  <div className="flex flex-wrap gap-1.5 mb-3">
                    {labels.map(l => (
                      <span key={l} className="flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100">
                        <IcoLabel />{l}
                        <button onClick={() => toggleLabel(l)} className="ml-0.5 hover:text-red-500 transition-colors"><IcoX /></button>
                      </span>
                    ))}
                    {labels.length === 0 && <span className="text-xs text-slate-400">No labels added yet</span>}
                  </div>

                  {/* Label suggestions */}
                  <div className="relative">
                    <div className="flex items-center gap-2">
                      <div className="flex items-center gap-2 px-3 h-9 rounded-lg border border-slate-200 bg-white flex-1 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100 transition-all">
                        <IcoSearch />
                        <input value={labelInput} onChange={e => { setLabelInput(e.target.value); setShowLabelDropdown(true); }}
                          onFocus={() => setShowLabelDropdown(true)}
                          onBlur={() => setTimeout(() => setShowLabelDropdown(false), 150)}
                          placeholder="Search or create label…"
                          className="flex-1 bg-transparent text-sm text-slate-700 placeholder:text-slate-400 outline-none" />
                      </div>
                      <button onClick={addCustomLabel} disabled={!labelInput.trim()}
                        className="h-9 px-3.5 rounded-lg border border-slate-200 bg-white text-sm font-medium text-slate-600 hover:bg-slate-50 disabled:opacity-40 transition-all">
                        Add
                      </button>
                    </div>

                    {showLabelDropdown && (
                      <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-200 rounded-xl shadow-lg z-10 p-2">
                        <div className="flex flex-wrap gap-1.5">
                          {ALL_LABELS.filter(l => l.includes(labelInput) && !labels.includes(l)).map(l => (
                            <button key={l} onMouseDown={() => toggleLabel(l)}
                              className="px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-600 hover:bg-blue-50 hover:text-blue-700 transition-colors">
                              {l}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </FormSection>
            </Card>

            {/* Attachments */}
            <Card className="p-6">
              <FormSection title="Attachments">
                {attachments.length > 0 && (
                  <div className="space-y-2 mb-3">
                    {attachments.map(f => (
                      <div key={f} className="flex items-center gap-3 px-3.5 py-2.5 rounded-lg border border-slate-200 bg-slate-50 group">
                        <span className="text-base">📄</span>
                        <p className="text-sm text-slate-600 flex-1 truncate">{f}</p>
                        <button onClick={() => setAttachments(a => a.filter(x => x !== f))}
                          className="opacity-0 group-hover:opacity-100 text-slate-400 hover:text-red-500 transition-all"><IcoX /></button>
                      </div>
                    ))}
                  </div>
                )}
                <div className="border-2 border-dashed border-slate-200 rounded-xl p-6 flex flex-col items-center gap-2 hover:border-blue-300 hover:bg-blue-50/20 transition-all cursor-pointer group">
                  <span className="text-slate-300 group-hover:text-blue-400 transition-colors"><IcoUpload /></span>
                  <p className="text-sm font-medium text-slate-500 group-hover:text-blue-600 transition-colors">Drop files here or click to browse</p>
                  <p className="text-xs text-slate-400">PDF, PNG, JPG, JSON up to 50 MB</p>
                </div>
              </FormSection>
            </Card>
          </div>

          {/* Right sidebar */}
          <div className="space-y-4">

            {/* Assignees */}
            <Card className="p-5">
              <FormSection title="Assignees">
                <div>
                  {errors.assignees && <p className="text-xs text-red-500 mb-2">{errors.assignees}</p>}
                  <div className="space-y-1.5">
                    {TEAM.map(m => {
                      const selected = assignees.includes(m.initials);
                      return (
                        <button key={m.initials} onClick={() => { toggleAssignee(m.initials); setErrors(er => ({ ...er, assignees: "" })); }}
                          className={`w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl border transition-all ${
                            selected ? "border-blue-200 bg-blue-50" : "border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50"
                          }`}>
                          <Avatar initials={m.initials} color={m.color} size={28} />
                          <div className="flex-1 text-left min-w-0">
                            <p className={`text-sm font-medium truncate ${selected ? "text-blue-800" : "text-slate-700"}`}>{m.name}</p>
                            <p className="text-xs text-slate-400">{m.role}</p>
                          </div>
                          <div className={`w-4 h-4 rounded-[4px] border flex items-center justify-center flex-shrink-0 transition-all ${
                            selected ? "text-white border-blue-600" : "border-slate-300"
                          }`} style={selected ? { background: PRIMARY } : {}}>
                            {selected && <IcoCheck />}
                          </div>
                        </button>
                      );
                    })}
                  </div>
                </div>
              </FormSection>
            </Card>

            {/* Due date */}
            <Card className="p-5">
              <FormSection title="Due Date">
                <div className="space-y-1.5">
                  <div className={`flex items-center gap-2.5 px-3.5 h-11 rounded-xl border bg-white transition-all ${
                    errors.due ? "border-red-400 ring-1 ring-red-200" : "border-slate-200 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100"
                  }`}>
                    <span className="text-slate-400"><IcoCalendar /></span>
                    <input type="date" value={dueDate} onChange={e => { setDueDate(e.target.value); setErrors(er => ({ ...er, due: "" })); }}
                      className="flex-1 bg-transparent text-sm text-slate-700 outline-none cursor-pointer" />
                  </div>
                  {errors.due && <p className="text-xs text-red-500">{errors.due}</p>}
                  {dueDate && (
                    <p className="text-xs text-slate-400 flex items-center gap-1"><IcoClock />
                      {new Date(dueDate) < new Date() ? "⚠ This date is in the past" : `Due in ${Math.ceil((new Date(dueDate).getTime() - Date.now()) / 86400000)} days`}
                    </p>
                  )}
                </div>
              </FormSection>
            </Card>

            {/* Preview */}
            <Card className="p-5 border-blue-100" style={{ background: "#f0f9ff" }}>
              <p className="text-xs font-bold text-blue-500 uppercase tracking-widest mb-3">Preview</p>
              <div className="space-y-3">
                <p className="text-sm font-semibold text-slate-800 leading-snug">{title || <span className="text-slate-300 font-normal">Untitled task</span>}</p>
                <div className="flex flex-wrap gap-1.5">
                  {status && <Badge label={statusLabel[status]} variant={status as "todo"|"inprogress"|"review"|"done"} />}
                  {priority && <Badge label={priority.charAt(0).toUpperCase() + priority.slice(1)} variant={priority as "high"|"medium"|"low"} />}
                </div>
                {assignees.length > 0 && (
                  <div className="flex -space-x-1.5">
                    {assignees.map(a => {
                      const m = TEAM.find(t => t.initials === a);
                      return m ? <Avatar key={a} initials={m.initials} color={m.color} size={24} /> : null;
                    })}
                  </div>
                )}
                {dueDate && <p className="text-xs text-slate-500 flex items-center gap-1"><IcoClock /> {new Date(dueDate).toLocaleDateString("en-US",{month:"short",day:"numeric",year:"numeric"})}</p>}
                {labels.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {labels.slice(0, 3).map(l => <span key={l} className="text-[10px] px-1.5 py-0.5 rounded-full bg-blue-100 text-blue-600 font-medium">{l}</span>)}
                    {labels.length > 3 && <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-slate-100 text-slate-500">+{labels.length - 3}</span>}
                  </div>
                )}
              </div>
            </Card>

          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Toggle Switch (reusable) ─────────────────────────────────────────────

function Toggle({ checked, onChange, size = "md" }: { checked: boolean; onChange: (v: boolean) => void; size?: "sm" | "md" }) {
  const w = size === "sm" ? "w-8 h-4" : "w-11 h-6";
  const knob = size === "sm" ? "w-3 h-3" : "w-4 h-4";
  const translate = size === "sm" ? (checked ? "translate-x-4" : "translate-x-0.5") : (checked ? "translate-x-5" : "translate-x-1");
  return (
    <button type="button" onClick={() => onChange(!checked)} role="switch" aria-checked={checked}
      className={`${w} relative inline-flex items-center rounded-full transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1`}
      style={{ background: checked ? PRIMARY : "#cbd5e1" }}>
      <span className={`${knob} ${translate} bg-white rounded-full shadow transition-transform duration-200 absolute`} />
    </button>
  );
}

// ─── Settings Row (reusable) ──────────────────────────────────────────────

function SettingsRow({
  label, description, children, border = true
}: {
  label: string; description?: string; children: React.ReactNode; border?: boolean;
}) {
  return (
    <div className={`flex items-center justify-between gap-6 py-4 ${border ? "border-b border-slate-100" : ""}`}>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-slate-800">{label}</p>
        {description && <p className="text-xs text-slate-400 mt-0.5 leading-relaxed">{description}</p>}
      </div>
      <div className="flex-shrink-0">{children}</div>
    </div>
  );
}

// ─── Section Header (reusable) ────────────────────────────────────────────

function SectionHeader({ title, description }: { title: string; description?: string }) {
  return (
    <div className="mb-5">
      <h3 className="text-base font-bold text-slate-900" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>{title}</h3>
      {description && <p className="text-sm text-slate-500 mt-0.5">{description}</p>}
    </div>
  );
}

// ─── User Profile Screen ──────────────────────────────────────────────────

const USER_PROFILE = {
  name: "James Wu",
  role: "Product Lead",
  department: "Product",
  email: "james.wu@taskflow.io",
  phone: "+1 (415) 555-0182",
  location: "San Francisco, CA",
  timezone: "America/Los_Angeles (GMT-7)",
  joined: "March 2023",
  bio: "Product leader with 8+ years building enterprise SaaS. Passionate about reducing friction in team workflows and creating systems that scale without sacrificing clarity.",
  initials: "JW",
  avatarColor: "#2563eb",
  team: [
    { initials: "KL", color: "#8b5cf6", name: "Kiran Lal", role: "Backend Lead" },
    { initials: "MR", color: "#10b981", name: "Maya Reed", role: "Designer" },
    { initials: "ST", color: "#f97316", name: "Sam Torres", role: "Engineer" },
    { initials: "AL", color: "#ec4899", name: "Ava Lin", role: "Researcher" },
  ],
  stats: [
    { label: "Tasks Completed", value: "284", trend: "+12 this month" },
    { label: "Active Tasks", value: "18", trend: "3 overdue" },
    { label: "Projects", value: "6", trend: "2 active sprints" },
    { label: "Avg. Completion", value: "2.4d", trend: "vs 3.1d team avg" },
  ],
  recentTasks: [
    { title: "Q3 roadmap planning", status: "done" as const, priority: "high" as const, due: "Jun 20" },
    { title: "Stakeholder presentation deck", status: "inprogress" as const, priority: "high" as const, due: "Jun 28" },
    { title: "User interview synthesis", status: "review" as const, priority: "medium" as const, due: "Jul 1" },
    { title: "Q4 OKR documentation", status: "todo" as const, priority: "medium" as const, due: "Jul 5" },
    { title: "Sprint 13 kickoff notes", status: "todo" as const, priority: "low" as const, due: "Jul 8" },
  ],
  activity: [
    { action: "Completed", task: "Q3 roadmap planning", time: "2h ago", color: "#10b981" },
    { action: "Commented on", task: "API integration review", time: "5h ago", color: "#2563eb" },
    { action: "Created", task: "Stakeholder presentation deck", time: "1d ago", color: "#8b5cf6" },
    { action: "Moved to Review", task: "User interview synthesis", time: "2d ago", color: "#f59e0b" },
    { action: "Assigned to team", task: "Q4 OKR documentation", time: "3d ago", color: "#64748b" },
  ],
};

function UserProfileScreen({ onEdit }: { onEdit: () => void }) {
  const u = USER_PROFILE;

  return (
    <div className="flex-1 overflow-auto" style={{ background: "#f8fafc" }}>
      {/* Hero banner — taller so avatar overlap works cleanly */}
      <div className="relative h-44 flex-shrink-0"
        style={{ background: "linear-gradient(120deg, #1d4ed8 0%, #4f46e5 55%, #7c3aed 100%)" }}>
        <div className="absolute inset-0 opacity-10"
          style={{ backgroundImage: "radial-gradient(circle at 75% 50%, #a78bfa, transparent 55%), radial-gradient(circle at 20% 80%, #60a5fa, transparent 45%)" }} />
        <div className="absolute inset-0 opacity-[0.06]"
          style={{ backgroundImage: "radial-gradient(circle, #fff 1px, transparent 1px)", backgroundSize: "24px 24px" }} />
        {/* Edit Profile lives inside the banner — always visible */}
        <div className="absolute bottom-4 right-8">
          <button onClick={onEdit}
            className="flex items-center gap-1.5 px-4 h-9 rounded-xl bg-white/20 hover:bg-white/30 border border-white/30 text-white text-sm font-semibold transition-all backdrop-blur-sm">
            <IcoEdit /> Edit Profile
          </button>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-8 pb-10 space-y-5">

        {/* Profile header card — avatar overlaps banner by 50% */}
        <Card className="pt-0 pb-5 px-6 -mt-10 relative">
          {/* Avatar row */}
          <div className="flex items-end gap-5 -mt-10 mb-4">
            <div className="relative flex-shrink-0">
              <div className="w-24 h-24 rounded-2xl flex items-center justify-center text-white font-bold text-3xl border-4 border-white shadow-xl"
                style={{ background: u.avatarColor, fontFamily: "'Plus Jakarta Sans',sans-serif" }}>
                {u.initials}
              </div>
              <span className="absolute -bottom-1 -right-1 w-5 h-5 rounded-full bg-emerald-400 border-2 border-white" title="Online" />
            </div>
            {/* Name block — sits below avatar's top edge once card clears banner */}
            <div className="pb-1 min-w-0">
              <h1 className="text-xl font-bold text-slate-900 leading-tight" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>{u.name}</h1>
              <p className="text-sm text-slate-500 mt-0.5">{u.role} · {u.department}</p>
            </div>
          </div>

          {/* Meta row */}
          <div className="flex items-center gap-5 flex-wrap mb-4">
            <span className="flex items-center gap-1.5 text-xs text-slate-500">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" className="text-slate-400"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
              {u.location}
            </span>
            <span className="flex items-center gap-1.5 text-xs text-slate-500">
              <span className="text-slate-400"><IcoClock /></span>{u.timezone}
            </span>
            <span className="flex items-center gap-1.5 text-xs text-slate-500">
              <span className="text-slate-400"><IcoCalendar /></span>Joined {u.joined}
            </span>
            <span className="flex items-center gap-1.5 text-xs font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />Online
            </span>
          </div>

          {/* Bio */}
          <p className="text-sm text-slate-600 leading-relaxed border-t border-slate-100 pt-4">{u.bio}</p>
        </Card>

        {/* Stats row */}
        <div className="grid grid-cols-4 gap-4">
          {u.stats.map(s => (
            <Card key={s.label} className="p-5">
              <p className="text-2xl font-bold text-slate-900 mb-0.5" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>{s.value}</p>
              <p className="text-xs font-semibold text-slate-500">{s.label}</p>
              <p className="text-xs text-slate-400 mt-1">{s.trend}</p>
            </Card>
          ))}
        </div>

        <div className="grid grid-cols-3 gap-6">
          {/* Left col: contact + team */}
          <div className="space-y-5">

            {/* Contact info */}
            <Card className="p-5">
              <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Contact Details</h3>
              <div className="space-y-3">
                {[
                  { icon: <IcoEmail />, label: "Email", value: u.email },
                  { icon: <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" className="text-slate-400"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>, label: "Phone", value: u.phone },
                  { icon: <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" className="text-slate-400"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>, label: "Location", value: u.location },
                  { icon: <IcoClock />, label: "Timezone", value: "GMT-7 (PDT)" },
                ].map(item => (
                  <div key={item.label} className="flex items-start gap-3">
                    <span className="mt-0.5 text-slate-400 flex-shrink-0">{item.icon}</span>
                    <div>
                      <p className="text-xs text-slate-400 font-medium">{item.label}</p>
                      <p className="text-sm text-slate-700 font-medium">{item.value}</p>
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            {/* Team */}
            <Card className="p-5">
              <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Team Members</h3>
              <div className="space-y-2.5">
                {u.team.map(m => (
                  <div key={m.initials} className="flex items-center gap-2.5 p-2 rounded-lg hover:bg-slate-50 transition-colors cursor-pointer group">
                    <Avatar initials={m.initials} color={m.color} size={32} />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-slate-800 truncate group-hover:text-blue-600 transition-colors">{m.name}</p>
                      <p className="text-xs text-slate-400">{m.role}</p>
                    </div>
                    <span className="w-2 h-2 rounded-full bg-emerald-400 flex-shrink-0" />
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Center col: recent tasks */}
          <div className="space-y-5">
            <Card className="p-5">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Recent Tasks</h3>
                <button className="text-xs text-blue-600 font-medium hover:underline">View all</button>
              </div>
              <div className="space-y-2">
                {u.recentTasks.map(t => (
                  <div key={t.title} className="flex items-start gap-3 p-2.5 rounded-lg hover:bg-slate-50 transition-colors cursor-pointer group border border-transparent hover:border-slate-200">
                    <div className={`w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0 ${
                      t.status === "done" ? "bg-emerald-400" :
                      t.status === "inprogress" ? "bg-blue-500" :
                      t.status === "review" ? "bg-violet-500" : "bg-slate-300"
                    }`} />
                    <div className="flex-1 min-w-0">
                      <p className={`text-sm font-medium leading-snug group-hover:text-blue-600 transition-colors ${t.status === "done" ? "line-through text-slate-400" : "text-slate-700"}`}>
                        {t.title}
                      </p>
                      <div className="flex items-center gap-2 mt-1">
                        <Badge label={statusLabel[t.status]} variant={t.status} />
                        <span className="text-xs text-slate-400">{t.due}</span>
                      </div>
                    </div>
                    <Badge label={t.priority.charAt(0).toUpperCase()+t.priority.slice(1)} variant={t.priority} />
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Right col: activity */}
          <div className="space-y-5">
            <Card className="p-5">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Activity</h3>
                <button className="text-xs text-blue-600 font-medium hover:underline">View all</button>
              </div>
              <div className="relative pl-5">
                <div className="absolute left-1.5 top-0 bottom-0 w-px bg-slate-100" />
                <div className="space-y-4">
                  {u.activity.map((a, i) => (
                    <div key={i} className="relative">
                      <div className="absolute -left-[15px] w-2.5 h-2.5 rounded-full border-2 border-white mt-0.5 flex-shrink-0"
                        style={{ background: a.color }} />
                      <p className="text-sm text-slate-600 leading-snug">
                        <span className="font-medium" style={{ color: a.color }}>{a.action}</span>{" "}
                        <span className="font-medium text-slate-700">"{a.task}"</span>
                      </p>
                      <p className="text-xs text-slate-400 mt-0.5">{a.time}</p>
                    </div>
                  ))}
                </div>
              </div>
            </Card>

            {/* Contribution heatmap */}
            <Card className="p-5">
              <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">Task Heatmap · June</h3>
              <div className="grid gap-1" style={{ gridTemplateColumns: "repeat(7, 1fr)" }}>
                {Array.from({ length: 30 }, (_, i) => {
                  const intensity = [0,1,2,3,2,1,0,3,2,1,0,2,3,1,0,2,1,3,2,0,1,2,3,1,0,2,1,0,3,2][i];
                  const colors = ["#f1f5f9","#bfdbfe","#60a5fa","#2563eb"];
                  return (
                    <div key={i} className="aspect-square rounded-sm transition-all hover:scale-110 cursor-pointer"
                      style={{ background: colors[intensity] }}
                      title={`Jun ${i+1}: ${[0,2,5,8][intensity]} tasks`} />
                  );
                })}
              </div>
              <div className="flex items-center gap-2 mt-3 justify-end">
                <span className="text-[10px] text-slate-400">Less</span>
                {["#f1f5f9","#bfdbfe","#60a5fa","#2563eb"].map(c => (
                  <div key={c} className="w-3 h-3 rounded-sm" style={{ background: c }} />
                ))}
                <span className="text-[10px] text-slate-400">More</span>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Settings Screen ──────────────────────────────────────────────────────

type SettingsTab = "general" | "appearance" | "notifications" | "security" | "integrations";

function SettingsScreen() {
  const [tab, setTab] = useState<SettingsTab>("general");
  const [saved, setSaved] = useState(false);

  // General
  const [displayName, setDisplayName] = useState("James Wu");
  const [email, setEmail] = useState("james.wu@taskflow.io");
  const [phone, setPhone] = useState("+1 (415) 555-0182");
  const [bio, setBio] = useState("Product leader with 8+ years building enterprise SaaS.");
  const [language, setLanguage] = useState("en");
  const [timezone, setTimezone] = useState("America/Los_Angeles");
  const [dateFormat, setDateFormat] = useState("MMM D, YYYY");

  // Appearance
  const [theme, setTheme] = useState<"light"|"dark"|"system">("light");
  const [accentColor, setAccentColor] = useState("#2563EB");
  const [density, setDensity] = useState<"comfortable"|"compact"|"cozy">("comfortable");
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [animationsEnabled, setAnimationsEnabled] = useState(true);

  // Notifications
  const [notifEmail, setNotifEmail] = useState(true);
  const [notifPush, setNotifPush] = useState(true);
  const [notifSlack, setNotifSlack] = useState(false);
  const [notifAssigned, setNotifAssigned] = useState(true);
  const [notifMention, setNotifMention] = useState(true);
  const [notifDue, setNotifDue] = useState(true);
  const [notifComment, setNotifComment] = useState(true);
  const [notifStatus, setNotifStatus] = useState(false);
  const [digestFreq, setDigestFreq] = useState("daily");

  // Security
  const [twofa, setTwofa] = useState(false);
  const [sessionTimeout, setSessionTimeout] = useState("8h");
  const [currentPw, setCurrentPw] = useState("");
  const [newPw, setNewPw] = useState("");
  const [confirmPw, setConfirmPw] = useState("");
  const [showCurrentPw, setShowCurrentPw] = useState(false);
  const [showNewPw, setShowNewPw] = useState(false);
  const [pwSaved, setPwSaved] = useState(false);
  const [sessions] = useState([
    { device: "MacBook Pro 16″", browser: "Chrome 124", location: "San Francisco, CA", time: "Active now", current: true },
    { device: "iPhone 15 Pro", browser: "Safari Mobile", location: "San Francisco, CA", time: "2 hours ago", current: false },
    { device: "Windows PC", browser: "Edge 122", location: "New York, NY", time: "3 days ago", current: false },
  ]);

  // Integrations
  const [integrations, setIntegrations] = useState([
    { id: "github", name: "GitHub", desc: "Sync issues and pull requests", icon: "🐙", connected: true, since: "Mar 2024" },
    { id: "slack", name: "Slack", desc: "Send notifications to channels", icon: "💬", connected: true, since: "Jan 2024" },
    { id: "jira", name: "Jira", desc: "Import and export tickets", icon: "🔷", connected: false, since: null },
    { id: "figma", name: "Figma", desc: "Attach design files to tasks", icon: "🎨", connected: false, since: null },
    { id: "linear", name: "Linear", desc: "Mirror issues bidirectionally", icon: "📐", connected: false, since: null },
    { id: "notion", name: "Notion", desc: "Link pages and docs to tasks", icon: "📝", connected: false, since: null },
  ]);
  const [apiKeys] = useState([
    { name: "Production API Key", key: "tf_live_sk_••••••••••••Xk9m", created: "Jan 12, 2024", last: "Today" },
    { name: "CI / CD Pipeline", key: "tf_live_sk_••••••••••••Bz3r", created: "Mar 5, 2024", last: "2 days ago" },
  ]);

  const toggleIntegration = (id: string) =>
    setIntegrations(prev => prev.map(i => i.id === id ? { ...i, connected: !i.connected, since: !i.connected ? "Jul 2026" : null } : i));

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  const tabs: Array<{ id: SettingsTab; label: string; icon: React.ReactNode }> = [
    { id: "general", label: "General", icon: <IcoSettings /> },
    { id: "appearance", label: "Appearance", icon: <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9c.83 0 1.5-.67 1.5-1.5 0-.39-.15-.74-.39-1.01-.23-.26-.38-.61-.38-.99 0-.83.67-1.5 1.5-1.5H16c2.76 0 5-2.24 5-5 0-4.42-4.03-8-9-8zm-5.5 9c-.83 0-1.5-.67-1.5-1.5S5.67 9 6.5 9 8 9.67 8 10.5 7.33 12 6.5 12zm3-4C8.67 8 8 7.33 8 6.5S8.67 5 9.5 5s1.5.67 1.5 1.5S10.33 8 9.5 8zm5 0c-.83 0-1.5-.67-1.5-1.5S13.67 5 14.5 5s1.5.67 1.5 1.5S15.33 8 14.5 8zm3 4c-.83 0-1.5-.67-1.5-1.5S16.67 9 17.5 9s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg> },
    { id: "notifications", label: "Notifications", icon: <IcoBell /> },
    { id: "security", label: "Security", icon: <IcoLock /> },
    { id: "integrations", label: "Integrations", icon: <IcoLink /> },
  ];

  const pwStrength = newPw.length === 0 ? 0 : newPw.length < 6 ? 1 : newPw.length < 10 ? 2 : 3;
  const pwStrengthLabel = ["","Weak","Fair","Strong"][pwStrength];
  const pwStrengthColor = ["","bg-red-400","bg-amber-400","bg-emerald-500"][pwStrength];

  return (
    <div className="flex-1 overflow-auto" style={{ background: "#f8fafc" }}>
      <div className="max-w-5xl mx-auto px-8 py-7">
        {/* Page header */}
        <div className="flex items-center justify-between mb-7">
          <div>
            <h1 className="text-xl font-bold text-slate-900" style={{ fontFamily: "'Plus Jakarta Sans',sans-serif" }}>Settings</h1>
            <p className="text-sm text-slate-500 mt-0.5">Manage your account preferences and workspace configuration</p>
          </div>
          <button onClick={handleSave}
            className={`flex items-center gap-2 px-5 h-10 rounded-xl text-white text-sm font-semibold transition-all ${saved ? "bg-emerald-500" : "hover:opacity-90"}`}
            style={saved ? {} : { background: PRIMARY }}>
            {saved ? <><IcoCheck /> Saved!</> : "Save Changes"}
          </button>
        </div>

        <div className="flex gap-6">
          {/* Tabs sidebar */}
          <aside className="w-48 flex-shrink-0">
            <nav className="space-y-0.5">
              {tabs.map(t => (
                <button key={t.id} onClick={() => setTab(t.id)}
                  className={`w-full flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                    tab === t.id ? "text-blue-700 bg-blue-50" : "text-slate-500 hover:text-slate-800 hover:bg-slate-100/60"
                  }`}>
                  <span className={tab === t.id ? "text-blue-600" : "text-slate-400"}>{t.icon}</span>
                  {t.label}
                  {tab === t.id && <span className="ml-auto w-1.5 h-1.5 rounded-full" style={{ background: PRIMARY }} />}
                </button>
              ))}
            </nav>
          </aside>

          {/* Tab content */}
          <div className="flex-1 min-w-0 space-y-5">

            {/* ── General ── */}
            {tab === "general" && (
              <>
                <Card className="p-6">
                  <SectionHeader title="Personal Information" description="Update your name, bio, and public profile details." />
                  <div className="space-y-4">
                    <div className="flex items-center gap-4 pb-4 border-b border-slate-100">
                      <div className="w-16 h-16 rounded-2xl flex items-center justify-center text-white font-bold text-xl flex-shrink-0"
                        style={{ background: "#2563eb", fontFamily: "'Plus Jakarta Sans',sans-serif" }}>JW</div>
                      <div>
                        <button className="text-sm font-medium text-blue-600 hover:underline">Change avatar</button>
                        <p className="text-xs text-slate-400 mt-0.5">JPG, PNG or GIF. Max 2 MB.</p>
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-1.5">
                        <FormLabel>Display Name</FormLabel>
                        <div className="flex items-center gap-2.5 px-3.5 h-11 rounded-xl border border-slate-200 bg-white focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100 transition-all">
                          <input value={displayName} onChange={e => setDisplayName(e.target.value)}
                            className="flex-1 bg-transparent text-sm text-slate-700 outline-none" />
                        </div>
                      </div>
                      <div className="space-y-1.5">
                        <FormLabel>Email Address</FormLabel>
                        <div className="flex items-center gap-2.5 px-3.5 h-11 rounded-xl border border-slate-200 bg-white focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100 transition-all">
                          <IcoEmail />
                          <input value={email} onChange={e => setEmail(e.target.value)} type="email"
                            className="flex-1 bg-transparent text-sm text-slate-700 outline-none" />
                        </div>
                      </div>
                      <div className="space-y-1.5">
                        <FormLabel>Phone Number</FormLabel>
                        <div className="flex items-center gap-2.5 px-3.5 h-11 rounded-xl border border-slate-200 bg-white focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100 transition-all">
                          <input value={phone} onChange={e => setPhone(e.target.value)}
                            className="flex-1 bg-transparent text-sm text-slate-700 outline-none" />
                        </div>
                      </div>
                      <div className="space-y-1.5">
                        <FormLabel>Role / Title</FormLabel>
                        <div className="flex items-center gap-2.5 px-3.5 h-11 rounded-xl border border-slate-200 bg-white focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100 transition-all">
                          <input defaultValue="Product Lead"
                            className="flex-1 bg-transparent text-sm text-slate-700 outline-none" />
                        </div>
                      </div>
                    </div>
                    <div className="space-y-1.5">
                      <FormLabel>Bio</FormLabel>
                      <FormTextarea value={bio} onChange={setBio} rows={3} />
                      <p className="text-xs text-slate-400">{bio.length}/200 characters</p>
                    </div>
                  </div>
                </Card>

                <Card className="p-6">
                  <SectionHeader title="Localization" description="Set your language, timezone, and date preferences." />
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-1.5">
                      <FormLabel>Language</FormLabel>
                      <FormSelect value={language} onChange={setLanguage} options={[
                        { value: "en", label: "🇺🇸 English (US)" },
                        { value: "en-gb", label: "🇬🇧 English (UK)" },
                        { value: "de", label: "🇩🇪 German" },
                        { value: "fr", label: "🇫🇷 French" },
                        { value: "ja", label: "🇯🇵 Japanese" },
                      ]} />
                    </div>
                    <div className="space-y-1.5">
                      <FormLabel>Timezone</FormLabel>
                      <FormSelect value={timezone} onChange={setTimezone} options={[
                        { value: "America/Los_Angeles", label: "Pacific Time (GMT-7)" },
                        { value: "America/New_York", label: "Eastern Time (GMT-4)" },
                        { value: "Europe/London", label: "London (GMT+1)" },
                        { value: "Asia/Tokyo", label: "Tokyo (GMT+9)" },
                      ]} />
                    </div>
                    <div className="space-y-1.5">
                      <FormLabel>Date Format</FormLabel>
                      <FormSelect value={dateFormat} onChange={setDateFormat} options={[
                        { value: "MMM D, YYYY", label: "Jun 25, 2026" },
                        { value: "DD/MM/YYYY", label: "25/06/2026" },
                        { value: "MM/DD/YYYY", label: "06/25/2026" },
                        { value: "YYYY-MM-DD", label: "2026-06-25" },
                      ]} />
                    </div>
                    <div className="space-y-1.5">
                      <FormLabel>Week Starts On</FormLabel>
                      <FormSelect value="monday" onChange={() => {}} options={[
                        { value: "monday", label: "Monday" },
                        { value: "sunday", label: "Sunday" },
                        { value: "saturday", label: "Saturday" },
                      ]} />
                    </div>
                  </div>
                </Card>
              </>
            )}

            {/* ── Appearance ── */}
            {tab === "appearance" && (
              <>
                <Card className="p-6">
                  <SectionHeader title="Theme" description="Choose how TaskFlow looks on your device." />
                  <div className="grid grid-cols-3 gap-3">
                    {([
                      { id: "light", label: "Light", preview: ["#ffffff","#f1f5f9","#2563eb"] },
                      { id: "dark", label: "Dark", preview: ["#0f172a","#1e293b","#3b82f6"] },
                      { id: "system", label: "System", preview: ["#ffffff","#1e293b","#6366f1"] },
                    ] as const).map(t => (
                      <button key={t.id} onClick={() => setTheme(t.id)}
                        className={`p-3 rounded-xl border-2 transition-all text-left ${theme === t.id ? "border-blue-500" : "border-slate-200 hover:border-slate-300"}`}>
                        <div className="rounded-lg overflow-hidden mb-2 h-16 flex gap-0.5 p-0">
                          <div className="w-8 rounded-l-lg flex-shrink-0" style={{ background: t.preview[1] }} />
                          <div className="flex-1 flex flex-col gap-0.5 p-1.5" style={{ background: t.preview[0] }}>
                            <div className="h-1.5 w-full rounded" style={{ background: t.preview[2] }} />
                            <div className="h-1 w-3/4 rounded bg-slate-200" />
                            <div className="h-1 w-1/2 rounded bg-slate-200" />
                          </div>
                        </div>
                        <p className={`text-xs font-semibold ${theme === t.id ? "text-blue-700" : "text-slate-600"}`}>{t.label}</p>
                      </button>
                    ))}
                  </div>
                </Card>

                <Card className="p-6">
                  <SectionHeader title="Accent Color" description="Personalize the primary color used across the interface." />
                  <div className="flex items-center gap-3 flex-wrap">
                    {[
                      { color: "#2563eb", label: "Blue" },
                      { color: "#7c3aed", label: "Violet" },
                      { color: "#059669", label: "Emerald" },
                      { color: "#dc2626", label: "Red" },
                      { color: "#d97706", label: "Amber" },
                      { color: "#db2777", label: "Pink" },
                      { color: "#0891b2", label: "Cyan" },
                    ].map(c => (
                      <button key={c.color} onClick={() => setAccentColor(c.color)} title={c.label}
                        className={`w-9 h-9 rounded-xl transition-all ${accentColor === c.color ? "ring-2 ring-offset-2 ring-slate-400 scale-110" : "hover:scale-105"}`}
                        style={{ background: c.color }} />
                    ))}
                  </div>
                </Card>

                <Card className="p-6">
                  <SectionHeader title="Density & Layout" />
                  <div className="space-y-0">
                    <SettingsRow label="Information Density" description="Controls how much content is shown per row.">
                      <div className="flex items-center gap-1 bg-slate-100 rounded-lg p-1">
                        {(["compact","comfortable","cozy"] as const).map(d => (
                          <button key={d} onClick={() => setDensity(d)}
                            className={`px-3 py-1.5 rounded-md text-xs font-medium capitalize transition-all ${density === d ? "bg-white text-slate-800 shadow-sm" : "text-slate-500 hover:text-slate-700"}`}>
                            {d}
                          </button>
                        ))}
                      </div>
                    </SettingsRow>
                    <SettingsRow label="Collapsed Sidebar by Default" description="Start with a minimal icon-only sidebar.">
                      <Toggle checked={sidebarCollapsed} onChange={setSidebarCollapsed} />
                    </SettingsRow>
                    <SettingsRow label="Interface Animations" description="Smooth transitions and micro-animations." border={false}>
                      <Toggle checked={animationsEnabled} onChange={setAnimationsEnabled} />
                    </SettingsRow>
                  </div>
                </Card>
              </>
            )}

            {/* ── Notifications ── */}
            {tab === "notifications" && (
              <>
                <Card className="p-6">
                  <SectionHeader title="Delivery Channels" description="Choose how you want to receive notifications." />
                  <div className="space-y-0">
                    <SettingsRow label="Email Notifications" description="Receive updates at james.wu@taskflow.io">
                      <Toggle checked={notifEmail} onChange={setNotifEmail} />
                    </SettingsRow>
                    <SettingsRow label="Push Notifications" description="Browser and desktop push alerts">
                      <Toggle checked={notifPush} onChange={setNotifPush} />
                    </SettingsRow>
                    <SettingsRow label="Slack Integration" description="Post updates to your connected workspace" border={false}>
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-slate-400">Not connected</span>
                        <Toggle checked={notifSlack} onChange={setNotifSlack} />
                      </div>
                    </SettingsRow>
                  </div>
                </Card>

                <Card className="p-6">
                  <SectionHeader title="Notify Me When…" description="Fine-tune which events trigger a notification." />
                  <div className="space-y-0">
                    {[
                      { label: "A task is assigned to me", state: notifAssigned, set: setNotifAssigned },
                      { label: "Someone @mentions me in a comment", state: notifMention, set: setNotifMention },
                      { label: "A task I own is due soon (24h)", state: notifDue, set: setNotifDue },
                      { label: "A new comment is added to my tasks", state: notifComment, set: setNotifComment },
                      { label: "Task status changes on my projects", state: notifStatus, set: setNotifStatus, last: true },
                    ].map((item, i) => (
                      <SettingsRow key={i} label={item.label} border={!item.last}>
                        <Toggle checked={item.state} onChange={item.set} />
                      </SettingsRow>
                    ))}
                  </div>
                </Card>

                <Card className="p-6">
                  <SectionHeader title="Digest Settings" description="Receive a summary instead of individual alerts." />
                  <SettingsRow label="Email Digest Frequency" border={false}>
                    <FormSelect value={digestFreq} onChange={setDigestFreq} options={[
                      { value: "realtime", label: "Real-time" },
                      { value: "hourly", label: "Hourly" },
                      { value: "daily", label: "Daily summary" },
                      { value: "weekly", label: "Weekly summary" },
                      { value: "never", label: "Never" },
                    ]} />
                  </SettingsRow>
                </Card>
              </>
            )}

            {/* ── Security ── */}
            {tab === "security" && (
              <>
                {/* Change password */}
                <Card className="p-6">
                  <SectionHeader title="Change Password" description="Use a strong, unique password you don't use elsewhere." />
                  <div className="space-y-4 max-w-sm">
                    <div className="space-y-1.5">
                      <FormLabel>Current Password</FormLabel>
                      <div className="flex items-center gap-2.5 px-3.5 h-11 rounded-xl border border-slate-200 bg-white focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100 transition-all">
                        <IcoLock />
                        <input type={showCurrentPw ? "text" : "password"} value={currentPw} onChange={e => setCurrentPw(e.target.value)}
                          placeholder="Enter current password"
                          className="flex-1 bg-transparent text-sm text-slate-700 outline-none" />
                        <button type="button" onClick={() => setShowCurrentPw(p => !p)} className="text-slate-400 hover:text-slate-600">
                          <IcoEye off={!showCurrentPw} />
                        </button>
                      </div>
                    </div>
                    <div className="space-y-1.5">
                      <FormLabel>New Password</FormLabel>
                      <div className="flex items-center gap-2.5 px-3.5 h-11 rounded-xl border border-slate-200 bg-white focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100 transition-all">
                        <IcoLock />
                        <input type={showNewPw ? "text" : "password"} value={newPw} onChange={e => setNewPw(e.target.value)}
                          placeholder="Min. 8 characters"
                          className="flex-1 bg-transparent text-sm text-slate-700 outline-none" />
                        <button type="button" onClick={() => setShowNewPw(p => !p)} className="text-slate-400 hover:text-slate-600">
                          <IcoEye off={!showNewPw} />
                        </button>
                      </div>
                      {newPw.length > 0 && (
                        <div className="flex items-center gap-2">
                          <div className="flex gap-1 flex-1">
                            {[1,2,3].map(i => <div key={i} className={`h-1 flex-1 rounded-full transition-all ${pwStrength >= i ? pwStrengthColor : "bg-slate-200"}`} />)}
                          </div>
                          <span className={`text-xs font-medium ${pwStrength===1?"text-red-500":pwStrength===2?"text-amber-500":"text-emerald-600"}`}>{pwStrengthLabel}</span>
                        </div>
                      )}
                    </div>
                    <div className="space-y-1.5">
                      <FormLabel>Confirm New Password</FormLabel>
                      <div className={`flex items-center gap-2.5 px-3.5 h-11 rounded-xl border bg-white transition-all ${
                        confirmPw && newPw !== confirmPw ? "border-red-400 ring-1 ring-red-200" : "border-slate-200 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100"
                      }`}>
                        <IcoLock />
                        <input type="password" value={confirmPw} onChange={e => setConfirmPw(e.target.value)}
                          placeholder="Re-enter new password"
                          className="flex-1 bg-transparent text-sm text-slate-700 outline-none" />
                      </div>
                      {confirmPw && newPw !== confirmPw && <p className="text-xs text-red-500">Passwords do not match</p>}
                    </div>
                    <button onClick={() => { setPwSaved(true); setTimeout(() => setPwSaved(false), 2500); }}
                      className={`flex items-center gap-2 px-4 h-10 rounded-xl text-white text-sm font-semibold transition-all ${pwSaved ? "bg-emerald-500" : "hover:opacity-90"}`}
                      style={pwSaved ? {} : { background: PRIMARY }}>
                      {pwSaved ? <><IcoCheck /> Updated!</> : "Update Password"}
                    </button>
                  </div>
                </Card>

                {/* 2FA */}
                <Card className="p-6">
                  <SectionHeader title="Two-Factor Authentication" description="Add an extra layer of security to your account." />
                  <div className="flex items-start gap-4 p-4 rounded-xl mb-4"
                    style={{ background: twofa ? "#f0fdf4" : "#fff7ed", border: `1px solid ${twofa ? "#bbf7d0" : "#fed7aa"}` }}>
                    <span className="text-2xl">{twofa ? "🔐" : "⚠️"}</span>
                    <div className="flex-1">
                      <p className={`text-sm font-semibold ${twofa ? "text-emerald-800" : "text-amber-800"}`}>
                        {twofa ? "2FA is enabled" : "2FA is not enabled"}
                      </p>
                      <p className={`text-xs mt-0.5 ${twofa ? "text-emerald-600" : "text-amber-600"}`}>
                        {twofa ? "Your account is protected with an authenticator app." : "Your account is vulnerable to password-based attacks."}
                      </p>
                    </div>
                    <Toggle checked={twofa} onChange={setTwofa} />
                  </div>
                  {twofa && (
                    <div className="space-y-3">
                      <p className="text-sm text-slate-600">Scan this QR code with your authenticator app (e.g. Authy, Google Authenticator).</p>
                      <div className="w-32 h-32 bg-slate-100 rounded-xl flex items-center justify-center">
                        <div className="grid gap-0.5" style={{ display: "grid", gridTemplateColumns: "repeat(7,1fr)", width: 80, height: 80 }}>
                          {Array.from({ length: 49 }, (_, i) => (
                            <div key={i} className="rounded-[1px]" style={{ background: Math.random() > 0.5 ? "#1e293b" : "transparent" }} />
                          ))}
                        </div>
                      </div>
                      <div className="flex items-center gap-2 p-3 rounded-lg bg-slate-50 border border-slate-200 max-w-xs">
                        <code className="text-xs font-mono text-slate-700 flex-1">JBSWY3DPEHPK3PXP</code>
                        <button className="text-slate-400 hover:text-blue-600"><IcoCopy /></button>
                      </div>
                    </div>
                  )}
                </Card>

                {/* Sessions */}
                <Card className="p-6">
                  <SectionHeader title="Active Sessions" description="Manage devices currently signed in to your account." />
                  <div className="space-y-3">
                    {sessions.map((s, i) => (
                      <div key={i} className={`flex items-center gap-3 p-3.5 rounded-xl border ${s.current ? "border-blue-200 bg-blue-50/30" : "border-slate-200"}`}>
                        <span className="text-xl">{s.device.includes("Mac") ? "💻" : s.device.includes("iPhone") ? "📱" : "🖥️"}</span>
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            <p className="text-sm font-medium text-slate-800">{s.device}</p>
                            {s.current && <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700">Current</span>}
                          </div>
                          <p className="text-xs text-slate-400">{s.browser} · {s.location} · {s.time}</p>
                        </div>
                        {!s.current && (
                          <button className="text-xs font-medium text-red-500 hover:text-red-700 transition-colors px-3 py-1.5 rounded-lg hover:bg-red-50">
                            Revoke
                          </button>
                        )}
                      </div>
                    ))}
                  </div>
                  <div className="mt-4 pt-4 border-t border-slate-100">
                    <SettingsRow label="Session Timeout" description="Automatically sign out after inactivity." border={false}>
                      <FormSelect value={sessionTimeout} onChange={setSessionTimeout} options={[
                        { value: "1h", label: "1 hour" },
                        { value: "8h", label: "8 hours" },
                        { value: "24h", label: "24 hours" },
                        { value: "7d", label: "7 days" },
                        { value: "never", label: "Never" },
                      ]} />
                    </SettingsRow>
                  </div>
                </Card>
              </>
            )}

            {/* ── Integrations ── */}
            {tab === "integrations" && (
              <>
                <Card className="p-6">
                  <SectionHeader title="Connected Apps" description="Integrate TaskFlow with the tools your team already uses." />
                  <div className="grid grid-cols-2 gap-3">
                    {integrations.map(item => (
                      <div key={item.id} className={`flex items-start gap-3 p-4 rounded-xl border transition-all ${
                        item.connected ? "border-blue-200 bg-blue-50/20" : "border-slate-200 hover:border-slate-300"
                      }`}>
                        <span className="text-2xl flex-shrink-0">{item.icon}</span>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-0.5">
                            <p className="text-sm font-semibold text-slate-800">{item.name}</p>
                            {item.connected && (
                              <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded-full bg-emerald-100 text-emerald-700">Connected</span>
                            )}
                          </div>
                          <p className="text-xs text-slate-400 mb-2 leading-relaxed">{item.desc}</p>
                          {item.connected && item.since && (
                            <p className="text-[10px] text-slate-400 mb-2">Since {item.since}</p>
                          )}
                          <button onClick={() => toggleIntegration(item.id)}
                            className={`text-xs font-semibold px-3 py-1.5 rounded-lg transition-all ${
                              item.connected
                                ? "bg-white border border-slate-200 text-slate-600 hover:border-red-200 hover:text-red-600"
                                : "text-white hover:opacity-90"
                            }`}
                            style={item.connected ? {} : { background: PRIMARY }}>
                            {item.connected ? "Disconnect" : "Connect"}
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>

                <Card className="p-6">
                  <SectionHeader title="API Keys" description="Use API keys to authenticate requests from external services." />
                  <div className="space-y-3 mb-4">
                    {apiKeys.map((k, i) => (
                      <div key={i} className="flex items-center gap-3 p-4 rounded-xl border border-slate-200 bg-slate-50/50">
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-semibold text-slate-800">{k.name}</p>
                          <div className="flex items-center gap-2 mt-1">
                            <code className="text-xs font-mono text-slate-500 bg-white px-2 py-0.5 rounded border border-slate-200">{k.key}</code>
                            <button className="text-slate-400 hover:text-blue-600 transition-colors"><IcoCopy /></button>
                          </div>
                          <p className="text-[10px] text-slate-400 mt-1">Created {k.created} · Last used {k.last}</p>
                        </div>
                        <button className="text-xs font-medium text-red-500 hover:text-red-700 px-3 py-1.5 rounded-lg hover:bg-red-50 transition-all">
                          Revoke
                        </button>
                      </div>
                    ))}
                  </div>
                  <button className="flex items-center gap-2 px-4 h-9 rounded-xl border border-slate-200 bg-white text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors">
                    <IcoPlus /> Generate new API key
                  </button>
                </Card>
              </>
            )}

          </div>
        </div>
      </div>
    </div>
  );
}

// ─── App Shell ────────────────────────────────────────────────────────────

function AppShell({ screen, onNavigate }: { screen: string; onNavigate: (s: string) => void }) {
  const titleMap: Record<string, string> = {
    dashboard: "Dashboard",
    tasklist: "Task List",
    taskdetail: "Task Details",
    createtask: "Create Task",
    edittask: "Edit Task",
    profile: "My Profile",
    settings: "Settings",
    calendar: "Calendar",
    team: "Team",
    analytics: "Analytics",
  };

  const appScreens = ["taskdetail","createtask","edittask","profile","settings"];
  const sidebarActive = appScreens.includes(screen) ? "tasklist" : screen;

  return (
    <div className="flex h-screen w-full overflow-hidden">
      <Sidebar active={sidebarActive} onNavigate={onNavigate} />
      <div className="flex-1 flex flex-col min-w-0">
        <TopNav title={titleMap[screen] ?? screen} onNavigate={onNavigate} />
        {screen === "dashboard" && <DashboardScreen />}
        {screen === "tasklist" && <TaskListScreen />}
        {screen === "taskdetail" && <TaskDetailScreen onEdit={() => onNavigate("edittask")} />}
        {screen === "createtask" && <CreateTaskScreen onCancel={() => onNavigate("tasklist")} />}
        {screen === "edittask" && <CreateTaskScreen onCancel={() => onNavigate("taskdetail")} editMode />}
        {screen === "profile" && <UserProfileScreen onEdit={() => onNavigate("settings")} />}
        {screen === "settings" && <SettingsScreen />}
        {["calendar","team","analytics"].includes(screen) && (
          <div className="flex-1 flex items-center justify-center text-slate-400 text-sm">
            <div className="text-center space-y-2">
              <div className="text-5xl opacity-20">⊙</div>
              <p className="font-medium text-slate-500">{titleMap[screen]} coming soon</p>
              <p className="text-xs">Navigate to Dashboard or Task List to explore</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Root ──────────────────────────────────────────────────────────────────

type Screen = "login" | "register" | "dashboard" | "tasklist" | "taskdetail" | "createtask" | "edittask" | "profile" | "settings" | string;

export default function App() {
  const [screen, setScreen] = useState<Screen>("login");

  const screens: Array<{ id: Screen; label: string }> = [
    { id: "login", label: "Login" },
    { id: "register", label: "Register" },
    { id: "dashboard", label: "Dashboard" },
    { id: "tasklist", label: "Tasks" },
    { id: "taskdetail", label: "Detail" },
    { id: "createtask", label: "Create" },
    { id: "profile", label: "Profile" },
    { id: "settings", label: "Settings" },
  ];

  const isApp = !["login","register"].includes(screen);

  return (
    <div className="min-h-screen" style={{ fontFamily: "'Inter',sans-serif" }}>
      {/* Screen switcher pill */}
      <div className="fixed top-3 left-1/2 -translate-x-1/2 z-[999] bg-white/95 backdrop-blur border border-slate-200 rounded-full p-1 flex gap-0.5 shadow-md shadow-slate-200/60">
        {screens.map(s => (
          <button key={s.id} onClick={() => setScreen(s.id)}
            className="px-3 py-1.5 rounded-full text-xs font-semibold transition-all"
            style={screen === s.id ? { background: PRIMARY, color: "#fff" } : { color: "#64748b" }}>
            {s.label}
          </button>
        ))}
      </div>

      {screen === "login" && <LoginScreen onSwitch={() => setScreen("register")} />}
      {screen === "register" && <RegisterScreen onSwitch={() => setScreen("login")} />}
      {isApp && <AppShell screen={screen} onNavigate={setScreen} />}
    </div>
  );
}
