# Social-Media-Hashtag-Trend-Analyzer-Application
This project is a Social Media Hashtag Trend Analyzer application built using Streamlit, AWS Lambda, and DynamoDB.  The application allows users to compose posts with hashtags, store them in a DynamoDB table, and analyze trending hashtags.

## Features

* Compose and submit posts with hashtags.
* Store posts and hashtags in a DynamoDB table.
* Analyze and display trending hashtags.

## Prerequisites

* Python 3.7 or higher
* AWS account with access to Lambda and DynamoDB
* Streamlit
* Boto3


# Hashtag Trend Analyzer

This Streamlit app helps you analyze trends in hashtags across social media posts. It allows you to:

## Post content with hashtags: 
create your own post and include relevant hashtags.

## Submit your post: 
Click the "Post" button to send the post content to an AWS Lambda function for processing.

## Analyze trending hashtags: 
Click the "Show Trending Hashtags" button to view the most popular hashtags based on recent posts.


# How it Works

## Compose your post: 

Include hashtags with the "#" symbol in your post text.

## Submit your post: 

**Clicking "Post" triggers the following actions:**
The post content is sent to an AWS Lambda function configured with the name hashtag.
The Lambda function extracts hashtags using regular expressions.
Extracted hashtags and the original post content are stored in a DynamoDB table named post_content.

## View trending hashtags: 

**Clicking "Show Trending Hashtags" triggers the following actions:**
The app retrieves data from the DynamoDB table.
Hashtag occurrences are counted to determine their popularity.
The top 10 trending hashtags are displayed in a list.
