from fastapi import FastAPI, Response

app = FastAPI(title="Cost of borrowing API")


@app.get("/health", status_code=204)
def health() -> Response:
    return Response(status_code=204)

