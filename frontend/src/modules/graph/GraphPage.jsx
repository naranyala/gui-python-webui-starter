import React, { useMemo, useEffect, useState } from 'react';
import CytoscapeComponent from 'react-cytoscapejs';
import { useService } from '../../core/ServiceProvider.jsx';
import { GraphService } from '../../services/GraphService';

export default function GraphPage() {
  const [graphData, setGraphData] = useState(null);
  const graphService = useService(GraphService);
  
  useEffect(() => {
    const loadGraph = async () => {
      const data = await graphService.getGraph();
      setGraphData(data);
    };
    loadGraph();
  }, [graphService]);

  const style = { width: '100%', height: 'calc(100vh - 150px)' };
  const layout = { name: 'cose', animate: true };

  const elements = useMemo(() => {
    if (!graphData) return [];
    return [...(graphData.nodes || []), ...(graphData.edges || [])];
  }, [graphData]);

  return (
    <div className="graph-container">
      <h2>Interactive Graph</h2>
      {elements.length > 0 ? (
        <CytoscapeComponent
          elements={elements}
          style={style}
          layout={layout}
          stylesheet={[
            { 
              selector: 'node', 
              style: { 
                label: 'data(label)', 
                backgroundColor: '#007acc', 
                color: '#fff', 
                width: 40, 
                height: 40, 
                fontSize: '10px', 
                textValign: 'center' 
              } 
            },
            { 
              selector: 'edge', 
              style: { 
                width: 2, 
                lineColor: '#3e3e42', 
                targetArrowShape: 'triangle', 
                curveStyle: 'bezier' 
              } 
            },
          ]}
        />
      ) : <p>No graph data</p>}
    </div>
  );
}
