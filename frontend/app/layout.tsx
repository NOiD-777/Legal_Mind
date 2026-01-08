import type { Metadata } from 'next'
import { Manrope, Sora } from 'next/font/google'
import './globals.css'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'
import ThemeProvider from '@/components/providers/ThemeProvider'

const manrope = Manrope({ variable: '--font-manrope', subsets: ['latin'] })
const sora = Sora({ variable: '--font-sora', subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'LegalMind - AI Legal Document Analysis',
  description: 'AI-powered legal document risk assessment with multi-model analysis',
  icons: {
    icon: '⚖️',
  }
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${manrope.variable} ${sora.variable} antialiased`}>
        <ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
          <div className="flex flex-col min-h-screen">
            <Navbar />
            <main className="flex-1">
              {children}
            </main>
            <Footer />
          </div>
        </ThemeProvider>
      </body>
    </html>
  )
}
