"""
Edges module - exports all edge definitions
"""

import importlib.util
import os
import sys

# Import from orchestrator.edges directory  
_edges_dir = os.path.join(os.path.dirname(__file__), 'orchestrator.edges')
sys.path.insert(0, _edges_dir)
try:
    from workflow_edges import create_workflow_edges
finally:
    sys.path.remove(_edges_dir)

__all__ = ['create_workflow_edges'] 