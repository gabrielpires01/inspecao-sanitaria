from app.enums import Severity, Status

SEVERITY_TO_STATUS = {
    Severity.low: Status.low,
    Severity.moderate: Status.moderate,
    Severity.major: Status.major,
    Severity.critical: Status.critical,
}
