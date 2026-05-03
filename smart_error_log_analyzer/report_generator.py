"""
Report Generator Module
Generates comprehensive summary reports from classified logs.
"""

import json
from typing import List, Dict
from datetime import datetime
from collections import defaultdict


class ReportGenerator:
    """Generate analysis reports from classified logs."""
    
    def __init__(self):
        """Initialize the report generator."""
        self.classified_logs = []
        self.report = {}
    
    def generate_report(self, classified_logs: List[Dict]) -> Dict:
        """
        Generate a comprehensive analysis report.
        
        Args:
            classified_logs: List of classified log entries
            
        Returns:
            Dictionary containing the report data
        """
        self.classified_logs = classified_logs
        
        self.report = {
            'timestamp': datetime.now().isoformat(),
            'total_logs': len(classified_logs),
            'summary': self._generate_summary(),
            'categories': self._generate_category_breakdown(),
            'sources': self._generate_source_analysis(),
            'top_errors': self._generate_top_errors(),
            'top_warnings': self._generate_top_warnings(),
            'confidence_analysis': self._generate_confidence_analysis(),
            'recommendations': self._generate_recommendations()
        }
        
        return self.report
    
    def _generate_summary(self) -> Dict:
        """Generate summary statistics."""
        total = len(self.classified_logs)
        
        errors = sum(1 for log in self.classified_logs if log['category'] == 'ERROR')
        warnings = sum(1 for log in self.classified_logs if log['category'] == 'WARNING')
        info = sum(1 for log in self.classified_logs if log['category'] == 'INFO')
        
        error_pct = (errors / total * 100) if total > 0 else 0
        warning_pct = (warnings / total * 100) if total > 0 else 0
        info_pct = (info / total * 100) if total > 0 else 0
        
        return {
            'total_entries': total,
            'error_count': errors,
            'warning_count': warnings,
            'info_count': info,
            'error_percentage': round(error_pct, 2),
            'warning_percentage': round(warning_pct, 2),
            'info_percentage': round(info_pct, 2),
            'severity_level': self._assess_severity(errors, total)
        }
    
    def _generate_category_breakdown(self) -> Dict:
        """Generate detailed breakdown by category."""
        breakdown = defaultdict(list)
        
        for log in self.classified_logs:
            category = log['category']
            breakdown[category].append({
                'line': log['line_number'],
                'message': log['message'],
                'source': log['source'],
                'confidence': log['confidence']
            })
        
        return {
            'errors': breakdown['ERROR'],
            'warnings': breakdown['WARNING'],
            'info': breakdown['INFO']
        }
    
    def _generate_source_analysis(self) -> Dict:
        """Analyze logs by source/component."""
        source_stats = defaultdict(lambda: {'count': 0, 'errors': 0, 'warnings': 0})
        
        for log in self.classified_logs:
            source = log['source']
            source_stats[source]['count'] += 1
            
            if log['category'] == 'ERROR':
                source_stats[source]['errors'] += 1
            elif log['category'] == 'WARNING':
                source_stats[source]['warnings'] += 1
        
        # Sort by count
        sorted_sources = sorted(source_stats.items(), key=lambda x: x[1]['count'], reverse=True)
        
        return {source: stats for source, stats in sorted_sources[:10]}  # Top 10 sources
    
    def _generate_top_errors(self) -> List[Dict]:
        """Generate list of top errors."""
        errors = [log for log in self.classified_logs if log['category'] == 'ERROR']
        
        # Group similar errors
        error_groups = defaultdict(int)
        for error in errors:
            msg = error['message'][:100]  # First 100 chars
            error_groups[msg] += 1
        
        # Sort by frequency
        sorted_errors = sorted(error_groups.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {'message': msg, 'count': count}
            for msg, count in sorted_errors[:10]  # Top 10 errors
        ]
    
    def _generate_top_warnings(self) -> List[Dict]:
        """Generate list of top warnings."""
        warnings = [log for log in self.classified_logs if log['category'] == 'WARNING']
        
        # Group similar warnings
        warning_groups = defaultdict(int)
        for warning in warnings:
            msg = warning['message'][:100]  # First 100 chars
            warning_groups[msg] += 1
        
        # Sort by frequency
        sorted_warnings = sorted(warning_groups.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {'message': msg, 'count': count}
            for msg, count in sorted_warnings[:10]  # Top 10 warnings
        ]
    
    def _generate_confidence_analysis(self) -> Dict:
        """Analyze classification confidence."""
        confidences = [log['confidence'] for log in self.classified_logs]
        
        if not confidences:
            return {'average': 0, 'min': 0, 'max': 0}
        
        return {
            'average': round(sum(confidences) / len(confidences), 2),
            'min': min(confidences),
            'max': max(confidences),
            'total_classified': len(confidences)
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        summary = self.report.get('summary', {})
        
        error_count = summary.get('error_count', 0)
        warning_count = summary.get('warning_count', 0)
        total = summary.get('total_entries', 1)
        
        # Error-based recommendations
        if error_count > total * 0.2:  # More than 20% errors
            recommendations.append("High error rate detected. Investigate critical components immediately.")
        
        if error_count > warning_count and error_count > 0:
            recommendations.append("Errors outweigh warnings. Focus debugging efforts on error sources.")
        
        # Warning-based recommendations
        if warning_count > total * 0.3:
            recommendations.append("Significant number of warnings detected. Review and address potential issues.")
        
        # Positive recommendations
        if error_count == 0:
            recommendations.append("No errors detected in this log period. System appears stable.")
        
        if error_count + warning_count < total * 0.1:
            recommendations.append("Low error/warning ratio. System is operating normally.")
        
        if not recommendations:
            recommendations.append("Continue monitoring log patterns for potential issues.")
        
        return recommendations
    
    def _assess_severity(self, error_count: int, total: int) -> str:
        """Assess overall severity level."""
        if total == 0:
            return "UNKNOWN"
        
        error_pct = (error_count / total) * 100
        
        if error_pct > 30:
            return "CRITICAL"
        elif error_pct > 15:
            return "HIGH"
        elif error_pct > 5:
            return "MEDIUM"
        else:
            return "LOW"
    
    def save_report_json(self, output_path: str) -> bool:
        """
        Save report as JSON file.
        
        Args:
            output_path: Path to save the JSON report
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.report, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving JSON report: {e}")
            return False
    
    def save_report_html(self, output_path: str) -> bool:
        """
        Save report as HTML file.
        
        Args:
            output_path: Path to save the HTML report
            
        Returns:
            True if successful, False otherwise
        """
        try:
            html_content = self._generate_html_report()
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return True
        except Exception as e:
            print(f"Error saving HTML report: {e}")
            return False
    
    def _generate_html_report(self) -> str:
        """Generate HTML formatted report."""
        summary = self.report['summary']
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Smart Error Log Analyzer - Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1000px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 20px; }}
        .summary {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0; }}
        .stat-box {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center; border-left: 4px solid #007bff; }}
        .stat-box.error {{ border-left-color: #dc3545; }}
        .stat-box.warning {{ border-left-color: #ffc107; }}
        .stat-box.info {{ border-left-color: #17a2b8; }}
        .stat-number {{ font-size: 24px; font-weight: bold; color: #333; }}
        .stat-label {{ color: #666; font-size: 12px; margin-top: 5px; }}
        .severity {{ font-size: 18px; font-weight: bold; padding: 10px; border-radius: 5px; }}
        .severity.critical {{ background-color: #dc3545; color: white; }}
        .severity.high {{ background-color: #fd7e14; color: white; }}
        .severity.medium {{ background-color: #ffc107; color: #333; }}
        .severity.low {{ background-color: #28a745; color: white; }}
        .recommendations {{ background-color: #e7f3ff; border-left: 4px solid #2196F3; padding: 15px; margin: 15px 0; border-radius: 4px; }}
        .recommendations ul {{ margin: 10px 0; padding-left: 20px; }}
        .recommendations li {{ margin: 8px 0; }}
        .timestamp {{ color: #999; font-size: 12px; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Smart Error Log Analyzer Report</h1>
        
        <div class="summary">
            <div class="stat-box error">
                <div class="stat-number">{summary['error_count']}</div>
                <div class="stat-label">Errors ({summary['error_percentage']}%)</div>
            </div>
            <div class="stat-box warning">
                <div class="stat-number">{summary['warning_count']}</div>
                <div class="stat-label">Warnings ({summary['warning_percentage']}%)</div>
            </div>
            <div class="stat-box info">
                <div class="stat-number">{summary['info_count']}</div>
                <div class="stat-label">Info ({summary['info_percentage']}%)</div>
            </div>
        </div>
        
        <h2>System Status</h2>
        <div class="severity {summary['severity_level'].lower()}">
            Severity: {summary['severity_level']}
        </div>
        <p>Total Log Entries: {summary['total_entries']}</p>
        
        <h2>Recommendations</h2>
        <div class="recommendations">
            <ul>
"""
        
        for rec in self.report['recommendations']:
            html += f"                <li>{rec}</li>\n"
        
        html += """
            </ul>
        </div>
        
        <div class="timestamp">
"""
        html += f"Generated: {self.report['timestamp']}\n"
        html += """
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def print_report(self) -> None:
        """Print report to console."""
        summary = self.report['summary']
        
        print("\n" + "="*60)
        print("📊 SMART ERROR LOG ANALYZER - REPORT")
        print("="*60)
        
        print(f"\nTimestamp: {self.report['timestamp']}")
        print(f"Total Log Entries: {summary['total_entries']}")
        
        print("\n--- Summary ---")
        print(f"❌ Errors:   {summary['error_count']} ({summary['error_percentage']}%)")
        print(f"⚠️  Warnings: {summary['warning_count']} ({summary['warning_percentage']}%)")
        print(f"ℹ️  Info:     {summary['info_count']} ({summary['info_percentage']}%)")
        
        print(f"\nSeverity Level: {summary['severity_level']}")
        
        print("\n--- Top Errors ---")
        for i, error in enumerate(self.report['top_errors'][:5], 1):
            print(f"{i}. {error['message'][:70]}... (Count: {error['count']})")
        
        print("\n--- Top Warnings ---")
        for i, warning in enumerate(self.report['top_warnings'][:5], 1):
            print(f"{i}. {warning['message'][:70]}... (Count: {warning['count']})")
        
        print("\n--- Recommendations ---")
        for rec in self.report['recommendations']:
            print(f"• {rec}")
        
        print("\n" + "="*60 + "\n")
    
    def get_report(self) -> Dict:
        """Return the generated report."""
        return self.report
