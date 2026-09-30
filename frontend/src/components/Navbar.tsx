import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Briefcase, User as UserIcon, LogOut, PlusCircle, Bookmark, CheckCircle2 } from 'lucide-react';

interface NavbarProps {
  onOpenAuth: (mode: 'login' | 'register') => void;
  onOpenPostJob: () => void;
  currentView: 'search' | 'candidate-dashboard' | 'recruiter-dashboard';
  setCurrentView: (view: 'search' | 'candidate-dashboard' | 'recruiter-dashboard') => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  onOpenAuth,
  onOpenPostJob,
  currentView,
  setCurrentView
}) => {
  const { user, logout } = useAuth();

  return (
    <header className="navbar" data-testid="navbar">
      <div className="container nav-container">
        {/* Brand */}
        <div 
          className="brand-logo" 
          style={{ cursor: 'pointer' }}
          onClick={() => setCurrentView('search')}
          data-testid="navbar-logo"
        >
          <div style={{
            background: 'linear-gradient(135deg, #2563eb 0%, #1e40af 100%)',
            color: 'white',
            borderRadius: '10px',
            padding: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Briefcase size={22} />
          </div>
          <span>HireMatch</span>
          <span className="brand-badge">QA</span>
        </div>

        {/* Navigation links */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          <button
            onClick={() => setCurrentView('search')}
            className={`btn btn-sm ${currentView === 'search' ? 'btn-secondary' : 'btn-outline'}`}
            data-testid="nav-find-jobs"
          >
            Find Jobs
          </button>

          {user?.role === 'candidate' && (
            <button
              onClick={() => setCurrentView('candidate-dashboard')}
              className={`btn btn-sm ${currentView === 'candidate-dashboard' ? 'btn-secondary' : 'btn-outline'}`}
              data-testid="nav-candidate-dashboard"
            >
              <Bookmark size={15} />
              My Applications & Saved
            </button>
          )}

          {user?.role === 'recruiter' && (
            <>
              <button
                onClick={() => setCurrentView('recruiter-dashboard')}
                className={`btn btn-sm ${currentView === 'recruiter-dashboard' ? 'btn-secondary' : 'btn-outline'}`}
                data-testid="nav-recruiter-dashboard"
              >
                <CheckCircle2 size={15} />
                Recruiter Portal
              </button>
              <button
                onClick={onOpenPostJob}
                className="btn btn-sm btn-primary"
                data-testid="nav-post-job-btn"
              >
                <PlusCircle size={15} />
                Post a Job
              </button>
            </>
          )}
        </nav>

        {/* Auth controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '6px 12px',
                borderRadius: '8px',
                background: '#f1f5f9'
              }} data-testid="user-profile-badge">
                <UserIcon size={16} color="#64748b" />
                <span style={{ fontSize: '0.875rem', fontWeight: 600 }} data-testid="user-display-name">
                  {user.full_name}
                </span>
                <span className="badge badge-blue" style={{ fontSize: '0.7rem' }}>
                  {user.role}
                </span>
              </div>
              <button
                onClick={logout}
                className="btn btn-sm btn-outline"
                style={{ color: '#ef4444', borderColor: '#fca5a5' }}
                data-testid="nav-logout-btn"
                title="Logout"
              >
                <LogOut size={15} />
                Logout
              </button>
            </div>
          ) : (
            <div style={{ display: 'flex', gap: '10px' }}>
              <button
                onClick={() => onOpenAuth('login')}
                className="btn btn-sm btn-outline"
                data-testid="nav-login-btn"
              >
                Log In
              </button>
              <button
                onClick={() => onOpenAuth('register')}
                className="btn btn-sm btn-primary"
                data-testid="nav-register-btn"
              >
                Register
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
