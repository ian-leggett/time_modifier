# Time Parse

A simple Python library for parsing human-readable time expressions and calculating datetime values.

## Overview

This library provides a `parse()` function that interprets time expressions in the format `now() [+/-] [value][unit][@snap]` and returns a corresponding `datetime` object.

## Features

- Parse relative time expressions from a reference point
- Support for multiple time units (seconds, minutes, hours, days, months)
- Optional time snapping to specific boundaries
- Proper handling of month calculations and leap years

## Usage

```python
from index import parse
from datetime import datetime

# Basic usage with default "now"
result = parse("now() + 5h")  # 5 hours from now
result = parse("now() - 2d")  # 2 days ago

# Using a custom reference time
fixed_date = datetime(2025, 7, 10, 21, 20, 42)
result = parse("now() + 3d", now=fixed_date)  # 3 days from fixed_date

# Using time snapping
result = parse("now() + 1mon@d")  # 1 month from now, snapped to start of day
```

## Expression Format

```
now() [+/-] [value][unit][@snap]
```

### Supported Units
- `s`: seconds
- `m`: minutes  
- `h`: hours
- `d`: days
- `mon`: months

### Supported Snap Values
- `s`: Snap to minute (zero seconds and microseconds)
- `m`: Snap to hour (zero minutes, seconds, and microseconds)
- `d`: Snap to day (zero hours, minutes, seconds, and microseconds)
- `mon`: Snap to month (set day to 1 and zero time components)

## Examples

```python
# Add time
parse("now() + 30s")     # 30 seconds from now
parse("now() + 15m")     # 15 minutes from now
parse("now() + 6h")      # 6 hours from now
parse("now() + 7d")      # 7 days from now
parse("now() + 2mon")    # 2 months from now

# Subtract time
parse("now() - 1h")      # 1 hour ago
parse("now() - 10d")     # 10 days ago

# With snapping
parse("now() + 1d@d")    # Tomorrow at midnight
parse("now() + 1mon@mon") # Next month on the 1st at midnight
```

## Running Tests

```bash
python test.py
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)