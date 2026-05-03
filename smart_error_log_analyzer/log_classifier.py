"""
Log Classifier Module
Classifies logs into ERROR, WARNING, and INFO categories using pattern matching
and keyword analysis.
"""

import re
from typing import List, Dict, Tuple
from collections import defaultdict


class LogClassifier:
    """Classify log entries into categories."""
    
    # Error keywords and patterns
    ERROR_KEYWORDS = [
        'error', 'failed', 'failure', 'exception', 'critical', 'fatal',
        'crash', 'broken', 'invalid', 'denied', 'unauthorized', 'forbidden',
        'not found', 'failed to', 'unable to', 'cannot', 'could not',
        'wrong', 'bad request', 'timeout', 'deadlock', 'overflow',
        'segmentation', 'assertion', 'panic'
    ]
    
    # Warning keywords and patterns
    WARNING_KEYWORDS = [
        'warning', 'warn', 'caution', 'deprecated', 'obsolete',
        'slow', 'performance', 'delay', 'retry', 'attempt',
        'suspicious', 'unusual', 'unknown', 'unrecognized',
        'deprecated', 'may fail', 'might', 'possible', 'potential'
    ]
    
    # Info keywords
    INFO_KEYWORDS = [
        'info', 'information', 'started', 'stopped', 'initialized',
        'connected', 'disconnected', 'loaded', 'unloaded', 'created',
        'deleted', 'modified', 'completed', 'finished', 'success'
    ]
    
    def __init__(self):
        """Initialize the classifier."""
        self.classified_logs = []
        self.statistics = defaultdict(int)
    
    def classify_logs(self, logs: List[Dict]) -> List[Dict]:
        """
        Classify a list of log entries.
        
        Args:
            logs: List of log entries
            
        Returns:
            List of classified log entries
        """
        self.classified_logs = []
        self.statistics = defaultdict(int)
        
        for log in logs:
            classified_log = self._classify_entry(log)
            self.classified_logs.append(classified_log)
            self.statistics[classified_log['category']] += 1
        
        return self.classified_logs
    
    def _classify_entry(self, log: Dict) -> Dict:
        """
        Classify a single log entry.
        
        Args:
            log: Log entry dictionary
            
        Returns:
            Log entry with added category
        """
        # Start with level-based classification
        level = log.get('level', 'UNKNOWN').upper()
        
        # If level is already set to ERROR, classify as ERROR
        if level == 'ERROR':
            category = 'ERROR'
        elif level in ('WARNING', 'WARN'):
            category = 'WARNING'
        elif level in ('INFO', 'INFORMATION'):
            category = 'INFO'
        else:
            # Enhanced classification using message content
            category = self._classify_by_content(log)
        
        confidence = self._calculate_confidence(log, category)
        
        log['category'] = category
        log['confidence'] = confidence
        
        return log
    
    def _classify_by_content(self, log: Dict) -> str:
        """
        Classify log by analyzing message content.
        
        Args:
            log: Log entry
            
        Returns:
            Classification category
        """
        message = (log.get('message', '') + ' ' + log.get('raw_line', '')).lower()
        
        # Check for error patterns
        error_score = sum(message.count(keyword) for keyword in self.ERROR_KEYWORDS)
        
        # Check for warning patterns
        warning_score = sum(message.count(keyword) for keyword in self.WARNING_KEYWORDS)
        
        # Check for info patterns
        info_score = sum(message.count(keyword) for keyword in self.INFO_KEYWORDS)
        
        # Determine category based on highest score
        if error_score > warning_score and error_score > info_score:
            return 'ERROR'
        elif warning_score > info_score:
            return 'WARNING'
        else:
            return 'INFO'
    
    def _calculate_confidence(self, log: Dict, category: str) -> float:
        """
        Calculate confidence score for classification.
        
        Args:
            log: Log entry
            category: Assigned category
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        message = (log.get('message', '') + ' ' + log.get('raw_line', '')).lower()
        
        if category == 'ERROR':
            keywords = self.ERROR_KEYWORDS
        elif category == 'WARNING':
            keywords = self.WARNING_KEYWORDS
        else:
            keywords = self.INFO_KEYWORDS
        
        matches = sum(message.count(keyword) for keyword in keywords)
        confidence = min(1.0, 0.5 + (matches * 0.1))
        
        return round(confidence, 2)
    
    def get_classified_logs(self) -> List[Dict]:
        """Return all classified logs."""
        return self.classified_logs
    
    def get_statistics(self) -> Dict[str, int]:
        """Return classification statistics."""
        return dict(self.statistics)
    
    def filter_by_category(self, category: str) -> List[Dict]:
        """
        Filter logs by category.
        
        Args:
            category: Category to filter by (ERROR, WARNING, INFO)
            
        Returns:
            Filtered list of logs
        """
        return [log for log in self.classified_logs if log['category'] == category]
    
    def get_errors(self) -> List[Dict]:
        """Get all error logs."""
        return self.filter_by_category('ERROR')
    
    def get_warnings(self) -> List[Dict]:
        """Get all warning logs."""
        return self.filter_by_category('WARNING')
    
    def get_info(self) -> List[Dict]:
        """Get all info logs."""
        return self.filter_by_category('INFO')
