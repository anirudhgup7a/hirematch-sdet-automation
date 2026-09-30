let defaultBase = 'http://localhost:8000/api/v1';
if (typeof window !== 'undefined' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
  defaultBase = 'https://hirematch-api.onrender.com/api/v1';
}

let rawBase = (import.meta as any).env?.VITE_API_URL || defaultBase;
if (rawBase && !rawBase.startsWith('http://') && !rawBase.startsWith('https://') && !rawBase.startsWith('/')) {
  rawBase = `https://${rawBase}`;
}
if (rawBase && !rawBase.endsWith('/api/v1') && !rawBase.endsWith('/api/v1/')) {
  rawBase = rawBase.replace(/\/+$/, '') + '/api/v1';
}
export const BASE_URL = rawBase;

export function getAuthToken(): string | null {
  return localStorage.getItem('hirematch_token');
}

export function setAuthToken(token: string): void {
  localStorage.setItem('hirematch_token', token);
}

export function removeAuthToken(): void {
  localStorage.removeItem('hirematch_token');
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = getAuthToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {})
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers
  });

  if (!response.ok) {
    let errorDetail = 'An unexpected error occurred';
    try {
      const errorJson = await response.json();
      errorDetail = errorJson.detail || errorJson.message || errorDetail;
    } catch {
      errorDetail = response.statusText;
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

export const api = {
  // Auth
  register: (data: any) => request('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  login: (data: any) => request('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  getMe: () => request('/auth/me'),
  getMyProfile: () => request('/auth/me/profile'),
  updateMyProfile: (data: any) => request('/auth/me/profile', { method: 'PUT', body: JSON.stringify(data) }),

  // Jobs
  getJobs: (params: Record<string, any> = {}) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, val]) => {
      if (val !== undefined && val !== null && val !== '') {
        query.append(key, String(val));
      }
    });
    return request(`/jobs?${query.toString()}`);
  },
  getJob: (id: number) => request(`/jobs/${id}`),
  createJob: (data: any) => request('/jobs', { method: 'POST', body: JSON.stringify(data) }),
  updateJob: (id: number, data: any) => request(`/jobs/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteJob: (id: number) => request(`/jobs/${id}`, { method: 'DELETE' }),
  getRecruiterJobs: () => request('/jobs/recruiter/my-jobs'),
  getSuggestions: (q: string) => request(`/jobs/search/suggestions?q=${encodeURIComponent(q)}`),

  // Applications
  apply: (data: any) => request('/applications', { method: 'POST', body: JSON.stringify(data) }),
  getMyApplications: () => request('/applications/my-applications'),
  getJobApplications: (jobId: number) => request(`/applications/job/${jobId}`),
  updateAppStatus: (appId: number, status: string) =>
    request(`/applications/${appId}/status`, { method: 'PATCH', body: JSON.stringify({ status }) }),

  // Saved Jobs
  getSavedJobs: () => request('/saved-jobs'),
  toggleSaveJob: (jobId: number) => request('/saved-jobs/toggle', { method: 'POST', body: JSON.stringify({ job_id: jobId }) })
};
