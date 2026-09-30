import React from 'react';
import { Job } from '../types';
import { MapPin, Briefcase, IndianRupee, Clock, Bookmark, ArrowRight } from 'lucide-react';

interface JobCardProps {
  job: Job;
  isSaved?: boolean;
  onSelect: (job: Job) => void;
  onToggleSave?: (jobId: number) => void;
}

export const JobCard: React.FC<JobCardProps> = ({
  job,
  isSaved = false,
  onSelect,
  onToggleSave
}) => {
  const formatSalary = (min: number, max: number) => {
    const minLPA = (min / 100000).toFixed(1);
    const maxLPA = (max / 100000).toFixed(1);
    return `₹${minLPA} - ₹${maxLPA} LPA`;
  };

  const skillsList = job.skills_required.split(',').map(s => s.trim());

  return (
    <div className="card card-hover" style={{ display: 'flex', flexDirection: 'column', gap: '14px', position: 'relative' }} data-testid={`job-card-${job.id}`}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h3 
            style={{ fontSize: '1.2rem', marginBottom: '4px', cursor: 'pointer', color: '#1e293b' }}
            onClick={() => onSelect(job)}
            data-testid={`job-title-${job.id}`}
          >
            {job.title}
          </h3>
          <p style={{ fontWeight: 600, color: '#2563eb', fontSize: '0.95rem' }} data-testid={`job-company-${job.id}`}>
            {job.company_name}
          </p>
        </div>

        {onToggleSave && (
          <button
            onClick={() => onToggleSave(job.id)}
            className="btn-outline btn-sm"
            style={{
              padding: '6px',
              borderRadius: '8px',
              color: isSaved ? '#2563eb' : '#94a3b8',
              backgroundColor: isSaved ? '#eff6ff' : 'transparent',
              borderColor: isSaved ? '#bfdbfe' : '#e2e8f0'
            }}
            data-testid={`job-save-btn-${job.id}`}
            title={isSaved ? "Saved" : "Save job"}
          >
            <Bookmark size={18} fill={isSaved ? '#2563eb' : 'none'} />
          </button>
        )}
      </div>

      {/* Meta tags */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '14px', fontSize: '0.85rem', color: '#64748b' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          <Briefcase size={15} color="#94a3b8" />
          <span data-testid={`job-exp-${job.id}`}>{job.min_experience}-{job.max_experience} Yrs</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          <IndianRupee size={15} color="#94a3b8" />
          <span data-testid={`job-salary-${job.id}`}>{formatSalary(job.min_salary, job.max_salary)}</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          <MapPin size={15} color="#94a3b8" />
          <span data-testid={`job-location-${job.id}`}>{job.location}</span>
        </div>
      </div>

      {/* Description Snippet */}
      <p style={{ fontSize: '0.875rem', color: '#475569', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
        {job.description}
      </p>

      {/* Skills & Action */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 'auto', paddingTop: '10px', borderTop: '1px solid #f1f5f9' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', maxWidth: '75%' }}>
          <span className="badge badge-blue">{job.job_type}</span>
          {skillsList.slice(0, 3).map((skill, index) => (
            <span key={index} className="badge badge-gray">{skill}</span>
          ))}
          {skillsList.length > 3 && (
            <span className="badge badge-gray">+{skillsList.length - 3}</span>
          )}
        </div>

        <button
          onClick={() => onSelect(job)}
          className="btn btn-sm btn-outline"
          data-testid={`job-details-btn-${job.id}`}
        >
          Details
          <ArrowRight size={14} />
        </button>
      </div>
    </div>
  );
};
