import { Badge } from './UI';
import { Lock, Check, X, ShieldAlert } from 'lucide-react';
import { api } from '../services/api';

export function RecordTable({ records, onActionComplete, showActions = false }) {
  
  const handleApprove = async (id) => {
    try {
      await api.approveRecord(id, 'Analyst Alice');
      if (onActionComplete) onActionComplete();
    } catch (e) {
      alert('Failed to approve');
    }
  };

  const handleReject = async (id) => {
    try {
      await api.rejectRecord(id, 'Analyst Alice', 'Rejected via UI');
      if (onActionComplete) onActionComplete();
    } catch (e) {
      alert('Failed to reject');
    }
  };
  
  const handleLock = async (id) => {
    try {
      await api.lockRecord(id, 'Manager Bob');
      if (onActionComplete) onActionComplete();
    } catch (e) {
      alert('Failed to lock');
    }
  };

  if (!records || records.length === 0) {
    return (
      <div className="text-center py-12 text-slate-500">
        No records found.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm text-left text-slate-600">
        <thead className="text-xs text-slate-500 uppercase bg-slate-50/80 border-b border-slate-200">
          <tr>
            <th className="px-4 py-3">Source</th>
            <th className="px-4 py-3">Category</th>
            <th className="px-4 py-3 text-right">Quantity</th>
            <th className="px-4 py-3">Status</th>
            <th className="px-4 py-3">Audit</th>
            {showActions && <th className="px-4 py-3 text-right">Actions</th>}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {records.map((record) => (
            <tr key={record.id} className="hover:bg-slate-50/50 transition-colors">
              <td className="px-4 py-3 font-medium text-slate-900">
                {record.source_of_truth}
                <div className="text-xs text-slate-500 font-normal">Scope {record.scope}</div>
              </td>
              <td className="px-4 py-3">{record.category}</td>
              <td className="px-4 py-3 text-right font-medium">
                {Number(record.quantity).toLocaleString()} <span className="text-slate-400">{record.normalized_unit}</span>
                <div className="text-xs text-brand-600">{Number(record.estimated_emissions).toLocaleString()} kg CO2e</div>
              </td>
              <td className="px-4 py-3">
                <div className="flex flex-col gap-1 items-start">
                  {record.status === 'pending_review' && <Badge variant="warning">Pending</Badge>}
                  {record.status === 'approved' && <Badge variant="success">Approved</Badge>}
                  {record.status === 'rejected' && <Badge variant="danger">Rejected</Badge>}
                  
                  {record.suspicious_reason && (
                    <div className="flex items-center text-xs text-red-600 mt-1 max-w-[200px]" title={record.suspicious_reason}>
                      <ShieldAlert className="w-3 h-3 mr-1 flex-shrink-0" />
                      <span className="truncate">{record.suspicious_reason}</span>
                    </div>
                  )}
                </div>
              </td>
              <td className="px-4 py-3">
                {record.locked_for_audit ? (
                  <Badge variant="default" className="bg-slate-200"><Lock className="w-3 h-3 mr-1" /> Locked</Badge>
                ) : (
                  <span className="text-xs text-slate-400">Unlocked</span>
                )}
              </td>
              
              {showActions && (
                <td className="px-4 py-3 text-right">
                  <div className="flex items-center justify-end space-x-2">
                    {record.status === 'pending_review' && (
                      <>
                        <button onClick={() => handleApprove(record.id)} className="p-1.5 text-emerald-600 hover:bg-emerald-50 rounded-md transition-colors" title="Approve">
                          <Check className="w-4 h-4" />
                        </button>
                        <button onClick={() => handleReject(record.id)} className="p-1.5 text-red-600 hover:bg-red-50 rounded-md transition-colors" title="Reject">
                          <X className="w-4 h-4" />
                        </button>
                      </>
                    )}
                    {record.status === 'approved' && !record.locked_for_audit && (
                       <button onClick={() => handleLock(record.id)} className="p-1.5 text-slate-600 hover:bg-slate-100 rounded-md transition-colors border border-slate-200 text-xs flex items-center font-medium">
                         <Lock className="w-3 h-3 mr-1" /> Lock
                       </button>
                    )}
                  </div>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
