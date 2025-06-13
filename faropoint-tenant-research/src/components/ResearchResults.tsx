import React from 'react';
import { motion } from 'framer-motion';
import { TenantResearchResult } from '../types';
import { 
  FaCheckCircle, FaExclamationTriangle, FaTimesCircle, 
  FaChartLine, FaShieldAlt, FaStar, FaBuilding,
  FaCalendarAlt, FaDollarSign, FaUsers, FaMapMarkerAlt
} from 'react-icons/fa';
import { RadialBarChart, RadialBar, ResponsiveContainer, PolarAngleAxis } from 'recharts';

interface ResearchResultsProps {
  results: TenantResearchResult;
}

const ResearchResults: React.FC<ResearchResultsProps> = ({ results }) => {
  const getRecommendationColor = (recommendation: string) => {
    switch (recommendation) {
      case 'Highly Recommended':
        return 'text-green-600 bg-green-50';
      case 'Recommended':
        return 'text-blue-600 bg-blue-50';
      case 'Proceed with Caution':
        return 'text-yellow-600 bg-yellow-50';
      case 'Not Recommended':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return '#10b981'; // green
    if (score >= 60) return '#3b82f6'; // blue
    if (score >= 40) return '#f59e0b'; // yellow
    return '#ef4444'; // red
  };

  const scoreData = [{
    name: 'Score',
    value: results.overallScore,
    fill: getScoreColor(results.overallScore)
  }];

  return (
    <div className="space-y-6">
      {/* Header Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-lg shadow-md p-6"
      >
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{results.companyName}</h2>
            <p className="text-gray-600 mt-1">{results.location} • {results.industry}</p>
          </div>
          <span className={`px-4 py-2 rounded-full text-sm font-medium ${getRecommendationColor(results.recommendation)}`}>
            {results.recommendation}
          </span>
        </div>

        {/* Overall Score */}
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="flex items-center">
            <div className="w-32 h-32">
              <ResponsiveContainer width="100%" height="100%">
                <RadialBarChart cx="50%" cy="50%" innerRadius="60%" outerRadius="90%" data={scoreData}>
                  <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
                  <RadialBar dataKey="value" cornerRadius={10} fill={getScoreColor(results.overallScore)} />
                  <text x="50%" y="50%" textAnchor="middle" dominantBaseline="middle" className="fill-gray-900">
                    <tspan className="text-3xl font-bold">{results.overallScore.toFixed(0)}</tspan>
                    <tspan className="text-sm" x="50%" dy="1.5em">/100</tspan>
                  </text>
                </RadialBarChart>
              </ResponsiveContainer>
            </div>
            <div className="ml-6">
              <h3 className="text-lg font-semibold text-gray-900">Tenant Score</h3>
              <p className="text-sm text-gray-600 mt-1">
                Based on {results.dataSources} data sources
              </p>
              <p className="text-sm text-gray-600">
                {(results.confidenceLevel * 100).toFixed(0)}% confidence level
              </p>
            </div>
          </div>

          {/* Key Metrics */}
          <div className="grid grid-cols-2 gap-4">
            <div className="flex items-center space-x-2">
              <FaCalendarAlt className="text-gray-400" />
              <div>
                <p className="text-sm text-gray-600">Years in Business</p>
                <p className="font-semibold">{results.keyMetrics.yearsInBusiness}</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <FaDollarSign className="text-gray-400" />
              <div>
                <p className="text-sm text-gray-600">Revenue</p>
                <p className="font-semibold">{results.keyMetrics.revenue}</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <FaUsers className="text-gray-400" />
              <div>
                <p className="text-sm text-gray-600">Employees</p>
                <p className="font-semibold">{results.keyMetrics.employees}</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <FaMapMarkerAlt className="text-gray-400" />
              <div>
                <p className="text-sm text-gray-600">Locations</p>
                <p className="font-semibold">{results.keyMetrics.currentLocations}</p>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Score Breakdown */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white rounded-lg shadow-md p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Score Breakdown</h3>
        <div className="space-y-4">
          <ScoreBar icon={<FaShieldAlt />} label="Stability" value={results.scores.stability} />
          <ScoreBar icon={<FaChartLine />} label="Growth Potential" value={results.scores.growth} />
          <ScoreBar icon={<FaExclamationTriangle />} label="Risk Level" value={1 - results.scores.risk} inverted />
          <ScoreBar icon={<FaStar />} label="Reputation" value={results.scores.reputation} />
        </div>
      </motion.div>

      {/* Strengths and Concerns */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-lg shadow-md p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <FaCheckCircle className="text-green-500 mr-2" />
            Strengths
          </h3>
          <ul className="space-y-2">
            {results.strengths.map((strength, index) => (
              <li key={index} className="flex items-start">
                <span className="text-green-500 mr-2">•</span>
                <span className="text-gray-700 text-sm">{strength}</span>
              </li>
            ))}
          </ul>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-lg shadow-md p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <FaExclamationTriangle className="text-yellow-500 mr-2" />
            Concerns
          </h3>
          <ul className="space-y-2">
            {results.concerns.map((concern, index) => (
              <li key={index} className="flex items-start">
                <span className="text-yellow-500 mr-2">•</span>
                <span className="text-gray-700 text-sm">{concern}</span>
              </li>
            ))}
          </ul>
        </motion.div>
      </div>

      {/* Business Verification */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-white rounded-lg shadow-md p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Business Verification</h3>
        <div className="flex items-center space-x-4">
          <div className={`flex items-center space-x-2 px-3 py-1 rounded-full ${
            results.keyMetrics.verified ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          }`}>
            {results.keyMetrics.verified ? <FaCheckCircle /> : <FaTimesCircle />}
            <span className="text-sm font-medium">
              {results.keyMetrics.verified ? 'Verified' : 'Not Verified'}
            </span>
          </div>
          <span className="text-gray-600">
            {results.keyMetrics.businessType} • {results.industry}
          </span>
        </div>
      </motion.div>
    </div>
  );
};

const ScoreBar: React.FC<{
  icon: React.ReactNode;
  label: string;
  value: number;
  inverted?: boolean;
}> = ({ icon, label, value, inverted }) => {
  const getBarColor = (val: number) => {
    if (val >= 0.8) return 'bg-green-500';
    if (val >= 0.6) return 'bg-blue-500';
    if (val >= 0.4) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="flex items-center space-x-3">
      <div className="text-gray-400">{icon}</div>
      <div className="flex-grow">
        <div className="flex justify-between mb-1">
          <span className="text-sm font-medium text-gray-700">{label}</span>
          <span className="text-sm text-gray-600">{(value * 100).toFixed(0)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <motion.div
            className={`h-2 rounded-full ${getBarColor(value)}`}
            initial={{ width: 0 }}
            animate={{ width: `${value * 100}%` }}
            transition={{ duration: 0.5, delay: 0.2 }}
          />
        </div>
      </div>
    </div>
  );
};

export default ResearchResults;