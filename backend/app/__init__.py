import logging
import connexion
from pathlib import Path
from werkzeug.exceptions import HTTPException

from app.core.logging import setup_logging

logger = logging.getLogger(__name__)

def create_app():
    # Setup logging immediately
    setup_logging()
    
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
    
    # Register global exception handler for unhandled exceptions
    @connexion_app.app.errorhandler(Exception)
    def handle_unhandled_exception(e):
        """Catch-all handler for unhandled exceptions. Logs error and returns consistent 500 response."""
        # If it's already a Werkzeug HTTPException or Connexion exception, let it propagate
        # (Connexion/Flask will handle it and return appropriate HTTP response)
        if isinstance(e, (HTTPException, connexion.exceptions.ConnexionException)):
            raise e
        
        # Log the unexpected error with full context
        logger.error(f"Unhandled exception: {type(e).__name__}: {str(e)}", exc_info=True)
        
        # Return a safe error response without exposing internal details
        return {'detail': 'An internal error occurred'}, 500
    
    return connexion_app
