import re
import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

def extract_time_expressions(text):
    """Extract time expressions from text and convert them to timestamps."""
    today = datetime.datetime.now()
    
    # Dictionary to map time of day to hour ranges
    time_of_day = {
        "morning": (8, 0),  # 8:00 AM
        "noon": (12, 0),    # 12:00 PM
        "afternoon": (15, 0),  # 3:00 PM
        "evening": (18, 0),   # 6:00 PM
        "night": (21, 0),    # 9:00 PM
        "midnight": (0, 0),  # 12:00 AM
    }
    
    # Patterns for different time expressions
    patterns = [
        # yesterday + time of day
        (r'yesterday\s+(morning|noon|afternoon|evening|night|midnight)', 
         lambda match: (today - datetime.timedelta(days=1)).replace(
             hour=time_of_day[match.group(1)][0], 
             minute=time_of_day[match.group(1)][1], 
             second=0, microsecond=0)),
        
        # today + time of day
        (r'today\s+(morning|noon|afternoon|evening|night|midnight)', 
         lambda match: today.replace(
             hour=time_of_day[match.group(1)][0], 
             minute=time_of_day[match.group(1)][1], 
             second=0, microsecond=0)),
         
        # tomorrow + time of day
        (r'tomorrow\s+(morning|noon|afternoon|evening|night|midnight)', 
         lambda match: (today + datetime.timedelta(days=1)).replace(
             hour=time_of_day[match.group(1)][0], 
             minute=time_of_day[match.group(1)][1], 
             second=0, microsecond=0)),
        
        # last week/month/year
        (r'last\s+(week|month|year)', 
         lambda match: today - relativedelta(**{f"{match.group(1)}s": 1})),
        
        # next week/month/year
        (r'next\s+(week|month|year)', 
         lambda match: today + relativedelta(**{f"{match.group(1)}s": 1})),
        
        # n days/weeks/months/years ago
        (r'(\d+)\s+(day|week|month|year)s?\s+ago', 
         lambda match: today - relativedelta(**{f"{match.group(2)}s": int(match.group(1))})),
        
        # n days/weeks/months/years from now
        (r'(\d+)\s+(day|week|month|year)s?\s+from\s+now', 
         lambda match: today + relativedelta(**{f"{match.group(2)}s": int(match.group(1))})),
        
        # specific dates (e.g., "February 14, 2025")
        (r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(?:st|nd|rd|th)?,\s+(\d{4})\b',
         lambda match: parse(f"{match.group(1)} {match.group(2)}, {match.group(3)}")),
    ]
    
    results = []
    for pattern, handler in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                timestamp = handler(match)
                # Format timestamp as requested: DD-MM-YYYY H:MM AM/PM
                formatted_timestamp = timestamp.strftime("%d-%m-%Y %I:%M %p")
                results.append({
                    'original_text': match.group(0),
                    'timestamp': formatted_timestamp,
                    'start_pos': match.start(),
                    'end_pos': match.end()
                })
            except Exception as e:
                print(f"Error processing {match.group(0)}: {e}")
    
    return results

def convert_time_expressions(text):
    """Convert time expressions in text to timestamps."""
    expressions = extract_time_expressions(text)
    result_text = text
    
    # Sort expressions by their position in reverse order to avoid messing up positions
    for expr in sorted(expressions, key=lambda x: x['start_pos'], reverse=True):
        replacement = f"{expr['original_text']} ({expr['timestamp']})"
        result_text = result_text[:expr['start_pos']] + replacement + result_text[expr['end_pos']:]
    
    return result_text, expressions

# Example usage
if __name__ == "__main__":
    examples = [
        "Yesterday morning I went to the cinema.",
        "I have a meeting tomorrow afternoon.",
        "She said she visited Paris last week.",
        "The event was scheduled for 3 days ago.",
        "I'll see you next month.",
        "Let's meet for coffee today noon.",
        "The deadline is in 2 weeks from now.",
        "I have an appointment on February 28, 2025."
    ]
    
    for example in examples:
        converted_text, expressions = convert_time_expressions(example)
        print(f"Original: {example}")
        print(f"Converted: {converted_text}")
        print("Extracted expressions:")
        for expr in expressions:
            print(f"  - {expr['original_text']} → {expr['timestamp']}")
        print()