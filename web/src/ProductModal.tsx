// ProductModal.tsx
import React from 'react';
import { Star } from 'lucide-react';

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

interface ProductModalProps {
  product: Product;
  onClose: () => void;
}

const ProductModal: React.FC<ProductModalProps> = ({ product, onClose }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-start">
            <h2 className="text-2xl font-bold text-gray-900">{product.title}</h2>
            <button onClick={onClose} className="text-gray-400 hover:text-gray-500">
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
              src={product.img_url}
              alt={product.title}
              className="w-full h-96 object-contain rounded-lg"
            />
            <div className="mt-4 space-y-4">
              <p className="text-gray-600">{product.description || 'No description available'}</p>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-3xl font-bold text-gray-900">${product.price.toFixed(2)}</p>
                  {product.list_price > product.price && (
                    <p className="text-sm text-gray-500 line-through">
                      ${product.list_price.toFixed(2)}
                    </p>
                  )}
                </div>
                <div className="flex items-center">
                  {Array.from({ length: Math.round(product.stars) }).map((_, i) => (
                    <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                  ))}
                  <span className="ml-2 text-sm text-gray-600">({product.reviews} reviews)</span>
                </div>
              </div>
              {product.bought_in_last_month && (
                <p className="text-sm text-gray-600">
                  {product.bought_in_last_month} bought in the last month
                </p>
              )}
              <div className="flex space-x-4">
                <a
                  href={product.amazon_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors duration-200 text-center"
                >
                  View on Amazon
                </a>
                <button className="flex-1 bg-gray-100 text-gray-900 py-3 px-4 rounded-lg hover:bg-gray-200 transition-colors duration-200">
                  Add to Cart
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductModal;
