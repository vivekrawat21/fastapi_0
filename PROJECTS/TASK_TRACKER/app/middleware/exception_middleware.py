import logging
import uuid
import time
from datetime import datetime
from typing import Callable

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

logger = logging.getLogger("uvicorn.error")

def _make_problem_details(
    request: Request,
    status: int,
    title: str,
    detail: str,
    trace_id: str,
    type_: str = "about:blank",
):
    return {
        "type": type_,
        "title": title,
        "status": status,
        "detail": detail,
        "instance": str(request.url.path),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "trace_id": trace_id,
    }

def exception_middleware_factory():
    async def exception_middleware(request: Request, call_next: Callable):
        trace_id = str(uuid.uuid4())
        start = time.perf_counter()
        # Let CORS preflight pass through untouched
        if request.method == "OPTIONS":
            return await call_next(request)

        try:
            response = await call_next(request)
            duration_ms = int((time.perf_counter() - start) * 1000)
            logger.info(
                "request",
                extra={
                    "method": request.method,
                    "path": str(request.url.path),
                    "status": getattr(response, "status_code", None),
                    "duration_ms": duration_ms,
                    "trace_id": trace_id,
                },
            )
            # Convert any non-successful response into ProblemDetails for consistency
            if response.status_code >= 400:
                # If the response already looks like a ProblemDetails (has trace_id), return as-is
                try:
                    body = response.json()
                    if isinstance(body, dict) and "trace_id" in body:
                        return response
                    detail = body.get("detail") if isinstance(body, dict) else str(body)
                except Exception:
                    try:
                        detail = response.text
                    except Exception:
                        detail = str(response.status_code)

                payload = _make_problem_details(
                    request,
                    status=response.status_code,
                    title=response.status_code and f"HTTP {response.status_code}" or "Error",
                    detail=detail,
                    trace_id=trace_id,
                    type_=f"about:blank#http{response.status_code}",
                )
                return JSONResponse(payload, status_code=response.status_code)

            return response

        except HTTPException as exc:
            payload = _make_problem_details(
                request,
                status=exc.status_code,
                title=exc.detail if isinstance(exc.detail, str) else "HTTP error",
                detail=str(exc.detail),
                trace_id=trace_id,
                type_=f"about:blank#http{exc.status_code}",
            )
            logger.warning("http_exception", exc_info=exc, extra={"trace_id": trace_id})
            return JSONResponse(payload, status_code=exc.status_code)

        except RequestValidationError as exc:
            detail = exc.errors() if hasattr(exc, "errors") else str(exc)
            payload = _make_problem_details(
                request,
                status=422,
                title="Validation Error",
                detail=str(detail),
                trace_id=trace_id,
                type_="about:blank#validation",
            )
            logger.warning("validation_error", exc_info=exc, extra={"trace_id": trace_id})
            return JSONResponse(payload, status_code=422)

        except Exception as exc:
            logger.exception("unhandled_exception", exc_info=exc, extra={"trace_id": trace_id})
            payload = _make_problem_details(
                request,
                status=500,
                title="Internal Server Error",
                detail="An unexpected error occurred.",
                trace_id=trace_id,
                type_="about:blank#internal",
            )
            return JSONResponse(payload, status_code=500)

    return exception_middleware
