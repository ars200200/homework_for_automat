CREATE TYPE eorderstatus AS ENUM ('WAITING', 'ACCEPTED', 'REJECTED', 'CANCELED', 'FINISHED');


CREATE TABLE user_base_info (
        user_id SERIAL NOT NULL, 
        login VARCHAR, 
        encrypted_pass VARCHAR, 
        email VARCHAR, 
        name VARCHAR, 
        surname VARCHAR, 
        points INTEGER, 
        phone_number VARCHAR, 
        review_count INTEGER, 
        review_sum INTEGER, 
        PRIMARY KEY (user_id), 
        UNIQUE (login)
);

 
CREATE TABLE cars (
        car_id SERIAL NOT NULL, 
        capacity FLOAT, 
        status INTEGER, 
        model VARCHAR, 
        year_of_release TIMESTAMP WITHOUT TIME ZONE, 
        PRIMARY KEY (car_id)
);


CREATE TABLE tariffs (
        type VARCHAR NOT NULL, 
        availability INTEGER, 
        PRIMARY KEY (type)
);


CREATE TABLE payment (
        payment_id UUID NOT NULL, 
        price FLOAT, 
        payment_method VARCHAR, 
        payment_status VARCHAR, 
        number_of_points_awarded INTEGER, 
        promo VARCHAR, 
        PRIMARY KEY (payment_id)
);


CREATE TABLE driver_info (
        user_id INTEGER NOT NULL, 
        driver_id VARCHAR, 
        license_number VARCHAR, 
        review_count INTEGER, 
        review_sum INTEGER, 
        PRIMARY KEY (user_id), 
        FOREIGN KEY(user_id) REFERENCES user_base_info (user_id)
);


CREATE TABLE user_bank_cards (
        user_id INTEGER NOT NULL, 
        bank_card_number VARCHAR NOT NULL, 
        encrypted_bank_data VARCHAR, 
        PRIMARY KEY (user_id, bank_card_number), 
        FOREIGN KEY(user_id) REFERENCES user_base_info (user_id)
);


CREATE TABLE user_reviews_info (
        review_id UUID NOT NULL, 
        user_id INTEGER NOT NULL, 
        reviewer_user_id INTEGER NOT NULL, 
        score INTEGER, 
        created_at TIMESTAMP WITHOUT TIME ZONE, 
        comment VARCHAR, 
        is_client_review BOOLEAN, 
        PRIMARY KEY (review_id, user_id, reviewer_user_id), 
        FOREIGN KEY(user_id) REFERENCES user_base_info (user_id), 
        FOREIGN KEY(reviewer_user_id) REFERENCES user_base_info (user_id)
);


CREATE TABLE features (
        feature VARCHAR NOT NULL, 
        description VARCHAR, 
        PRIMARY KEY (feature)
);


CREATE TABLE car_types (
        car_id INTEGER NOT NULL, 
        type VARCHAR NOT NULL, 
        PRIMARY KEY (car_id, type), 
        FOREIGN KEY(car_id) REFERENCES cars (car_id), 
        FOREIGN KEY(type) REFERENCES tariffs (type)
);


CREATE TABLE user_cars (
        user_id INTEGER NOT NULL, 
        car_id INTEGER NOT NULL, 
        date_from TIMESTAMP WITHOUT TIME ZONE, 
        date_to TIMESTAMP WITHOUT TIME ZONE, 
        PRIMARY KEY (user_id, car_id), 
        FOREIGN KEY(user_id) REFERENCES driver_info (user_id), 
        FOREIGN KEY(car_id) REFERENCES cars (car_id)
);


CREATE TABLE car_features (
        car_id INTEGER NOT NULL, 
        feature VARCHAR NOT NULL, 
        PRIMARY KEY (car_id, feature), 
        FOREIGN KEY(car_id) REFERENCES cars (car_id), 
        FOREIGN KEY(feature) REFERENCES features (feature)
);


CREATE TABLE order_info (
        order_id UUID NOT NULL, 
        client_user_id INTEGER, 
        driver_user_id INTEGER, 
        created_at TIMESTAMP WITHOUT TIME ZONE, 
        order_status eorderstatus, 
        map_coordinates JSON, 
        payment_id UUID, 
        tariff_type VARCHAR, 
        PRIMARY KEY (order_id), 
        FOREIGN KEY(client_user_id) REFERENCES user_base_info (user_id), 
        FOREIGN KEY(driver_user_id) REFERENCES driver_info (user_id), 
        FOREIGN KEY(payment_id) REFERENCES payment (payment_id), 
        FOREIGN KEY(tariff_type) REFERENCES tariffs (type)
);
