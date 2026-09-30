import React, { useState, useEffect } from 'react';
import { Job, JobFiltersState, JobListResponse } from './types';
import { api } from './api';
import { useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { JobCard } from './components/JobCard';
import { JobFilters } from './components/JobFilters';
import { JobModal } from './components/JobModal';
import { CandidateDashboard } from './components/CandidateDashboard';
import { RecruiterDashboard } from './components/RecruiterDashboard';
import { AuthModal } from './components/AuthModal';
import { PostJobModal } from './components/PostJobModal';
import { Search, MapPin, Briefcase, ChevronLeft, ChevronRight, AlertCircle } from 'lucide-react';

export const App: React.FC = () => {
  const { user } = useAuth();
  const [currentView, setCurrentView] = useState<'search' | 'candidate-dashboard' | 'recruiter-dashboard'>('search');
  const [authModal, setAuthModal] = useState<{ open: boolean; mode: 'login' | 'register' }>({ open: false, mode: 'login' });
  const [postJobOpen, setPostJobOpen] = useState(false);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);

  // Search & Filter State
  const [searchInput, setSearchInput] = useState('');
  const [searchLocation, setSearchLocation] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  const [filters, setFilters] = useState<JobFiltersState>({
    keyword: '',
    location: '',
    job_type: '',
    experience_level: '',
    min_salary: undefined,
    sort_by: 'newest'
  });

  const [currentPage, setCurrentPage] = useState(1);
  const [jobResponse, setJobResponse] = useState<JobListResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [savedJobIds, setSavedJobIds] = useState<Set<number>>(new Set());

  // Fetch jobs
  const fetchJobs = async () => {
    setLoading(true);
    try {
      const res = await api.getJobs({
        keyword: filters.keyword,
        location: filters.location,
        job_type: filters.job_type,
        experience_level: filters.experience_level,
        min_salary: filters.min_salary,
        sort_by: filters.sort_by,
        page: currentPage,
        size: 8
      });
      setJobResponse(res as JobListResponse);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch saved job IDs for candidate
  const fetchSavedStatus = async () => {
    if (user?.role === 'candidate') {
      try {
        const saved = await api.getSavedJobs();
        const ids = new Set((saved as any[]).map(s => s.job_id));
        setSavedJobIds(ids);
      } catch (e) {
        console.error(e);
      }
    } else {
      setSavedJobIds(new Set());
    }
  };

  useEffect(() => {
    fetchJobs();
  }, [filters, currentPage]);

  useEffect(() => {
    fetchSavedStatus();
  }, [user]);

  // Suggestions debounced search
  useEffect(() => {
    if (searchInput.trim().length > 1) {
      const timer = setTimeout(async () => {
        try {
          const list = await api.getSuggestions(searchInput.trim());
          setSuggestions(list as string[]);
          setShowSuggestions(true);
        } catch {
          setSuggestions([]);
        }
      }, 250);
      return () => clearTimeout(timer);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  }, [searchInput]);

  const handleHeroSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setShowSuggestions(false);
    setFilters(prev => ({
      ...prev,
      keyword: searchInput,
      location: searchLocation || prev.location
    }));
    setCurrentPage(1);
  };

  const handleToggleSave = async (jobId: number) => {
    if (!user) {
      setAuthModal({ open: true, mode: 'login' });
      return;
    }
    if (user.role !== 'candidate') return;

    try {
      const res: any = await api.toggleSaveJob(jobId);
      setSavedJobIds(prev => {
        const next = new Set(prev);
        if (res.saved) next.add(jobId);
        else next.delete(jobId);
        return next;
      });
    } catch (err: any) {
      alert(err.message || 'Failed to toggle save');
    }
  };

  const resetFilters = () => {
    setSearchInput('');
    setSearchLocation('');
    setFilters({
      keyword: '',
      location: '',
      job_type: '',
      experience_level: '',
      min_salary: undefined,
      sort_by: 'newest'
    });
    setCurrentPage(1);
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Navigation */}
      <Navbar
        onOpenAuth={(mode) => setAuthModal({ open: true, mode })}
        onOpenPostJob={() => setPostJobOpen(true)}
        currentView={currentView}
        setCurrentView={setCurrentView}
      />

      {/* Main Content Router */}
      {currentView === 'candidate-dashboard' ? (
        <CandidateDashboard onSelectJob={(j) => setSelectedJob(j)} />
      ) : currentView === 'recruiter-dashboard' ? (
        <RecruiterDashboard
          onOpenPostJob={() => setPostJobOpen(true)}
          onSelectJob={(j) => setSelectedJob(j)}
        />
      ) : (
        <>
          {/* Hero Search Section */}
          <section className="hero-section" data-testid="hero-section">
            <div className="container">
              <h1 className="hero-title" data-testid="hero-title">
                Find Your Next Career Move in Tech
              </h1>
              <p className="hero-subtitle">
                Discover verified engineering, QA, SDET, and product roles at India's leading tech companies.
              </p>

              {/* Search Bar Form */}
              <form onSubmit={handleHeroSearch} className="search-box-wrapper" style={{ position: 'relative' }}>
                <div className="search-input-group">
                  <Search size={20} color="#64748b" />
                  <input
                    type="text"
                    className="search-field"
                    placeholder="Role, skills (e.g. SDET, Playwright, Python)"
                    value={searchInput}
                    onChange={(e) => setSearchInput(e.target.value)}
                    onFocus={() => suggestions.length > 0 && setShowSuggestions(true)}
                    data-testid="search-input"
                  />
                </div>

                <div className="search-divider" />

                <div className="search-input-group">
                  <MapPin size={20} color="#64748b" />
                  <input
                    type="text"
                    className="search-field"
                    placeholder="Location (e.g. Bengaluru, Gurgaon, Remote)"
                    value={searchLocation}
                    onChange={(e) => setSearchLocation(e.target.value)}
                    data-testid="search-location-input"
                  />
                </div>

                <button
                  type="submit"
                  className="btn btn-primary"
                  style={{ borderRadius: '9999px', padding: '12px 28px' }}
                  data-testid="search-submit-btn"
                >
                  Search Jobs
                </button>

                {/* Suggestions Dropdown */}
                {showSuggestions && suggestions.length > 0 && (
                  <div
                    style={{
                      position: 'absolute',
                      top: '100%',
                      left: 0,
                      right: 0,
                      background: '#ffffff',
                      borderRadius: '12px',
                      boxShadow: '0 10px 25px rgba(0,0,0,0.15)',
                      marginTop: '8px',
                      zIndex: 50,
                      overflow: 'hidden',
                      textAlign: 'left'
                    }}
                    data-testid="search-suggestions-dropdown"
                  >
                    {suggestions.map((s, index) => (
                      <div
                        key={index}
                        onClick={() => {
                          setSearchInput(s);
                          setFilters(prev => ({ ...prev, keyword: s }));
                          setShowSuggestions(false);
                        }}
                        style={{
                          padding: '10px 20px',
                          cursor: 'pointer',
                          color: '#1e293b',
                          fontSize: '0.9rem',
                          borderBottom: '1px solid #f1f5f9'
                        }}
                        className="suggestion-item"
                        data-testid={`suggestion-item-${index}`}
                      >
                        {s}
                      </div>
                    ))}
                  </div>
                )}
              </form>
            </div>
          </section>

          {/* Job Listings & Filters Section */}
          <main className="container main-layout">
            {/* Filters Sidebar */}
            <JobFilters
              filters={filters}
              onChange={(updated) => {
                setFilters(prev => ({ ...prev, ...updated }));
                setCurrentPage(1);
              }}
              onReset={resetFilters}
            />

            {/* Job Cards Column */}
            <div data-testid="job-results-container">
              {/* Results Header */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h3 style={{ fontSize: '1.25rem' }} data-testid="results-count-heading">
                  {jobResponse ? `${jobResponse.total} Open Opportunities` : 'Loading roles...'}
                </h3>
                {filters.keyword && (
                  <span className="badge badge-blue">
                    Keyword: "{filters.keyword}"
                  </span>
                )}
              </div>

              {/* Jobs List */}
              {loading ? (
                <div style={{ textAlign: 'center', padding: '60px 0', color: '#64748b' }}>
                  Searching verified job openings...
                </div>
              ) : jobResponse?.items && jobResponse.items.length > 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }} data-testid="job-list">
                  {jobResponse.items.map((job) => (
                    <JobCard
                      key={job.id}
                      job={job}
                      isSaved={savedJobIds.has(job.id)}
                      onSelect={(j) => setSelectedJob(j)}
                      onToggleSave={user?.role === 'candidate' ? handleToggleSave : undefined}
                    />
                  ))}

                  {/* Pagination */}
                  {jobResponse.total_pages > 1 && (
                    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '14px', marginTop: '30px' }} data-testid="pagination-controls">
                      <button
                        onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                        disabled={currentPage === 1}
                        className="btn btn-sm btn-outline"
                        data-testid="pagination-prev"
                      >
                        <ChevronLeft size={16} />
                        Previous
                      </button>
                      <span style={{ fontSize: '0.9rem', color: '#64748b' }} data-testid="current-page">
                        Page {currentPage} of {jobResponse.total_pages}
                      </span>
                      <button
                        onClick={() => setCurrentPage(p => Math.min(jobResponse.total_pages, p + 1))}
                        disabled={currentPage === jobResponse.total_pages}
                        className="btn btn-sm btn-outline"
                        data-testid="pagination-next"
                      >
                        Next
                        <ChevronRight size={16} />
                      </button>
                    </div>
                  )}
                </div>
              ) : (
                <div className="card" style={{ textAlign: 'center', padding: '60px 20px', color: '#64748b' }} data-testid="empty-search-state">
                  <Briefcase size={44} style={{ margin: '0 auto 12px', color: '#cbd5e1' }} />
                  <h3 style={{ fontSize: '1.2rem', marginBottom: '6px' }}>No matching jobs found</h3>
                  <p style={{ fontSize: '0.9rem', marginBottom: '16px' }}>
                    Try adjusting your filters, location, or search keywords.
                  </p>
                  <button onClick={resetFilters} className="btn btn-outline btn-sm">
                    Reset All Filters
                  </button>
                </div>
              )}
            </div>
          </main>
        </>
      )}

      {/* Footer */}
      <footer style={{ marginTop: 'auto', background: '#0f172a', color: '#94a3b8', padding: '36px 0', borderTop: '1px solid #1e293b', fontSize: '0.875rem' }}>
        <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <span style={{ fontWeight: 700, color: '#ffffff' }}>HireMatch QA</span> — Intelligent Recruitment & SDET Test Bench
          </div>
          <div>
            Engineered for comprehensive test automation, functional, and performance validation.
          </div>
        </div>
      </footer>

      {/* Modals */}
      {selectedJob && (
        <JobModal
          job={selectedJob}
          onClose={() => setSelectedJob(null)}
          onRequireLogin={() => {
            setSelectedJob(null);
            setAuthModal({ open: true, mode: 'login' });
          }}
        />
      )}

      {authModal.open && (
        <AuthModal
          initialMode={authModal.mode}
          onClose={() => setAuthModal({ open: false, mode: 'login' })}
          onSuccess={() => {
            fetchJobs();
            fetchSavedStatus();
          }}
        />
      )}

      {postJobOpen && (
        <PostJobModal
          onClose={() => setPostJobOpen(false)}
          onJobCreated={() => {
            fetchJobs();
            if (currentView === 'recruiter-dashboard') {
              // refresh recruiter view
            }
          }}
        />
      )}
    </div>
  );
};
