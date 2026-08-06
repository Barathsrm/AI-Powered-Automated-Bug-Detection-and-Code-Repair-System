import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import AnalysisPage from './pages/AnalysisPage'
import DiffViewerPage from './pages/DiffViewerPage'
import ReportPage from './pages/ReportPage'
import UploadPage from './pages/UploadPage'

function App(){
  return (
    <BrowserRouter>
      <nav style={{padding:10}}>
        <Link to="/analysis" style={{marginRight:10}}>Analysis</Link>
        <Link to="/upload" style={{marginRight:10}}>Upload</Link>
        <Link to="/report" style={{marginRight:10}}>Reports</Link>
        <Link to="/diff" style={{marginRight:10}}>Diff</Link>
      </nav>
      <Routes>
        <Route path="/analysis" element={<AnalysisPage/>} />
        <Route path="/upload" element={<UploadPage/>} />
        <Route path="/report" element={<ReportPage/>} />
        <Route path="/diff" element={<DiffViewerPage/>} />
        <Route path="/" element={<UploadPage/>} />
      </Routes>
    </BrowserRouter>
  )
}

createRoot(document.getElementById('root')).render(<App />)
