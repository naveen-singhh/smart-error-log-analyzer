# Smart Error Log Analyzer

A powerful Python-based log analysis tool that automatically parses, classifies, and analyzes system logs to enable faster debugging and improved system monitoring.

## 🎯 Key Features

✅ **Intelligent Log Parsing**
- Extracts timestamps, log levels, sources, and messages from various log formats
- Supports multiple timestamp patterns (YYYY-MM-DD HH:MM:SS, DD/Mon/YYYY, etc.)
- Handles malformed entries gracefully

✅ **Automatic Classification**
- Categorizes logs into **ERROR**, **WARNING**, and **INFO** classes
- Uses pattern matching and keyword analysis for accurate classification
- Provides confidence scores for each classification

✅ **Comprehensive Reporting**
- Generates detailed analysis reports
- Provides summary statistics and breakdowns
- Identifies top errors and warnings
- Analyzes logs by source/component
- Offers actionable recommendations

✅ **Multiple Output Formats**
- JSON reports for programmatic processing
- HTML reports for visual analysis
- Console output for quick insights

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher

### Setup

1. Clone or navigate to the project directory:
```bash
cd "Smart Error Log Analyzer"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Usage

### Basic Usage

Analyze a single log file:
```bash
python smart_error_log_analyzer/main.py system.log
```

Analyze all logs in a directory:
```bash
python smart_error_log_analyzer/main.py ./logs/
```

### Example 1: Analyze Sample Log
```bash
python smart_error_log_analyzer/main.py sample_logs/system.log
```

This will:
1. Parse all log entries
2. Classify them into ERROR, WARNING, and INFO
3. Generate a comprehensive report
4. Save JSON and HTML reports to the `output/` directory
5. Display a summary in the console

### Example 2: Batch Analysis
```bash
python smart_error_log_analyzer/main.py sample_logs/
```

Analyzes all `.log` files in the directory.

## 📊 Report Components

Each generated report includes:

### Summary Statistics
- Total log entries
- Error, warning, and info count
- Percentage distribution
- Overall severity level (LOW, MEDIUM, HIGH, CRITICAL)

### Category Breakdown
- Detailed list of entries in each category
- Line numbers for reference
- Source/component information
- Classification confidence scores

### Source Analysis
- Error and warning distribution by component
- Top sources causing issues

### Top Errors & Warnings
- Most frequently occurring errors
- Most frequently occurring warnings
- Occurrence count for each

### Confidence Analysis
- Average, minimum, and maximum confidence scores
- Overall classification reliability metrics

### Recommendations
- Actionable insights based on log analysis
- Severity assessments
- Suggestions for system improvement

## 🏗️ Project Structure

```
Smart Error Log Analyzer/
│
├── smart_error_log_analyzer/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Entry point application
│   ├── log_parser.py            # Log parsing module
│   ├── log_classifier.py        # Log classification module
│   ├── report_generator.py      # Report generation module
│   └── (main modules)
│
├── sample_logs/                 # Sample log files for testing
│   ├── system.log
│   └── app.log
│
├── output/                      # Generated reports directory
│   ├── system_report.json
│   ├── system_report.html
│   ├── app_report.json
│   └── app_report.html
│
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── LICENSE                      # License file

```

## 🔧 Module Details

### log_parser.py
**LogParser** class handles log file parsing:
- `parse_file(file_path)` - Parse a log file and extract structured data
- `get_logs()` - Retrieve all parsed logs
- `get_parsed_count()` - Get number of parsed entries

**Features:**
- Multiple timestamp pattern matching
- Automatic level detection (ERROR, WARNING, INFO, DEBUG)
- Source extraction from log structure
- Message cleanup and extraction

### log_classifier.py
**LogClassifier** class categorizes logs:
- `classify_logs(logs)` - Classify a list of log entries
- `get_classified_logs()` - Get all classified logs
- `get_statistics()` - Get classification statistics
- `filter_by_category(category)` - Filter logs by category
- `get_errors()` / `get_warnings()` / `get_info()` - Get specific categories

**Classification Methods:**
- Level-based (from parsed log level)
- Content-based (keyword matching)
- Confidence scoring

### report_generator.py
**ReportGenerator** class creates analysis reports:
- `generate_report(classified_logs)` - Generate comprehensive report
- `save_report_json(output_path)` - Save as JSON
- `save_report_html(output_path)` - Save as HTML with styling
- `print_report()` - Print to console
- `get_report()` - Get report dictionary

**Report Sections:**
- Summary statistics
- Category breakdown
- Source analysis
- Top errors and warnings
- Confidence metrics
- Recommendations

## 📝 Sample Log Formats Supported

The parser supports various common log formats:

```
# Format 1: Timestamp + Level + Message
2024-01-15 08:00:00 [ERROR] Database connection failed

