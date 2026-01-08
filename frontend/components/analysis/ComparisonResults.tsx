'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { BarChart, Bar, LineChart, Line, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { TrendingUp, Zap, Eye } from 'lucide-react'
import type { ComparisonResult } from '@/types'

export default function ComparisonResults({ result }: { result: ComparisonResult }) {
  const modelComparison = result.model_results?.map((r: any) => ({
    model: r.model_name || 'Unknown',
    risk: r.overall_risk_score || 0,
    issues: r.issues?.length || 0
  })) || []

  const confidenceData = result.model_results?.map((r: any) => ({
    model: r.model_name?.split('-')[0] || 'Model',
    confidence: r.issues?.length > 0
      ? (r.issues.reduce((sum: number, i: any) => sum + (i.confidence || 0), 0) / r.issues.length * 100)
      : 0
  })) || []

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
          <p className="text-sm text-gray-400 mb-2">Models Compared</p>
          <p className="text-3xl font-bold text-white">{modelComparison.length}</p>
        </motion.div>

        <motion.div
          whileHover={{ y: -5 }}
          className="glass rounded-xl p-6 border border-white/10"
        >
          <p className="text-sm text-gray-400 mb-2">Average Risk</p>
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
          <p className="text-sm text-gray-400 mb-2">Total Issues</p>
          <p className="text-3xl font-bold text-white">{modelComparison.reduce((sum, m) => sum + m.issues, 0)}</p>
        </motion.div>
      </div>

      {/* Comparison Charts */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Risk Scores */}
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
            <BarChart data={modelComparison}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="model" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }} />
              <Bar dataKey="risk" fill="#3b82f6" radius={[8, 8, 0, 0]} />
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
            <LineChart data={modelComparison}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="model" stroke="#94a3b8" />
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
        <ResponsiveContainer width="100%" height={400}>
          <RadarChart data={confidenceData}>
            <PolarGrid stroke="#334155" />
            <PolarAngleAxis dataKey="model" stroke="#94a3b8" />
            <PolarRadiusAxis angle={90} domain={[0, 100]} stroke="#94a3b8" />
            <Radar name="Confidence %" dataKey="confidence" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.6} />
            <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }} />
            <Legend />
          </RadarChart>
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
            className="glass rounded-xl p-6 border border-white/10"
          >
            <h4 className="font-semibold text-white mb-3">{modelResult.model_name}</h4>
            <div className="grid md:grid-cols-3 gap-4 mb-4">
              <div>
                <p className="text-xs text-gray-400">Risk Score</p>
                <p className="text-xl font-bold text-white">{modelResult.overall_risk_score?.toFixed(1) || 'N/A'}/10</p>
              </div>
              <div>
                <p className="text-xs text-gray-400">Issues Found</p>
                <p className="text-xl font-bold text-white">{modelResult.issues?.length || 0}</p>
              </div>
              <div>
                <p className="text-xs text-gray-400">Response Time</p>
                <p className="text-xl font-bold text-white">{modelResult.response_time?.toFixed(2) || 'N/A'}s</p>
              </div>
            </div>
            {modelResult.issues?.length > 0 && (
              <div>
                <p className="text-sm font-semibold text-gray-300 mb-2">Top Issues:</p>
                <div className="space-y-2">
                  {modelResult.issues.slice(0, 3).map((issue: any, i: number) => (
                    <div key={i} className="flex items-start gap-2 text-sm">
                      <span className="text-blue-400">→</span>
                      <span className="text-gray-400">{issue.title}</span>
                    </div>
                  ))}
                </div>
              </div>
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
          <h3 className="font-semibold text-purple-400 mb-3">🔮 Consensus Insights</h3>
          <p className="text-gray-300">{result.consensus_insights}</p>
        </motion.div>
      )}
    </motion.div>
  )
}
