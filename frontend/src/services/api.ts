const API_BASE_URL = "http://127.0.0.1:8000/api"

class APIError extends Error {
    public status: number

    constructor(status: number, message: string) {
        super(message)
        this.name = "APIError"
        this.status = status
    }
}

const getAuthHeaders = (): Record<string, string> => {
    const token = localStorage.getItem("token")
    return token ? { Authorization: `JWT ${token}` } : {}
}

const handleResponse = async (response: Response) => {
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        const message = errorData.detail || errorData.message || "An error occurred"
        throw new APIError(response.status, message)
    }
    return response.json()
}

// Auth API
export const authAPI = {
    login: async (credentials: { email: string; password: string }) => {
        const response = await fetch(`${API_BASE_URL}/auth/login/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(credentials),
        })
        return handleResponse(response)
    },

    register: async (userData: any) => {
        const response = await fetch(`${API_BASE_URL}/auth/register/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(userData),
        })
        return handleResponse(response)
    },
}

// Tours API
export const toursAPI = {
    getCategories: async () => {
        const response = await fetch(`${API_BASE_URL}/tour/categories/`)
        return handleResponse(response)
    },

    getTours: async (params?: URLSearchParams) => {
        const url = params ? `${API_BASE_URL}/tour/tours/?${params}` : `${API_BASE_URL}/tour/tours/`
        const response = await fetch(url)
        return handleResponse(response)
    },

    getTour: async (id: string) => {
        const response = await fetch(`${API_BASE_URL}/tour/tours/${id}/`)
        return handleResponse(response)
    },

    createTour: async (tourData: any) => {
        const response = await fetch(`${API_BASE_URL}/tour/tours/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(tourData),
        })
        return handleResponse(response)
    },
}

// Bookings API
export const bookingsAPI = {
    getBookings: async () => {
        const response = await fetch(`${API_BASE_URL}/tour/bookings/`, {
            headers: {
                ...getAuthHeaders(),
            },
        })
        return handleResponse(response)
    },

    createBooking: async (bookingData: { tour: number; people_count: number }) => {
        const response = await fetch(`${API_BASE_URL}/tour/bookings/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(bookingData),
        })
        return handleResponse(response)
    },

    confirmBooking: async (id: number) => {
        const response = await fetch(`${API_BASE_URL}/tour/bookings/${id}/confirm/`, {
            method: "POST",
            headers: {
                ...getAuthHeaders(),
            },
        })
        return handleResponse(response)
    },

    cancelBooking: async (id: number) => {
        const response = await fetch(`${API_BASE_URL}/tour/bookings/${id}/cancel/`, {
            method: "POST",
            headers: {
                ...getAuthHeaders(),
            },
        })
        return handleResponse(response)
    },
}
