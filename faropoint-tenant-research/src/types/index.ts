export interface TenantResearchResult {
  companyName: string;
  location: string;
  industry: string;
  recommendation: 'Highly Recommended' | 'Recommended' | 'Proceed with Caution' | 'Not Recommended';
  overallScore: number;
  scores: {
    stability: number;
    growth: number;
    risk: number;
    reputation: number;
  };
  keyMetrics: {
    yearsInBusiness: number;
    businessType: string;
    verified: boolean;
    revenue: string;
    employees: string;
    currentLocations: number;
  };
  strengths: string[];
  concerns: string[];
  confidenceLevel: number;
  dataSources: number;
}

export interface ResearchStep {
  id: string;
  name: string;
  status: 'pending' | 'active' | 'completed';
}