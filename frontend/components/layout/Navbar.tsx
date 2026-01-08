'use client'

import Link from 'next/link'
import { useTheme } from 'next-themes'
import { Moon, Sun, Scale } from 'lucide-react'
import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

export default function Navbar() {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => setMounted(true), [])

  return (
    <nav className="sticky top-0 z-50 glass border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 group">
          <motion.div
            whileHover={{ scale: 1.1, rotate: 10 }}
            whileTap={{ scale: 0.95 }}
          >
            <Scale className="w-8 h-8 text-blue-500 group-hover:text-blue-400 transition-colors" />
          </motion.div>
          <span className="text-xl font-bold gradient-text">LegalMind</span>
        </Link>

        <div className="flex items-center gap-8">
          <Link href="/analyze" className="text-gray-300 hover:text-white transition-colors">
            Analyze
          </Link>
          <Link href="/docs" className="text-gray-300 hover:text-white transition-colors">
            Documentation
          </Link>

          {mounted && (
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors"
            >
              {theme === 'dark' ? (
                <Sun className="w-5 h-5" />
              ) : (
                <Moon className="w-5 h-5" />
              )}
            </motion.button>
          )}
        </div>
      </div>
    </nav>
  )
}
