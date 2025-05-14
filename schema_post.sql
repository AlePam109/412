-- schema_post.sql: Post-population schema constraints

-- adding Primary Keys:
ALTER TABLE business ADD PRIMARY KEY (business_id);
ALTER TABLE review ADD PRIMARY KEY (review_id);
ALTER TABLE yelp_user ADD PRIMARY KEY (user_id);
ALTER TABLE business_account
    ALTER COLUMN account_id ADD GENERATED ALWAYS AS IDENTITY;
ALTER TABLE business_account ADD PRIMARY KEY (account_id);

-- adding Foreign Keys
ALTER TABLE business
    ADD CONSTRAINT fk_business_account
    FOREIGN KEY (business_account_id) REFERENCES business_account(account_id);

ALTER TABLE review
    ADD CONSTRAINT fk_review_user FOREIGN KEY (user_id) REFERENCES yelp_user(user_id) NOT VALID, --some existing reviews lack 		
																								 --	referential integrity
    ADD CONSTRAINT fk_review_business FOREIGN KEY (business_id) REFERENCES business(business_id);

ALTER TABLE tip
    ADD CONSTRAINT fk_tip_user FOREIGN KEY (user_id) REFERENCES yelp_user(user_id),
    ADD CONSTRAINT fk_tip_business FOREIGN KEY (business_id) REFERENCES business(business_id);


-- Conversions:
ALTER TABLE business
    ALTER COLUMN is_open TYPE BOOLEAN
    USING is_open::BOOLEAN;

