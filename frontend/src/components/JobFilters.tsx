import React from 'react';
import { JobFiltersState } from '../types';
import { Filter, RotateCcw } from 'lucide-react';

interface JobFiltersProps {
  filters: JobFiltersState;
  onChange: (updated: Partial<JobFiltersState>) => void;
  onReset: () => void;
}

export const JobFilters: React.FC<JobFiltersProps> = ({
  filters,
  onChange,
  onReset
}) => {
  return (
    <aside className="card" style={{ height: 'fit-content', padding: '20px' }} data-testid="job-filters-panel">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', borderBottom: '1px solid #e2e8f0', paddingBottom: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Filter size={18} color="#2563eb" />
          <h4 style={{ fontSize: '1rem', fontWeight: 700 }}>All Filters</h4>
        </div>
        <button
          onClick={onReset}
          className="btn-outline btn-sm"
          style={{ fontSize: '0.75rem', padding: '4px 8px', border: 'none', color: '#64748b' }}
          data-testid="clear-filters-btn"
        >
          <RotateCcw size={12} />
          Reset
        </button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
        {/* Location Filter */}
        <div>
          <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px', color: '#475569' }}>
            Location
          </label>
          <select
            className="select"
            value={filters.location}
            onChange={(e) => onChange({ location: e.target.value })}
            data-testid="filter-location-select"
          >
            <option value="">All Locations</option>
            <option value="Bengaluru">Bengaluru</option>
            <option value="Gurgaon">Gurgaon</option>
            <option value="Noida">Noida</option>
            <option value="Hyderabad">Hyderabad</option>
            <option value="Pune">Pune</option>
            <option value="Mumbai">Mumbai</option>
            <option value="Remote">Remote</option>
          </select>
        </div>

        {/* Job Type Filter */}
        <div>
          <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px', color: '#475569' }}>
            Work Mode / Job Type
          </label>
          <select
            className="select"
            value={filters.job_type}
            onChange={(e) => onChange({ job_type: e.target.value })}
            data-testid="filter-jobtype-select"
          >
            <option value="">All Modes</option>
            <option value="Full-time">Full-time</option>
            <option value="Remote">Remote</option>
            <option value="Hybrid">Hybrid</option>
            <option value="Part-time">Part-time</option>
            <option value="Contract">Contract</option>
          </select>
        </div>

        {/* Experience Level */}
        <div>
          <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px', color: '#475569' }}>
            Experience Level
          </label>
          <select
            className="select"
            value={filters.experience_level}
            onChange={(e) => onChange({ experience_level: e.target.value })}
            data-testid="filter-experience-select"
          >
            <option value="">Any Experience</option>
            <option value="Entry-level">Entry-level (0-2 yrs)</option>
            <option value="Mid-level">Mid-level (3-5 yrs)</option>
            <option value="Senior">Senior (5-8 yrs)</option>
            <option value="Lead">Lead (8+ yrs)</option>
          </select>
        </div>

        {/* Min Salary Filter */}
        <div>
          <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px', color: '#475569' }}>
            Minimum Salary (INR)
          </label>
          <select
            className="select"
            value={filters.min_salary || ''}
            onChange={(e) => onChange({ min_salary: e.target.value ? Number(e.target.value) : undefined })}
            data-testid="filter-salary-select"
          >
            <option value="">Any Salary</option>
            <option value="600000">₹6 Lakhs +</option>
            <option value="1000000">₹10 Lakhs +</option>
            <option value="1500000">₹15 Lakhs +</option>
            <option value="2000000">₹20 Lakhs +</option>
            <option value="2500000">₹25 Lakhs +</option>
          </select>
        </div>

        {/* Sort By */}
        <div>
          <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px', color: '#475569' }}>
            Sort By
          </label>
          <select
            className="select"
            value={filters.sort_by}
            onChange={(e) => onChange({ sort_by: e.target.value })}
            data-testid="filter-sort-select"
          >
            <option value="newest">Newest First</option>
            <option value="salary_desc">Salary: High to Low</option>
            <option value="salary_asc">Salary: Low to High</option>
            <option value="experience">Experience: Low to High</option>
          </select>
        </div>
      </div>
    </aside>
  );
};
