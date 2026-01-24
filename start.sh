#!/bin/bash
echo "Starting Empire OS..."
docker-compose up --build -d
echo "System started. Access at http://localhost"
echo "Dashboard: http://localhost"
echo "API Docs: http://localhost/docs"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
