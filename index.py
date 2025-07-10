import re
from datetime import datetime, timedelta


def snap_to_value(dt: datetime, snap_value: str) -> datetime:
    """
    Snaps a datetime to a specified precision by zeroing out smaller units.
    Args:
        dt (datetime): The datetime object to snap.
        snap_value (str): The precision to snap to.
            's': Snap to minute (zeroes seconds and microseconds)
            'm': Snap to hour (zeroes minutes, seconds, and microseconds)
            'd': Snap to day (zeroes hours, minutes, seconds, and microseconds)
            'mon': Snap to month (sets day to 1 and zeroes hours, minutes, seconds, and microseconds)
    Returns:
        datetime: A new datetime object snapped to the specified precision.
    """

    if snap_value == "s":
        return dt.replace(second=0, microsecond=0)
    elif snap_value == "m":
        return dt.replace(minute=0, second=0, microsecond=0)
    elif snap_value == "d":
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    elif snap_value == "mon":
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    raise ValueError(f"Uknown snap value: @{snap_value}")


def calculate_months(dt: datetime, months: int) -> datetime:
    """
    Calculate a new datetime by adding or subtracting a specified number of months.
    This function properly handles month boundaries and leap years when calculating dates.
    Args:
        dt (datetime): The original datetime object.
        months (int): Number of months to add (positive) or subtract (negative).
    Returns:
        datetime: A new datetime object with the month adjustment applied.
    Examples:
        >>> from datetime import datetime
        >>> dt = datetime(2023, 1, 31)
        >>> calculate_months(dt, 1)
        datetime.datetime(2023, 2, 28)
        >>> calculate_months(dt, -2)
        datetime.datetime(2022, 11, 30)
    """

    # Calculate new month and year
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1

    # Handle day overflow (e.g., 31st -> 28th or 30th)
    day = min(
        dt.day,
        [
            31,
            29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31,
        ][month - 1],
    )

    return dt.replace(year=year, month=month, day=day)


def parse(expr: str, now: datetime = datetime.now()) -> datetime:
    """
    Parse a time expression and return a datetime object.
    The expression must follow the format: now() [+/-] [value][unit][@snap]
    Parameters:
        expr (str): The time expression to parse.
            Format: now() [+/-] [value][unit][@snap]
            Examples:
                - "now() + 5h"       (5 hours from now)
                - "now() - 10d"      (10 days ago)
                - "now() + 3m@day"   (3 months from now, snapped to start of day)
        now (datetime, optional): The reference datetime to use as "now".
            Defaults to the current datetime.
    Returns:
        datetime: The calculated datetime based on the expression.
    Raises:
        ValueError: If the expression does not match the expected format.
    Supported units:
        - s: seconds
        - m: minutes
        - h: hours
        - d: days
        - mon: months
    Supported snap values:
        Can be used with @[snap] at the end of the expression to snap the
        resulting datetime to a specific time boundary.
    """

    new_date = None

    # Handle white space and force lowercase
    expr.strip().lower()

    # check the format of the argument
    pattern = r"^now\(\)\s*([+-])\s*(\d+)(s|m|h|d|mon)(@([a-z]+))?$"
    match = re.match(pattern, expr)

    # Unpack values and units
    symbol, value, time_value, _, snap_value = match.groups()
    value = int(value)

    # Error if the string does not match the regex
    if not match:
        raise ValueError(f"{expr} is invalid")

    # A map for the timedelta function
    time_value_map = {
        "s": "seconds",
        "m": "minutes",
        "h": "hours",
        "d": "days",
    }

    # Check if we are adding or subtracting datetimes
    if symbol == "+":
        new_date = (
            calculate_months(now, value)
            if time_value == "m"
            else now + timedelta(**{time_value_map[time_value]: value})
        )
    else:
        new_date = (
            calculate_months(now, -value)
            if time_value == "m"
            else now - timedelta(**{time_value_map[time_value]: value})
        )

    if snap_value:
        new_date = snap_to_value(new_date, snap_value)

    return new_date


result = parse("now()+1m@m")
