
CREATE VIEW UberByCities AS
SELECT DISTINCT count (id), location__city
FROM restaurants
GROUP BY location__city
ORDER BY count (id) DESC


CREATE VIEW top_pizzas AS
SELECT restaurants.title, restaurants.rating__rating_value, restaurants.rating__review_count FROM restaurant_to_categories
INNER JOIN restaurants ON restaurant_to_categories.restaurant_id=restaurants.id
WHERE restaurant_to_categories.category='Pizzas'
ORDER BY restaurants.rating__rating_value DESC
LIMIT 10

CREATE VIEW WhereCanIFindSomeSnow AS
SELECT DISTINCT restaurants.location__latitude, restaurants.location__longitude FROM menu_items
INNER JOIN restaurants ON menu_items.restaurant_id=restaurants.id
WHERE description LIKE '%cola%' OR description LIKE '%coca%'

CREATE VIEW avgkapsalonprice AS
SELECT AVG(menu_items.price) FROM menu_items
INNER JOIN restaurants ON menu_items.restaurant_id=restaurants.id
WHERE description LIKE '%kapsalon%'

CREATE VIEW distribution_of_restaurants AS
SELECT DISTINCT count (locations_to_restaurants.restaurant_id), locations_to_restaurants.location_id, locations.name
FROM locations
INNER JOIN locations_to_restaurants ON locations.id=locations_to_restaurants.location_id
GROUP BY locations_to_restaurants.location_id
ORDER BY count (locations_to_restaurants.restaurant_id) DESC

CREATE VIEW kapsalonprice AS
SELECT menu_items.price, restaurants.location__latitude, restaurants.location__longitude FROM menu_items
INNER JOIN restaurants ON menu_items.restaurant_id=restaurants.id
WHERE description LIKE '%kapsalon%' 
ORDER BY menu_items.price

CREATE VIEW price_repartion AS
SELECT price FROM menu_items