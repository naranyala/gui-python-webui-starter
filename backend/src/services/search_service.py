from .base import BaseService
from shared.types import SearchResult, Document

class SearchService(BaseService):
    """Service for searching documents."""
    
    def __init__(self, container):
        super().__init__(container)
        self._threshold = 0.4
    
    def on_initialize(self) -> None:
        # Will resolve document service when needed
        pass
    
    def search(self, query: str, docs: list[Document], limit: int = 10) -> list[SearchResult]:
        if not query:
            return []
        
        query_lower = query.lower()
        results = []
        
        for doc in docs:
            score = self._calculate_score(query_lower, doc)
            if score >= self._threshold:
                results.append(SearchResult(
                    item=doc,
                    score=score,
                    matches=self._find_matches(query_lower, doc)
                ))
        
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]
    
    def _calculate_score(self, query: str, doc: Document) -> float:
        """Calculate relevance score for a document."""
        title_lower = doc.title.lower()
        content_lower = doc.content.lower()
        
        # Exact match in title gets highest score
        if query == title_lower:
            return 1.0
        
        # Title contains query
        if query in title_lower:
            return 0.9
        
        # Content exact match
        if query in content_lower:
            return 0.7
        
        # Word match in title
        query_words = query.split()
        title_words = title_lower.split()
        for qw in query_words:
            for tw in title_words:
                if qw in tw or tw in qw:
                    return 0.6
        
        # Word match in content
        for qw in query_words:
            if qw in content_lower:
                return 0.4
        
        return 0.0
    
    def _find_matches(self, query: str, doc: Document) -> list[dict]:
        """Find matching positions in document."""
        matches = []
        query_words = query.split()
        
        for word in query_words:
            if word in doc.title.lower():
                matches.append({"field": "title", "text": word})
            if word in doc.content.lower():
                matches.append({"field": "content", "text": word})
        
        return matches
    
    def set_threshold(self, threshold: float):
        self._threshold = max(0.0, min(1.0, threshold))