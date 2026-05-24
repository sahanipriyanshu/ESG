import { useState, useEffect } from 'react';
import { Card } from '../components/UI';
import { RecordTable } from '../components/RecordTable';
import { api } from '../services/api';
import { RefreshCw } from 'lucide-react';

export function ReviewDashboard() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchRecords = async () => {
    setLoading(true);
    try {
      const data = await api.getRecords();
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
          <h2 className="text-2xl font-bold text-slate-800">All ESG Records</h2>
          <p className="text-sm text-slate-500 mt-1">View and monitor all ingested sustainability data across scopes.</p>
        </div>
        <button onClick={fetchRecords} className="btn-secondary flex items-center">
          <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      <Card className="p-0 overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-slate-400">Loading records...</div>
        ) : (
          <RecordTable records={records} showActions={false} />
        )}
      </Card>
    </div>
  );
}
