from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_text(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    print(f"\nText: '{text}'")
    print(f"Positive: {scores['pos']:.3f}")
    print(f"Negative: {scores['neg']:.3f}")
    print(f"Neutral: {scores['neu']:.3f}")
    print(f"Compound: {scores['compound']:.3f}")
    if scores['compound'] > 0.05:
        print("Overall: Positive")
    elif scores['compound'] < -0.05:
        print("Overall: Negative")
    else:
        print("Overall: Neutral")
    print("-" * 50)

# Example 1: Strongly Positive
text1 = "I absolutely love this product! It's amazing and works perfectly. Best purchase ever!!!"
analyze_text(text1)

# Example 2: Mildly Positive
text2 = "This is a good product. It works well and I'm satisfied with it."
analyze_text(text2)

# Example 3: Strongly Negative
text3 = "I HATE this product! It's TERRIBLE and completely useless. Worst purchase ever!!!"
analyze_text(text3)

# Example 4: Mildly Negative
text4 = "This product is not very good. It could be better."
analyze_text(text4)

# Example 5: Neutral
text5 = "This is a product. It exists and functions as described."
analyze_text(text5)

# Example 6: Mixed Sentiment
text6 = "The product is great but the customer service is awful."
analyze_text(text6)

# Example 7: With Capitalization and Punctuation
text7 = "LOVE this product!!! It's AMAZING!!!"
analyze_text(text7)

# Example 8: With Degree Modifiers
text8 = "This is very very good, but not extremely perfect."
analyze_text(text8)

# Example 9: With Negation
text9 = "This is not bad at all, in fact it's quite good."
analyze_text(text9)

# Example 10: Complex Sentence
text10 = "While the product itself is excellent, the packaging was damaged and the delivery was late, but overall I'm satisfied."
analyze_text(text10) 