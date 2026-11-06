import React from 'react';

export const StatCard = ({ title, value, unit, icon: Icon, change, trend = 'up', color = 'emerald', subtitle }) => {
  const colorMap = {
    emerald: 'bg-emerald-50 text-emerald-600 border-emerald-100',
    blue: 'bg-blue-50 text-blue-600 border-blue-100',
    amber: 'bg-amber-50 text-amber-600 border-amber-100',
    purple: 'bg-purple-50 text-purple-600 border-purple-100',
    rose: 'bg-rose-50 text-rose-600 border-rose-100',
  };

  const activeColor = colorMap[color] || colorMap.emerald;

  return (
    <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-xs hover:shadow-sm transition-shadow">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">{title}</p>
          <div className="flex items-baseline gap-1.5 mt-2">
            <span className="text-2xl font-bold text-slate-900 tracking-tight">{value}</span>
            {unit && <span className="text-xs font-medium text-slate-500">{unit}</span>}
          </div>
        </div>
        <div className={`p-2.5 rounded-lg border ${activeColor}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
      {(change || subtitle) && (
        <div className="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
          {change && (
            <span className={`font-semibold flex items-center gap-1 ${trend === 'up' ? 'text-emerald-600' : 'text-slate-600'}`}>
              {change}
            </span>
          )}
          {subtitle && <span className="text-slate-500 text-[11px]">{subtitle}</span>}
        </div>
      )}
    </div>
  );
};
