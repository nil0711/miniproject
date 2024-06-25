
# Chat Analyzer

## Overview

The Chat Analyzer is a web application designed to analyze WhatsApp conversations. It provides data visualization, sentiment analysis, and a chatbot feature to interact with users. The application leverages various Python libraries and tools, including Streamlit for the web interface, Matplotlib and Plotly for data visualization, and Google's Generative AI for the chatbot.

## Features

- **Data Visualization**: Visualize chat data with graphs and charts.
- **Sentiment Analysis**: Analyze the sentiment of chat messages over time.
- **Chatbot Integration**: Interact with an AI chatbot for insights and queries about the analysis.
- **Activity Maps**: View user activity heatmaps and most active days/months.
- **Word Cloud and Common Words**: Generate word clouds and lists of the most common words and emojis.
- **Topic Modeling**: Identify and display keywords for different topics discussed in the chat.

## File Structure

- `app.py`: Main Python script running the web application.
- `helper.py`: Helper functions for statistical analysis and visualization.
- `requirements.txt`: List of dependencies required to run the application.


## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages listed in `requirements.txt`
- Google API key for the chatbot functionality

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/nil0711/miniproject.git
   ```
   
2. Navigate to the project directory:
   ```sh
   cd miniproject
   ```
   
3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   
4. Set up your Google API key in the Streamlit secrets:
   ```sh
   streamlit secrets set GOOGLE_API "your-google-api-key"
   ```

### Usage

1. Run the application:
   ```sh
   streamlit run app.py
   ```
   
2. Open a web browser and go to `http://127.0.0.1:8501` to access the application.

### Features and Interaction

1. **Upload a Chat File**: Upload a WhatsApp conversation text file to start the analysis.
2. **Select User**: Choose a specific user or analyze overall chat activity.
3. **View Visualizations**: Explore various visualizations including message statistics, activity maps, and word clouds.
4. **Sentiment Analysis**: Analyze the sentiment and emotions over time.
5. **Chatbot**: Ask questions and interact with the AI chatbot for insights about the analysis.

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests for any enhancements or bug fixes.
```
