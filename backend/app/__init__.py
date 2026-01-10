import connexion
from pathlib import Path

def create_app():
    # Specification dir
    specification_dir = Path(__file__).parent.parent / 'openapi'
    
    # Create the Connexion application instance (v2 style)
    connexion_app = connexion.App(__name__, specification_dir=specification_dir)
    
    # Read the openapi.yaml
    connexion_app.add_api(
        'openapi.yaml', 
        strict_validation=True, 
        validate_responses=True
    )
    
    return connexion_app
