#!/bin/bash
echo "Empire OS - System Monitor"
echo "=========================="
echo ""
echo "1. Check container status:"
docker-compose ps
echo ""
echo "2. Check system logs:"
docker-compose logs --tail=50
echo ""
echo "3. Check resource usage:"
docker stats --no-stream
echo ""
echo "4. Check database connections:"
docker exec empire-db psql -U empire -d empire -c "SELECT count(*) FROM pg_stat_activity;"
echo ""
echo "5. System health:"
curl -s http://localhost/system/health | python3 -m json.tool
