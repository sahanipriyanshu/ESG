import { useState, useEffect } from 'react';
import { Card, Badge } from '../components/UI';
import { api } from '../services/api';
import { FileClock, User } from 'lucide-react';

export function AuditHistory() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const data = await api.getAuditLog();
        setLogs(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchLogs();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 flex items-center">
            <FileClock className="w-6 h-6 text-slate-600 mr-2" />
            Audit History
          </h2>
          <p className="text-sm text-slate-500 mt-1">Immutable ledger of all workflow actions and mutations.</p>
        </div>
      </div>

      <Card className="p-0">
        {loading ? (
          <div className="p-12 text-center text-slate-400">Loading audit trail...</div>
        ) : (
          <div className="divide-y divide-slate-100">
            {logs.length === 0 ? (
              <div className="p-12 text-center text-slate-400">No audit logs found.</div>
            ) : (
              logs.map((log) => (
                <div key={log.id} className="p-6 flex items-start space-x-4 hover:bg-slate-50/50 transition-colors">
                  <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center flex-shrink-0 text-slate-500">
                    <User className="w-5 h-5" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-slate-900">
                      {log.actor} <span className="font-normal text-slate-500">performed</span> {log.action.toUpperCase()}
                    </p>
                    <p className="text-xs text-slate-500 mt-0.5">
                      on {log.content_type} <span className="font-mono text-[10px] text-slate-400">({log.object_id})</span>
                    </p>
                    
                    {log.action !== 'lock' && log.new_values && (
                      <div className="mt-3 text-xs bg-slate-50 p-3 rounded border border-slate-100 font-mono text-slate-600 overflow-x-auto">
                        {log.action === 'approve' || log.action === 'reject' ? (
                           <span>Status changed to <Badge variant="default" className="ml-1">{log.new_values.status}</Badge></span>
                        ) : (
                          JSON.stringify(log.new_values, null, 2)
                        )}
                      </div>
                    )}
                  </div>
                  <div className="text-xs text-slate-400 whitespace-nowrap">
                    {new Date(log.timestamp).toLocaleString()}
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </Card>
    </div>
  );
}
