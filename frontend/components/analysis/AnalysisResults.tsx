'use client'

import React, { useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import gsap from 'gsap'
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { AlertCircle, TrendingUp, Eye } from 'lucide-react'
import type { AnalysisResult } from '@/types'

interface IssueDetailProps {
  issue: any
  index: number
}

function IssueDetail({ issue, index }: IssueDetailProps) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (ref.current) {
      gsap.fromTo(
        ref.current,
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.5, delay: index * 0.1, ease: 'power3.out' }
      )
    }
  }, [index])

  const getRiskColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high': return 'text-red-400 bg-red-500/10 border-red-500/30'
      case 'medium': return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30'
      case 'low': return 'text-green-400 bg-green-500/10 border-green-500/30'
      default: return 'text-blue-400 bg-blue-500/10 border-blue-500/30'
    }
  }

  return (
    <motion.div
      ref={ref}
      whileHover={{ x: 5 }}
      className={`glass rounded-xl p-4 border ${getRiskColor(issue.risk_level)} transition-all`}
    >
      <div className="flex items-start gap-4">
        <AlertCircle className="w-5 h-5 flex-shrink-0 mt-1" />
        <div className="flex-1">
          <h4 className="font-semibold text-white mb-1">{issue.title}</h4>
          <p className="text-sm text-gray-400 mb-3">{issue.description}</p>
          <div className="flex flex-wrap gap-2 mb-3">
            <span className="px-2 py-1 rounded bg-white/10 text-xs text-gray-300">
              {issue.category}
            </span>
            <span className="px-2 py-1 rounded bg-white/10 text-xs text-gray-300">
              Confidence: {(issue.confidence * 100).toFixed(0)}%
            </span>
          </div>
          {issue.recommendations && (
            <div>
              <p className="text-xs font-semibold text-gray-400 mb-2">Recommendations:</p>
              <ul className="space-y-1">
                {issue.recommendations.map((rec: string, i: number) => (
                  <li key={i} className="text-xs text-gray-400 flex gap-2">
                    <span>•</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  )
}

export default function AnalysisResults({ result }: { result: AnalysisResult }) {
  const riskData = [
    { name: 'Risk Score', value: result.overall_risk_score, fill: '#ef4444' }
  ]

  const categoryData = (result.issues || []).reduce((acc: any, issue: any) => {
    const cat = issue.category || 'Other'
    const existing = acc.find((a: any) => a.name === cat)
    if (existing) {
      existing.value += 1
    } else {
      acc.push({ name: cat, value: 1 })
    }
    return acc
  }, [])

  const riskLevelData = (result.issues || []).reduce((acc: any, issue: any) => {
    const level = issue.risk_level || 'Medium'
    const existing = acc.find((a: any) => a.name === level)
    if (existing) {
      existing.value += 1
    } else {
      acc.push({ name: level, value: 1 })
    }
    return acc
  }, [])

  const colors = { High: '#ef4444', Medium: '#f59e0b', Low: '#10b981' }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      {/* Summary Cards */}
      <div className="grid md:grid-cols-3 gap-4">
        <motion.div
          whileHover={{ y: -5 }}
          className="glass rounded-xl p-6 border border-white/10"
        >
          <p className="text-sm text-gray-400 mb-2">Overall Risk Score</p>
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring' }}
            className="text-4xl font-bold gradient-text mb-2"
          >
            {result.overall_risk_score.toFixed(1)}/10
          </motion.div>
          <p className="text-xs text-gray-500">
            {result.issues?.length || 0} issues identified
          </p>
        </motion.div>

        <motion.div
          whileHover={{ y: -5 }}
          className="glass rounded-xl p-6 border border-white/10"
        >
          <p className="text-sm text-gray-400 mb-2">Document Type</p>
          <p className="text-xl font-semibold text-white">{result.document_type || 'Unknown'}</p>
        </motion.div>

        <motion.div
          whileHover={{ y: -5 }}
          className="glass rounded-xl p-6 border border-white/10"
        >
          <p className="text-sm text-gray-400 mb-2">Avg Confidence</p>
          <p className="text-xl font-semibold text-white">
            {result.issues && result.issues.length > 0
              ? ((result.issues.reduce((sum: number, i: any) => sum + (i.confidence || 0), 0) / result.issues.length) * 100).toFixed(0)
              : '0'}%
          </p>
        </motion.div>
      </div>

      {/* Charts */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Risk by Category */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className="glass rounded-xl p-6 border border-white/10"
        >
          <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
            <Eye className="w-5 h-5" />
            Issues by Category
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={categoryData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="name" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }} />
              <Bar dataKey="value" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Risk Distribution */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="glass rounded-xl p-6 border border-white/10"
        >
          <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            Risk Distribution
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={riskLevelData} cx="50%" cy="50%" labelLine={false} label outerRadius={80} fill="#8884d8" dataKey="value">
                {riskLevelData.map((entry: any, index: number) => (
                  <Cell key={`cell-${index}`} fill={(colors as any)[entry.name] || '#3b82f6'} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }} />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Issues */}
      <div>
        <h3 className="text-xl font-semibold text-white mb-4">Identified Issues</h3>
        <div className="space-y-3">
          {result.issues && result.issues.length > 0 ? (
            result.issues.map((issue: any, i: number) => (
              <IssueDetail key={i} issue={issue} index={i} />
            ))
          ) : (
            <p className="text-gray-400">No issues identified</p>
          )}
        </div>
      </div>

      {/* Positive Aspects */}
      {result.positive_aspects && result.positive_aspects.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-xl p-6 border border-green-500/30 bg-green-500/5"
        >
          <h3 className="font-semibold text-green-400 mb-3">✅ Positive Aspects</h3>
          <ul className="space-y-2">
            {result.positive_aspects.map((aspect: string, i: number) => (
              <li key={i} className="text-sm text-gray-300 flex gap-2">
                <span>→</span>
                <span>{aspect}</span>
              </li>
            ))}
          </ul>
        </motion.div>
      )}
    </motion.div>
  )
}
