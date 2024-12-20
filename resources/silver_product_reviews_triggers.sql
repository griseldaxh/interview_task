CREATE OR REPLACE FUNCTION insert_into_silver_product_reviews_clean_history_table()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert the new record into history_table
    INSERT INTO silver_product_reviews_clean_history (product_brand, customer_review_rating, customer_review_title, customer_review_description, child_asin, created_at_ts, updated_at_ts, ingested_at_ts, history_operation, history_ts)
    VALUES (NEW.product_brand, NEW.customer_review_rating, NEW.customer_review_title, NEW.customer_review_description, NEW.child_asin, NEW.created_at_ts, NEW.updated_at_ts, NEW.ingested_at_ts, 'I', CURRENT_TIMESTAMP);

    -- Return the new row for the insert operation to proceed (important for triggers that run before insert)
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger for insert
CREATE TRIGGER trg_insert_into_silver_products_reviews_clean
AFTER INSERT ON silver_product_reviews_clean
FOR EACH ROW
EXECUTE FUNCTION insert_into_silver_product_reviews_clean_history_table();



CREATE OR REPLACE FUNCTION update_into_silver_product_reviews_clean_history_table()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert the new record into history_table
    INSERT INTO silver_product_reviews_clean_history (product_brand, customer_review_rating, customer_review_title, customer_review_description, child_asin, created_at_ts, updated_at_ts, ingested_at_ts, history_operation, history_ts)
    VALUES (NEW.product_brand, NEW.customer_review_rating, NEW.customer_review_title, NEW.customer_review_description, NEW.child_asin, NEW.created_at_ts, NEW.updated_at_ts, NEW.ingested_at_ts, 'U', CURRENT_TIMESTAMP);

    -- Return the new row for the insert operation to proceed (important for triggers that run before insert)
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Create the trigger for insert
CREATE TRIGGER trg_update_into_silver_products_reviews_clean
AFTER UPDATE ON silver_product_reviews_clean
FOR EACH ROW
EXECUTE FUNCTION update_into_silver_product_reviews_clean_history_table();
