import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, UploadCloud, AlertTriangle, FileClock, Leaf } from 'lucide-react';
import { cn } from './UI';

export function Layout({ children }) {
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard },
    { name: 'Upload Center', href: '/upload', icon: UploadCloud },
    { name: 'Suspicious Records', href: '/suspicious', icon: AlertTriangle },
    { name: 'Audit History', href: '/audit', icon: FileClock },
  ];

  return (
    <div className="min-h-screen flex bg-slate-50">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r border-slate-200 flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-slate-200">
          <Leaf className="w-6 h-6 text-brand-600 mr-2" />
          <span className="font-bold text-lg text-slate-900 tracking-tight">ESG Core</span>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  'flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-all duration-200 group',
                  isActive 
                    ? 'bg-brand-50 text-brand-700' 
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                )}
              >
                <item.icon className={cn('w-5 h-5 mr-3', isActive ? 'text-brand-600' : 'text-slate-400 group-hover:text-slate-600')} />
                {item.name}
              </Link>
            )
          })}
        </nav>
        <div className="p-4 border-t border-slate-200">
          <div className="flex items-center">
            <div className="w-8 h-8 rounded-full bg-brand-100 flex items-center justify-center text-brand-700 font-bold text-sm">
              AA
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-slate-900">Analyst Alice</p>
              <p className="text-xs text-slate-500">Acme Corp</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8">
          <h1 className="text-xl font-semibold text-slate-800">
            {navigation.find(n => n.href === location.pathname)?.name || 'ESG Dashboard'}
          </h1>
          <div className="flex items-center space-x-4">
             {/* Additional header items could go here */}
          </div>
        </header>
        <main className="flex-1 overflow-auto p-8 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-brand-50/40 via-slate-50 to-slate-50">
          <div className="max-w-7xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
