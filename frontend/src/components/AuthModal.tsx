import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api';
import { X, Lock, Mail, User, AlertCircle, Briefcase, UserCheck } from 'lucide-react';

interface AuthModalProps {
  initialMode: 'login' | 'register';
  onClose: () => void;
  onSuccess?: () => void;
}

export const AuthModal: React.FC<AuthModalProps> = ({
  initialMode,
  onClose,
  onSuccess
}) => {
  const { login } = useAuth();
  const [mode, setMode] = useState<'login' | 'register'>(initialMode);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [role, setRole] = useState<'candidate' | 'recruiter'>('candidate');
  const [errorMsg, setErrorMsg] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    setLoading(true);

    try {
      if (mode === 'login') {
        const res: any = await api.login({ email, password });
        login(res.access_token, res.user);
        onClose();
        if (onSuccess) onSuccess();
      } else {
        // Register flow
        await api.register({
          email,
          password,
          full_name: fullName,
          role
        });
        // Auto-login after registration
        const loginRes: any = await api.login({ email, password });
        login(loginRes.access_token, loginRes.user);
        onClose();
        if (onSuccess) onSuccess();
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Authentication failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose} data-testid="auth-modal">
      <div className="modal-content" style={{ maxWidth: '440px' }} onClick={(e) => e.stopPropagation()}>
        <button
          onClick={onClose}
          style={{ position: 'absolute', top: '18px', right: '18px', background: 'none', border: 'none', cursor: 'pointer', color: '#64748b' }}
          data-testid="auth-modal-close-btn"
        >
          <X size={20} />
        </button>

        {/* Modal Header */}
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <h2 style={{ fontSize: '1.45rem', marginBottom: '6px' }}>
            {mode === 'login' ? 'Sign In to HireMatch' : 'Create an Account'}
          </h2>
          <p style={{ color: '#64748b', fontSize: '0.875rem' }}>
            {mode === 'login' ? 'Access your applications, saved jobs, and profile' : 'Start discovering opportunities or hiring top tech talent'}
          </p>
        </div>

        {errorMsg && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: '#fef2f2', color: '#991b1b', padding: '10px 14px', borderRadius: '8px', marginBottom: '18px', fontSize: '0.875rem' }} data-testid="auth-error-msg">
            <AlertCircle size={16} />
            <span>{errorMsg}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {mode === 'register' && (
            <>
              {/* Role Selection */}
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px', color: '#475569' }}>
                  I want to:
                </label>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                  <button
                    type="button"
                    onClick={() => setRole('candidate')}
                    className={`btn btn-sm ${role === 'candidate' ? 'btn-primary' : 'btn-outline'}`}
                    style={{ padding: '8px' }}
                    data-testid="auth-role-candidate"
                  >
                    <User size={15} />
                    Find Jobs
                  </button>
                  <button
                    type="button"
                    onClick={() => setRole('recruiter')}
                    className={`btn btn-sm ${role === 'recruiter' ? 'btn-primary' : 'btn-outline'}`}
                    style={{ padding: '8px' }}
                    data-testid="auth-role-recruiter"
                  >
                    <Briefcase size={15} />
                    Hire Talent
                  </button>
                </div>
              </div>

              {/* Full Name */}
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px', color: '#475569' }}>
                  Full Name
                </label>
                <div style={{ position: 'relative' }}>
                  <input
                    type="text"
                    required
                    className="input"
                    placeholder="e.g. Anirudh Gupta"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    data-testid="auth-fullname-input"
                  />
                </div>
              </div>
            </>
          )}

          {/* Email */}
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px', color: '#475569' }}>
              Work / Personal Email
            </label>
            <input
              type="email"
              required
              className="input"
              placeholder="name@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              data-testid="auth-email-input"
            />
          </div>

          {/* Password */}
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px', color: '#475569' }}>
              Password
            </label>
            <input
              type="password"
              required
              minLength={6}
              className="input"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              data-testid="auth-password-input"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', marginTop: '6px' }}
            data-testid="auth-submit-btn"
          >
            {loading ? 'Processing...' : mode === 'login' ? 'Sign In' : 'Create Account'}
          </button>
        </form>

        {/* Switch Mode Footer */}
        <div style={{ textAlign: 'center', marginTop: '20px', paddingTop: '16px', borderTop: '1px solid #f1f5f9', fontSize: '0.875rem', color: '#64748b' }}>
          {mode === 'login' ? (
            <span>
              Don't have an account?{' '}
              <button
                type="button"
                onClick={() => { setMode('register'); setErrorMsg(''); }}
                style={{ background: 'none', border: 'none', color: '#2563eb', fontWeight: 600, cursor: 'pointer' }}
                data-testid="auth-switch-mode-btn"
              >
                Register here
              </button>
            </span>
          ) : (
            <span>
              Already have an account?{' '}
              <button
                type="button"
                onClick={() => { setMode('login'); setErrorMsg(''); }}
                style={{ background: 'none', border: 'none', color: '#2563eb', fontWeight: 600, cursor: 'pointer' }}
                data-testid="auth-switch-mode-btn"
              >
                Sign in here
              </button>
            </span>
          )}
        </div>
      </div>
    </div>
  );
};
