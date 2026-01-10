import re
from datetime import datetime
from collections import defaultdict
from pathlib import Path
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# Paths (robust: relative to this script, not where Python is run)
# ---------------------------------------------------------------------

BASE_DIR = Path(__file__).parent
COURSE_README = BASE_DIR / "course_readme" / "README.md"
SUBJECTS_FILE = BASE_DIR / "subjects.txt"


# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------

VALID_DAYS = {1, 2, 3, 4, 5, 6, 8}

CATEGORIES = [
    "≥2 days before",
    "1 day before",
    "day of deadline",
    "1 day after",
    "≥2 days after",
]


# ---------------------------------------------------------------------
# README parsing
# ---------------------------------------------------------------------

def parse_deadlines(readme_path: Path) -> dict[int, datetime]:
    """
    Extract assignment deadlines from the course README.
    Returns: {day_number: deadline_datetime}
    """
    deadlines = {}

    assignment_re = re.compile(
        r"Assignment\s*\(\s*day\s*(\d)\s*\)",
        re.IGNORECASE
    )

    deadline_re = re.compile(
        r"Dead-line:\s*(\d{4}\.\d{2}\.\d{2})\s*([0-9:]+)"
    )

    current_day = None

    with readme_path.open(encoding="utf-8") as f:
        for line in f:
            assignment_match = assignment_re.search(line)
            if assignment_match:
                current_day = int(assignment_match.group(1))
                continue

            if current_day is not None:
                deadline_match = deadline_re.search(line)
                if deadline_match:
                    date_part = deadline_match.group(1)
                    time_part = deadline_match.group(2)

                    deadlines[current_day] = datetime.strptime(
                        f"{date_part} {time_part}",
                        "%Y.%m.%d %H:%M"
                    )
                    current_day = None

    return deadlines


# ---------------------------------------------------------------------
# subjects.txt parsing
# ---------------------------------------------------------------------

def extract_day_from_title(title: str) -> int | None:
    """
    Extract day number from a project title.
    Accepts:
      Day01, day1, day 01, DAY 8, etc.
    """
    match = re.search(
        r"\bday\s*0?([1-6]|8)\b",
        title,
        re.IGNORECASE
    )
    if match:
        return int(match.group(1))
    return None


def parse_submissions(subjects_path: Path) -> list[tuple[int, datetime]]:
    """
    Parse subjects.txt and return:
    [(day_number, submission_datetime), ...]
    Columns are tab-separated:
    submission_number, status, title, (empty), timestamp
    """
    submissions = []

    with subjects_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()

            # Split by tabs
            parts = line.split("\t")
            if len(parts) < 5:
                continue

            # parts[0] = submission number
            # parts[1] = OPEN/CLOSED status
            # parts[2] = title
            # parts[3] = empty column
            # parts[4] = timestamp

            title = parts[2]
            timestamp = parts[4]

            day = extract_day_from_title(title)
            if day is None or day not in VALID_DAYS:
                continue

            try:
                submitted = datetime.strptime(
                    timestamp.strip(),
                    "%Y-%m-%dT%H:%M:%SZ"
                )
            except ValueError:
                continue

            submissions.append((day, submitted))

    return submissions


# ---------------------------------------------------------------------
# Categorization logic
# ---------------------------------------------------------------------

def categorize_submission(delta_days: int) -> int:
    """
    Convert day difference into category index.
    """
    if delta_days <= -2:
        return 0
    elif delta_days == -1:
        return 1
    elif delta_days == 0:
        return 2
    elif delta_days == 1:
        return 3
    else:
        return 4


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:
    # Sanity check
    if not COURSE_README.exists():
        raise FileNotFoundError(f"Course README not found: {COURSE_README}")
    if not SUBJECTS_FILE.exists():
        raise FileNotFoundError(f"subjects.txt not found: {SUBJECTS_FILE}")

    deadlines = parse_deadlines(COURSE_README)
    submissions = parse_submissions(SUBJECTS_FILE)

    counts = {
        day: [0] * len(CATEGORIES)
        for day in sorted(VALID_DAYS)
    }

    for day, submitted_time in submissions:
        if day not in deadlines:
            continue

        delta_days = (submitted_time.date() - deadlines[day].date()).days
        category = categorize_submission(delta_days)
        counts[day][category] += 1

    # -----------------------------------------------------------------
    # Plot
    # -----------------------------------------------------------------

    days = sorted(counts.keys())
    bottoms = [0] * len(days)

    plt.figure(figsize=(10, 6))

    for idx, label in enumerate(CATEGORIES):
        values = [counts[d][idx] for d in days]
        plt.bar(days, values, bottom=bottoms, label=label)
        bottoms = [b + v for b, v in zip(bottoms, values)]

    plt.xlabel("Assignment Day")
    plt.ylabel("Number of Submissions")
    plt.title("Submission Timing Relative to Deadline")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
