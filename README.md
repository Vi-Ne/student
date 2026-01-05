# Student Management System

A simple CRUD API for managing students with PostgreSQL database, Docker deployment, and monitoring tools.

## Features

- **CRUD Operations**: Create, Read, Update, Delete students
- **PostgreSQL Database**: Persistent data storage
- **Docker Support**: Containerized deployment
- **Monitoring**: Prometheus, Grafana, cAdvisor integration
- **Health Checks**: API health monitoring
- **Render Deployment**: Cloud deployment ready

## API Endpoints

- `GET /health` - Health check
- `GET /students` - Get all students
- `GET /students/{id}` - Get student by ID
- `POST /students` - Create new student
- `PUT /students/{id}` - Update student
- `DELETE /students/{id}` - Delete student

## Student Schema

```json
{
  "name": "string",
  "email": "string",
  "age": "integer",
  "course": "string"
}
```

## Local Development

### Using Docker Compose (Recommended)

```bash
# Start all services (app, database, monitoring)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set database URL
export DATABASE_URL="postgresql://postgres:Vi1279_@2004@localhost:5432/student_db"

# Run application
python app.py
```

## Services Access

- **API**: http://localhost:5000
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **cAdvisor**: http://localhost:8080
- **PostgreSQL**: localhost:5432

## API Usage Examples

### Create Student
```bash
curl -X POST http://localhost:5000/students \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "age": 20, "course": "Computer Science"}'
```

### Get All Students
```bash
curl http://localhost:5000/students
```

### Update Student
```bash
curl -X PUT http://localhost:5000/students/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "age": 21}'
```

### Delete Student
```bash
curl -X DELETE http://localhost:5000/students/1
```

## Render Deployment

1. **Create PostgreSQL Database** on Render
2. **Update render.yaml** with your database URL
3. **Deploy** using Render's GitHub integration
4. **Set Environment Variables**:
   - `DATABASE_URL`: Your Render PostgreSQL connection string

## Monitoring Setup

### Grafana Dashboards
1. Access Grafana at http://localhost:3000
2. Login with admin/admin
3. Add Prometheus data source: http://prometheus:9090
4. Import dashboard for Flask metrics and container monitoring

### Prometheus Metrics
- Application metrics: `/metrics` endpoint
- Container metrics: cAdvisor integration
- Custom business metrics available

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `PORT`: Application port (default: 5000)

## Production Considerations

- Use environment-specific database credentials
- Enable SSL for database connections
- Configure proper logging
- Set up backup strategies
- Monitor resource usage through Grafana dashboards