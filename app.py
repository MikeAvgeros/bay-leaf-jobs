import os
from application import create_app

# Instantiate the app
app = create_app()

# Run the app
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")))
