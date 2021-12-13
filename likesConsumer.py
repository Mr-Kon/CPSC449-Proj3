import requests
import json
import redis
import greenstalk

# Set up for Redis taken from likes.py
#
red = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True) # posts as key
red1 = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True) # popular posts 
red2 = redis.Redis(host='localhost', port=6379, db=2, decode_responses=True) # users as key

name1 = "Posts"   
name2 = "PopularPosts" 
name3 = "UserLiked" 

#Producer is expecting 2 strings separated by comma
with greenstalk.Client(('127.0.0.1', 11300)) as client:
    while True:
        job = client.reserve()
        userAndtweet = job.body.split(",")  # [0] = username, and [1] = tweet id
        print(job.body)

        # checking if tweet exists
        r = requests.get(f"http://localhost/posts/{userAndtweet[1]}") 
        temp = json.loads(r.text)
        if not temp:   #temp2 returns nothing if empty
            ############## SEND EMAIL FOR FAILURE HERE ################
            print ("DOES NOT EXIST")
        else:
            print("SUCCESS!")
            if red.sadd(userAndtweet[1], userAndtweet[0]): 
                red1.zincrby(name2, 1, userAndtweet[1])
            red2.sadd(userAndtweet[0], userAndtweet[1])
        
        client.delete(job)






# Setting data for redis

# If statment tries to insert into set
# If successfull (equals to 1), new user liked the post!
# Thus increase the score for value in the sorted set
# If statment not successful -> the user already liked the tweet
# Thus don't increment the score for value in sorted set
