# Full stack on a VM preparation scripts

This is something I use to set up a new server for my full stack projects hosted on simple VM:s. It includes scripts to prepare the server, set up a reverse proxy using nginx, setting up nginx configs for SPA-apps (using React spa with react-router) and a separate API server (using Fastapi, but can be used with other frameworks compatable with Gunicorn). Scripts to set up supervisor to manage the API server are also included.

### Environment Variables
- Make sure to set the environment variables in `.env.scripts` before running the setup script.
- The `.env.scripts.example` file provides a template for the required variables.   

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
    cd <repository-name>
    ```

2. Copy the example environment file:
   ```bash
   cp .env.scripts.example .env.scripts
   ```

3. Edit the `.env.scripts` file to set your server configuration:
   ```bash
   nano .env.scripts
   ```  

4. Create a venv and install the required Python packages:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. Run the updater:
   ```bash
   python perform_update_to_server.py
   ```