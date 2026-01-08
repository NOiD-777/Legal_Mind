'use client'

import { motion } from 'framer-motion'
import Hero from '@/components/sections/Hero'
import Features from '@/components/sections/Features'

export default function Home() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <Hero />
      <Features />
    </motion.div>
  )
}
