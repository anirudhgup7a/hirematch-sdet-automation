import React, { useState } from 'react';
import { api } from '../api';
import { X, PlusCircle, AlertCircle } from 'lucide-react';

interface PostJobModalProps {
  onClose: () => void;
  onJobCreated: () => void;
}

export const PostJobModal: React.FC<PostJobModalProps> = ({
  onClose,
  onJobCreated
}) => {
  const [title, setTitle] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [location, setLocation] = useState('Bengaluru');
  const [jobType, setJobType] = useState('Full-time');
  const [minExp, setMinExp] = useState(2);
  const [maxExp, setMaxExp] = useState(5);
  const [minSalary, setMinSalary] = useState(1000000);
  const [maxSalary, setMaxSalary] = useState(1800000);
  const [skillsRequired, setSkillsRequired] = useState('');
  const [description, setDescription] = useState('');
  const [requirements, setRequirements] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    setSubmitting(true);

    try {
      await api.createJob({
        title,
        company_name: companyName,
        location,
        job_type: jobType,
        experience_level: `${minExp}-${maxExp} yrs`,
        min_experience: Number(minExp),
        max_experience: Number(maxExp),
        min_salary: Number(minSalary),
        max_salary: Number(maxSalary),
        skills_required: skillsRequired,
        description,
        requirements
      });
      onJobCreated();
      onClose();
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to create job.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose} data-testid="post-job-modal">
      <div className="modal-content" style={{ maxWidth: '650px' }} onClick={(e) => e.stopPropagation()}>
        <button
          onClick={onClose}
          style={{ position: 'absolute', top: '20px', right: '20px', background: 'none', border: 'none', cursor: 'pointer', color: '#64748b' }}
          data-testid="post-job-close-btn"
        >
          <X size={22} />
        </button>

        <h2 style={{ fontSize: '1.4rem', marginBottom: '6px' }}>Post New Job Opening</h2>
        <p style={{ color: '#64748b', fontSize: '0.875rem', marginBottom: '20px' }}>
          Publish open positions to thousands of candidates across India.
        </p>

        {errorMsg && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: '#fef2f2', color: '#991b1b', padding: '12px', borderRadius: '8px', marginBottom: '16px', fontSize: '0.875rem' }} data-testid="post-job-error">
            <AlertCircle size={16} />
            <span>{errorMsg}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px' }}>Job Title</label>
              <input
                required
                className="input"
                placeholder="e.g. Lead SDET / Automation Engineer"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                data-testid="post-job-title"
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px' }}>Company Name</label>
              <input
                required
                className="input"
                placeholder="e.g. ZetaCloud Innovations"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                data-testid="post-job-company"
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px' }}>Location</label>
              <select
                className="select"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                data-testid="post-job-location"
              >
                <option value="Bengaluru">Bengaluru</option>
                <option value="Gurgaon">Gurgaon</option>
                <option value="Noida">Noida</option>
                <option value="Hyderabad">Hyderabad</option>
                <option value="Pune">Pune</option>
                <option value="Mumbai">Mumbai</option>
                <option value="Remote">Remote</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px' }}>Work Mode</label>
              <select
                className="select"
                value={jobType}
                onChange={(e) => setJobType(e.target.value)}
                data-testid="post-job-type"
              >
                <option value="Full-time">Full-time</option>
                <option value="Remote">Remote</option>
                <option value="Hybrid">Hybrid</option>
                <option value="Part-time">Part-time</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>Min Exp (Yrs)</label>
              <input
                type="number"
                min={0}
                required
                className="input"
                value={minExp}
                onChange={(e) => setMinExp(Number(e.target.value))}
                data-testid="post-job-minexp"
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>Max Exp (Yrs)</label>
              <input
                type="number"
                min={0}
                required
                className="input"
                value={maxExp}
                onChange={(e) => setMaxExp(Number(e.target.value))}
                data-testid="post-job-maxexp"
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>Min Sal (INR)</label>
              <input
                type="number"
                min={0}
                required
                className="input"
                value={minSalary}
                onChange={(e) => setMinSalary(Number(e.target.value))}
                data-testid="post-job-minsalary"
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>Max Sal (INR)</label>
              <input
                type="number"
                min={0}
                required
                className="input"
                value={maxSalary}
                onChange={(e) => setMaxSalary(Number(e.target.value))}
                data-testid="post-job-maxsalary"
              />
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px' }}>
              Required Skills (Comma separated)
            </label>
            <input
              required
              className="input"
              placeholder="e.g. Playwright, Python, Pytest, Docker, CI/CD"
              value={skillsRequired}
              onChange={(e) => setSkillsRequired(e.target.value)}
              data-testid="post-job-skills"
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px' }}>Job Description</label>
            <textarea
              required
              rows={3}
              className="textarea"
              placeholder="Detailed description of responsibilities..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              data-testid="post-job-description"
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px' }}>Requirements & Qualifications</label>
            <textarea
              required
              rows={2}
              className="textarea"
              placeholder="Educational and practical qualifications..."
              value={requirements}
              onChange={(e) => setRequirements(e.target.value)}
              data-testid="post-job-requirements"
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '10px' }}>
            <button type="button" onClick={onClose} className="btn btn-outline">Cancel</button>
            <button type="submit" disabled={submitting} className="btn btn-primary" data-testid="post-job-submit-btn">
              <PlusCircle size={16} />
              {submitting ? 'Posting...' : 'Publish Job'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
