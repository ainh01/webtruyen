# Use a lightweight Node.js 18 image as the base
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and yarn.lock first to leverage Docker cache
# (This prevents re-installing dependencies if only source code changes)
COPY package.json yarn.lock ./

# Install dependencies
RUN yarn install

# Copy the rest of the application code
COPY . .

# Expose port 3000 (Adjust this if your app runs on a different port, e.g., 5173 for Vite)
EXPOSE 3000

# Start the application
CMD ["yarn", "dev"]
