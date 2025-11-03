# Failure Pattern Detection in CI Logs

A DevOps project that analyzes CI logs to detect failure patterns and provide insights.

## Features

- Automated CI log analysis
- Pattern detection for common failures
- Web interface for manual log upload
- GitHub Actions integration
- Deployment to Render

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `pytest`
4. Start the application: `python app.py`

## GitHub Actions

The project includes a CI/CD pipeline that:
- Runs tests on push and pull requests
- Analyzes logs for patterns
- Deploys to Render on main branch

## Deployment

The application is configured for deployment on Render. The `render.yaml` file contains the deployment configuration.

## Usage

1. Upload CI log files through the web interface
2. Or use the API endpoint: `POST /analyze` with log content
3. View analysis results with patterns and recommendations