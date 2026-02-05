/**
 * Type definitions and interfaces for DAWMS automation
 * Provides strong typing for drug submission workflows
 */

export interface BrowserConfig {
  browserType: 'chromium' | 'firefox' | 'webkit';
  headless: boolean;
  viewport?: { width: number; height: number };
  slowMo?: number;
  video?: boolean;
  screenshot?: boolean;
}

export interface SubmissionData {
  submissionType: string;
  applicationNumber: string;
  sponsorName?: string;
  drugName?: string;
  priority?: 'Standard' | 'Priority' | 'Fast Track';
}

export interface ReviewerData {
  role: string;
  name: string;
  specialty?: string;
  experience?: string;
}

export interface SignerData {
  name: string;
  role: string;
  level?: number;
}

export enum SubmissionStatus {
  Draft = 'Draft',
  Submitted = 'Submitted',
  UnderReview = 'Under Review',
  PendingSignature = 'Pending Signature',
  Approved = 'Approved',
  Rejected = 'Rejected'
}

export enum SubmissionType {
  NDA = 'NDA',
  ANDA = 'ANDA',
  BLA = 'BLA',
  IND = 'IND'
}

export enum MilestoneType {
  IntakeCreated = 'Intake Created',
  ReviewerAssigned = 'Reviewer Assigned',
  ReviewInProgress = 'Review In Progress',
  SignatureRouting = 'Signature Routing',
  Completed = 'Completed'
}

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
  warnings?: string[];
}

export interface WorkflowResult {
  status: string;
  milestone: string;
  timestamp: Date;
  submissionId?: string;
  message?: string;
}
