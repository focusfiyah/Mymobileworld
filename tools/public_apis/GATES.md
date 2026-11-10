# Gates: Public APIs link (2026-11-10)
G1 every lookup.py command returns real data, $0, no key. CHECK: bash tools/public_apis/test.sh EXPECT: PUBLIC_APIS_OK
G2 Brain note + Tools row + session log, check passes. CHECK: python3 tools/brain/check.py --terms "public apis,open food facts,openfda,datamuse" EXPECT: BRAIN_OK
G3 rule saved + gate test passes. CHECK: python3 grace/tests/test_public_data.py EXPECT: PUBLIC_DATA_TESTS_OK
