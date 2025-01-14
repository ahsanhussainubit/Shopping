import React, { useState, useEffect } from 'react';
import { Search, Star, ShoppingCart, ChevronLeft, ChevronRight } from 'lucide-react';

interface Product {
  id: number;
  title: string;
  price: number;
  stars: number;
  reviews: number;
  list_price: number;
  img_url: string;
  description?: string;
  amazon_link: string;
  bought_in_last_month?: number;
}

function App() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [totalPages, setTotalPages] = useState(1);
  const [categories, setCategories] = useState<{ id: number; name: string }[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<number | null>(null);
  const limit = 12;

  // Fetch categories
  const fetchCategories = async () => {
    try {
      const response = await fetch('http://localhost:8000/category/');
      const data = await response.json();
      setCategories(data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  // Fetch products based on search term, category, and page
  const fetchProducts = async (page: number = 1, keyword: string = '', categoryId: number | null = null) => {
    try {
      setLoading(true);
      const categoryQuery = categoryId ? `&category_id=${categoryId}` : '';
      const response = await fetch(`http://0.0.0.0:8000/products/?keyword=${keyword}&page=${page}&limit=${limit}${categoryQuery}`);
      const data = await response.json();
      setProducts(data.products);  // Update with products array from backend
      setTotalPages(data.total_pages);  // Set totalPages from the response
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  // Initial load of categories and products
  useEffect(() => {
    fetchCategories();
  }, []);

  useEffect(() => {
    fetchProducts(currentPage, searchTerm, selectedCategory);
  }, [currentPage, searchTerm, selectedCategory]);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(prev => prev - 1);
    }
  };

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(prev => prev + 1);
    }
  };

  const generatePageNumbers = () => {
    const range: number[] = [];
    const maxPage = totalPages;

    // Display first page and the last page, with the current page in between
    range.push(1);
    if (currentPage > 2) range.push(currentPage - 1);
    range.push(currentPage);
    if (currentPage < maxPage - 1) range.push(currentPage + 1);
    range.push(maxPage);

    // Filter duplicates and return the range
    return [...new Set(range)].filter(page => page > 0 && page <= maxPage);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">ShopEasy</h1>
            <div className="relative">
              <ShoppingCart className="h-6 w-6 text-gray-600" />
            </div>
          </div>
        </div>
      </header>

      {/* Filter and Search Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex flex-col sm:flex-row items-center space-x-4 sm:space-x-6">
          {/* Category Filter */}
          <select
            value={selectedCategory || ''}
            onChange={(e) => {
              setSelectedCategory(Number(e.target.value));
              setCurrentPage(1);  // Reset to first page when filter changes
            }}
            className="border border-gray-300 rounded-lg px-4 py-2 w-full sm:w-auto"
          >
            <option value="">All Categories</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>

          {/* Search Bar */}
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
            <input
              type="text"
              placeholder="Search products..."
              value={searchTerm}
              onChange={handleSearch}
              className="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      {/* Product Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {products.map((product) => (
                <div
                  key={product.id}
                  className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300"
                >
                  <div className="aspect-w-1 aspect-h-1">
                    <img
                      src={product.img_url}
                      alt={product.title}
                      className="w-full h-64 object-cover"
                    />
                  </div>
                  <div className="p-4">
                    <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
                      {product.title}
                    </h3>
                    <div className="mt-2 flex items-center">
                      {Array.from({ length: Math.round(product.stars) }).map((_, i) => (
                        <Star
                          key={i}
                          className="h-5 w-5 text-yellow-400 fill-current"
                        />
                      ))}
                      <span className="ml-2 text-sm text-gray-600">
                        ({product.reviews} reviews)
                      </span>
                    </div>
                    <div className="mt-2">
                      <span className="text-2xl font-bold text-gray-900">
                        ${product.price.toFixed(2)}
                      </span>
                      {product.list_price > product.price && (
                        <span className="ml-2 text-sm text-gray-500 line-through">
                          ${product.list_price.toFixed(2)}
                        </span>
                      )}
                    </div>
                    <button
                      onClick={() => setSelectedProduct(product)}
                      className="mt-4 w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors duration-200"
                    >
                      View Details
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Pagination */}
            <div className="mt-8 flex justify-center items-center space-x-4">
              <button
                onClick={handlePrevPage}
                disabled={currentPage === 1}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg ${
                  currentPage === 1
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                <ChevronLeft className="h-5 w-5" />
                <span>Previous</span>
              </button>

              {generatePageNumbers().map(page => (
                <button
                  key={page}
                  onClick={() => setCurrentPage(page)}
                  className={`px-4 py-2 rounded-lg ${
                    currentPage === page
                      ? 'bg-blue-600 text-white'
                      : 'bg-white text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  {page}
                </button>
              ))}

              <button
                onClick={handleNextPage}
                disabled={currentPage === totalPages}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg ${
                  currentPage === totalPages
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                <span>Next</span>
                <ChevronRight className="h-5 w-5" />
              </button>
            </div>
          </>
        )}
      </div>

      {/* Product Modal */}
      {selectedProduct && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-start">
                <h2 className="text-2xl font-bold text-gray-900">
                  {selectedProduct.title}
                </h2>
                <button
                  onClick={() => setSelectedProduct(null)}
                  className="text-gray-400 hover:text-gray-500"
                >
                  <span className="sr-only">Close</span>
                  <svg
                    className="h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
              <div className="mt-6">
                <img
                  src={selectedProduct.img_url}
                  alt={selectedProduct.title}
                  className="w-full h-96 object-contain rounded-lg"
                />
                <div className="mt-4 space-y-4">
                  <p className="text-gray-600">
                    {selectedProduct.description || 'No description available'}
                  </p>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-3xl font-bold text-gray-900">
                        ${selectedProduct.price.toFixed(2)}
                      </p>
                      {selectedProduct.list_price > selectedProduct.price && (
                        <p className="text-sm text-gray-500 line-through">
                          ${selectedProduct.list_price.toFixed(2)}
                        </p>
                      )}
                    </div>
                    <a
                      href={selectedProduct.amazon_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
                    >
                      Buy on Amazon
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
