-- Llists all bands with Glam rock as their main style, ranked by their longevity
SELECT band_name,
	CASE
		WHEN split IS NOT NULL THEN split - formed
		ELSE 2022 - formed
	END AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
ORDER BY lifespan DESC;
