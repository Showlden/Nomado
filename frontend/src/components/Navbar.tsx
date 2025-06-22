"use client"

import { Link, useNavigate } from "react-router-dom"
import { useAuth } from "../contexts/AuthContext"
import { MapPin, User, LogOut, Plus } from "lucide-react"

const Navbar = () => {
    const { user, logout } = useAuth()
    const navigate = useNavigate()

    const handleLogout = () => {
        logout()
        navigate("/")
    }

    return (
        <nav className="bg-white shadow-lg border-b border-green-100">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                    <div className="flex items-center">
                        <Link to="/" className="flex items-center space-x-2">
                            <MapPin className="h-8 w-8 text-green-600" />
                            <span className="text-2xl font-bold text-gray-900">TourBooker</span>
                        </Link>
                    </div>

                    <div className="flex items-center space-x-8">
                        <Link
                            to="/tours"
                            className="text-gray-700 hover:text-green-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                        >
                            Tours
                        </Link>

                        {user ? (
                            <div className="flex items-center space-x-4">
                                {user.is_staff && (
                                    <Link
                                        to="/create-tour"
                                        className="flex items-center space-x-1 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
                                    >
                                        <Plus className="h-4 w-4" />
                                        <span>Create Tour</span>
                                    </Link>
                                )}

                                <Link
                                    to="/dashboard"
                                    className="flex items-center space-x-1 text-gray-700 hover:text-green-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                                >
                                    <User className="h-4 w-4" />
                                    <span>Dashboard</span>
                                </Link>

                                <button
                                    onClick={handleLogout}
                                    className="flex items-center space-x-1 text-gray-700 hover:text-red-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                                >
                                    <LogOut className="h-4 w-4" />
                                    <span>Logout</span>
                                </button>
                            </div>
                        ) : (
                            <div className="flex items-center space-x-4">
                                <Link
                                    to="/login"
                                    className="text-gray-700 hover:text-green-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                                >
                                    Login
                                </Link>
                                <Link
                                    to="/register"
                                    className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
                                >
                                    Register
                                </Link>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    )
}

export default Navbar
