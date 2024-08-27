import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

class SentimentVisualizer:
    def __init__(self, sentiment_file_path, comments_file_path):
        self.df_sentiment = self.load_data(sentiment_file_path)
        self.df_comments = self.load_data(comments_file_path)
        self.df = self.join_dataframes()

    @staticmethod
    def load_data(file_path):
        """Load data from CSV"""
        try:
            abs_file_path = os.path.abspath(file_path)
            print(f"Attempting to load file from: {abs_file_path}")
            
            df = pd.read_csv(abs_file_path)
            print(f"Successfully loaded data from {abs_file_path}")
            return df
        except FileNotFoundError:
            print(f"Error: The file {abs_file_path} was not found.")
            sys.exit(1)
        except pd.errors.EmptyDataError:
            print(f"Error: The file {abs_file_path} is empty.")
            sys.exit(1)
        except pd.errors.ParserError:
            print(f"Error: Unable to parse the file {abs_file_path}. Make sure it's a valid CSV.")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred while reading the file: {e}")
            sys.exit(1)

    def join_dataframes(self):
        """Join sentiment data with comment data"""
        print("Columns in sentiment dataframe:")
        print(self.df_sentiment.columns.tolist())
        print("\nColumns in comments dataframe:")
        print(self.df_comments.columns.tolist())

        print("\nJoining sentiment data with comment data...")
        joined_df = pd.merge(self.df_sentiment, self.df_comments, 
                             left_on='Comment_ID', right_on='Id', 
                             how='left', suffixes=('_sentiment', '_comment'))

        # Ensure we have a 'Subreddit' column
        if 'Subreddit_sentiment' in joined_df.columns:
            joined_df['Subreddit'] = joined_df['Subreddit_sentiment']
        elif 'Subreddit_comment' in joined_df.columns:
            joined_df['Subreddit'] = joined_df['Subreddit_comment']

        return joined_df

    def ensure_dir(self, file_path):
        """Make sure the directory exists for the given file path and return the full path"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, file_path)
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        return full_path

    def plot_overall_sentiment(self):
        """Plot the overall sentiment distribution"""
        plt.figure(figsize=(10, 6))
        sns.countplot(x='Sentiment', data=self.df)
        plt.title('Overall Sentiment Distribution')
        
        output_path = self.ensure_dir('../imgs/overall_sentiment.png')
        
        plt.savefig(output_path)
        print(f"Saved overall sentiment plot to: {output_path}")
        plt.close()

    def plot_subreddit_sentiment(self, top_n=10):
        """Plot sentiment distribution for top N subreddits"""
        top_subreddits = self.df['Subreddit'].value_counts().nlargest(top_n).index
        subreddit_sentiments = self.df[self.df['Subreddit'].isin(top_subreddits)]

        plt.figure(figsize=(12, 8))
        sns.countplot(x='Subreddit', hue='Sentiment', data=subreddit_sentiments)
        plt.title(f'Sentiment Distribution in Top {top_n} Subreddits')
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Sentiment')
        plt.tight_layout()
        output_path = self.ensure_dir('../imgs/subreddit_sentiment.png')
        plt.savefig(output_path)
        print(f"Saved subreddit sentiment plot to: {output_path}")
        plt.close()

    def sentiment_percentage(self):
        """Calculate and print sentiment percentages"""
        total = len(self.df)
        sentiment_counts = self.df['Sentiment'].value_counts()
        percentages = (sentiment_counts / total * 100).round(2)
        print("Sentiment Percentages:")
        print(percentages)
        return percentages

    def display_sample_comments(self, sentiment, n=5):
        """Display sample comments for a given sentiment"""
        sample = self.df[self.df['Sentiment'] == sentiment].sample(n=n)
        print(f"\n{sentiment.capitalize()} Sentiment Examples:")
        for _, row in sample.iterrows():
            print(f"Subreddit: r/{row['Subreddit']}")
            print(f"Comment: {row['Comment'][:200]}...")  # Display first 200 characters
            print("-" * 80)

    def visualize_all(self):
        """Run all visualization methods"""
        self.plot_overall_sentiment()
        self.plot_subreddit_sentiment()
        percentages = self.sentiment_percentage()
        self.display_sample_comments("POSITIVE")
        self.display_sample_comments("NEGATIVE")
        print("\nVisualization complete. Check the 'data' folder for generated plots.")
        return percentages

def main():
    if len(sys.argv) > 2:
        sentiment_file_path = sys.argv[1]
        comments_file_path = sys.argv[2]
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sentiment_file_path = os.path.join(script_dir, '..', 'data', 'comments_sentiment_summary.csv')
        comments_file_path = os.path.join(script_dir, '..', 'data', 'comments.csv')
    
    visualizer = SentimentVisualizer(sentiment_file_path, comments_file_path)
    visualizer.visualize_all()

if __name__ == "__main__":
    main()