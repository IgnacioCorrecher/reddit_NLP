# reddit_NLP

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Features](#features)
4. [Installation](#installation)
    - [Clone the Repository](#clone-the-repository)
    - [Set Up Reddit API Credentials](#set-up-reddit-api-credentials)
5. [Usage](#usage)
    - [Run the Data Collection Script](#run-the-data-collection-script)
    - [Perform Sentiment Analysis](#perform-sentiment-analysis)
    - [Visualize the Results](#visualize-the-results)
6. [Results](#results)
7. [License](#license)

## Overview

`reddit_NLP` is a data science project focused on sentiment analysis of Reddit comments. By leveraging Reddit's API, this project collects a dataset of 1 million comments from various subreddits and performs sentiment analysis to understand the overall mood and opinions expressed by users.

## Project Structure

```
reddit_NLP/
├── data/                    # Folder for storing collected data
├── notebooks/               # Jupyter notebooks for exploratory analysis
├── src/                     # Source code for data collection, analysis, and visualization
├── README.md                # Project documentation
```

## Features

-   **Data Collection**: Utilizes Reddit's API to scrape 1 million comments from a diverse range of subreddits.
-   **Sentiment Analysis**: Implements various sentiment analysis techniques to classify comments as positive, negative, or neutral.
-   **Data Visualization**: Provides visual insights into the sentiment distribution across different subreddits and time periods.
-   **Customizable Parameters**: Allows users to adjust the number of comments or subreddits for data collection.

## Installation

To run this project, you'll need to have Python installed. Follow the steps below to get started:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your_username/reddit_NLP.git
    cd reddit_NLP
    ```
2. **Set up Reddit API credentials**:

## Usage

After setting up the environment and installing the necessary dependencies, you can start the data collection and sentiment analysis process.

1. **Run the data collection script**:

    ```bash
    python fetch_comments.py
    ```

    This script will use the Reddit API to scrape 1M comments based on the parameters set in the script.

2. **Perform sentiment analysis**:

    ```bash
    python sentiment_analysis.py
    ```

    This script will process the collected comments and classify them as positive, negative, or neutral.

3. **Visualize the results**:

    ```bash
    python visualize_results.py
    ```

    This script will generate various plots to help you understand the sentiment trends within the data.

## Results

The project provides insights into the sentiment of Reddit users across various topics and subreddits. The results can help in understanding public opinion, detecting trends, and identifying patterns in online discourse.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
