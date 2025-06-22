import { Link } from "react-router-dom"
import { MapPin, Star, Users, Calendar } from "lucide-react"

const Home = () => {
    return (
        <div className="min-h-screen">
            {/* Hero Section */}
            <section className="relative bg-gradient-to-r from-green-600 to-emerald-600 text-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
                    <div className="text-center">
                        <h1 className="text-4xl md:text-6xl font-bold mb-6">Discover Amazing Tours</h1>
                        <p className="text-xl md:text-2xl mb-8 text-green-100">
                            Explore the world with our carefully curated travel experiences
                        </p>
                        <Link
                            to="/tours"
                            className="inline-block bg-white text-green-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-green-50 transition-colors"
                        >
                            Browse Tours
                        </Link>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-20 bg-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Why Choose TourBooker?</h2>
                        <p className="text-xl text-gray-600">We make travel planning easy and enjoyable</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                        <div className="text-center">
                            <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                <MapPin className="h-8 w-8 text-green-600" />
                            </div>
                            <h3 className="text-xl font-semibold mb-2">Amazing Destinations</h3>
                            <p className="text-gray-600">Discover breathtaking locations around the world</p>
                        </div>

                        <div className="text-center">
                            <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                <Star className="h-8 w-8 text-green-600" />
                            </div>
                            <h3 className="text-xl font-semibold mb-2">Top Rated Tours</h3>
                            <p className="text-gray-600">All our tours are highly rated by previous travelers</p>
                        </div>

                        <div className="text-center">
                            <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                <Users className="h-8 w-8 text-green-600" />
                            </div>
                            <h3 className="text-xl font-semibold mb-2">Expert Guides</h3>
                            <p className="text-gray-600">Professional guides with local knowledge and expertise</p>
                        </div>

                        <div className="text-center">
                            <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                <Calendar className="h-8 w-8 text-green-600" />
                            </div>
                            <h3 className="text-xl font-semibold mb-2">Easy Booking</h3>
                            <p className="text-gray-600">Simple and secure booking process in just a few clicks</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 bg-green-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Ready to Start Your Adventure?</h2>
                    <p className="text-xl text-gray-600 mb-8">Join thousands of happy travelers who have booked with us</p>
                    <Link
                        to="/tours"
                        className="inline-block bg-green-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-green-700 transition-colors"
                    >
                        Explore Tours Now
                    </Link>
                </div>
            </section>
        </div>
    )
}

export default Home
