export interface Issue {
  title: string
  description: string
  category: string
  risk_level: 'High' | 'Medium' | 'Low'
  confidence: number
  potential_impact: string
  recommendations: string[]
  legal_citation?: string
  urgency: string
}

export interface AnalysisResult {
  issues: Issue[]
  overall_risk_score: number
  document_type: string
  compliance_flags: string[]
  positive_aspects: string[]
  tokens_used?: number
  response_time?: number
}

export interface ModelAnalysisResult extends AnalysisResult {
  model_name: string
}

export interface ComparisonResult {
  model_results: ModelAnalysisResult[]
  consensus_insights?: string
  best_match?: string
  response_time?: number
}
