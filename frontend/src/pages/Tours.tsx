"use client"

import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { toursAPI } from "../services/api"
import { Search, MapPin, Clock, Users } from "lucide-react"
import toast from "react-hot-toast"

interface Tour {
    id: number
    title: string
    description: string
    category: number
    category_name: string
    city: string
    country: string
    price: string
    duration_hours: number
    start_date: string
    end_date: string
    max_people: number
    available_slots: number
    is_active: boolean
    created_at: string
}

interface Category {
    id: number
    name: string
}

const Tours = () => {
    const [tours, setTours] = useState<Tour[]>([])
    const [categories, setCategories] = useState<Category[]>([])
    const [loading, setLoading] = useState(true)
    const [searchTerm, setSearchTerm] = useState("")
    const [selectedCategory, setSelectedCategory] = useState("")
    const [selectedCity, setSelectedCity] = useState("")
    const [sortBy, setSortBy] = useState("created_at")

    useEffect(() => {
        fetchData()
    }, [])

    useEffect(() => {
        fetchTours()
    }, [searchTerm, selectedCategory, selectedCity, sortBy])

    const fetchData = async () => {
        try {
            const [toursData, categoriesData] = await Promise.all([toursAPI.getTours(), toursAPI.getCategories()])
            setTours(toursData)
            setCategories(categoriesData)
        } catch (error: any) {
            toast.error("Failed to load data")
        } finally {
            setLoading(false)
        }
    }

    const fetchTours = async () => {
        try {
            const params = new URLSearchParams()
            if (searchTerm) params.append("search", searchTerm)
            if (selectedCategory) params.append("category", selectedCategory)
            if (selectedCity) params.append("city", selectedCity)
            if (sortBy) params.append("ordering", sortBy)

            const data = await toursAPI.getTours(params)
            setTours(data)
        } catch (error: any) {
            toast.error("Failed to load tours")
        }
    }

    const uniqueCities = [...new Set(tours.map((tour) => tour.city))]

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
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 mb-4">Explore Tours</h1>

                    {/* Filters */}
                    <div className="bg-white p-6 rounded-lg shadow-md mb-8">
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
                                <div className="relative">
                                    <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                                    <input
                                        type="text"
                                        placeholder="Search tours..."
                                        value={searchTerm}
                                        onChange={(e) => setSearchTerm(e.target.value)}
                                        className="pl-10 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-green-500 focus:border-green-500"
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
                                <select
                                    value={selectedCategory}
                                    onChange={(e) => setSelectedCategory(e.target.value)}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-green-500 focus:border-green-500"
                                >
                                    <option value="">All Categories</option>
                                    {categories.map((category) => (
                                        <option key={category.id} value={category.id}>
                                            {category.name}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">City</label>
                                <select
                                    value={selectedCity}
                                    onChange={(e) => setSelectedCity(e.target.value)}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-green-500 focus:border-green-500"
                                >
                                    <option value="">All Cities</option>
                                    {uniqueCities.map((city) => (
                                        <option key={city} value={city}>
                                            {city}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">Sort by</label>
                                <select
                                    value={sortBy}
                                    onChange={(e) => setSortBy(e.target.value)}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-green-500 focus:border-green-500"
                                >
                                    <option value="-created_at">Newest First</option>
                                    <option value="created_at">Oldest First</option>
                                    <option value="price">Price: Low to High</option>
                                    <option value="-price">Price: High to Low</option>
                                    <option value="start_date">Start Date</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    {/* Tours Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {tours.map((tour) => (
                            <div
                                key={tour.id}
                                className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
                            >
                                <div className="p-6">
                                    <div className="flex justify-between items-start mb-3">
                                        <span className="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                                            {tour.category_name}
                                        </span>
                                        <span className="text-2xl font-bold text-green-600">${tour.price}</span>
                                    </div>

                                    <h3 className="text-xl font-semibold text-gray-900 mb-2">{tour.title}</h3>

                                    <p className="text-gray-600 mb-4 line-clamp-3">{tour.description}</p>

                                    <div className="space-y-2 mb-4">
                                        <div className="flex items-center text-sm text-gray-500">
                                            <MapPin className="h-4 w-4 mr-2" />
                                            {tour.city}, {tour.country}
                                        </div>
                                        <div className="flex items-center text-sm text-gray-500">
                                            <Clock className="h-4 w-4 mr-2" />
                                            {tour.duration_hours} hours
                                        </div>
                                        <div className="flex items-center text-sm text-gray-500">
                                            <Users className="h-4 w-4 mr-2" />
                                            {tour.available_slots} / {tour.max_people} available
                                        </div>
                                    </div>

                                    <Link
                                        to={`/tours/${tour.id}`}
                                        className="block w-full bg-green-600 text-white text-center py-2 px-4 rounded-md hover:bg-green-700 transition-colors"
                                    >
                                        View Details
                                    </Link>
                                </div>
                            </div>
                        ))}
                    </div>

                    {tours.length === 0 && (
                        <div className="text-center py-12">
                            <p className="text-gray-500 text-lg">No tours found matching your criteria.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default Tours
