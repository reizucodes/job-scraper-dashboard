from app.core.config import Settings


def test_cors_allowed_origins_default() -> None:
    settings = Settings()
    assert settings.parsed_cors_allowed_origins() == [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


def test_cors_allowed_origins_parsed_from_csv() -> None:
    settings = Settings(cors_allowed_origins="http://localhost:5173, https://my-app.vercel.app")
    assert settings.parsed_cors_allowed_origins() == [
        "http://localhost:5173",
        "https://my-app.vercel.app",
    ]
