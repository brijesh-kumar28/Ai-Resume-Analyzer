import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-gray-900 mb-4">
          Resume Analyzer
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          AI-powered resume analysis platform
        </p>
        <Link
          href="/upload"
          className="inline-block px-8 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition"
        >
          Start Analysis
        </Link>
      </div>
    </main>
  )
}
