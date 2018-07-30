SELECT count, name AS color_name, colorId
FROM
    (select
        count(*) as count,
        CAST((parameters->>'colorId') AS bigint) as colorId
    from puretask_car
    group by colorId) AS cars_count
LEFT JOIN puretask_color AS color ON (cars_count.colorId = color.id)
ORDER BY count DESC;
