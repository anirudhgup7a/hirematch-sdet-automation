import React, { useState, useEffect } from 'react';
import { Job, Application } from '../types';
import { api } from '../api';
import { Briefcase, Users, PlusCircle, CheckCircle, Trash2, ExternalLink } from 'lucide-react';

interface RecruiterDashboardProps {
  onOpenPostJob: () => void;
  onSelectJob: (job: Job) => void;
}

export const RecruiterDashboard: React.FC<RecruiterDashboardProps> = ({
  onOpenPostJob,
  onSelectJob
}) => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingApps, setLoadingApps] = useState(false);
  const [statusUpdates, setStatusUpdates] = useState<Record<number, string>>({});
  const [actionSuccess, setActionSuccess] = useState<string>('');

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const data = await api.getRecruiterJobs();
      setJobs(data as Job[]);
      if ((data as Job[]).length > 0 && !selectedJob) {
        handleSelectJob((data as Job[])[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const handleSelectJob = async (job: Job) => {
    setSelectedJob(job);
    setLoadingApps(true);
    try {
      const apps = await api.getJobApplications(job.id);
      setApplications(apps as Application[]);
      const initialStatuses: Record<number, string> = {};
      (apps as Application[]).forEach(a => {
        initialStatuses[a.id] = a.status;
      });
      setStatusUpdates(initialStatuses);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingApps(false);
    }
  };

  const handleStatusChange = async (appId: number) => {
    const newStatus = statusUpdates[appId];
    if (!newStatus) return;

    try {
      const updated = await api.updateAppStatus(appId, newStatus);
      setApplications(prev => prev.map(a => a.id === appId ? (updated as Application) : a));
      setActionSuccess(`Application #${appId} updated to "${newStatus}"`);
      setTimeout(() => setActionSuccess(''), 3000);
    } catch (err: any) {
      alert(err.message || 'Failed to update status');
    }
  };

  const handleDeleteJob = async (jobId: number) => {
    if (!confirm('Are you sure you want to deactivate this job posting?')) return;
    try {
      await api.deleteJob(jobId);
      setActionSuccess(`Job #${jobId} marked inactive.`);
      fetchJobs();
      if (selectedJob?.id === jobId) {
        setSelectedJob(null);
        setApplications([]);
      }
    } catch (err: any) {
      alert(err.message || 'Failed to delete job');
    }
  };

  return (
    <div className="container" style={{ margin: '40px auto 60px' }} data-testid="recruiter-dashboard">
      {/* Header Banner */}
      <div className="card" style={{ marginBottom: '30px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '1.4rem', marginBottom: '4px' }}>Recruiter Portal & ATS</h2>
          <p style={{ color: '#64748b', fontSize: '0.9rem' }}>
            Manage candidate pipelines, review applications, and update hiring stages.
          </p>
        </div>
        <button
          onClick={onOpenPostJob}
          className="btn btn-primary"
          data-testid="recruiter-post-job-btn"
        >
          <PlusCircle size={18} />
          Post New Opening
        </button>
      </div>

      {actionSuccess && (
        <div style={{ background: '#ecfdf5', color: '#065f46', padding: '12px 18px', borderRadius: '8px', marginBottom: '20px', fontWeight: 600, fontSize: '0.9rem' }} data-testid="recruiter-action-success">
          {actionSuccess}
        </div>
      )}

      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px 0', color: '#64748b' }}>
          Loading recruiter openings...
        </div>
      ) : jobs.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '60px 20px', color: '#64748b' }}>
          <Briefcase size={44} style={{ margin: '0 auto 14px', color: '#cbd5e1' }} />
          <h3 style={{ fontSize: '1.2rem', marginBottom: '8px' }}>No active job listings</h3>
          <p style={{ fontSize: '0.9rem', marginBottom: '18px' }}>Post your first opening to start receiving qualified applicants.</p>
          <button onClick={onOpenPostJob} className="btn btn-primary">
            Create First Job
          </button>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '340px 1fr', gap: '30px' }}>
          {/* Left Column: Job List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }} data-testid="recruiter-jobs-list">
            <h4 style={{ fontSize: '1rem', color: '#475569', fontWeight: 700 }}>Your Job Openings ({jobs.length})</h4>
            {jobs.map((job) => (
              <div
                key={job.id}
                onClick={() => handleSelectJob(job)}
                className="card"
                style={{
                  cursor: 'pointer',
                  padding: '16px',
                  borderColor: selectedJob?.id === job.id ? '#2563eb' : '#e2e8f0',
                  backgroundColor: selectedJob?.id === job.id ? '#eff6ff' : '#ffffff',
                  boxShadow: selectedJob?.id === job.id ? '0 0 0 1px #2563eb' : 'none'
                }}
                data-testid={`recruiter-job-item-${job.id}`}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <h5 style={{ fontSize: '1rem', marginBottom: '4px' }}>{job.title}</h5>
                  <span className={`badge ${job.is_active ? 'badge-green' : 'badge-gray'}`} style={{ fontSize: '0.7rem' }}>
                    {job.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                <p style={{ fontSize: '0.85rem', color: '#64748b' }}>{job.location} • {job.job_type}</p>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '10px' }}>
                  <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>ID: #{job.id}</span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteJob(job.id);
                    }}
                    style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', padding: '4px' }}
                    title="Deactivate Job"
                    data-testid={`deactivate-job-btn-${job.id}`}
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Right Column: Applicants for Selected Job */}
          <div className="card" style={{ padding: '24px' }} data-testid="recruiter-applicants-panel">
            {selectedJob ? (
              <>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #e2e8f0', paddingBottom: '16px', marginBottom: '20px' }}>
                  <div>
                    <h3 style={{ fontSize: '1.25rem', marginBottom: '4px' }}>{selectedJob.title}</h3>
                    <p style={{ color: '#64748b', fontSize: '0.875rem' }}>
                      Reviewing candidates for {selectedJob.company_name} ({selectedJob.location})
                    </p>
                  </div>
                  <span className="badge badge-blue" style={{ fontSize: '0.85rem' }} data-testid="applicants-count-badge">
                    {applications.length} Applicants
                  </span>
                </div>

                {loadingApps ? (
                  <div style={{ textAlign: 'center', padding: '40px 0', color: '#64748b' }}>
                    Loading applicants...
                  </div>
                ) : applications.length === 0 ? (
                  <div style={{ textAlign: 'center', padding: '50px 20px', color: '#64748b' }} data-testid="no-applicants-msg">
                    <Users size={40} style={{ margin: '0 auto 12px', color: '#cbd5e1' }} />
                    <p>No candidates have applied to this role yet.</p>
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    {applications.map((app) => (
                      <div
                        key={app.id}
                        style={{ border: '1px solid #e2e8f0', borderRadius: '10px', padding: '16px', background: '#f8fafc' }}
                        data-testid={`recruiter-app-card-${app.id}`}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                          <div>
                            <h4 style={{ fontSize: '1.05rem', color: '#1e293b' }} data-testid={`candidate-name-${app.id}`}>
                              {app.candidate?.full_name || `Applicant #${app.candidate_id}`}
                            </h4>
                            <p style={{ fontSize: '0.85rem', color: '#64748b' }}>{app.candidate?.email}</p>
                          </div>
                          <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
                            Applied: {new Date(app.applied_at).toLocaleDateString()}
                          </span>
                        </div>

                        {app.cover_letter && (
                          <div style={{ background: '#ffffff', padding: '10px 14px', borderRadius: '8px', border: '1px solid #e2e8f0', fontSize: '0.875rem', color: '#475569', marginBottom: '12px' }}>
                            <strong>Pitch:</strong> {app.cover_letter}
                          </div>
                        )}

                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #e2e8f0', paddingTop: '12px' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#475569' }}>Status:</span>
                            <select
                              className="select"
                              style={{ width: 'auto', padding: '6px 10px', fontSize: '0.85rem' }}
                              value={statusUpdates[app.id] || app.status}
                              onChange={(e) => setStatusUpdates(prev => ({ ...prev, [app.id]: e.target.value }))}
                              data-testid={`status-select-${app.id}`}
                            >
                              <option value="Applied">Applied</option>
                              <option value="Under Review">Under Review</option>
                              <option value="Shortlisted">Shortlisted</option>
                              <option value="Interview Scheduled">Interview Scheduled</option>
                              <option value="Rejected">Rejected</option>
                              <option value="Offered">Offered</option>
                            </select>
                            <button
                              onClick={() => handleStatusChange(app.id)}
                              className="btn btn-sm btn-primary"
                              data-testid={`update-status-btn-${app.id}`}
                            >
                              Update
                            </button>
                          </div>

                          {app.resume_url && (
                            <a
                              href={app.resume_url}
                              target="_blank"
                              rel="noreferrer"
                              className="btn btn-sm btn-outline"
                              style={{ gap: '4px' }}
                              data-testid={`view-resume-link-${app.id}`}
                            >
                              <ExternalLink size={14} />
                              Resume
                            </a>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <div style={{ textAlign: 'center', padding: '60px 0', color: '#64748b' }}>
                Select a job from the left to view applicants.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
