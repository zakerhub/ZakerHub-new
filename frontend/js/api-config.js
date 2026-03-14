/**
 * ZakerHub API Configuration & Unified Fetch Service
 */

const API_CONFIG = {
    BASE_URL: "http://127.0.0.1:8000/api/v1", // Change to production URL for Render
    TOKEN_KEY: "zaker_auth_token",
    USER_KEY: "zaker_user_data"
};

/**
 * Enhanced fetch wrapper for ZakerHub API
 * @param {string} endpoint - API endpoint (e.g., "/auth/login/")
 * @param {object} options - Fetch options (method, body, etc.)
 */
async function apiFetch(endpoint, options = {}) {
    const url = `${API_CONFIG.BASE_URL}${endpoint}`;
    const token = localStorage.getItem(API_CONFIG.TOKEN_KEY);

    // Default headers
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    // Add Authorization header if token exists
    if (token) {
        headers['Authorization'] = `Token ${token}`;
    }

    const config = {
        ...options,
        headers
    };

    try {
        const response = await fetch(url, config);
        
        // Handle 401 Unauthorized (Token expired or invalid)
        if (response.status === 401) {
            handleUnauthorized();
            throw new Error("Unauthorized access. Please login again.");
        }

        const data = await response.json();

        if (!response.ok) {
            // Standardize error reporting
            const error = new Error(data.detail || data.non_field_errors?.[0] || "API Request Failed");
            error.data = data;
            throw error;
        }

        return data;
    } catch (err) {
        console.error(`API Error [${endpoint}]:`, err);
        throw err;
    }
}

/**
 * Handle session expiration or unauthorized access
 */
function handleUnauthorized() {
    localStorage.removeItem(API_CONFIG.TOKEN_KEY);
    localStorage.removeItem(API_CONFIG.USER_KEY);
    // Only redirect if not already on a login/signup page
    const publicPages = ['signin.html', 'signup.html', 'index.html'];
    const currentPage = window.location.pathname.split('/').pop();
    if (!publicPages.includes(currentPage) && currentPage !== "") {
        window.location.href = 'signin.html';
    }
}

/**
 * Auth Helpers
 */
const AuthService = {
    login: async (username, password) => {
        const data = await apiFetch('/auth/login/', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        localStorage.setItem(API_CONFIG.TOKEN_KEY, data.token);
        localStorage.setItem(API_CONFIG.USER_KEY, JSON.stringify(data));
        return data;
    },
    signup: async (userData) => {
        return await apiFetch('/auth/signup/', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    },
    logout: () => {
        localStorage.removeItem(API_CONFIG.TOKEN_KEY);
        localStorage.removeItem(API_CONFIG.USER_KEY);
        window.location.href = 'signin.html';
    },
    getUser: () => {
        const user = localStorage.getItem(API_CONFIG.USER_KEY);
        return user ? JSON.parse(user) : null;
    },
    isAuthenticated: () => {
        return !!localStorage.getItem(API_CONFIG.TOKEN_KEY);
    }
};

// Export to window for vanilla JS usage across files
window.ZakerAPI = {
    fetch: apiFetch,
    auth: AuthService,
    config: API_CONFIG
};
