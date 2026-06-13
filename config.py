# VULNERABILITY: Hardcoded secret - Gitleaks will detect this

DATABASE_URL = "postgresql://admin:password123@localhost:5432/mydb"
SECRET_TOKEN = "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef01"
# Another leaked credential for testing
