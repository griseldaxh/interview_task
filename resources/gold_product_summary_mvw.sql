CREATE MATERIALIZED VIEW gold_product_summary AS 
SELECT child_asin, count(*) as no_of_reviews, avg(customer_review_rating) as average_rating,
max(customer_review_rating) as max_rating, min(customer_review_rating) as min_rating
FROM postgres.public.silver_product_reviews_clean
group by child_asin;