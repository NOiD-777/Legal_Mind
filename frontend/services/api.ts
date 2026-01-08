import axios from 'axios'
import type { AnalysisResult, ComparisonResult } from '@/types'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
})

export const analyzeDocument = async (
  file: File,
  depth: string,
  focusAreas: string[],
  model: string
): Promise<AnalysisResult> => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('analysis_depth', depth)
  formData.append('focus_areas', JSON.stringify(focusAreas))
  formData.append('model', model)

  const response = await api.post('/analyze', formData)
  return response.data
}

export const compareModels = async (
  file: File,
  depth: string,
  focusAreas: string[],
  models: string[]
): Promise<ComparisonResult> => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('analysis_depth', depth)
  formData.append('focus_areas', JSON.stringify(focusAreas))
  formData.append('models', JSON.stringify(models))

  const response = await api.post('/compare', formData)
  return response.data
}

export default api
