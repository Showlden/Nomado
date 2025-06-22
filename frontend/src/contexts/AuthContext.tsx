"use client"

import type React from "react"
import { createContext, useContext, useState, useEffect, type ReactNode } from "react"

interface User {
    id: number
    email: string
    first_name: string
    last_name: string
    is_staff: boolean
}

interface AuthContextType {
    user: User | null
    token: string | null
    login: (email: string, password: string) => Promise<void>
    register: (userData: RegisterData) => Promise<void>
    logout: () => void
    isLoading: boolean
}

interface RegisterData {
    email: string
    password: string
    first_name: string
    last_name: string
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
    const context = useContext(AuthContext)
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider")
    }
    return context
}

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null)
    const [token, setToken] = useState<string | null>(null)
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        const savedToken = localStorage.getItem("token")
        const savedUser = localStorage.getItem("user")

        if (savedToken && savedUser) {
            setToken(savedToken)
            setUser(JSON.parse(savedUser))
        }
        setIsLoading(false)
    }, [])

    const login = async (email: string, password: string) => {
        try {
            const response = await fetch("http://127.0.0.1:8000/api/auth/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email, password }),
            })

            if (!response.ok) {
                throw new Error("Login failed")
            }

            const data = await response.json()
            setToken(data.access)
            setUser(data.user)
            localStorage.setItem("token", data.access)
            localStorage.setItem("user", JSON.stringify(data.user))
        } catch (error) {
            throw error
        }
    }

    const register = async (userData: RegisterData) => {
        try {
            const response = await fetch("http://localhost:8000/api/auth/register/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(userData),
            })

            if (!response.ok) {
                throw new Error("Registration failed")
            }

            const data = await response.json()
            setToken(data.access)
            setUser(data.user)
            localStorage.setItem("token", data.access)
            localStorage.setItem("user", JSON.stringify(data.user))
        } catch (error) {
            throw error
        }
    }

    const logout = () => {
        setUser(null)
        setToken(null)
        localStorage.removeItem("token")
        localStorage.removeItem("user")
    }

    const value = {
        user,
        token,
        login,
        register,
        logout,
        isLoading,
    }

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
