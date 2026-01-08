'use client'

import React, { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import gsap from 'gsap'
import { Search, Scale } from 'lucide-react'
import DocumentUpload from '@/components/analysis/DocumentUpload'
import AnalysisResults from '@/components/analysis/AnalysisResults'
import ComparisonResults from '@/components/analysis/ComparisonResults'
import { analyzeDocument, compareModels } from '@/services/api'
import type { AnalysisResult, ComparisonResult } from '@/types'

export default function AnalyzePage() {
  const [analysisMode, setAnalysisMode] = useState<'single' | 'compare'>('single')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<AnalysisResult | ComparisonResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // GSAP entrance animation
    if (containerRef.current) {
      gsap.fromTo(
        containerRef.current,
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }
      )
    }
  }, [])

  const handleAnalyze = async (file: File, depth: string, focusAreas: string[], models: string[]) => {
    setLoading(true)
    setError(null)
    
    try {
      let result
      if (analysisMode === 'single') {
        result = await analyzeDocument(file, depth, focusAreas, models[0])
      } else {
        result = await compareModels(file, depth, focusAreas, models)
      }
      
      setResults(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div ref={containerRef} className="min-h-screen bg-transparent py-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl font-bold gradient-text mb-4">
            Legal Document Analysis
          </h1>
          <p className="text-xl text-white/80 max-w-2xl mx-auto">
            Upload your legal documents and get AI-powered risk assessments powered by multiple advanced models
          </p>
        </motion.div>

        {/* Mode Selector */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="flex justify-center gap-4 mb-8"
        >
          {(['single', 'compare'] as const).map((mode) => (
            <button
              key={mode}
              onClick={() => setAnalysisMode(mode)}
              className={`px-8 py-3 rounded-lg font-semibold transition-all flex items-center gap-2 ${
                analysisMode === mode
                  ? 'bg-primary-600 text-white shadow-lg shadow-primary-500/50'
                  : 'bg-white/10 text-white/80 hover:bg-white/20'
              }`}
            >
              {mode === 'single' ? (
                <><Search className="w-4 h-4" /> Single Model</>
              ) : (
                <><Scale className="w-4 h-4" /> Compare Models</>
              )}
            </button>
          ))}
        </motion.div>

        {/* Content */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Upload Section */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3, duration: 0.5 }}
            className="lg:col-span-1"
          >
            <DocumentUpload
              mode={analysisMode}
              onAnalyze={handleAnalyze}
              loading={loading}
            />
          </motion.div>

          {/* Results Section */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4, duration: 0.5 }}
            className="lg:col-span-2"
          >
            {error && (
              <div className="glass rounded-2xl p-6 border-red-500/50 mb-6">
                <p className="text-red-400">{error}</p>
              </div>
            )}
            
            {loading && (
              <div className="glass rounded-2xl p-12 text-center">
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                  className="inline-block mb-4"
                >
                  <div className="w-12 h-12 border-4 border-primary-500/20 border-t-primary-500 rounded-full" />
                </motion.div>
                <p className="text-white/70">Analyzing your document...</p>
              </div>
            )}
            
            {results && !loading && (
              analysisMode === 'single' ? (
                <AnalysisResults result={results as AnalysisResult} />
              ) : (
                <ComparisonResults result={results as ComparisonResult} />
              )
            )}
            
            {!results && !loading && !error && (
              <div className="glass rounded-2xl p-12 text-center">
                <p className="text-white/70">Upload a document to see results here</p>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  )
}
