const API_URL = 'http://localhost:8000';

const getAuthHeader = () => {
    const token = localStorage.getItem('token');
    if (!token) return {};
    return { 'Authorization': `Bearer ${token}` };
};

export const api = {
    setToken(token: string) {
        localStorage.setItem('token', token);
    },

    clearCredentials() {
        localStorage.removeItem('token');
    },

    isAuthenticated() {
        return !!localStorage.getItem('token');
    },

    async login(username: string, password: string) {
        const formData = new URLSearchParams();
        formData.set('username', username);
        formData.set('password', password);

        const response = await fetch(`${API_URL}/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Login failed: ${response.statusText}`);
        }

        const token = await response.json();
        api.setToken(token.access_token);
        return token;
    },

    async fetch(endpoint: string, options: RequestInit = {}) {
        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json',
                ...options.headers,
            },
        });
        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }
        if (response.status === 204) return null;
        return response.json();
    },

    categories: {
        list: () => api.fetch('/config/product-categories/'),
        create: (name: string) => api.fetch('/config/product-categories/', {
            method: 'POST',
            body: JSON.stringify({ name }),
        }),
        update: (id: string, name: string) => api.fetch(`/config/product-categories/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ name }),
        }),
        delete: (id: string) => api.fetch(`/config/product-categories/${id}`, {
            method: 'DELETE',
        }),
    },

    products: {
        list: () => api.fetch('/config/products/'),
        create: (data: { name: string; category_id: string }) => api.fetch('/config/products/', {
            method: 'POST',
            body: JSON.stringify(data),
        }),
        update: (id: string, data: { name: string; category_id: string }) => api.fetch(`/config/products/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        }),
        delete: (id: string) => api.fetch(`/config/products/${id}`, {
            method: 'DELETE',
        }),
    },

    users: {
        list: () => api.fetch('/config/users/'),
        create: (data: { name: string; password: string; role: string }) => api.fetch('/config/users/', {
            method: 'POST',
            body: JSON.stringify(data),
        }),
        update: (id: string, data: { name: string; password_hash: string }) => api.fetch(`/config/users/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        }),
        delete: (id: string) => api.fetch(`/config/users/${id}`, {
            method: 'DELETE',
        }),
    },
    bar: {
        listStates: () => api.fetch('/bar/product/'),
        setEnough: (productId: string) => api.fetch(`/bar/product/${productId}/state/enough`, { method: 'PUT' }),
        setRequired: (productId: string) => api.fetch(`/bar/product/${productId}/state/required`, { method: 'PUT' }),
        setEmergency: (productId: string) => api.fetch(`/bar/product/${productId}/state/emergency`, { method: 'PUT' }),
    }
};
