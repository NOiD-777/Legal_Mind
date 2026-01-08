'use client'

import React, { useState, useRef, useCallback } from 'react'
import { motion } from 'framer-motion'
import { Upload, FileText, Trash2 } from 'lucide-react'

interface DocumentUploadProps {
  mode: 'single' | 'compare'
  onAnalyze: (file: File, depth: string, focusAreas: string[], models: string[]) => void
  loading: boolean
}

const MODELS = {
  gemini: ['gemini-3-flash-preview', 'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'gemini-2.5-pro'],
  anthropic: ['claude-3-5-haiku-20241022', 'claude-3-5-sonnet-20241022'],
  groq: ['llama-3.1-70b-versatile', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768']
}

export default function DocumentUpload({ mode, onAnalyze, loading }: DocumentUploadProps) {
  const [file, setFile] = useState<File | null>(null)
  const [depth, setDepth] = useState('Comprehensive')
  const [focusAreas, setFocusAreas] = useState<string[]>([])
  const [selectedModels, setSelectedModels] = useState<string[]>(['gemini-3-flash-preview'])
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newFile = e.target.files?.[0]
    if (newFile && ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'].includes(newFile.type)) {
      setFile(newFile)
    }
  }

  const handleDragDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    const newFile = e.dataTransfer.files?.[0]
    if (newFile) setFile(newFile)
  }, [])

  const focusAreasList = ['Contract Terms', 'Compliance', 'Liability', 'Intellectual Property', 'Employment Law', 'Privacy & Data Protection', 'Financial Terms', 'Dispute Resolution']

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      {/* File Upload */}
      <motion.div
        onDragOver={handleDragDrop}
        onDrop={handleDragDrop}
        whileHover={{ scale: 1.02 }}
        className="glass rounded-2xl p-8 border-2 border-dashed border-blue-500/30 hover:border-blue-500 transition-colors cursor-pointer"
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={handleFileChange}
          className="hidden"
        />
        <div className="text-center">
          <motion.div
            animate={{ y: [0, -8, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="mb-4"
          >
            <Upload className="w-12 h-12 text-blue-400 mx-auto" />
          </motion.div>
          <h3 className="font-semibold text-white mb-2">Drop your document</h3>
          <p className="text-sm text-gray-400">or click to browse (PDF, DOCX, TXT)</p>
        </div>
      </motion.div>

      {/* Selected File */}
      {file && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-lg p-4 flex items-center justify-between border border-green-500/30"
        >
          <div className="flex items-center gap-3">
            <FileText className="w-5 h-5 text-green-400" />
            <div>
              <p className="font-semibold text-white">{file.name}</p>
              <p className="text-xs text-gray-400">{(file.size / 1024).toFixed(0)} KB</p>
            </div>
          </div>
          <button
            onClick={() => setFile(null)}
            className="p-2 hover:bg-white/10 rounded-lg transition-colors"
          >
            <Trash2 className="w-5 h-5 text-red-400" />
          </button>
        </motion.div>
      )}

      {/* Analysis Depth */}
      <div>
        <label className="block text-sm font-semibold text-gray-300 mb-3">Analysis Depth</label>
        <select
          value={depth}
          onChange={(e) => setDepth(e.target.value)}
          className="w-full glass rounded-lg px-4 py-2 border border-white/10 text-white focus:outline-none focus:border-blue-500"
        >
          <option>Quick</option>
          <option>Comprehensive</option>
          <option>Focused</option>
        </select>
      </div>

      {/* Focus Areas */}
      <div>
        <label className="block text-sm font-semibold text-gray-300 mb-3">Focus Areas (Optional)</label>
        <div className="grid grid-cols-2 gap-2">
          {focusAreasList.map((area) => (
            <button
              key={area}
              onClick={() => setFocusAreas(prev => 
                prev.includes(area) ? prev.filter(a => a !== area) : [...prev, area]
              )}
              className={`px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                focusAreas.includes(area)
                  ? 'bg-blue-500 text-white'
                  : 'bg-white/10 text-gray-300 hover:bg-white/20'
              }`}
            >
              {area}
            </button>
          ))}
        </div>
      </div>

      {/* Model Selection */}
      <div>
        <label className="block text-sm font-semibold text-gray-300 mb-3">
          {mode === 'single' ? 'Select Model' : 'Select Models (2-4)'}
        </label>
        <div className="space-y-2">
          {Object.entries(MODELS).map(([provider, models]) => (
            <div key={provider}>
              <p className="text-xs font-semibold text-gray-400 uppercase mb-2">{provider}</p>
              <div className="grid grid-cols-2 gap-2 mb-3">
                {models.map((model) => (
                  <button
                    key={model}
                    onClick={() => {
                      if (mode === 'single') {
                        setSelectedModels([model])
                      } else {
                        setSelectedModels(prev =>
                          prev.includes(model)
                            ? prev.filter(m => m !== model)
                            : prev.length < 4 ? [...prev, model] : prev
                        )
                      }
                    }}
                    className={`px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                      selectedModels.includes(model)
                        ? 'bg-blue-500 text-white'
                        : 'bg-white/10 text-gray-300 hover:bg-white/20'
                    }`}
                  >
                    {model.split('-').slice(0, 2).join('-')}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Analyze Button */}
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        disabled={!file || selectedModels.length === 0 || loading}
        onClick={() => file && onAnalyze(file, depth, focusAreas, selectedModels)}
        className="w-full py-3 bg-gradient-to-r from-blue-600 to-blue-500 text-white rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg hover:shadow-blue-500/50 transition-all"
      >
        {loading ? 'Analyzing...' : '🔍 Analyze Document'}
      </motion.button>
    </motion.div>
  )
}
