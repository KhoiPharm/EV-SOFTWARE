from __future__ import annotations


class AppError(Exception):
    """Base typed error with a safe public representation."""

    code = "application_error"
    public_message = "The application could not complete the request."
    status_code = 500


class ConfigurationError(AppError):
    code = "configuration_error"
    public_message = "Application configuration is invalid."


class DatabaseUnavailableError(AppError):
    code = "database_unavailable"
    public_message = "Required database infrastructure is unavailable."
    status_code = 503


class InternalError(AppError):
    code = "internal_error"
    public_message = "An unexpected internal error occurred."
