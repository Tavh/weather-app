
import connexion
from typing import Optional, Dict, Any
from pathlib import Path

def create_app(test_config: Optional[Dict[str, Any]] = None) -> connexion.FlaskApp:
    """
    Current Folder Layout:
    /app
      /__init__.py
      /api
      /core
      ...
    /openapi
      /openapi.yaml
    """
    # Specification is in ../openapi/openapi.yaml relative to this file
    specification_dir = Path(__file__).parent.parent / 'openapi'
    
    app = connexion.FlaskApp(__name__, specification_dir=specification_dir)
    
    # Load the OpenAPI specification
    # This automatically registers the routes defined in openapi.yaml
    # pointing to functions in the 'app.api' package (operationId)
    app.add_api(
        'openapi.yaml', 
        strict_validation=True, 
        validate_responses=True
    )
    
    flask_app = app.app
    
    # Configure Flask app here (DB, etc)
    # flask_app.config.from_object('app.core.config.Config')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=8080)
