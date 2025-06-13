import React, { useState } from 'react';
import { FaSearch, FaMapMarkerAlt, FaBuilding } from 'react-icons/fa';
import { motion } from 'framer-motion';

interface TenantSearchFormProps {
  onSearch: (companyName: string, location: string) => void;
  isSearching: boolean;
}

const TenantSearchForm: React.FC<TenantSearchFormProps> = ({ onSearch, isSearching }) => {
  const [companyName, setCompanyName] = useState('');
  const [location, setLocation] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (companyName.trim() && location.trim()) {
      onSearch(companyName.trim(), location.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          <FaBuilding className="inline mr-2 text-gray-400" />
          Company Name
        </label>
        <input
          type="text"
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="e.g., Blue Bottle Coffee"
          disabled={isSearching}
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          <FaMapMarkerAlt className="inline mr-2 text-gray-400" />
          Location
        </label>
        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="e.g., San Francisco, CA"
          disabled={isSearching}
          required
        />
      </div>

      <motion.button
        type="submit"
        disabled={isSearching}
        whileHover={{ scale: isSearching ? 1 : 1.02 }}
        whileTap={{ scale: isSearching ? 1 : 0.98 }}
        className={`w-full py-3 px-4 rounded-lg font-medium transition-colors ${
          isSearching
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-blue-600 text-white hover:bg-blue-700'
        }`}
      >
        {isSearching ? (
          <span className="flex items-center justify-center">
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Researching...
          </span>
        ) : (
          <span className="flex items-center justify-center">
            <FaSearch className="mr-2" />
            Research Tenant
          </span>
        )}
      </motion.button>

      <div className="mt-4 p-4 bg-blue-50 rounded-lg">
        <p className="text-sm text-blue-800">
          <strong>Tip:</strong> Our AI analyzes online presence, financial indicators, business verification, and risk factors to provide comprehensive tenant evaluation.
        </p>
      </div>
    </form>
  );
};

export default TenantSearchForm;