import React, { useState } from 'react';
import { Job } from '../types';
import { useAuth } from '../context/AuthContext';
import { api } from '../api';
import { X, MapPin, Briefcase, IndianRupee, Send, CheckCircle2, AlertCircle } from 'lucide-react';

interface JobModalProps {
  job: Job | null;
  onClose: () => void;
  onRequireLogin: () => void;
}

export const JobModal: React.FC<JobModalProps> = ({
  job,
  onClose,
  onRequireLogin
}) => {
  const { user } = useAuth();
  const [coverLetter, setCoverLetter] = useState('');
  const [resumeUrl, setResumeUrl] = useState('');
  const [applying, setApplying] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  if (!job) return null;

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) {
      onRequireLogin();
      return;
    }
    if (user.role !== 'candidate') {
      setErrorMsg('Only candidate accounts can apply for jobs.');
      return;
    }

    setApplying(true);
    setErrorMsg('');
    setSuccessMsg('');

    try {
      await api.apply({
        job_id: job.id,
        cover_letter: coverLetter,
        resume_url: resumeUrl || undefined
      });
      setSuccessMsg('Your application has been submitted successfully!');
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to submit application.');
    } finally {
      setApplying(false);
    }
  };

  const formatSalary = (min: number, max: number) => {
    return `₹${(min / 100000).toFixed(1)} - ₹${(max / 100000).toFixed(1)} LPA`;
  };

  return (
    <div className="modal-overlay" onClick={onClose} data-testid="job-details-modal">
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {/* Close Button */}
        <button
          onClick={onClose}
          style={{ position: 'absolute', top: '20px', right: '20px', background: 'none', border: 'none', cursor: 'pointer', color: '#64748b' }}
          data-testid="modal-close-btn"
        >
          <X size={22} />
        </button>

        {/* Header */}
        <div style={{ marginBottom: '20px' }}>
          <span className="badge badge-blue" style={{ marginBottom: '8px' }}>{job.job_type}</span>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '6px' }} data-testid="modal-job-title">{job.title}</h2>
          <p style={{ fontSize: '1.05rem', color: '#2563eb', fontWeight: 600 }} data-testid="modal-job-company">{job.company_name}</p>
        </div>

        {/* Key Metrics */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px', background: '#f8fafc', padding: '14px', borderRadius: '10px', marginBottom: '24px' }}>
          <div>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Experience</div>
            <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{job.min_experience}-{job.max_experience} Yrs</div>
          </div>
          <div>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Salary</div>
            <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{formatSalary(job.min_salary, job.max_salary)}</div>
          </div>
          <div>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Location</div>
            <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{job.location}</div>
          </div>
        </div>

        {/* Description & Requirements */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginBottom: '28px' }}>
          <div>
            <h4 style={{ fontSize: '0.95rem', marginBottom: '6px', color: '#334155' }}>Role Overview</h4>
            <p style={{ fontSize: '0.9rem', color: '#475569', lineHeight: 1.6 }} data-testid="modal-job-description">
              {job.description}
            </p>
          </div>

          <div>
            <h4 style={{ fontSize: '0.95rem', marginBottom: '6px', color: '#334155' }}>Candidate Requirements</h4>
            <p style={{ fontSize: '0.9rem', color: '#475569', lineHeight: 1.6 }}>
              {job.requirements}
            </p>
          </div>

          <div>
            <h4 style={{ fontSize: '0.95rem', marginBottom: '8px', color: '#334155' }}>Required Skills</h4>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {job.skills_required.split(',').map((skill, index) => (
                <span key={index} className="badge badge-gray">{skill.trim()}</span>
              ))}
            </div>
          </div>
        </div>

        {/* Application Form */}
        <div style={{ borderTop: '1px solid #e2e8f0', paddingTop: '20px' }}>
          {successMsg && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: '#ecfdf5', color: '#065f46', padding: '12px', borderRadius: '8px', marginBottom: '16px', fontSize: '0.9rem' }} data-testid="application-success-alert">
              <CheckCircle2 size={18} />
              <span>{successMsg}</span>
            </div>
          )}

          {errorMsg && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: '#fef2f2', color: '#991b1b', padding: '12px', borderRadius: '8px', marginBottom: '16px', fontSize: '0.9rem' }} data-testid="application-error-alert">
              <AlertCircle size={18} />
              <span>{errorMsg}</span>
            </div>
          )}

          {!user ? (
            <div style={{ textAlign: 'center', padding: '12px' }}>
              <p style={{ fontSize: '0.9rem', color: '#64748b', marginBottom: '12px' }}>
                You must be logged in as a candidate to submit your application.
              </p>
              <button
                onClick={onRequireLogin}
                className="btn btn-primary"
                data-testid="login-to-apply-btn"
              >
                Log In to Apply
              </button>
            </div>
          ) : user.role === 'recruiter' ? (
            <div style={{ background: '#f8fafc', padding: '12px', borderRadius: '8px', textAlign: 'center', color: '#64748b', fontSize: '0.85rem' }}>
              You are currently logged in as a <strong>Recruiter</strong>. Job applications are only available to Candidate accounts.
            </div>
          ) : (
            <form onSubmit={handleApply} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <h4 style={{ fontSize: '1rem', fontWeight: 700 }}>Apply for this Role</h4>

              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px', color: '#475569' }}>
                  Cover Note / Pitch (Optional)
                </label>
                <textarea
                  className="textarea"
                  rows={3}
                  placeholder="Tell the hiring team why you are a great fit for this position..."
                  value={coverLetter}
                  onChange={(e) => setCoverLetter(e.target.value)}
                  data-testid="application-cover-letter"
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px', color: '#475569' }}>
                  Resume Link (PDF / Portfolio URL)
                </label>
                <input
                  type="url"
                  className="input"
                  placeholder="https://drive.google.com/your-resume.pdf"
                  value={resumeUrl}
                  onChange={(e) => setResumeUrl(e.target.value)}
                  data-testid="application-resume-input"
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '6px' }}>
                <button
                  type="button"
                  onClick={onClose}
                  className="btn btn-outline"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={applying || !!successMsg}
                  className="btn btn-primary"
                  data-testid="submit-application-btn"
                >
                  <Send size={15} />
                  {applying ? 'Submitting...' : 'Submit Application'}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};
