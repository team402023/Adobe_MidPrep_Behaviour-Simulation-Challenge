# Tweet Engagement Prediction and Content Generation

This repository contains the solution for a two-part challenge hosted by Adobe in INTER IIT Tech Meet 12.0. The challenge involves predicting user engagement (likes) for tweets and generating tweet content based on tweet metadata.

## Overview

This project aims to predict user engagement and generate tweet content based on provided tweet metadata. It consists of two tasks:

### Task 1: Behavior Simulation
Given tweet metadata (text, company, username, media URLs, timestamp), the task is to predict user engagement, measured by likes.

#### Dataset Preprocessing:
- **Features:** The dataset comprises tweet metadata, including date, time, brand name, username, content, media URLs, and timestamp.
- **Target:** The target variable is the number of likes a tweet receives.
- **Feature Engineering:**
  - **Embeddings for Media and Content:** Created embeddings to represent media and textual content information.
  - **Brand Name Embeddings:** Utilized domain-specific information, obtained from wiki data related to the company, to create embeddings for brand names.
  - **One-Hot Encoding for Date Information:** Encoded month and day information, recognizing their potential relationships with the target variable.

#### Model Architecture:
- **Multi-Modal Neural Network:** Developed a neural network capable of handling multiple modalities of data, considering the embeddings and one-hot encoded features.
- **Feature Fusion:** Incorporated a fusion strategy to merge the information from different modalities effectively.

#### Training:
- **Training Data Size:** The dataset comprises around 300,000 data points.
- **Model Training:** Utilized the neural network to train the model on the prepared dataset.

### Task 2: Content Simulation
Given tweet metadata (company, username, media URL, timestamp) and user engagement (likes), the task is to generate the tweet text.

#### Dataset Preprocessing:
- **Features:** The dataset comprises tweet metadata including date, time, brand name, username, media URLs, user engagement (likes), and timestamp.
- **Target:** The target variable is the caption or textual content of the tweet.
- **Preprocessing:**
  - **Incorporating User Engagement:** Used content as a feature to potentially influence text generation.
  - **Link extraction:** Extracted the media from the links

#### Model Selection and Implementation:
- **LLava Model (Large Language and Vision Assistant Explained):**
  - **Prompt-Based Approach:** Employed few-shot prompting techniques to guide the LLava model to generate tweet text.
  - **Prompt Fine-Tuning:** Incorporated brand name, username, and likes information within the prompt to fine-tune the model.

#### Training and Fine-Tuning:
- **Training Data Size:** The dataset consists of around 300,000 data points.
- **Fine-Tuning Process:** Conducted fine-tuning of the LLava model using the provided tweet metadata and user engagement information.

## License and Acknowledgments
The provided dataset is open source, and the intellectual property rights to the final solution will belong to Adobe.
