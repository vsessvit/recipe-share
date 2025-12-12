"""
Custom middleware for security headers
"""


class SecurityHeadersMiddleware:
    """Add additional security headers to responses"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only add security headers in production (when HTTPS is available)
        if not request.is_secure():
            return response

        # Permissions Policy (formerly Feature Policy)
        response["Permissions-Policy"] = (
            "geolocation=(), "
            "microphone=(), "
            "camera=(), "
            "payment=(), "
            "usb=(), "
            "magnetometer=(), "
            "gyroscope=(), "
            "accelerometer=()"
        )

        # Content Security Policy (allows all legitimate external resources)
        response["Content-Security-Policy"] = (
            "default-src 'self'; "
            "img-src 'self' https://res.cloudinary.com https: data: blob:; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://stackpath.bootstrapcdn.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "font-src 'self' https://cdnjs.cloudflare.com data:; "
            "connect-src 'self' https://res.cloudinary.com; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )

        return response
