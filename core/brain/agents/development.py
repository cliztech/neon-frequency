from dataclasses import dataclass
import ast
import os
from typing import Dict, Any, Iterable

@dataclass
class CodeChemist:
    """
    The Lead Developer Agent.
    Responsible for simple static analysis and quality checks.
    """
    
    def review_file(self, file_path: str) -> Dict[str, Any]:
        """Performs a basic AST-based review of a Python file."""
        if not os.path.exists(file_path):
            return {"error": "File not found"}
        
        issues = []
        score = 100
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Check 1: Docstrings present for functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not ast.get_docstring(node):
                        issues.append(f"Missing docstring in function '{node.name}' (Line {node.lineno})")
                        score -= 5
                
                # Check 2: Class docstrings
                if isinstance(node, ast.ClassDef):
                    if not ast.get_docstring(node):
                        issues.append(f"Missing docstring in class '{node.name}' (Line {node.lineno})")
                        score -= 5

            # Check 3: Todo comments
            for i, line in enumerate(content.split('\n')):
                if "# TODO" in line:
                    issues.append(f"TODO found on line {i+1}: {line.strip()}")
                    score -= 1

        except SyntaxError as e:
            return {"score": 0, "issues": [f"Syntax Error: {e}"]}
        except Exception as e:
            return {"score": 0, "issues": [f"Analysis Error: {e}"]}
            
        return {
            "file": os.path.basename(file_path),
            "score": max(0, score),
            "issues": issues
        }

    def scan_codebase(
        self,
        root_dir: str,
        exclude_dirs: Iterable[str] | None = None,
    ) -> Dict[str, Any]:
        """Scans python files in the directory for issues."""
        results: Dict[str, Any] = {}
        total_score = 0
        file_count = 0
        ignored = set(exclude_dirs or ())
        ignored.update({".git", "__pycache__", "node_modules", "venv", ".venv"})

        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in ignored]
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    review = self.review_file(full_path)
                    relative_path = os.path.relpath(full_path, root_dir)
                    results[relative_path] = review
                    total_score += review.get("score", 0)
                    file_count += 1

        avg_score = total_score / file_count if file_count > 0 else 0
        return {
            "average_code_health": avg_score,
            "files_analyzed": file_count,
            "details": results
        }
