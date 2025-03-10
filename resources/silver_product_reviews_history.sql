create table silver_product_reviews_clean_history (
	product_brand text,
	customer_review_rating int,
	customer_review_title text,
	customer_review_description text,
	child_asin varchar(255),
    created_at_ts timestamp,
    updated_at_ts timestamp,
    ingested_at_ts timestamp,
    history_operation varchar(5),
    history_ts timestamp
)