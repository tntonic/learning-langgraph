import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import TenantSearchForm from './components/TenantSearchForm';
import ResearchResults from './components/ResearchResults';
import WorkflowProgress from './components/WorkflowProgress';
import { TenantResearchResult, ResearchStep } from './types';
import { FaBuilding } from 'react-icons/fa';
import api from './services/api';

function App() {
  const [isSearching, setIsSearching] = useState(false);
  const [currentStep, setCurrentStep] = useState<ResearchStep | null>(null);
  const [results, setResults] = useState<TenantResearchResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (companyName: string, location: string) => {
    setIsSearching(true);
    setResults(null);
    setError(null);
    
    try {
      await api.startResearch(
        { companyName, location },
        // Progress callback
        (progress) => {
          setCurrentStep({
            id: progress.stepId,
            name: progress.stepName,
            status: progress.status
          });
        },
        // Complete callback
        (result) => {
          setResults(result);
          setIsSearching(false);
        },
        // Error callback
        (err) => {
          setError(err.message);
          setIsSearching(false);
        }
      );
    } catch (err) {
      setError('Failed to start research');
      setIsSearching(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center space-x-3">
            <FaBuilding className="text-blue-600 text-3xl" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Faropoint Tenant Research</h1>
              <p className="text-sm text-gray-600">AI-Powered Commercial Tenant Analysis</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Search Form */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Research New Tenant</h2>
              <TenantSearchForm onSearch={handleSearch} isSearching={isSearching} />
            </div>

            {/* Workflow Progress */}
            <AnimatePresence>
              {isSearching && currentStep && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="mt-6"
                >
                  <WorkflowProgress currentStep={currentStep} />
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Results */}
          <div className="lg:col-span-2">
            <AnimatePresence>
              {results && (
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                >
                  <ResearchResults results={results} />
                </motion.div>
              )}
            </AnimatePresence>

            {!results && !isSearching && (
              <div className="bg-white rounded-lg shadow-md p-12 text-center">
                <FaBuilding className="text-gray-300 text-6xl mx-auto mb-4" />
                <h3 className="text-xl font-medium text-gray-900 mb-2">No Research Yet</h3>
                <p className="text-gray-600">Enter a company name and location to begin tenant analysis</p>
              </div>
            )}

            {isSearching && (
              <div className="bg-white rounded-lg shadow-md p-12 text-center">
                <div className="animate-pulse">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
                    <div className="w-8 h-8 bg-blue-600 rounded-full animate-ping"></div>
                  </div>
                  <h3 className="text-xl font-medium text-gray-900 mb-2">Researching Tenant...</h3>
                  <p className="text-gray-600">Analyzing multiple data sources</p>
                </div>
              </div>
            )}

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-red-800 mb-2">Research Error</h3>
                <p className="text-red-600">{error}</p>
                <button
                  onClick={() => setError(null)}
                  className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                >
                  Dismiss
                </button>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;