// Hardcoded for prototype
export const ORG_ID = '4cd7399b-c1af-4052-aa60-eb624520e0c6'; // Acme Corp Test ID from python test script
const BASE_URL = 'http://localhost:8000/api';

export const api = {
  // Ingestion
  uploadSAP: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('organization_id', ORG_ID);
    const res = await fetch(`${BASE_URL}/ingestion/sap/`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error('Upload failed');
    return res.json();
  },
  
  uploadUtility: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('organization_id', ORG_ID);
    const res = await fetch(`${BASE_URL}/ingestion/utility/`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error('Upload failed');
    return res.json();
  },

  triggerTravel: async (payloads) => {
    const res = await fetch(`${BASE_URL}/ingestion/travel/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ organization_id: ORG_ID, payloads }),
    });
    if (!res.ok) throw new Error('API Trigger failed');
    return res.json();
  },

  // Records Workflow
  getRecords: async (filters = {}) => {
    const query = new URLSearchParams(filters).toString();
    const res = await fetch(`${BASE_URL}/records/?${query}`);
    if (!res.ok) throw new Error('Failed to fetch records');
    const data = await res.json();
    return data.results ? data.results : data;
  },

  approveRecord: async (id, actor) => {
    const res = await fetch(`${BASE_URL}/records/${id}/approve/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ actor }),
    });
    if (!res.ok) throw new Error('Failed to approve');
    return res.json();
  },

  rejectRecord: async (id, actor, reason) => {
    const res = await fetch(`${BASE_URL}/records/${id}/reject/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ actor, reason }),
    });
    if (!res.ok) throw new Error('Failed to reject');
    return res.json();
  },

  // Audit
  getAuditLog: async (recordId = null) => {
    const url = recordId ? `${BASE_URL}/audit/?record_id=${recordId}` : `${BASE_URL}/audit/`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch audit log');
    const data = await res.json();
    return data.results ? data.results : data;
  }
};
