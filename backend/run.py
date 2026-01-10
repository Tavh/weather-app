
from app import create_app
from app.core.database import init_db

connexion_app = create_app()
app = connexion_app.app  # Expose the internal Flask app

if __name__ == '__main__':
    # Initialize DB tables explicitly
    print("Initializing database...")
    init_db()
    
    # Use the underlying Flask app's run method to avoid needing uvicorn
    app.run(port=8080, debug=True)
