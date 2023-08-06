DUPLICATES = (
    ("path", "hash", "size_bytes", "type"),
    """\
SELECT path, hash, size_bytes, 'dir' as type
FROM dir
WHERE hash IN (
    SELECT hash
    FROM dir
    GROUP BY hash
    HAVING COUNT(DISTINCT path) > 1
)
UNION ALL
SELECT path, hash, size_bytes, 'file' as type
FROM file
WHERE hash IN (
    SELECT hash
    FROM file
    GROUP BY hash
    HAVING COUNT(DISTINCT path) > 1
)
ORDER BY size_bytes DESC, hash DESC;
""",
)

BIGGEST_FILES = (
    ("path", "hash", "size_bytes"),
    """\
SELECT path, hash, size_bytes
FROM file
ORDER BY size_bytes DESC
LIMIT 100;
""",
)

BIGGEST_EXTENSIONS = (
    ("extension", "total_size"),
    """\
SELECT extension, SUM(size_bytes) AS total_size
FROM file
GROUP BY extension
ORDER BY total_size DESC
LIMIT 100;
""",
)

QUERIES = {
    "100-biggest-files": BIGGEST_FILES,
    "100-biggest-extensions": BIGGEST_EXTENSIONS,
    "duplicates": DUPLICATES,
}
