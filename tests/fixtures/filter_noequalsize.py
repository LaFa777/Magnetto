from .utils import build_data

mock_noequalsize_1 = (
    build_data(size=5000),
    build_data(size=1024),
    build_data(size=1000),
    build_data(size=2000),
    build_data(size=1500),
)

mock_noequalsize_2 = [
    build_data(size=5000),
    build_data(size=2000),
]
