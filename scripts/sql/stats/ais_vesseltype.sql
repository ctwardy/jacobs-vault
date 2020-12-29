SELECT vesseltype, n, 
    CASE WHEN vesseltype in ('0', '20', '21', '22', '23', '24', '30', '31', '32', '33', '34', '35', '36', '37', '40', '41', '42', '43', '44', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '69', '70', '71', '72', '73', '74', '79', '80', '81', '82', '83', '84', '89', '90', '91', '92', '93', '94', '99')
        THEN 'valid' 
        ELSE 'invalid' 
        END
FROM (
    select vesseltype, count(*) as n 
    from af_vault.ais 
    group by vesseltype 
) A
order by vesseltype;
