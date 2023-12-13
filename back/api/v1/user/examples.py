from typing import Any, Dict

from fastapi.params import Path

param_path_user_id = Path(..., title="User ID", examples=[1])