# Format 2: With Source/Component
2024-01-15 08:01:20 [ERROR] [AuthService] Authentication denied

# Format 3: Abbreviated Level
2024-01-15 09:00:00 [ERR] System error occurred

# Format 4: Without Brackets
2024-01-15 08:00:00 ERROR Database connection failed
```

## 🎨 Output Examples

### Console Output
```
============================================================
📊 SMART ERROR LOG ANALYZER - REPORT
============================================================

Timestamp: 2024-01-15T10:30:45.123456
Total Log Entries: 40

--- Summary ---
❌ Errors:   8 (20.0%)
⚠️  Warnings: 10 (25.0%)
ℹ️  Info:     22 (55.0%)

Severity Level: MEDIUM

--- Recommendations ---
• Significant number of warnings detected. Review and address potential issues.
• Continue monitoring log patterns for potential issues.
```

### HTML Report
- Styled dashboard with statistics
- Visual severity indicator
- Color-coded categories
- Generated timestamp
- Professional formatting

### JSON Report
Machine-readable format with all details for integration with other tools.

## 🔍 Classification Logic

Logs are classified using a multi-level approach:

1. **Level-based Classification** (Primary)
   - If log has ERROR level → ERROR category
   - If log has WARNING/WARN level → WARNING category
   - If log has INFO level → INFO category

2. **Content-based Classification** (Fallback)
   - Analyzes message for error keywords (failed, exception, critical, etc.)
   - Analyzes message for warning keywords (warn, deprecated, slow, etc.)
   - Analyzes message for info keywords (started, completed, loaded, etc.)

3. **Confidence Scoring**
   - Based on keyword matches
   - Range: 0.0 to 1.0
   - Higher score = higher confidence in classification

## 📊 Severity Assessment

The system automatically assesses overall severity:

- **CRITICAL**: > 30% error rate
- **HIGH**: > 15% error rate
- **MEDIUM**: > 5% error rate
- **LOW**: ≤ 5% error rate

## 🚀 Performance Features

- **Efficient String Processing**: Uses regex patterns for fast parsing
- **Streaming Parsing**: Processes large files without loading entire file in memory
- **Optimized Classification**: Keyword-based classification with caching
- **Quick Report Generation**: Generates insights in seconds

## 💡 Use Cases

1. **System Administration**
   - Monitor server health
   - Identify failing services
   - Track system performance issues

2. **Application Debugging**
   - Quick error categorization
   - Identify error patterns
   - Track warning trends

3. **Security Monitoring**
   - Detect unauthorized access attempts
   - Identify suspicious log patterns
   - Alert on critical events

4. **Performance Analysis**
   - Track slow operations
   - Monitor resource constraints
   - Identify bottlenecks

## 🔐 Best Practices

1. **Log Rotation**: Regularly archive old logs
2. **Backup Reports**: Keep report copies for audit trails
3. **Regular Analysis**: Schedule periodic log analysis
4. **Alert Integration**: Use JSON reports to feed into monitoring systems
5. **Pattern Recognition**: Review top errors regularly

## 📈 Future Enhancements

Potential improvements:

- Machine learning-based classification
- Real-time log streaming analysis
- Database storage integration
- Alert notification system
- Web UI dashboard
- Log correlation across multiple files
- Anomaly detection
- Historical trend analysis

## 🤝 Contributing

Feel free to enhance this tool with:
- Additional log format support
- Improved classification algorithms
- New report formats
- Performance optimizations

## 📄 License

This project is open source and available for educational and professional use.

## 🆘 Troubleshooting

**Issue: Script not found**
```bash
# Make sure you're in the correct directory
cd "Smart Error Log Analyzer"
```

**Issue: No logs found**
```bash
# Check log file exists and has .log extension
# Or specify full path to log file
python smart_error_log_analyzer/main.py /full/path/to/logfile.log
```

**Issue: Import errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## 📞 Quick Start

```bash
# 1. Navigate to project
cd "Smart Error Log Analyzer"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Analyze sample logs
python smart_error_log_analyzer/main.py sample_logs/system.log

# 4. Check output folder for generated reports
# - output/system_report.html (visual dashboard)
# - output/system_report.json (data export)
```

---

**Smart Error Log Analyzer v1.0** - Making log analysis faster and smarter! 🚀
