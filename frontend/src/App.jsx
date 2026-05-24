import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import { ReviewDashboard } from './pages/ReviewDashboard';
import { UploadCenter } from './pages/UploadCenter';
import { SuspiciousRecords } from './pages/SuspiciousRecords';
import { AuditHistory } from './pages/AuditHistory';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<ReviewDashboard />} />
          <Route path="/upload" element={<UploadCenter />} />
          <Route path="/suspicious" element={<SuspiciousRecords />} />
          <Route path="/audit" element={<AuditHistory />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
