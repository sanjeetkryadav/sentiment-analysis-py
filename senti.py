#from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

def get_sentiment_explanation(scores):
    
    compound = scores['compound']
    explanation = (
        f"Sentiment Scores Explanation:\n\n"
        f"1. Compound Score ({compound:.3f}):\n"
        f"   - This is the normalized score between -1 (most negative) and +1 (most positive)\n"
        f"   - Scores > 0.05 indicate positive sentiment\n"
        f"   - Scores < -0.05 indicate negative sentiment\n"
        f"   - Scores between -0.05 and 0.05 indicate neutral sentiment\n\n"
        f"2. Positive Score ({scores['pos']:.3f}):\n"
        f"   - Proportion of text that is positive\n\n"
        f"3. Negative Score ({scores['neg']:.3f}):\n"
        f"   - Proportion of text that is negative\n\n"
        f"4. Neutral Score ({scores['neu']:.3f}):\n"
        f"   - Proportion of text that is neutral\n"
    )
    return explanation

def second():
    
    # Initialize VADER analyzer
    analyzer = SentimentIntensityAnalyzer()
    
    # Get path to input.txt in same directory as this script
    input_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
    
    try:
        # Read transcribed text
        with open(input_file, "r", encoding='utf-8') as file:
            text = file.read().strip()
            if not text:
                return "Error: No text to analyze", 0.0, ""
                
            # Get sentiment scores
            scores = analyzer.polarity_scores(text)
            compound_score = scores['compound']
            explanation = get_sentiment_explanation(scores)
            
            # Classify sentiment based on compound score
            # Using VADER's standard thresholds:
            # positive >= 0.05
            # negative <= -0.05
            # neutral between -0.05 and 0.05
            if compound_score > 0.05:
                sentiment = "Video sentiment is positive"
            elif compound_score < -0.05:
                sentiment = "Video sentiment is negative"
            else:
                sentiment = "Video sentiment is neutral"
                
            return sentiment, compound_score, explanation
            
    except FileNotFoundError:
        return "Error: Input file not found", 0.0, ""
    except Exception as e:
        return f"Error during analysis: {str(e)}", 0.0, ""
