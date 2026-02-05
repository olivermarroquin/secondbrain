/**
 * Type definitions and interfaces for CBAPS automation
 * Provides strong typing for better IDE support and type safety
 */

export interface BrowserConfig {
  browserType: 'chromium' | 'firefox' | 'webkit';
  headless: boolean;
  viewport?: { width: number; height: number };
  slowMo?: number;
  video?: boolean;
  screenshot?: boolean;
}

export interface RequisitionData {
  title: string;
  fundType: string;
  description?: string;
  priority?: 'Low' | 'Medium' | 'High' | 'Critical';
}

export interface FundingLineData {
  amount: string;
  fiscalYear?: string;
  category?: string;
  description?: string;
}

export interface ApproverData {
  name: string;
  role: string;
  level?: number;
}

export enum RequisitionStatus {
  Draft = 'Draft',
  Submitted = 'Submitted',
  InReview = 'In Review',
  Approved = 'Approved',
  Rejected = 'Rejected',
  Cancelled = 'Cancelled'
}

export enum FundType {
  Operations = 'Operations',
  Technology = 'Technology',
  Facilities = 'Facilities',
  Research = 'Research',
  Training = 'Training'
}

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
  warnings?: string[];
}

export interface WorkflowResult {
  status: string;
  timestamp: Date;
  requisitionId?: string;
  message?: string;
}
