import { useState } from 'react';
import { Card } from '../components/UI';
import { api } from '../services/api';
import { Upload, FileText, Plane } from 'lucide-react';

export function UploadCenter() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileUpload = async (e, type) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    setMessage('');
    try {
      let res;
      if (type === 'sap') res = await api.uploadSAP(file);
      if (type === 'utility') res = await api.uploadUtility(file);
      setMessage(`Successfully processed ${res.records_processed} records.`);
    } catch (err) {
      setMessage('Failed to upload file.');
    } finally {
      setLoading(false);
      e.target.value = null;
    }
  };

  const handleTriggerTravel = async () => {
    setLoading(true);
    setMessage('');
    try {
      const payloads = [
        {"type": "flight", "date": "2023-05-01", "origin": "JFK", "destination": "LHR"},
        {"type": "hotel", "date": "2023-05-01", "nights": 3}
      ];
      const res = await api.triggerTravel(payloads);
      setMessage(`Successfully triggered API and processed ${res.records_processed} travel records.`);
    } catch (err) {
      setMessage('Failed to trigger travel API.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-800">Upload Center</h2>
        <p className="text-sm text-slate-500 mt-1">Ingest raw data from enterprise systems to normalize and analyze.</p>
      </div>

      {message && (
        <div className="p-4 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-lg text-sm">
          {message}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* SAP Upload */}
        <Card className="flex flex-col items-center justify-center p-8 text-center border-dashed border-2 border-slate-200 hover:border-brand-400 transition-colors">
          <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mb-4">
            <FileText className="w-6 h-6" />
          </div>
          <h3 className="font-semibold text-slate-800 mb-1">SAP ERP Export</h3>
          <p className="text-xs text-slate-500 mb-6">Upload raw CSV containing Buchungsdatum, Werk, Menge, Einheit.</p>
          
          <label className="btn-primary cursor-pointer flex items-center">
            {loading ? 'Processing...' : <><Upload className="w-4 h-4 mr-2" /> Select CSV</>}
            <input type="file" accept=".csv" className="hidden" onChange={(e) => handleFileUpload(e, 'sap')} disabled={loading} />
          </label>
        </Card>

        {/* Utility Upload */}
        <Card className="flex flex-col items-center justify-center p-8 text-center border-dashed border-2 border-slate-200 hover:border-brand-400 transition-colors">
          <div className="w-12 h-12 bg-amber-50 text-amber-600 rounded-full flex items-center justify-center mb-4">
            <FileText className="w-6 h-6" />
          </div>
          <h3 className="font-semibold text-slate-800 mb-1">Utility Billing</h3>
          <p className="text-xs text-slate-500 mb-6">Upload CSV containing Meter ID, Billing Periods, and kWh.</p>
          
          <label className="btn-primary cursor-pointer flex items-center bg-amber-600 hover:bg-amber-500">
            {loading ? 'Processing...' : <><Upload className="w-4 h-4 mr-2" /> Select CSV</>}
            <input type="file" accept=".csv" className="hidden" onChange={(e) => handleFileUpload(e, 'utility')} disabled={loading} />
          </label>
        </Card>

        {/* Travel API Mock */}
        <Card className="flex flex-col items-center justify-center p-8 text-center border-dashed border-2 border-slate-200 hover:border-brand-400 transition-colors md:col-span-2">
          <div className="w-12 h-12 bg-purple-50 text-purple-600 rounded-full flex items-center justify-center mb-4">
            <Plane className="w-6 h-6" />
          </div>
          <h3 className="font-semibold text-slate-800 mb-1">Travel API Sync</h3>
          <p className="text-xs text-slate-500 mb-6">Simulate a webhook or API fetch from travel partner systems.</p>
          
          <button onClick={handleTriggerTravel} disabled={loading} className="btn-primary bg-purple-600 hover:bg-purple-500">
            {loading ? 'Syncing...' : 'Trigger Sync'}
          </button>
        </Card>
      </div>
    </div>
  );
}
