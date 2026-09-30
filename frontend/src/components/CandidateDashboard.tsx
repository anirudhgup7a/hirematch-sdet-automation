import React, { useState, useEffect } from 'react';
import { Application, SavedJob, Job } from '../types';
import { api } from '../api';
import { useAuth } from '../context/AuthContext';
import { Briefcase, Bookmark, FileText, CheckCircle, Clock, AlertCircle } from 'lucide-react';

interface CandidateDashboardProps {
  onSelectJob: (job: Job) => void;
}

export const CandidateDashboard: React.FC<CandidateDashboardProps> = ({ onSelectJob }) => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState<'applications' | 'saved'>('applications');
  const [applications, setApplications] = useState<Application[]>([]);
  const [savedJobs, setSavedJobs] = useState<SavedJob[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [apps, saved] = await Promise.all([
        api.getMyApplications(),
        api.getSavedJobs()
      ]);
      setApplications(apps as Application[]);
      setSavedJobs(saved as SavedJob[]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'Shortlisted':
        return <span className="badge badge-green" data-testid={`status-badge-${status}`}>{status}</span>;
      case 'Interview Scheduled':
        return <span className="badge badge-purple" data-testid={`status-badge-${status}`}>{status}</span>;
      case 'Under Review':
        return <span className="badge badge-amber" data-testid={`status-badge-${status}`}>{status}</span>;
      case 'Rejected':
        return <span className="badge" style={{ backgroundColor: '#fef2f2', color: '#991b1b', border: '1px solid #fecaca' }}>{status}</span>;
      case 'Offered':
        return <span className="badge" style={{ backgroundColor: '#ecfdf5', color: '#047857', border: '1px solid #6ee7b7' }}>{status}</span>;
      default:
        return <span className="badge badge-blue" data-testid={`status-badge-${status}`}>{status}</span>;
    }
  };

  return (
    <div className="container" style={{ margin: '40px auto 60px' }} data-testid="candidate-dashboard">
      {/* Candidate Profile Summary Banner */}
      <div className="card" style={{ marginBottom: '30px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '1.4rem', marginBottom: '4px' }}>Welcome back, {user?.full_name}!</h2>
          <p style={{ color: '#64748b', fontSize: '0.9rem' }}>
            Track your job applications and saved career opportunities.
          </p>
        </div>
        <div style={{ display: 'flex', gap: '20px' }}>
          <div style={{ textAlign: 'center', background: '#f8fafc', padding: '10px 18px', borderRadius: '10px' }}>
            <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#2563eb' }} data-testid="count-applications">
              {applications.length}
            </div>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Applications</div>
          </div>
          <div style={{ textAlign: 'center', background: '#f8fafc', padding: '10px 18px', borderRadius: '10px' }}>
            <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#0f172a' }} data-testid="count-saved-jobs">
              {savedJobs.length}
            </div>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Saved Jobs</div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', borderBottom: '1px solid #e2e8f0', paddingBottom: '10px' }}>
        <button
          onClick={() => setActiveTab('applications')}
          className={`btn btn-sm ${activeTab === 'applications' ? 'btn-primary' : 'btn-outline'}`}
          data-testid="tab-applications"
        >
          <FileText size={16} />
          My Applications ({applications.length})
        </button>
        <button
          onClick={() => setActiveTab('saved')}
          className={`btn btn-sm ${activeTab === 'saved' ? 'btn-primary' : 'btn-outline'}`}
          data-testid="tab-saved-jobs"
        >
          <Bookmark size={16} />
          Saved Jobs ({savedJobs.length})
        </button>
      </div>

      {/* Tab Content */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px 0', color: '#64748b' }}>
          Loading your candidate workspace...
        </div>
      ) : activeTab === 'applications' ? (
        applications.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '50px 20px', color: '#64748b' }} data-testid="empty-applications-state">
            <Briefcase size={40} style={{ margin: '0 auto 12px', color: '#cbd5e1' }} />
            <h4 style={{ fontSize: '1.1rem', marginBottom: '6px' }}>No applications yet</h4>
            <p style={{ fontSize: '0.9rem' }}>Browse open opportunities and apply to your dream roles.</p>
          </div>
        ) : (
          <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }} data-testid="applications-table">
              <thead style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0', color: '#475569' }}>
                <tr>
                  <th style={{ padding: '14px 20px' }}>Job Role & Company</th>
                  <th style={{ padding: '14px 20px' }}>Location</th>
                  <th style={{ padding: '14px 20px' }}>Applied Date</th>
                  <th style={{ padding: '14px 20px' }}>Status</th>
                  <th style={{ padding: '14px 20px', textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {applications.map((app) => (
                  <tr key={app.id} style={{ borderBottom: '1px solid #f1f5f9' }} data-testid={`application-row-${app.id}`}>
                    <td style={{ padding: '16px 20px' }}>
                      <div style={{ fontWeight: 600, color: '#1e293b' }} data-testid={`app-job-title-${app.id}`}>
                        {app.job?.title || `Job #${app.job_id}`}
                      </div>
                      <div style={{ fontSize: '0.8rem', color: '#64748b' }}>
                        {app.job?.company_name}
                      </div>
                    </td>
                    <td style={{ padding: '16px 20px', color: '#64748b' }}>
                      {app.job?.location || 'India'}
                    </td>
                    <td style={{ padding: '16px 20px', color: '#64748b' }}>
                      {new Date(app.applied_at).toLocaleDateString()}
                    </td>
                    <td style={{ padding: '16px 20px' }} data-testid={`application-status-${app.id}`}>
                      {getStatusBadge(app.status)}
                    </td>
                    <td style={{ padding: '16px 20px', textAlign: 'right' }}>
                      {app.job && (
                        <button
                          onClick={() => onSelectJob(app.job!)}
                          className="btn btn-sm btn-outline"
                          data-testid={`view-job-from-app-${app.id}`}
                        >
                          View Job
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )
      ) : (
        savedJobs.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '50px 20px', color: '#64748b' }} data-testid="empty-saved-jobs-state">
            <Bookmark size={40} style={{ margin: '0 auto 12px', color: '#cbd5e1' }} />
            <h4 style={{ fontSize: '1.1rem', marginBottom: '6px' }}>No saved jobs</h4>
            <p style={{ fontSize: '0.9rem' }}>Bookmark interesting jobs to review and apply later.</p>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '20px' }}>
            {savedJobs.map((item) => (
              item.job && (
                <div key={item.id} className="card" style={{ display: 'flex', flexDirection: 'column', gap: '10px' }} data-testid={`saved-job-card-${item.job_id}`}>
                  <h4 style={{ fontSize: '1.1rem' }}>{item.job.title}</h4>
                  <p style={{ color: '#2563eb', fontWeight: 600, fontSize: '0.9rem' }}>{item.job.company_name}</p>
                  <p style={{ fontSize: '0.85rem', color: '#64748b' }}>{item.job.location} • {item.job.job_type}</p>
                  <div style={{ marginTop: 'auto', paddingTop: '10px', display: 'flex', justifyContent: 'flex-end', gap: '8px' }}>
                    <button
                      onClick={() => onSelectJob(item.job!)}
                      className="btn btn-sm btn-primary"
                      data-testid={`apply-saved-job-btn-${item.job_id}`}
                    >
                      View & Apply
                    </button>
                  </div>
                </div>
              )
            ))}
          </div>
        )
      )}
    </div>
  );
};
