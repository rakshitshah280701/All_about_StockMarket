import os
import sys
import webbrowser
from threading import Timer
from dotenv import load_dotenv

def main():
    # Ensure we're in the right directory and load environment variables
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        bundle_dir = os.path.dirname(sys._MEIPASS)
        os.chdir(bundle_dir)
        # Load .env from the bundle directory
        env_path = os.path.join(bundle_dir, '.env')
        load_dotenv(env_path)
    else:
        # Running as script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        # Load .env from the script directory
        load_dotenv()
    
    # print(f"Working directory: {os.getcwd()}")
    # print(f"NEWSDATA_API_KEY present: {bool(os.getenv('NEWSDATA_API_KEY'))}")
    
    # Import app after environment variables are loaded
    from app import app
    
    # Open browser after a short delay
    def open_browser():
        webbrowser.open('http://localhost:5001')
    
    Timer(1.5, open_browser).start()
    
    # Run the Flask app
    app.run(host="0.0.0.0", port=5001, debug=False)

if __name__ == "__main__":
    main()