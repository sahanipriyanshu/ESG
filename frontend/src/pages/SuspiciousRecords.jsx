import { useState, useEffect } from 'react';
import { Card } from '../components/UI';
import { RecordTable } from '../components/RecordTable';
import { api } from '../services/api';
import { ShieldAlert, RefreshCw } from 'lucide-react';

export function SuspiciousRecords() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchRecords = async () => {
    setLoading(true);
    try {
      // Fetch only suspicious and pending records
      const data = await api.getRecords({ suspicious: 'true', status: 'pending_review' });
      setRecords(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecords();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 flex items-center">
            <ShieldAlert className="w-6 h-6 text-red-500 mr-2" />
            Action Required: Suspicious Records
          </h2>
          <p className="text-sm text-slate-500 mt-1">Review flagged anomalies before they are finalized in the ledger.</p>
        </div>
        <button onClick={fetchRecords} className="btn-secondary flex items-center">
          <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      <Card className="p-0 overflow-hidden border-red-100 ring-1 ring-red-50">
        {loading ? (
          <div className="p-12 text-center text-slate-400">Loading flagged records...</div>
        ) : (
          <RecordTable records={records} showActions={true} onActionComplete={fetchRecords} />
        )}
      </Card>
    </div>
  );
}
