import streamlit as st
import re
import json
import boto3
import uuid


# AWS Lambda function configuration
LAMBDA_FUNCTION_NAME = 'hashtag'  
AWS_REGION = 'us-east-1' 

# Initialize Boto3 client for Lambda
lambda_client = boto3.client('lambda', region_name=AWS_REGION)

# Prepare the payload to send to Lambda
def invoke_lambda(post_content):
    payload = {
        'post_content': post_content
    }

    # Invoke the Lambda function
    response = lambda_client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )

    # Parse the response from Lambda
    response_payload = json.loads(response['Payload'].read())
    return response_payload


#Streamlit app layout
st.title('Social Media Hashtag Trend Analyzer')

#Post composition
post_content = st.text_area('Compose your post (include hashtags with #)', '')

#Check if the post contains at least one hashtag
def contains_hashtag(text):
    return bool(re.search(r'#\w+', text))

# Send to Lambda if there is at least one hashtag after posting content
if st.button('Post'):
    if post_content:
        if contains_hashtag(post_content):       
            response = invoke_lambda(post_content)
            st.success('Post submitted successfully with hashtags!')
        else:
            st.error('Your post must contain at least one hashtag.')
    else:
        st.error('Post content cannot be empty.')


# Initialize Boto3 client for DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('post_content')  

def lambda_handler(event, context):
    post_content = event['post_content']
    hashtags = re.findall(r'#\w+', post_content)
    
    # Create a unique ID for the post
    post_id = str(uuid.uuid4())
    
    # Store the post content and hashtags in DynamoDB
    table.put_item(
        Item={
            'post_id': post_id,
            'post_content': post_content,
            'hashtags': hashtags
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Post stored successfully!')
    }
    
# Funtion to return the top 10 trending hashtags
def get_trending_hashtags():
    # Scan the DynamoDB table to get all posts
    response = table.scan()
    items = response.get('Items', [])

    hashtag_count = {}

    # Count the occurrences of each hashtag
    for item in items:
        hashtags = item.get('hashtags', [])
        for hashtag in hashtags:
            if hashtag in hashtag_count:
                hashtag_count[hashtag] += 1
            else:
                hashtag_count[hashtag] = 1

    # Sort the hashtags by count in descending order
    sorted_hashtags = sorted(hashtag_count.items(), key=lambda x: x[1], reverse=True)

    return sorted_hashtags[:10]  


# Show trending hashtags
if st.button('Show Trending Hashtags'):
    trending_hashtags = get_trending_hashtags()
    st.write('Trending Hashtags:')
    for hashtag, count in trending_hashtags:
        st.write(f'{hashtag}: {count} posts')
