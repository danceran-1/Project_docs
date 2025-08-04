SELECT customer_id,SUM(amount) AS TOTAL_SUM 
FROM orders
GROUP BY customer_id



SELECT 
    customer_id,
    SUM(amount) AS total_amount
FROM orders
GROUP BY customer_id
LIMIT 1;


SELECT COUNT(*) AS order_count_2023
FROM orders
WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31';

SELECT customer_id,AVG(amount)
FROM orders
GROUP BY customer_id