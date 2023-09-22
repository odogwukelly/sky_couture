# Import the Flask app object from the 'shop' module
from shop import app

# Check if this script is being run as the main program
if __name__ == "__main__":
     # Run the Flask app with debugging mode enabled
    app.run(debug=True)