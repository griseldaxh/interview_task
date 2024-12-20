create table gold_product_insights_cache (
	child_asin varchar(255),
    no_of_reviews int,
    average_rating numeric,
    max_rating int,
    min_rating int,
    created_at_ts timestamp,
    updated_at_ts timestamp
)