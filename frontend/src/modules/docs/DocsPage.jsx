import React, { useState, useMemo, useEffect } from 'react';
import { marked } from 'marked';
import hljs from 'highlight.js';
import DOMPurify from 'dompurify';
import { resolve, SERVICE_KEYS } from '../../core/index.js';

// Setup highlight.js
marked.setOptions({
  highlight: (code, lang) => {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value;
    }
    return hljs.highlightAuto(code).value;
  }
});

export default function DocsPage() {
  const [docs, setDocs] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDocs = async () => {
      try {
        const docService = resolve(SERVICE_KEYS.DOCUMENT_SERVICE);
        const remoteDocs = await docService.getAll();
        setDocs(remoteDocs);
        if (remoteDocs.length > 0) {
            // Priority for Architecture doc
            const arch = remoteDocs.find(d => d.id === 'arch') || remoteDocs[0];
            setSelectedDoc(arch);
        }
      } catch (err) {
        console.error('[DocsPage] Fetch failed:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchDocs();
  }, []);

   const filteredDocs = useMemo(() => {
     // Filter out documents with empty or whitespace-only titles
     const validDocs = docs.filter(doc => 
       doc.title && doc.title.trim().length > 0
     );
     
     if (!search) return validDocs;
     const lower = search.toLowerCase();
     return validDocs.filter(d => 
       d.title.toLowerCase().includes(lower) || 
       d.content.toLowerCase().includes(lower)
     );
   }, [docs, search]);

  if (loading) return (
    <div style={{ padding: '40px', color: '#9d9d9d', textAlign: 'center' }}>
      Loading project specifications...
    </div>
  );

  return (
    <div className="docs-layout">
      <div className="sidebar">
        <div className="sidebar-header">
          <h2>Project Wiki</h2>
          <p style={{ fontSize: '0.8rem', color: '#666', marginBottom: '15px' }}>Technical Abstractions</p>
        </div>
        <input
          type="text"
          className="search-box"
          placeholder="Fuzzy search docs..."
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        <ul className="doc-list">
          {filteredDocs.map(doc => (
            <li
              key={doc.id}
              className={selectedDoc?.id === doc.id ? 'active' : ''}
              onClick={() => setSelectedDoc(doc)}
            >
              <span className="doc-icon">📄</span>
              {doc.title}
            </li>
          ))}
        </ul>
      </div>

      <div className="doc-viewer">
        {selectedDoc ? (
          <div className="doc-content-wrapper">
            <div className="doc-header">
              <div className="doc-title-area">
                <span className="breadcrumb-tag">System Spec</span>
                <h2>{selectedDoc.title}</h2>
              </div>
            </div>
            <div 
              className="markdown-body" 
              dangerouslySetInnerHTML={{ 
                __html: DOMPurify.sanitize(marked.parse(selectedDoc.content)) 
              }} 
            />
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-icon">📂</div>
            <h3>No Documentation Selected</h3>
            <p>Select a topic from the sidebar to view technical details.</p>
          </div>
        )}
      </div>
    </div>
  );
}
