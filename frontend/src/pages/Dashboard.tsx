"use client"

import { useState, useEffect } from "react"
import { useAuth } from "../contexts/AuthContext"
import { bookingsAPI } from "../services/api"
import { Calendar, Users, DollarSign, CheckCircle, XCircle, Clock } from "lucide-react"
import toast from "react-hot-toast"

interface Booking {
    id: number
    tour_title: string
    people_count: number
    total_price: string
    status: "pending" | "confirmed" | "cancelled"
    created_at: string
}

const Dashboard = () => {
    const { user } = useAuth()
    const [bookings, setBookings] = useState<Booking[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchBookings()
    }, [])

    const fetchBookings = async () => {
        try {
            const data = await bookingsAPI.getBookings()
            setBookings(data)
        } catch (error: any) {
            toast.error("Failed to load bookings")
        } finally {
            setLoading(false)
        }
    }

    const handleCancelBooking = async (bookingId: number) => {
        if (!confirm("Are you sure you want to cancel this booking?")) return

        try {
            await bookingsAPI.cancelBooking(bookingId)
            toast.success("Booking cancelled successfully")
            fetchBookings()
        } catch (error: any) {
            toast.error(error.message || "Failed to cancel booking")
        }
    }

    const handleConfirmBooking = async (bookingId: number) => {
        try {
            await bookingsAPI.confirmBooking(bookingId)
            toast.success("Booking confirmed successfully")
            fetchBookings()
        } catch (error: any) {
            toast.error(error.message || "Failed to confirm booking")
        }
    }

    const getStatusIcon = (status: string) => {
        switch (status) {
            case "confirmed":
                return <CheckCircle className="h-5 w-5 text-green-600" />
            case "cancelled":
                return <XCircle className="h-5 w-5 text-red-600" />
            default:
                return <Clock className="h-5 w-5 text-yellow-600" />
        }
    }

    const getStatusColor = (status: string) => {
        switch (status) {
            case "confirmed":
                return "bg-green-100 text-green-800"
            case "cancelled":
                return "bg-red-100 text-red-800"
            default:
                return "bg-yellow-100 text-yellow-800"
        }
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-green-600"></div>
            </div>
        )
    }

    return (
        <div className="min-h-screen py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Welcome back, {user?.full_name}!</h1>
                    <p className="text-gray-600 mt-2">Manage your tour bookings</p>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div className="bg-white p-6 rounded-lg shadow-md">
                        <div className="flex items-center">
                            <Calendar className="h-8 w-8 text-green-600 mr-3" />
                            <div>
                                <div className="text-2xl font-bold text-gray-900">{bookings.length}</div>
                                <div className="text-gray-600">Total Bookings</div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white p-6 rounded-lg shadow-md">
                        <div className="flex items-center">
                            <CheckCircle className="h-8 w-8 text-green-600 mr-3" />
                            <div>
                                <div className="text-2xl font-bold text-gray-900">
                                    {bookings.filter((b) => b.status === "confirmed").length}
                                </div>
                                <div className="text-gray-600">Confirmed</div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white p-6 rounded-lg shadow-md">
                        <div className="flex items-center">
                            <DollarSign className="h-8 w-8 text-green-600 mr-3" />
                            <div>
                                <div className="text-2xl font-bold text-gray-900">
                                    ${bookings.reduce((sum, b) => sum + Number.parseFloat(b.total_price), 0).toFixed(2)}
                                </div>
                                <div className="text-gray-600">Total Spent</div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Bookings List */}
                <div className="bg-white rounded-lg shadow-md">
                    <div className="px-6 py-4 border-b border-gray-200">
                        <h2 className="text-xl font-semibold text-gray-900">Your Bookings</h2>
                    </div>

                    {bookings.length === 0 ? (
                        <div className="p-8 text-center">
                            <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                            <h3 className="text-lg font-medium text-gray-900 mb-2">No bookings yet</h3>
                            <p className="text-gray-600 mb-4">Start exploring our amazing tours!</p>
                            <a
                                href="/tours"
                                className="inline-block bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors"
                            >
                                Browse Tours
                            </a>
                        </div>
                    ) : (
                        <div className="divide-y divide-gray-200">
                            {bookings.map((booking) => (
                                <div key={booking.id} className="p-6">
                                    <div className="flex items-center justify-between">
                                        <div className="flex-1">
                                            <div className="flex items-center mb-2">
                                                <h3 className="text-lg font-semibold text-gray-900 mr-3">{booking.tour_title}</h3>
                                                <span
                                                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(booking.status)}`}
                                                >
                                                    {getStatusIcon(booking.status)}
                                                    <span className="ml-1 capitalize">{booking.status}</span>
                                                </span>
                                            </div>

                                            <div className="flex items-center space-x-4 text-sm text-gray-500">
                                                <div className="flex items-center">
                                                    <Users className="h-4 w-4 mr-1" />
                                                    {booking.people_count} people
                                                </div>
                                                <div className="flex items-center">
                                                    <DollarSign className="h-4 w-4 mr-1" />${booking.total_price}
                                                </div>
                                                <div className="flex items-center">
                                                    <Calendar className="h-4 w-4 mr-1" />
                                                    {new Date(booking.created_at).toLocaleDateString()}
                                                </div>
                                            </div>
                                        </div>

                                        <div className="flex items-center space-x-2">
                                            {user?.is_staff && booking.status === "pending" && (
                                                <button
                                                    onClick={() => handleConfirmBooking(booking.id)}
                                                    className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 transition-colors"
                                                >
                                                    Confirm
                                                </button>
                                            )}

                                            {booking.status === "pending" && (
                                                <button
                                                    onClick={() => handleCancelBooking(booking.id)}
                                                    className="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700 transition-colors"
                                                >
                                                    Cancel
                                                </button>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default Dashboard
