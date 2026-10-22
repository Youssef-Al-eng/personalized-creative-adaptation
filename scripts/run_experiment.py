from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from adapt import run
root=Path(__file__).parents[1]; print(json.dumps(run(root/'results'),indent=2))
