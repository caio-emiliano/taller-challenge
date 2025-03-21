import re
from collections import Counter

def analyze_logs(log_file_path, top_responses=3, top_errors=2):
    """
    Analyze log file and generate a structured report.
    
    Args:
        log_file_path (str): Path to the log file
        top_responses (int): Number of top responses to include
        top_errors (int): Number of top errors to include
        
    Returns:
        str: Formatted report string with log summary,
             top AI responses, and most common errors
    """
    # TODO: Implement this function
    return read_file(log_file_path)

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def parse_agent_logs(report_str):

    log_lines = report_str.splitlines()

    pattern = re.compile(r'\[(.*?)\]\s+(\w+)\s+-\s+(.*)')

    level_counter = Counter()
    ai_response_counter = Counter()
    error_counter = Counter()

    for line in log_lines:
        line = line.strip()

        if not line:
            continue

        match = pattern.match(line)
        if match:
            timestamp, level, message = match.groups()
            level_counter[level] += 1

            if level == "INFO" and "Agent Response:" in message:
                response_match = re.search(r'Agent Response:\s*"(.+?)"', message)
                if response_match:
                    response_text = response_match.group(1)
                    ai_response_counter[response_text] += 1

            if level == "ERROR":
                error_counter[message] += 1

    output_lines = []
    output_lines.append("Log Summary:")
    output_lines.append(f"- INFO messages: {level_counter.get('INFO', 0)}")
    output_lines.append(f"- ERROR messages: {level_counter.get('ERROR', 0)}")
    output_lines.append(f"- WARNING messages: {level_counter.get('WARNING', 0)}")
    output_lines.append("")
    
    output_lines.append("Top 3 AI Responses:")
    for i, (response, count) in enumerate(ai_response_counter.most_common(3), 1):
            output_lines.append(f"{i}. \"{response}\" ({count} times)")

    output_lines.append("")

    output_lines.append("Most Common Errors:")
    for i, (error, count) in enumerate(error_counter.most_common(), 1):
            output_lines.append(f"{i}. {error} ({count} times)")

    final_output = "\n".join(output_lines)
    return final_output


if __name__ == "__main__":
    report = analyze_logs("sample.log")
    final_output = parse_agent_logs(report)
    print(final_output)
    


