import React from 'react';

interface TooltipProps {
  message: string;
}

export default function Tooltip({ message }: TooltipProps) {
  return (
    <div className="absolute left-0 -top-12 z-10 max-w-[22rem] rounded bg-slate-800 px-3 py-2 text-sm text-white shadow-lg">
      <div className="flex items-start gap-2">
        <svg className="h-4 w-4 flex-shrink-0 text-orange-300" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.72-1.36 3.485 0l5.518 9.8c.75 1.333-.213 2.99-1.742 2.99H4.481c-1.53 0-2.492-1.657-1.742-2.99l5.518-9.8zM9 7a1 1 0 012 0v3a1 1 0 11-2 0V7zm1 7a1.25 1.25 0 100-2.5A1.25 1.25 0 0010 14z" clipRule="evenodd" />
        </svg>
        <div className="leading-tight">{message}</div>
      </div>
      <div className="absolute left-4 -bottom-1 h-3 w-3 rotate-45 bg-slate-800" />
    </div>
  );
}
