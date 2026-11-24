-- Chargement de l'historique (exécuté automatiquement au premier démarrage du conteneur)

COPY reservations (reservation_id, hotel_id, is_canceled, lead_time, arrival_date_year, arrival_date_month, arrival_date_week_number, arrival_date_day_of_month, stays_in_weekend_nights, stays_in_week_nights, adults, children, babies, meal, country, market_segment, distribution_channel, is_repeated_guest, previous_cancellations, previous_bookings_not_canceled, reserved_room_type, assigned_room_type, booking_changes, deposit_type, agent, company, days_in_waiting_list, customer_type, adr, required_car_parking_spaces, total_of_special_requests, reservation_status, reservation_status_date, arrival_date)
FROM '/docker-entrypoint-initdb.d/data/reservations.csv'
WITH (FORMAT csv, HEADER true);

CREATE INDEX idx_reservations_arrival_date ON reservations (arrival_date);
