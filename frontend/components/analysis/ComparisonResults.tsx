'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { BarChart, Bar, LineChart, Line, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { TrendingUp, Zap, Eye, Sparkles, ArrowRight } from 'lucide-react'
import type { ComparisonResult } from '@/types'

export default function ComparisonResults({ result }: { result: ComparisonResult }) {
  // Helper function to get short model name
  const getShortModelName = (modelName: string) => {
    const nameMap: Record<string, string> = {
      'gemini-3-pro-preview': 'Gemini 3 Pro',
      'gemini-3-flash-preview': 'Gemini 3 Flash',
      'gemini-2.5-flash': 'Gemini 2.5 Flash',
      'gemini-2.5-flash-lite': 'Gemini 2.5 Lite',
      'gemini-2.5-pro': 'Gemini 2.5 Pro',
      'claude-3-5-sonnet-20241022': 'Claude 3.5 Sonnet',
      'claude-3-5-haiku-20241022': 'Claude 3.5 Haiku',
      'llama-3.1-8b-instant': 'Llama 3.1 8B',
    }
    return nameMap[modelName] || modelName.split('-').slice(0, 2).join(' ')
  }

  const modelComparison = result.model_results?.filter((r: any) => !r.error).map((r: any) => ({
    model: getShortModelName(r.analysis_metadata?.model_used || r.model_name || 'Unknown'),
    risk: r.overall_risk_score || 0,
    issues: r.issues?.length || 0
  })) || [];

  const confidenceData = result.model_results?.filter((r: any) => !r.error).map((r: any) => ({
    model: getShortModelName(r.analysis_metadata?.model_used || r.model_name || 'Unknown'),
    confidence: r.issues?.length > 0
      ? (r.issues.reduce((sum: number, i: any) => sum + (i.confidence || 0), 0) / r.issues.length * 100)
      : 0
  })) || [];

  const useRadar = confidenceData.length >= 3;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      {/* Summary */}
      <div className="grid md:grid-cols-3 gap-4">
        <motion.div
          whileHover={{ y: -5 }}
          className="glass rounded-xl p-6 border border-white/10"
        >
          <p className="text-sm text-white/70 mb-2">Models Compared</p>
          <p className="text-3xl font-bold text-white">{modelComparison.length}</p>
        </motion.div>

        <motion.div
          whileHover={{ y: -5 }}
          className="glass rounded-xl p-6 border border-white/10"
        >
          <p className="text-sm text-white/70 mb-2">Average Risk</p>
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="text-3xl font-bold gradient-text"
          >
            {(modelComparison.reduce((sum, m) => sum + m.risk, 0) / modelComparison.length).toFixed(1)}/10
          </motion.div>
        </motion.div>

        <motion.div
          whileHover={{ y: -5 }}
          className="glass rounded-xl p-6 border border-white/10"
        >
          <p className="text-sm text-white/70 mb-2">Total Issues</p>
          <p className="text-3xl font-bold text-white">{modelComparison.reduce((sum, m) => sum + m.issues, 0)}</p>
        </motion.div>
      </div>

      {/* Comparison Charts */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Risk Scores (Bar Chart) */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass rounded-xl p-6 border border-white/10"
        >
          <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            Risk Score Comparison
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={modelComparison} margin={{ top: 5, right: 20, bottom: 40, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis 
                dataKey="model" 
                stroke="#94a3b8" 
                tick={{ fill: '#94a3b8', fontSize: 11 }} 
                angle={-15}
                textAnchor="end"
                height={60}
              />
              <YAxis domain={[0, 10]} stroke="#94a3b8" tick={{ fill: '#94a3b8' }} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
                formatter={(value: any) => [`${Number(value).toFixed(1)}/10`, 'Risk Score']}
              />
              <Bar dataKey="risk" fill="#a855f7" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Issues Found */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass rounded-xl p-6 border border-white/10"
        >
          <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
            <Eye className="w-5 h-5" />
            Issues Identified
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={modelComparison} margin={{ top: 5, right: 20, bottom: 40, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis 
                dataKey="model" 
                stroke="#94a3b8" 
                tick={{ fill: '#94a3b8', fontSize: 11 }}
                angle={-15}
                textAnchor="end"
                height={60}
              />
              <YAxis stroke="#94a3b8" />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }} />
              <Line type="monotone" dataKey="issues" stroke="#10b981" strokeWidth={2} dot={{ fill: '#10b981' }} />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Confidence Radar */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-xl p-6 border border-white/10"
      >
        <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
          <Zap className="w-5 h-5" />
          Model Confidence Levels
        </h3>
        <ResponsiveContainer width="100%" height={450}>
          {useRadar ? (
            <RadarChart data={confidenceData} margin={{ top: 20, right: 80, bottom: 20, left: 80 }}>
              <PolarGrid stroke="#334155" />
              <PolarAngleAxis 
                dataKey="model" 
                stroke="#94a3b8" 
                tick={{ fill: '#94a3b8', fontSize: 10 }}
              />
              <PolarRadiusAxis angle={90} domain={[0, 100]} stroke="#94a3b8" />
              <Radar name="Confidence %" dataKey="confidence" stroke="#a855f7" fill="#a855f7" fillOpacity={0.6} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
                formatter={(value: any) => [`${value.toFixed(1)}%`, 'Confidence']}
              />
              <Legend />
            </RadarChart>
          ) : (
            <BarChart data={confidenceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="model" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} />
              <YAxis domain={[0, 100]} stroke="#94a3b8" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
                formatter={(value: any) => [`${Number(value).toFixed(1)}%`, 'Confidence']}
              />
              <Bar dataKey="confidence" fill="#a855f7" radius={[8, 8, 0, 0]} />
            </BarChart>
          )}
        </ResponsiveContainer>
      </motion.div>

      {/* Model Details */}
      <div className="space-y-4">
        <h3 className="text-xl font-semibold text-white">Model Analysis Details</h3>
        {result.model_results?.map((modelResult: any, idx: number) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className={`glass rounded-xl p-6 border ${modelResult.error ? 'border-red-500/50 bg-red-500/5' : 'border-white/10'}`}
          >
            <div className="flex items-center justify-between mb-3">
              <h4 className="font-semibold text-white">{modelResult.model_name}</h4>
              {modelResult.error && (
                <span className="px-3 py-1 bg-red-500/20 text-red-400 text-xs font-semibold rounded-full border border-red-500/50">
                  FAILED
                </span>
              )}
            </div>
            {modelResult.error ? (
              <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4">
                <p className="text-sm text-red-400 font-medium mb-1">Analysis Failed</p>
                <p className="text-xs text-red-300/70">{modelResult.error}</p>
              </div>
            ) : (
            <>
              <div className="grid md:grid-cols-3 gap-4 mb-4">
                <div>
                  <p className="text-xs text-white/70">Risk Score</p>
                  <p className="text-xl font-bold text-white">{modelResult.overall_risk_score?.toFixed(1) || 'N/A'}/10</p>
                </div>
                <div>
                  <p className="text-xs text-white/70">Issues Found</p>
                  <p className="text-xl font-bold text-white">{modelResult.issues?.length || 0}</p>
                </div>
                <div>
                  <p className="text-xs text-white/70">Response Time</p>
                  <p className="text-xl font-bold text-white">{modelResult.response_time?.toFixed(2) || 'N/A'}s</p>
                </div>
              </div>
              {modelResult.issues?.length > 0 && (
                <div>
                  <p className="text-sm font-semibold text-white/80 mb-2">Top Issues:</p>
                  <div className="space-y-2">
                    {modelResult.issues.slice(0, 3).map((issue: any, i: number) => (
                      <div key={i} className="flex items-start gap-2 text-sm">
                        <ArrowRight className="w-4 h-4 text-primary-400 mt-0.5 flex-shrink-0" />
                        <span className="text-white/70">{issue.title}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
            )}
          </motion.div>
        ))}
      </div>

      {/* Consensus Insights */}
      {result.consensus_insights && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-xl p-6 border border-purple-500/30 bg-purple-500/5"
        >
          <h3 className="font-semibold text-purple-400 mb-3 flex items-center gap-2">
            <Sparkles className="w-5 h-5" />
            Consensus Insights
          </h3>
          <p className="text-white/80">{result.consensus_insights}</p>
        </motion.div>
      )}
    </motion.div>
  )
}
