"""
Log Report Generator Script
-----------------------------
Author: James Strickland
Contact: webmaster@strickstuff.com
Website: strickstuff.com

This script reads a web server log file, parses the data, and generates an HTML report.
The report includes information about IP addresses, operating systems, referrers,
and request counts, sorted by IP address.

Usage: python logreport.py <log_file_path>
"""

import sys
import re
from datetime import datetime
from collections import Counter, defaultdict
from urllib.parse import unquote

# Regex for parsing user-agent strings to extract the OS
os_regex = re.compile(r'\(([^)]+)\)')

# Function to parse a single log line
def parse_log_line(line):
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s-\s-\s'
        r'\[(?P<datetime>[^\]]+)\]\s'
        r'"(?P<request_method>GET|POST|PUT|DELETE|HEAD)\s'
        r'(?P<request_url>[^ ]+)\s'
        r'(?P<http_version>HTTP/\d\.\d)"\s'
        r'(?P<status_code>\d+)\s'
        r'(?P<response_size>\d+)\s'
        r'"(?P<referrer>[^"]*)"\s'
        r'"(?P<user_agent>[^"]*)"'
    )

    match = log_pattern.match(line)
    if match:
        data = match.groupdict()
        data['datetime'] = datetime.strptime(data['datetime'], '%d/%b/%Y:%H:%M:%S %z')
        data['request_url'] = unquote(data['request_url'])
        data['referrer'] = unquote(data['referrer'])
        os_match = os_regex.search(data['user_agent'])
        data['os'] = os_match.group(1) if os_match else 'Unknown'
        return data
    return None

# Read the log file
def read_log_file(file_path):
    with open(file_path, 'r') as file:
        return [parse_log_line(line) for line in file if parse_log_line(line) is not None]

# Function to generate HTML report
def generate_html_report(report_data):
    html_content = "<html><head><title>Log Report</title></head><body>"
    html_content += "<h1>Log Report</h1>"
    html_content += "<table border='1'><tr><th>IP Address</th><th>OS</th><th>Referrer</th><th>Request Count</th></tr>"

    for ip in sorted(report_data):
        os_info, referrer_info = report_data[ip]['os'][0], report_data[ip]['referrer'][0]
        html_content += f"<tr><td>{ip}</td><td>{os_info[0]}</td><td>{referrer_info[0]}</td><td>{report_data[ip]['count']}</td></tr>"

    html_content += "</table></body></html>"
    return html_content

# Function to write HTML content to a file
def write_html_file(content, filename):
    with open(filename, 'w') as file:
        file.write(content)

# Generate report from log data
def generate_report(log_data):
    report_data = defaultdict(lambda: {'os': Counter(), 'referrer': Counter(), 'count': 0})

    for entry in log_data:
        if entry:
            ip = entry['ip']
            report_data[ip]['os'][entry['os']] += 1
            report_data[ip]['referrer'][entry['referrer']] += 1
            report_data[ip]['count'] += 1

    # For simplicity, picking the most common OS and referrer for each IP
    for ip in report_data:
        report_data[ip]['os'] = report_data[ip]['os'].most_common(1)
        report_data[ip]['referrer'] = report_data[ip]['referrer'].most_common(1)

    return report_data

# Main function
def main():
    if len(sys.argv) != 2:
        print("Usage: python logreport.py <log_file_path>")
        sys.exit(1)

    log_file_path = sys.argv[1]
    log_data = read_log_file(log_file_path)
    report_data = generate_report(log_data)

    # Generate HTML content
    html_content = generate_html_report(report_data)

    # Write the HTML content to a file
    output_filename = "log_report.html"
    write_html_file(html_content, output_filename)
    print(f"Report generated: {output_filename}")

if __name__ == "__main__":
    main()

