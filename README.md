# docker-compose-env
 Building a Web Server for DevOps/ SRE environment.

 ## Setup Instructions
1. Clone this repository.
2. Ensure Docker and Docker Compose are installed.
3. Run `docker-compose up --build` to start the services.
4. Access the app at http://localhost.

## CI/CD
On push to main, GitHub Actions builds and pushes the Docker image to Docker Hub. Set DOCKER_USERNAME and DOCKER_PASSWORD in repository secrets.
