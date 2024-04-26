from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse
from modules.sentiment_analysis.sentiment_analysis import router as sentiment_analysis_router
from modules.trend_detector.trend_detector import router as trend_detector_router
from modules.data_toolkit.nse.nse_operations import  NSEIndices, NSEEquities
from modules.data_toolkit.screener.screener_equities import ScreenerEquities

app = FastAPI()

custom_docs_url = "https://fin-maestro-kin.apidog.io"

@app.middleware("http")
async def apidog_docs_redirect(request: Request, call_next):
    if request.url.path == "/docs":
        return RedirectResponse(url=custom_docs_url, status_code=307)
    return await call_next(request)

app.include_router(sentiment_analysis_router)
app.include_router(trend_detector_router)

screener_eq = ScreenerEquities()
screener_eq.register_routes(app)

nse_eq = NSEEquities()
nse_eq.register_routes(app)

nse_indices = NSEIndices()
nse_indices.register_routes(app)

