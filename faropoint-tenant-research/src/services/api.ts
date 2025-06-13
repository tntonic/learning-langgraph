import axios from 'axios';
import { TenantResearchResult } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface ResearchRequest {
  companyName: string;
  location: string;
}

export interface ResearchProgress {
  stepId: string;
  stepName: string;
  status: 'pending' | 'active' | 'completed';
  message?: string;
}

class TenantResearchAPI {
  private eventSource: EventSource | null = null;

  async startResearch(
    request: ResearchRequest,
    onProgress: (progress: ResearchProgress) => void,
    onComplete: (result: TenantResearchResult) => void,
    onError: (error: Error) => void
  ): Promise<void> {
    try {
      // For demo purposes, we'll simulate the API call
      // In production, this would connect to the LangGraph backend
      
      const steps = [
        'Company Identification',
        'Online Presence Analysis',
        'Business Verification',
        'Financial Indicators',
        'Real Estate History',
        'Risk Assessment',
        'Tenant Scoring',
        'Report Generation'
      ];

      // Simulate step-by-step progress
      for (let i = 0; i < steps.length; i++) {
        onProgress({
          stepId: steps[i].toLowerCase().replace(/\s+/g, '_'),
          stepName: steps[i],
          status: 'active',
          message: `Processing ${steps[i]}...`
        });

        await new Promise(resolve => setTimeout(resolve, 1500));

        onProgress({
          stepId: steps[i].toLowerCase().replace(/\s+/g, '_'),
          stepName: steps[i],
          status: 'completed',
          message: `${steps[i]} completed`
        });
      }

      // Simulate final result
      const mockResult: TenantResearchResult = {
        companyName: request.companyName,
        location: request.location,
        industry: this.getRandomIndustry(),
        recommendation: this.getRandomRecommendation(),
        overallScore: Math.floor(Math.random() * 40) + 60,
        scores: {
          stability: Math.random() * 0.4 + 0.6,
          growth: Math.random() * 0.4 + 0.5,
          risk: Math.random() * 0.3 + 0.1,
          reputation: Math.random() * 0.3 + 0.7
        },
        keyMetrics: {
          yearsInBusiness: Math.floor(Math.random() * 15) + 1,
          businessType: this.getRandomBusinessType(),
          verified: Math.random() > 0.3,
          revenue: this.getRandomRevenue(),
          employees: this.getRandomEmployees(),
          currentLocations: Math.floor(Math.random() * 5) + 1
        },
        strengths: this.getRandomStrengths(),
        concerns: this.getRandomConcerns(),
        confidenceLevel: Math.random() * 0.2 + 0.8,
        dataSources: Math.floor(Math.random() * 5) + 5
      };

      onComplete(mockResult);
    } catch (error) {
      onError(error as Error);
    }
  }

  // In production, this would make a real API call:
  async startResearchReal(
    request: ResearchRequest,
    onProgress: (progress: ResearchProgress) => void,
    onComplete: (result: TenantResearchResult) => void,
    onError: (error: Error) => void
  ): Promise<void> {
    try {
      // Start the research job
      const response = await axios.post(`${API_BASE_URL}/api/research`, request);
      const { jobId } = response.data;

      // Connect to SSE endpoint for progress updates
      this.eventSource = new EventSource(`${API_BASE_URL}/api/research/${jobId}/progress`);

      this.eventSource.addEventListener('progress', (event) => {
        const progress = JSON.parse(event.data);
        onProgress(progress);
      });

      this.eventSource.addEventListener('complete', (event) => {
        const result = JSON.parse(event.data);
        onComplete(result);
        this.disconnect();
      });

      this.eventSource.addEventListener('error', (event) => {
        onError(new Error('Research failed'));
        this.disconnect();
      });
    } catch (error) {
      onError(error as Error);
      this.disconnect();
    }
  }

  disconnect(): void {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }

  // Helper methods for mock data
  private getRandomIndustry(): string {
    const industries = ['Technology', 'Food & Beverage', 'Retail', 'Healthcare', 'Professional Services'];
    return industries[Math.floor(Math.random() * industries.length)];
  }

  private getRandomRecommendation(): TenantResearchResult['recommendation'] {
    const recommendations: TenantResearchResult['recommendation'][] = [
      'Highly Recommended',
      'Recommended',
      'Proceed with Caution',
      'Not Recommended'
    ];
    const weights = [0.2, 0.5, 0.25, 0.05];
    const random = Math.random();
    let sum = 0;
    for (let i = 0; i < weights.length; i++) {
      sum += weights[i];
      if (random < sum) return recommendations[i];
    }
    return recommendations[1];
  }

  private getRandomBusinessType(): string {
    const types = ['LLC', 'Corporation', 'Partnership', 'Sole Proprietorship'];
    return types[Math.floor(Math.random() * types.length)];
  }

  private getRandomRevenue(): string {
    const revenues = ['Under $1M', '$1-5M', '$5-10M', '$10-50M', '$50M+'];
    return revenues[Math.floor(Math.random() * revenues.length)];
  }

  private getRandomEmployees(): string {
    const employees = ['1-10', '10-50', '50-100', '100-500', '500+'];
    return employees[Math.floor(Math.random() * employees.length)];
  }

  private getRandomStrengths(): string[] {
    const allStrengths = [
      'Strong online reputation',
      'Verified business entity',
      'Consistent growth trajectory',
      'Multiple existing locations',
      'Established market presence',
      'Strong financial indicators',
      'Positive customer reviews',
      'Industry leader',
      'Stable management team'
    ];
    const count = Math.floor(Math.random() * 3) + 2;
    return allStrengths.sort(() => Math.random() - 0.5).slice(0, count);
  }

  private getRandomConcerns(): string[] {
    const allConcerns = [
      'Limited financial history',
      'High employee turnover',
      'Recent negative reviews',
      'Pending litigation',
      'Market volatility',
      'New to the area',
      'Regulatory compliance issues',
      'Limited online presence'
    ];
    const count = Math.floor(Math.random() * 2) + 1;
    return allConcerns.sort(() => Math.random() - 0.5).slice(0, count);
  }
}

export default new TenantResearchAPI();