from datetime import date, datetime
from importlib.resources import contents
from typing import Optional, List
from unittest import result
from uuid import UUID
import json

# Pydantic
from pydantic import BaseModel, EmailStr, Field

# FastAPI
from fastapi import Body, FastAPI, status

app = FastAPI()

# Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=20
    )
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

##Path Operations

@app.get(path="/")
def home():
    return {"Twitter API": "Working"}

## Users

@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register Users",
    tags=["Users"]
)
def signup(user: UserRegister = Body(...)):
    """
        # Signup

        This path operation register a user in the app

        Parameters:
            - Request body parameter
                - user: UserRegister

        Returns a json with the basic user information:
            - user_id: UUID
            - email: Emailstr
            - first_name: str
            - last_name: str
            - birth_date: str
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user

@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a Users",
    tags=["Users"]
)
def login():
    pass

@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Get All Users",
    tags=["Users"]
)
def get_users():
    """
        This path operation shows all users in the app

        Parameters:
            -

        Returns a json list with all users in the app, with the following keys:
            - user_id: UUID
            - email: Emailstr
            - first_name: str
            - last_name: str
            - birth_date: datetime
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Get an User By id",
    tags=["Users"]
)
def find_user():
    pass

@app.put(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update an User",
    tags=["Users"]
)
def update_user():
    pass

@app.delete(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete an User",
    tags=["Users"]
)
def delete_user():
    pass
## Tweets

@app.post(
    path="/tweets",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Create Tweet",
    tags=["Tweets"]
)
def create_tweet(tweet: Tweet = Body(...)):
    """
        Post a Tweet
        This path operation post a tweet in the app
        Parameters:
            - Request body parameter
                - tweet: Tweet

        Returns a json with the basic tweet information:
            tweet_id: UUID
            content: str
            created_at: datetime
            updated_at: Optional[datetime]
            by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])

        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet

@app.get(
    path="/tweets",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Get all Tweets",
    tags=["Tweets"]
)
def get_tweets():
    pass

@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Find Tweet",
    tags=["Tweets"]
)
def find_tweet():
    pass

@app.put(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a Tweet",
    tags=["Tweets"]
)
def update_tweet():
    pass

@app.delete(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a Tweet",
    tags=["Tweets"]
)
def delete_tweet():
    pass


"""
    Steroids Project
    https://github.com/JoseNoriegaa/platzi-twitter-api-fastapi
"""
