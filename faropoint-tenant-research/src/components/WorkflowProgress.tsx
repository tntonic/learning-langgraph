import React from 'react';
import { motion } from 'framer-motion';
import { FaCheckCircle, FaCircle, FaSpinner } from 'react-icons/fa';
import { ResearchStep } from '../types';

interface WorkflowProgressProps {
  currentStep: ResearchStep;
}

const workflowSteps: ResearchStep[] = [
  { id: 'identify', name: 'Company Identification', status: 'pending' },
  { id: 'online', name: 'Online Presence Analysis', status: 'pending' },
  { id: 'verify', name: 'Business Verification', status: 'pending' },
  { id: 'financial', name: 'Financial Indicators', status: 'pending' },
  { id: 'real_estate', name: 'Real Estate History', status: 'pending' },
  { id: 'risk', name: 'Risk Assessment', status: 'pending' },
  { id: 'score', name: 'Tenant Scoring', status: 'pending' },
  { id: 'report', name: 'Report Generation', status: 'pending' },
];

const WorkflowProgress: React.FC<WorkflowProgressProps> = ({ currentStep }) => {
  const currentIndex = workflowSteps.findIndex(step => step.id === currentStep.id);

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Research Progress</h3>
      <div className="space-y-3">
        {workflowSteps.map((step, index) => {
          const isCompleted = index < currentIndex;
          const isActive = index === currentIndex;
          const isPending = index > currentIndex;

          return (
            <motion.div
              key={step.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="flex items-center space-x-3"
            >
              <div className="flex-shrink-0">
                {isCompleted && (
                  <FaCheckCircle className="text-green-500 text-xl" />
                )}
                {isActive && (
                  <FaSpinner className="text-blue-600 text-xl animate-spin" />
                )}
                {isPending && (
                  <FaCircle className="text-gray-300 text-xl" />
                )}
              </div>
              <div className="flex-grow">
                <p className={`text-sm font-medium ${
                  isActive ? 'text-blue-600' : isCompleted ? 'text-gray-900' : 'text-gray-400'
                }`}>
                  {step.name}
                </p>
              </div>
            </motion.div>
          );
        })}
      </div>
      
      <div className="mt-4 bg-gray-100 rounded-full h-2">
        <motion.div
          className="bg-blue-600 h-2 rounded-full"
          initial={{ width: '0%' }}
          animate={{ width: `${((currentIndex + 1) / workflowSteps.length) * 100}%` }}
          transition={{ duration: 0.5 }}
        />
      </div>
    </div>
  );
};

export default WorkflowProgress;