import os
import git
import fnmatch
from pathlib import Path
from typing import List, Set, Optional
import logging

logger = logging.getLogger(__name__)

class CodeScanner:
    def __init__(self, config: dict):
        self.config = config
        self.supported_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.h', 
            '.hpp', '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala',
            '.r', '.m', '.sql', '.sh', '.bash', '.ps1', '.yaml', '.yml', '.json'
        }
        
    async def clone_repository(self, repo_url: str) -> Path:
        """Clone a git repository to a temporary directory"""
        repo_dir = Path(f"repos/{repo_url.split('/')[-1].replace('.git', '')}")
        
        if repo_dir.exists():
            logger.info(f"Repository already exists at {repo_dir}")
            return repo_dir
            
        try:
            logger.info(f"Cloning repository from {repo_url}")
            git.Repo.clone_from(repo_url, repo_dir)
            return repo_dir
        except Exception as e:
            logger.error(f"Failed to clone repository: {str(e)}")
            raise
            
    async def scan_directory(
        self,
        directory: Path,
        file_patterns: List[str] = None,
        exclude_patterns: List[str] = None
    ) -> List[Path]:
        """Scan directory for code files"""
        if not file_patterns:
            file_patterns = ['*.*']
            
        if not exclude_patterns:
            exclude_patterns = [
                'node_modules', '__pycache__', '.git', 'dist', 'build',
                'target', 'out', '.venv', 'venv', 'env', '.env',
                '*.pyc', '*.pyo', '*.pyd', '.DS_Store', 'Thumbs.db'
            ]
            
        files = []
        
        for root, dirs, filenames in os.walk(directory):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if not self._should_exclude(d, exclude_patterns)]
            
            for filename in filenames:
                file_path = Path(root) / filename
                
                # Check if file matches patterns and is not excluded
                if self._matches_patterns(filename, file_patterns) and \
                   not self._should_exclude(str(file_path), exclude_patterns):
                    
                    # Check if it's a supported code file
                    if file_path.suffix.lower() in self.supported_extensions:
                        files.append(file_path)
                        
        logger.info(f"Found {len(files)} code files to document")
        return sorted(files)
        
    def _matches_patterns(self, filename: str, patterns: List[str]) -> bool:
        """Check if filename matches any of the patterns"""
        for pattern in patterns:
            if fnmatch.fnmatch(filename, pattern):
                return True
        return False
        
    def _should_exclude(self, path: str, exclude_patterns: List[str]) -> bool:
        """Check if path should be excluded"""
        path_parts = Path(path).parts
        
        for pattern in exclude_patterns:
            # Check if any part of the path matches the exclude pattern
            for part in path_parts:
                if fnmatch.fnmatch(part, pattern):
                    return True
                    
            # Also check the full path
            if fnmatch.fnmatch(path, pattern):
                return True
                
        return False
        
    def get_file_stats(self, file_path: Path) -> dict:
        """Get statistics about a code file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.splitlines()
                
            return {
                'path': str(file_path),
                'name': file_path.name,
                'extension': file_path.suffix,
                'size_bytes': file_path.stat().st_size,
                'total_lines': len(lines),
                'code_lines': sum(1 for line in lines if line.strip() and not line.strip().startswith('#')),
                'comment_lines': sum(1 for line in lines if line.strip().startswith('#')),
                'blank_lines': sum(1 for line in lines if not line.strip())
            }
        except Exception as e:
            logger.error(f"Failed to get stats for {file_path}: {str(e)}")
            return None