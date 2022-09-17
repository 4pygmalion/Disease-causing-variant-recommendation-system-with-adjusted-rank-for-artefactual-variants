import os
import uvicorn
from utils import load_yaml

ASC_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    CONFIG = load_yaml(os.path.join(ASC_DIR, "config.yaml"))
    uvicorn.run(
        app="app:api",
        host=CONFIG["API"]["HOST"],
        port=CONFIG["API"]["PORT"],
        reload=True,
        workers=10,
    )
