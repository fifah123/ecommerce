# Product Recommendation System

This project aims to build a product recommendation system using TF-IDF and cosine similarity. The goal is to recommend similar products based on product descriptions.

## Project Structure

- `recommend_products(input_product, top_n=3)`: Function to recommend the top N similar products based on the input product description.
- `recommendation_results`: A list that stores the input product and its top 3 recommendations.
- `recommendation_results_df`: A DataFrame that stores the final results.

## How It Works

1. **TF-IDF Calculation**: 
   - The `train_df` DataFrame contains product descriptions.
   - TF-IDF (Term Frequency-Inverse Document Frequency) is calculated for these descriptions to create a feature matrix.

2. **Cosine Similarity**:
   - Cosine similarity is calculated between the input product and all other products in the training set.
   - The function `recommend_products` uses this similarity score to find the most similar products.

3. **Recommendation Generation**:
   - For each product in the training set, the top 3 similar products are recommended and stored in `recommendation_results_df`.

## Usage

1. **Run the Recommendation System**:
   - Simply call the `recommend_products` function with the desired product description.

2. **View Results**:
   - Results are stored in `recommendation_results_df`, where each product has its top 3 recommended products listed.

## Examples

```python
recommendations = recommend_products("NURSERY A,B,C PAINTED LETTERS")
print(recommendations)
