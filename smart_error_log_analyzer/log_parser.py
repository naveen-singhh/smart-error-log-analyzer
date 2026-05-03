"""
Log Parser Module
Handles parsing and extraction of meaningful information from log files.
"""

import re
from datetime import datetime
from typing import List, Dict, Tuple


class LogParser:
    """Parse and extract information from log files."""
    
    # Common log timestamp patterns
    TIMESTAMP_PATTERNS = [
        r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}',  # YYYY-MM-DD HH:MM:SS
        r'\d{2}/\w+/\d{4}\s\d{2}:\d{2}:\d{2}',    # DD/Mon/YYYY HH:MM:SS
        r'\w+\s+\d{1,2}\s\d{2}:\d{2}:\d{2}',      # Mon DD HH:MM:SS
    ]
    
    def __init__(self):
        """Initialize the log parser."""
        self.logs = []
        self.parsed_count = 0
    
    def parse_file(self, file_path: str) -> List[Dict]:
        """
        Parse a log file and extract structured information.
        
        Args:
            file_path: Path to the log file
            
        Returns:
            List of parsed log entries as dictionaries
        """
        self.logs = []
        self.parsed_count = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line:  # Skip empty lines
                        parsed_entry = self._parse_line(line, line_num)
                        if parsed_entry:
                            self.logs.append(parsed_entry)
                            self.parsed_count += 1
            
            return self.logs
        
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return []
        except Exception as e:
            print(f"Error parsing file: {e}")
            return []
    
    def _parse_line(self, line: str, line_num: int) -> Dict:
        """
        Parse a single log line.
        
        Args:
            line: The log line to parse
            line_num: Line number in the file
            
        Returns:
            Dictionary with parsed log information
        """
        timestamp = self._extract_timestamp(line)
        level = self._extract_level(line)
        source = self._extract_source(line)
        message = self._extract_message(line)
        
        return {
            'line_number': line_num,
            'timestamp': timestamp,
            'level': level,
            'source': source,
            'message': message,
            'raw_line': line
        }
    
    def _extract_timestamp(self, line: str) -> str:
        """Extract timestamp from log line."""
        for pattern in self.TIMESTAMP_PATTERNS:
            match = re.search(pattern, line)
            if match:
                return match.group(0)
        return "N/A"
    
    def _extract_level(self, line: str) -> str:
        """Extract log level from line."""
        level_patterns = {
            'ERROR': r'\[ERROR\]|\bERROR\b',
            'WARNING': r'\[WARN(ING)?\]|\bWARN(ING)?\b',
            'INFO': r'\[INFO\]|\bINFO\b',
            'DEBUG': r'\[DEBUG\]|\bDEBUG\b',
        }
        
        for level, pattern in level_patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                return level
        
        return "UNKNOWN"
    
    def _extract_source(self, line: str) -> str:
        """Extract source/component from log line."""
        # Try to extract source from common patterns like [ClassName] or (module)
        source_match = re.search(r'\[([^\]]+)\]|^\(([^)]+)\)', line)
        if source_match:
            return source_match.group(1) or source_match.group(2)
        
        # Try to extract from first word after timestamp
        parts = line.split()
        for i, part in enumerate(parts):
            if re.search(r'(ERROR|WARN|INFO|DEBUG)', part, re.IGNORECASE):
                if i + 1 < len(parts):
                    return parts[i + 1]
        
        return "Unknown"
    
    def _extract_message(self, line: str) -> str:
        """Extract the main message from log line."""
        # Remove timestamp if present
        message = re.sub(r'^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\s*', '', line)
        message = re.sub(r'^\d{2}/\w+/\d{4}\s\d{2}:\d{2}:\d{2}\s*', '', message)
        
        # Remove level indicator
        message = re.sub(r'\[(ERROR|WARN|INFO|DEBUG)\]\s*', '', message, flags=re.IGNORECASE)
        
        # Remove source if enclosed in brackets
        message = re.sub(r'^\[([^\]]+)\]\s*', '', message)
        
        return message.strip()
    
    def get_logs(self) -> List[Dict]:
        """Return all parsed logs."""
        return self.logs
    
    def get_parsed_count(self) -> int:
        """Return the number of parsed log entries."""
        return self.parsed_count
