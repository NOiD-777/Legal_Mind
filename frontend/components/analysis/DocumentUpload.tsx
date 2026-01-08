'use client'

import React, { useState, useRef, useCallback, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Upload, FileText, Trash2, Search } from 'lucide-react'
import { getAvailableModels, getWorkingModels } from '@/services/api'

interface DocumentUploadProps {
  mode: 'single' | 'compare'
  onAnalyze: (file: File, depth: string, focusAreas: string[], models: string[]) => void
  loading: boolean
}

// Models fetched dynamically from backend

export default function DocumentUpload({ mode, onAnalyze, loading }: DocumentUploadProps) {
  const [file, setFile] = useState<File | null>(null)
  const [depth, setDepth] = useState('Comprehensive')
  const [focusAreas, setFocusAreas] = useState<string[]>([])
  const [selectedModels, setSelectedModels] = useState<string[]>([])
  const [modelsByProvider, setModelsByProvider] = useState<Record<string, string[]>>({})
  const [modelDetails, setModelDetails] = useState<Record<string, any>>({})
  const [modelsLoading, setModelsLoading] = useState<boolean>(true)
  const [modelsError, setModelsError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    const fetchModels = async () => {
      try {
        setModelsLoading(true)
        // Prefer working models; fallback to available if endpoint not present
        let res
        try {
          res = await getWorkingModels()
        } catch {
          res = await getAvailableModels()
        }
        const grouped: Record<string, string[]> = {}
        const defaultModel = 'gemini-3-flash-preview'
        res.models.forEach((m) => {
          const provider = res.model_details[m]?.provider || 'other'
          grouped[provider] = grouped[provider] || []
          grouped[provider].push(m)
        })
        setModelsByProvider(grouped)
        setModelDetails(res.model_details)
        // Set default selection
        if (res.models.length) {
          if (res.models.includes(defaultModel)) {
            setSelectedModels([defaultModel])
          } else {
            setSelectedModels([res.models[0]])
          }
        }
      } catch (e: any) {
        setModelsError('Failed to load models')
      } finally {
        setModelsLoading(false)
      }
    }
    fetchModels()
  }, [])

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
        className="glass rounded-2xl p-8 border-2 border-dashed border-primary-500/30 hover:border-primary-500 transition-colors cursor-pointer"
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
            <Upload className="w-12 h-12 text-primary-400 mx-auto" />
          </motion.div>
          <h3 className="font-semibold text-white mb-2">Drop your document</h3>
          <p className="text-sm text-white/70">or click to browse (PDF, DOCX, TXT)</p>
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
              <p className="text-xs text-white/70">{(file.size / 1024).toFixed(0)} KB</p>
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
        <label className="block text-sm font-semibold text-white/90 mb-3">Analysis Depth</label>
        <select
          value={depth}
          onChange={(e) => setDepth(e.target.value)}
          className="w-full glass rounded-lg px-4 py-2 border border-white/10 text-white focus:outline-none focus:border-primary-500"
        >
          <option>Quick</option>
          <option>Comprehensive</option>
          <option>Focused</option>
        </select>
      </div>

      {/* Focus Areas */}
      <div>
        <label className="block text-sm font-semibold text-white/90 mb-3">Focus Areas (Optional)</label>
        <div className="grid grid-cols-2 gap-2">
          {focusAreasList.map((area) => (
            <button
              key={area}
              onClick={() => setFocusAreas(prev => 
                prev.includes(area) ? prev.filter(a => a !== area) : [...prev, area]
              )}
              className={`px-3 py-2 rounded-lg text-xs font-medium transition-all border ${
                focusAreas.includes(area)
                  ? 'bg-primary-600 text-white border-primary-600'
                  : 'bg-black text-white/80 hover:bg-white/5 border-white/20'
              }`}
            >
              {area}
            </button>
          ))}
        </div>
      </div>

      {/* Model Selection */}
      <div>
        <label className="block text-sm font-semibold text-white/90 mb-3">
          {mode === 'single' ? 'Select Model' : 'Select Models (2-4)'}
        </label>
        {modelsLoading ? (
          <p className="text-xs text-white/70">Loading available models...</p>
        ) : modelsError ? (
          <p className="text-xs text-red-400">{modelsError}</p>
        ) : (
          <div className="space-y-2">
            {Object.entries(modelsByProvider).map(([provider, models]) => (
              <div key={provider}>
                <p className="text-xs font-semibold text-white/70 uppercase mb-2">{provider}</p>
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
                      className={`px-3 py-2 rounded-lg text-xs font-medium transition-all border ${
                        selectedModels.includes(model)
                          ? 'bg-primary-600 text-white border-primary-600'
                          : 'bg-black text-white/80 hover:bg-white/5 border-white/20'
                      }`}
                    >
                      {modelDetails[model]?.name || model.split('-').slice(0, 2).join('-')}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Analyze Button */}
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        disabled={
          !file || 
          selectedModels.length === 0 || 
          (mode === 'compare' && selectedModels.length < 2) ||
          loading
        }
        onClick={() => file && onAnalyze(file, depth, focusAreas, selectedModels)}
        className="w-full py-3 bg-gradient-to-r from-primary-600 to-primary-500 text-white rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg hover:shadow-primary-500/50 transition-all flex items-center justify-center gap-2"
      >
        {loading ? 'Analyzing...' : (
          <>
            <Search className="w-5 h-5" />
            {mode === 'compare' && selectedModels.length < 2 
              ? 'Select at least 2 models' 
              : 'Analyze Document'
            }
          </>
        )}
      </motion.button>
    </motion.div>
  )
}
