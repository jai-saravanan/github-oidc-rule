# Customer API - FastAPI on AWS Lambda

A simple FastAPI application for managing customers with health check endpoint, ready for AWS Lambda deployment.

## Features

- **Health Check**: `/health` - Returns API status
- **Add Customer**: `POST /customers` - Create a new customer
- **List Customers**: `GET /customers` - Retrieve all customers
- **Get Customer**: `GET /customers/{customer_id}` - Get specific customer
- **Update Customer**: `PUT /customers/{customer_id}` - Update customer details
- **Delete Customer**: `DELETE /customers/{customer_id}` - Remove a customer

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run locally
python main.py
```

API available at: `http://localhost:8000`

### Swagger UI (Interactive API Docs)
- **Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Try it out:
- Click "Try it out" on any endpoint
- Fill in request body
- Click "Execute"
- See response instantly!

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Add Customer
```bash
curl -X POST http://localhost:8000/customers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-0123"
  }'
```

### List Customers
```bash
curl http://localhost:8000/customers
```

### Get Customer
```bash
curl http://localhost:8000/customers/1
```

### Update Customer
```bash
curl -X PUT http://localhost:8000/customers/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com"
  }'
```

### Delete Customer
```bash
curl -X DELETE http://localhost:8000/customers/1
```

## Deploy to AWS Lambda with GitHub Actions + OIDC

### Quick Start

Follow the **8-step guide** in [SETUP_GITHUB_OIDC.md](SETUP_GITHUB_OIDC.md):

1. Get AWS Account ID
2. Get GitHub details
3. Create OIDC Provider
4. Create IAM Role
5. Add Permissions
6. Verify Role
7. Update Workflow
8. Test Deployment

Then push to GitHub:
```bash
git push origin main
```

GitHub Actions deploys automatically! 🚀

### Test Deployed API

```bash
# Replace with your actual API endpoint
API_URL="https://xxxxx.execute-api.us-east-1.amazonaws.com/prod"

# Health check
curl $API_URL/health

# Add customer
curl -X POST $API_URL/customers \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com"}'

# List customers
curl $API_URL/customers
```

## Project Structure

```
.
├── main.py                          # FastAPI app
├── lambda_handler.py                # Lambda handler  
├── requirements.txt                 # Dependencies
├── serverless.yml                   # Serverless config
├── SETUP_GITHUB_OIDC.md             # GitHub OIDC setup (8 steps)
├── YOUTUBE_DEMO_CHECKLIST.md        # Demo script
└── .github/workflows/
    └── deploy.yml                   # GitHub Actions workflow
```

## Important Notes

- **Data Storage**: Currently uses in-memory storage. Data will be lost when Lambda function is invoked again. For production, integrate with DynamoDB or RDS.
- **Cold Start**: Lambda may have a cold start delay (~1-2 seconds). Use provisioned concurrency for consistent performance.
- **ARM64 Architecture**: Uses ARM64 (Graviton2) for better performance/cost ratio.

## Next Steps for Production

1. **Database Integration**:
   - Replace in-memory storage with DynamoDB or RDS
   - Add connection pooling for RDS

2. **Error Handling**:
   - Add comprehensive error logging
   - Implement request/response logging

3. **Authentication**:
   - Add API authentication (API keys, JWT)
   - Implement authorization checks

4. **Monitoring**:
   - Enable CloudWatch logging and metrics
   - Set up alarms for errors

5. **Testing**:
   - Add unit tests
   - Add integration tests

## Cleanup

To remove the deployed application:
```bash
serverless remove
```

This deletes the Lambda function and API Gateway. The IAM role and OIDC provider remain (reusable for future deployments).

## License

MIT
