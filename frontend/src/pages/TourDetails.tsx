"use client"

import { useState, useEffect } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { toursAPI, bookingsAPI } from "../services/api"
import { useAuth } from "../contexts/AuthContext"
import { MapPin, Clock, Users, Calendar } from "lucide-react"
import toast from "react-hot-toast"

interface Tour {
    id: number
    title: string
    description: string
    category_name: string
    city: string
    country: string
    price: string
    duration_hours: number
    start_date: string
    end_date: string
    max_people: number
    available_slots: number
}

const TourDetails = () => {
    const { id } = useParams<{ id: string }>()
    const { user } = useAuth()
    const navigate = useNavigate()
    const [tour, setTour] = useState<Tour | null>(null)
    const [loading, setLoading] = useState(true)
    const [bookingLoading, setBookingLoading] = useState(false)
    const [peopleCount, setPeopleCount] = useState(1)

    useEffect(() => {
        if (id) {
            fetchTour()
        }
    }, [id])

    const fetchTour = async () => {
        try {
            const data = await toursAPI.getTour(id!)
            setTour(data)
        } catch (error: any) {
            toast.error("Failed to load tour details")
            navigate("/tours")
        } finally {
            setLoading(false)
        }
    }

    const handleBooking = async () => {
        if (!user) {
            toast.error("Please login to book a tour")
            navigate("/login")
            return
        }

        if (peopleCount > tour!.available_slots) {
            toast.error("Not enough available slots")
            return
        }

        setBookingLoading(true)
        try {
            await bookingsAPI.createBooking({
                tour: tour!.id,
                people_count: peopleCount,
            })
            toast.success("Booking created successfully!")
            navigate("/dashboard")
        } catch (error: any) {
            toast.error(error.message || "Booking failed")
        } finally {
            setBookingLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-green-600"></div>
            </div>
        )
    }

    if (!tour) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <h2 className="text-2xl font-bold text-gray-900 mb-4">Tour not found</h2>
                    <button
                        onClick={() => navigate("/tours")}
                        className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
                    >
                        Back to Tours
                    </button>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen py-8">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="bg-white rounded-lg shadow-lg overflow-hidden">
                    {/* Header */}
                    <div className="bg-gradient-to-r from-green-600 to-emerald-600 text-white p-8">
                        <div className="flex justify-between items-start">
                            <div>
                                <span className="inline-block bg-white bg-opacity-20 text-white text-sm px-3 py-1 rounded-full mb-3">
                                    {tour.category_name}
                                </span>
                                <h1 className="text-3xl font-bold mb-2">{tour.title}</h1>
                                <div className="flex items-center text-green-100">
                                    <MapPin className="h-5 w-5 mr-2" />
                                    {tour.city}, {tour.country}
                                </div>
                            </div>
                            <div className="text-right">
                                <div className="text-3xl font-bold">${tour.price}</div>
                                <div className="text-green-100">per person</div>
                            </div>
                        </div>
                    </div>

                    {/* Content */}
                    <div className="p-8">
                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                            {/* Tour Details */}
                            <div className="lg:col-span-2">
                                <h2 className="text-2xl font-bold text-gray-900 mb-4">About This Tour</h2>
                                <p className="text-gray-600 mb-6 leading-relaxed">{tour.description}</p>

                                <div className="grid grid-cols-2 gap-4 mb-6">
                                    <div className="flex items-center p-4 bg-green-50 rounded-lg">
                                        <Clock className="h-8 w-8 text-green-600 mr-3" />
                                        <div>
                                            <div className="font-semibold text-gray-900">Duration</div>
                                            <div className="text-gray-600">{tour.duration_hours} hours</div>
                                        </div>
                                    </div>

                                    <div className="flex items-center p-4 bg-green-50 rounded-lg">
                                        <Users className="h-8 w-8 text-green-600 mr-3" />
                                        <div>
                                            <div className="font-semibold text-gray-900">Available Slots</div>
                                            <div className="text-gray-600">
                                                {tour.available_slots} / {tour.max_people}
                                            </div>
                                        </div>
                                    </div>

                                    <div className="flex items-center p-4 bg-green-50 rounded-lg">
                                        <Calendar className="h-8 w-8 text-green-600 mr-3" />
                                        <div>
                                            <div className="font-semibold text-gray-900">Start Date</div>
                                            <div className="text-gray-600">{new Date(tour.start_date).toLocaleDateString()}</div>
                                        </div>
                                    </div>

                                    <div className="flex items-center p-4 bg-green-50 rounded-lg">
                                        <Calendar className="h-8 w-8 text-green-600 mr-3" />
                                        <div>
                                            <div className="font-semibold text-gray-900">End Date</div>
                                            <div className="text-gray-600">{new Date(tour.end_date).toLocaleDateString()}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Booking Card */}
                            <div className="lg:col-span-1">
                                <div className="bg-gray-50 p-6 rounded-lg sticky top-8">
                                    <h3 className="text-xl font-bold text-gray-900 mb-4">Book This Tour</h3>

                                    <div className="mb-4">
                                        <label className="block text-sm font-medium text-gray-700 mb-2">Number of People</label>
                                        <select
                                            value={peopleCount}
                                            onChange={(e) => setPeopleCount(Number(e.target.value))}
                                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-green-500 focus:border-green-500"
                                        >
                                            {Array.from({ length: Math.min(tour.available_slots, 10) }, (_, i) => (
                                                <option key={i + 1} value={i + 1}>
                                                    {i + 1} {i === 0 ? "person" : "people"}
                                                </option>
                                            ))}
                                        </select>
                                    </div>

                                    <div className="mb-6">
                                        <div className="flex justify-between items-center mb-2">
                                            <span className="text-gray-600">Price per person:</span>
                                            <span className="font-semibold">${tour.price}</span>
                                        </div>
                                        <div className="flex justify-between items-center mb-2">
                                            <span className="text-gray-600">Number of people:</span>
                                            <span className="font-semibold">{peopleCount}</span>
                                        </div>
                                        <hr className="my-2" />
                                        <div className="flex justify-between items-center text-lg font-bold">
                                            <span>Total:</span>
                                            <span className="text-green-600">
                                                ${(Number.parseFloat(tour.price) * peopleCount).toFixed(2)}
                                            </span>
                                        </div>
                                    </div>

                                    {tour.available_slots > 0 ? (
                                        <button
                                            onClick={handleBooking}
                                            disabled={bookingLoading}
                                            className="w-full bg-green-600 text-white py-3 px-4 rounded-md font-semibold hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                        >
                                            {bookingLoading ? "Booking..." : "Book Now"}
                                        </button>
                                    ) : (
                                        <button
                                            disabled
                                            className="w-full bg-gray-400 text-white py-3 px-4 rounded-md font-semibold cursor-not-allowed"
                                        >
                                            Fully Booked
                                        </button>
                                    )}

                                    {!user && (
                                        <p className="text-sm text-gray-500 mt-3 text-center">
                                            Please{" "}
                                            <button
                                                onClick={() => navigate("/login")}
                                                className="text-green-600 hover:text-green-700 underline"
                                            >
                                                login
                                            </button>{" "}
                                            to book this tour
                                        </p>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default TourDetails
