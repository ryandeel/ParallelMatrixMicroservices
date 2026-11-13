import redis
import os
import sys

""" This will connect to our redis container """
def redis_connection():
    # try to connect to redis, this wont run until redis starts
    try:
        REDIS_CONTAINER = redis.Redis(host="redis", port=6379, decode_responses=True)
        REDIS_CONTAINER.ping()

        print("Connected to Redis")
        return REDIS_CONTAINER
    
    except redis.ConnectionError as error:
        print(f"Failed to connect to Redis container: {error}")
        sys.exit(1)

""" Establish variable to make reads and writes to our data store (Volume) """
def volume_connection():
    # Establish variable to make reads and writes to our data store (Volume)
    VOLUME = os.getenv("DATA_DIR", "./data")

    try:
        # This will create a new volume if it doesnt exist
        os.makedirs(VOLUME, exist_ok=True)

        print(f"Connected to Volume: {VOLUME}")
        return VOLUME
    
    except OSError as error:
        print(f"Could not access volume at {VOLUME}: {error}")
        sys.exit(1)

""" Utilize REDIS_CONTAINER and VOLUME in main to create new function"""
def main(REDIS_CONTAINER, VOLUME):
    print("congrats guys we made our connection") 
    return 

if __name__ == "__main__":
    # connections to redis and volume
    REDIS_CONTAINER = redis_connection()
    VOLUME = volume_connection()

    main(REDIS_CONTAINER, VOLUME)
