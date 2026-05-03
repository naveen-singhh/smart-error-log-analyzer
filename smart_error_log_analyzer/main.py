"""
Main Module - Entry Point
Smart Error Log Analyzer Application
"""

import os
import sys
from pathlib import Path
from log_parser import LogParser
from log_classifier import LogClassifier
from report_generator import ReportGenerator


class SmartErrorLogAnalyzer:
    """Main application class."""
    
    def __init__(self, output_dir: str = 'output'):
        """
        Initialize the analyzer.
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = output_dir
        self.parser = LogParser()
        self.classifier = LogClassifier()
        self.report_generator = ReportGenerator()
        
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(exist_ok=True)
    
    def analyze_log_file(self, file_path: str, save_report: bool = True) -> Dict:
        """
        Analyze a single log file.
        
        Args:
            file_path: Path to the log file
            save_report: Whether to save the report to files
            
        Returns:
            Generated report dictionary
        """
        print(f"\n{'='*60}")
        print(f"Analyzing: {file_path}")
        print(f"{'='*60}\n")
        
        # Step 1: Parse the log file
        print("[1/3] Parsing log file...")
        logs = self.parser.parse_file(file_path)
        print(f"✓ Parsed {self.parser.get_parsed_count()} log entries")
        
        if not logs:
            print("❌ No logs to analyze!")
            return {}
        
        # Step 2: Classify the logs
        print("\n[2/3] Classifying logs...")
        classified_logs = self.classifier.classify_logs(logs)
        stats = self.classifier.get_statistics()
        print(f"✓ Classification complete:")
        print(f"  - Errors:   {stats.get('ERROR', 0)}")
        print(f"  - Warnings: {stats.get('WARNING', 0)}")
        print(f"  - Info:     {stats.get('INFO', 0)}")
        
        # Step 3: Generate report
        print("\n[3/3] Generating report...")
        report = self.report_generator.generate_report(classified_logs)
        print("✓ Report generated")
        
        # Save reports
        if save_report:
            print("\n[4/3] Saving reports...")
            filename = Path(file_path).stem
            
            # Save JSON report
            json_path = os.path.join(self.output_dir, f"{filename}_report.json")
            if self.report_generator.save_report_json(json_path):
                print(f"✓ JSON report saved: {json_path}")
            
            # Save HTML report
            html_path = os.path.join(self.output_dir, f"{filename}_report.html")
            if self.report_generator.save_report_html(html_path):
                print(f"✓ HTML report saved: {html_path}")
        
        # Print report to console
        print("\n")
        self.report_generator.print_report()
        
        return report
    
    def analyze_directory(self, directory: str, pattern: str = "*.log") -> List[Dict]:
        """
        Analyze all log files in a directory.
        
        Args:
            directory: Path to directory containing log files
            pattern: File pattern to match (default: *.log)
            
        Returns:
            List of generated reports
        """
        print(f"\nAnalyzing directory: {directory}")
        
        reports = []
        log_files = list(Path(directory).glob(pattern))
        
        if not log_files:
            print(f"❌ No log files found matching '{pattern}'")
            return reports
        
        print(f"Found {len(log_files)} log file(s)\n")
        
        for log_file in log_files:
            report = self.analyze_log_file(str(log_file))
            if report:
                reports.append(report)
        
        return reports


def main():
    """Main entry point."""
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║     Smart Error Log Analyzer - v1.0                      ║")
    print("║  Automated Log Parsing & Classification Tool             ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # Initialize analyzer
    analyzer = SmartErrorLogAnalyzer(output_dir='output')
    
    # Check if log file argument provided
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
        
        if os.path.isfile(log_file):
            analyzer.analyze_log_file(log_file)
        elif os.path.isdir(log_file):
            analyzer.analyze_directory(log_file)
        else:
            print(f"❌ File or directory not found: {log_file}")
    else:
        # Default: Analyze sample logs if they exist
        sample_dir = 'sample_logs'
        if os.path.isdir(sample_dir):
            print(f"\nNo file specified. Analyzing sample logs from '{sample_dir}'...\n")
            analyzer.analyze_directory(sample_dir)
        else:
            print("\n📝 Usage:")
            print("  python main.py <log_file>       - Analyze a single log file")
            print("  python main.py <directory>      - Analyze all logs in directory")
            print("\nExample:")
            print("  python main.py system.log")
            print("  python main.py ./logs/")


if __name__ == '__main__':
    main()
