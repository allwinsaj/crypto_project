# Crypto Coins Project

This project is designed to fetch, store, and serve cryptocurrency data using the CoinGecko API, while providing user authentication and secure access to its features. The project utilizes Flask, MongoDB, and Docker for deployment.

---

## Prerequisites

- Docker (compatible with Linux or Windows environments)
- Basic understanding of Docker commands

---

## How to Run This Project

### Step 1: Clone the Repository
Pull the code from the GitHub repository:
```bash
# Example:
git clone git@github.com:allwinsaj/crypto_project.git
cd crypto_project
```

### Step 2: Build and Run Docker Containers
1. Build the Docker image for the Flask application:
   ```bash
   docker build -t crypto_project .
   ```

2. Run the Flask application container:
   ```bash
   docker run -it --name flask_app --network app-network -p 5001:5000 crypto_project
   ```

3. Run the MongoDB container:
   ```bash
   docker run -d --name mongodb --network app-network -p 27017:27017 mongo
   ```

4. Verify that both containers are on the same network:
   ```bash
   docker network inspect app-network
   ```

### Step 3: Access the Application
- Flask API will be running on: `http://localhost:5001`
- Swagger documentation can be accessed at: `http://localhost:5001/apidocs`

---

## Project Description

### Coin APIs
The application fetches cryptocurrency data from the CoinGecko API and stores it in a MongoDB database.

#### Database Details:
- **Database Name**: `crypto_db`
- **Collection Name**: `coin_details`
- **UserCollection Name**: `user`

#### Workflow:
1. **Fetch Data:**
   - Retrieve all unique coin IDs using the CoinGecko `coins list` API.
   - For each coin ID, fetch detailed data using the CoinGecko `coin data by ID` API.
   - Store the retrieved data in the MongoDB database.

2. **Rate Limiting:**
   - CoinGecko imposes rate limits on API usage. If a limit error occurs, the application waits for 30 seconds before retrying.

3. **Data Refresh:**
   - Trigger the data collection process by calling the `v1/data_refresh` endpoint.

#### Available Endpoints:
- **`GET /v1/coins`**: Retrieve a paginated list of all coins.
- **`GET /v1/coins/categories`**: Fetch a distinct list of coin categories.
- **`POST /v1/specific_coins`**: Retrieve filtered data based on `coin_ids` and `categories`, including price data in Canadian Dollars.

### User APIs
The application provides user authentication via JWT (JSON Web Token).

#### Available Endpoints:
1. **Signup API**: `POST /v1/signup`
   - Create a new user by providing `username`, `email`, and `password`.

2. **Login API**: `POST /v1/auth/login`
   - Authenticate an existing user by providing `username` and `password`.
   - On successful authentication, an access token is issued to access Coin APIs.
All the user details will be saved in `user` collection
---

## Example Workflow
1. **User Signup:**
   - Send a `POST` request to `/v1/auth/signup` with user details.

2. **User Login:**
   - Authenticate using `/v1/auth/login` to receive a JWT token.

3. **Data Refresh:**
   - Trigger the data collection by calling `v1/data_refresh`.

4. **Query Coins:**
   - Access the paginated list of coins, distinct categories, or filtered data using the respective endpoints, passing the JWT token in the `Authorization` header.

---

## Notes
- Ensure that Docker is properly installed and configured on your machine.
- All API calls to CoinGecko are subject to their rate limits.
- MongoDB stores all cryptocurrency data for efficient querying and filtering.

---

## Swagger Documentation
Swagger documentation is available at: `http://localhost:5001/apidocs`

Use this documentation for testing the APIs and understanding their request/response structure.

---

## Troubleshooting
1. **Containers Not Running on Same Network:**
   - Ensure both containers are connected to the `app-network`. Use the following command if needed:
     ```bash
     docker network connect app-network flask_app
     docker network connect app-network mongodb
     ```

2. **MongoDB Connection Issues:**
   - Verify that MongoDB is running on the correct port (`27017`) and accessible from the Flask container.

3. **Swagger Not Accessible:**
   - Ensure Flask is running and accessible on `localhost:5001`.

---

Enjoy exploring cryptocurrency data with this project!