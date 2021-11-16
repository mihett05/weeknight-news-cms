import os
from uvicorn import run
from app.pre_start import pre_start


if __name__ == "__main__":
    pre_start()
    is_debug = bool(os.getenv("DEBUG"))
    run(
        "app.main:app",
        host="localhost",
        port=8080,
        debug=is_debug,
        reload=is_debug,
    )
