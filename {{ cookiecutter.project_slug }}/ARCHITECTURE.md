# DESCRIPTION

This a RESTful python flask API application for ... that uses PostgreSQL for persistance and Celery+RabbitMQ for background tasks.

It also leverages JWT for authentication (with refresh tokens).

I will start with the a simple 3-tier architecture:

1) Data Layer (PostgreSQL)
2) API Layer (Flask)
3) Background Processing Layer (RabbitMQ with workers)

This architecture is simple and effective for ... API with background processing.

When I have time to improve it, then it can be refactored with some concepts of clean/hexagonal architecture.

## Data Layer

This layer handles all data persistency.

I chose to use "Fat Models", so they contain all the business logic.

NOTE: We could just have used a flask library that provided an automatic restful wrapper on the models, without giving them this responsibility. But then this application would be much less interesting. ;)

### Database tables

```

user:
- uuid
- username
- email
- password_hash (will need `flask-bcrypt` python lib)
- created_at
- last_updated_at
- ... (backref)

...

```

---

## API Layer (Flask)

This layer is responsible for collecting the user requests and directing them to the appropriate model(s) on the Data Layer. So, it contains no business logic.

The user authentication uses JWT.

### About JWT authentication

JWT (JSON Web Token) is a compact, URL-safe token used for authentication and authorization in web applications.

It consists of three parts:

- Header (metadata, typically contains alg and typ).
- Payload (claims, e.g., user ID, role, expiration).
- Signature (ensures token integrity).

JWTs are stateless because they don’t require server-side session storage - authentication information is embedded in the token itself.

#### JWT token library

I use the JWT token library `flask-jwt-extended`.

This library provides:

- Short-lived access tokens - preventing prolonged unauthorized access.
- Refresh tokens - allow secure re-authentication.
- No sensitive data in JWT payload (only user UUID).
- Token signing (prevents tampering).

#### JWT authentication workflow

1) User logs in with email/password.

2) Server verifies credentials and generates:
- Access Token (short-lived, used for authenticated requests).
- Refresh Token (long-lived, used to get a new access token).

3) Client stores tokens

4) Client sends the access token in the `Authorization: Bearer <token>` header for every request.

5) Server validates the token:
- If valid: process request.
- If expired: Client must use refresh token (see below) to get a new access token.

6) Refresh Token Flow:
- Client sends refresh token to /refresh endpoint.
- Server generates a new access token.

---

## Background Processing Layer (RabbitMQ with workers)

This layer is responsible for running tasks that will not fit the request-response model due to taking too long to execute.

The infrastructure to run Celery with RabbitMQ as the broker is fully functional, but due to time constraints there is no "useful" background task in the project yet that leverages it.

But there are 2 API endpoints that can be triggered via API to send a task to the queue:

- /compute
- /string

You can view them on the API docs using flasgger.
