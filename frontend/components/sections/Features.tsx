'use client'

import { motion } from 'framer-motion'
import { CheckCircle, Zap, LineChart, Share2 } from 'lucide-react'

export default function Features() {
  const features = [
    {
      icon: CheckCircle,
      title: 'Smart Document Upload',
      description: 'Upload any legal document in PDF, DOCX, or TXT format with instant validation'
    },
    {
      icon: Zap,
      title: 'Multi-Model Analysis',
      description: 'Leverage Google Gemini, Claude, and Groq for comprehensive insights'
    },
    {
      icon: LineChart,
      title: 'Visual Risk Assessment',
      description: 'Beautiful charts and graphs showing detailed risk breakdowns'
    },
    {
      icon: Share2,
      title: 'Model Comparison',
      description: 'Compare results from multiple AI models side-by-side'
    }
  ]

  return (
    <section className="py-20 px-4 bg-slate-900">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold gradient-text mb-4">
            Powerful Features
          </h2>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Everything you need for professional legal document analysis
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1, duration: 0.5 }}
              className="glass rounded-xl p-6 border border-white/10 hover:border-blue-500/50 transition-all"
            >
              <feature.icon className="w-10 h-10 text-blue-400 mb-4" />
              <h3 className="font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-sm text-gray-400">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
