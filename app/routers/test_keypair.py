import pytest
from fastapi.testclient import TestClient
from fastapi.exceptions import RequestValidationError
from .keypair import router

client = TestClient(router)


class TestHDWalletPostBip32Errors:
    def test_bip32_seed_only(self):
        seed = "0123456789abcdef0123456789abcdef"
        response = client.post("/keypair/from_derivation/", json={"seed": seed})
        assert response.status_code == 200

    def test_bip32_seed_missing(self):
        derivation = "m"
        with pytest.raises(RequestValidationError):
            _ = client.post(
                "/keypair/from_derivation/",
                json={"derivation": derivation},
            )

    def test_bip32_extra_data(self):
        seed = "0123456789abcdef0123456789abcdef"
        derivation = "m"
        with pytest.raises(RequestValidationError):
            _ = client.post(
                "/keypair/from_derivation/",
                json={"seed": seed, "derivation": derivation, "extra": "data"},
            )

    def test_bip32_seed_invalid(self):
        seed = "0123456789abcdeg0123456789abcdef"
        derivation = "m"
        with pytest.raises(RequestValidationError):
            _ = client.post(
                "/keypair/from_derivation/",
                json={"seed": seed, "derivation": derivation},
            )

    def test_bip32_seed_too_short(self):
        seed = "0123456789abcdef0123456789abcde"
        derivation = "m"
        with pytest.raises(RequestValidationError):
            _ = client.post(
                "/keypair/from_derivation/",
                json={"seed": seed, "derivation": derivation},
            )

    def test_bip32_seed_too_long(self):
        seed = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0"
        derivation = "m"
        with pytest.raises(RequestValidationError):
            _ = client.post(
                "/keypair/from_derivation/",
                json={"seed": seed, "derivation": derivation},
            )

    def test_bip32_derivation_invalid_master(self):
        seed = "0123456789abcdef0123456789abcdef"
        derivation = "a"
        with pytest.raises(RequestValidationError):
            _ = client.post(
                "/keypair/from_derivation/",
                json={"seed": seed, "derivation": derivation},
            )


class TestHDWalletPostBip32SeedVector1:
    SEED: str = "000102030405060708090a0b0c0d0e0f"

    def test_bip32_derivation_root_path(self):
        derivation = "m"
        expected_pub = "xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8"
        expected_prv = "xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi"

        response = client.post(
            "/keypair/from_derivation/",
            json={"seed": self.SEED, "derivation": derivation},
        )
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0h(self):
        derivation = "m/0'"
        expected_pub = "xpub68Gmy5EdvgibQVfPdqkBBCHxA5htiqg55crXYuXoQRKfDBFA1WEjWgP6LHhwBZeNK1VTsfTFUHCdrfp1bgwQ9xv5ski8PX9rL2dZXvgGDnw"
        expected_prv = "xprv9uHRZZhk6KAJC1avXpDAp4MDc3sQKNxDiPvvkX8Br5ngLNv1TxvUxt4cV1rGL5hj6KCesnDYUhd7oWgT11eZG7XnxHrnYeSvkzY7d2bhkJ7"

        response = client.post(
            "/keypair/from_derivation/",
            json={"seed": self.SEED, "derivation": derivation},
        )
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0h_1(self):
        derivation = "m/0'/1"
        expected_pub = "xpub6ASuArnXKPbfEwhqN6e3mwBcDTgzisQN1wXN9BJcM47sSikHjJf3UFHKkNAWbWMiGj7Wf5uMash7SyYq527Hqck2AxYysAA7xmALppuCkwQ"
        expected_prv = "xprv9wTYmMFdV23N2TdNG573QoEsfRrWKQgWeibmLntzniatZvR9BmLnvSxqu53Kw1UmYPxLgboyZQaXwTCg8MSY3H2EU4pWcQDnRnrVA1xe8fs"

        response = client.post(
            "/keypair/from_derivation/",
            json={"seed": self.SEED, "derivation": derivation},
        )
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0h_1_2h(self):
        derivation = "m/0'/1/2'"
        response = client.post(
            "/keypair/from_derivation/",
            json={"seed": self.SEED, "derivation": derivation},
        )

        expected_pub = "xpub6D4BDPcP2GT577Vvch3R8wDkScZWzQzMMUm3PWbmWvVJrZwQY4VUNgqFJPMM3No2dFDFGTsxxpG5uJh7n7epu4trkrX7x7DogT5Uv6fcLW5"
        expected_prv = "xprv9z4pot5VBttmtdRTWfWQmoH1taj2axGVzFqSb8C9xaxKymcFzXBDptWmT7FwuEzG3ryjH4ktypQSAewRiNMjANTtpgP4mLTj34bhnZX7UiM"
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0h_1_2h_2(self):
        derivation = "m/0'/1/2'/2"
        expected_pub = "xpub6FHa3pjLCk84BayeJxFW2SP4XRrFd1JYnxeLeU8EqN3vDfZmbqBqaGJAyiLjTAwm6ZLRQUMv1ZACTj37sR62cfN7fe5JnJ7dh8zL4fiyLHV"
        expected_prv = "xprvA2JDeKCSNNZky6uBCviVfJSKyQ1mDYahRjijr5idH2WwLsEd4Hsb2Tyh8RfQMuPh7f7RtyzTtdrbdqqsunu5Mm3wDvUAKRHSC34sJ7in334"

        response = client.post(
            "/keypair/from_derivation/",
            json={"seed": self.SEED, "derivation": derivation},
        )
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0h_1_2h_2_1000000000(self):
        derivation = "m/0'/1/2'/2/1000000000"
        expected_pub = "xpub6H1LXWLaKsWFhvm6RVpEL9P4KfRZSW7abD2ttkWP3SSQvnyA8FSVqNTEcYFgJS2UaFcxupHiYkro49S8yGasTvXEYBVPamhGW6cFJodrTHy"
        expected_prv = "xprvA41z7zogVVwxVSgdKUHDy1SKmdb533PjDz7J6N6mV6uS3ze1ai8FHa8kmHScGpWmj4WggLyQjgPie1rFSruoUihUZREPSL39UNdE3BBDu76"

        response = client.post(
            "/keypair/from_derivation/",
            json={"seed": self.SEED, "derivation": derivation},
        )
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}


class TestHDWalletPostBip32SeedVector2:
    SEED: str = "fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542"

    def test_chain_m(self):
        derivation = "m"
        expected_pub = "xpub661MyMwAqRbcFW31YEwpkMuc5THy2PSt5bDMsktWQcFF8syAmRUapSCGu8ED9W6oDMSgv6Zz8idoc4a6mr8BDzTJY47LJhkJ8UB7WEGuduB"
        expected_prv = "xprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e2DtALGdso3pGz6ssrdK4PFmM8NSpSBHNqPqm55Qn3LqFtT2emdEXVYsCzC2U"

        response = client.post(
            "/keypair/from_derivation/",
            json={"seed": self.SEED, "derivation": derivation},
        )
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0(self):
        derivation = "m/0"
        expected_pub = "xpub69H7F5d8KSRgmmdJg2KhpAK8SR3DjMwAdkxj3ZuxV27CprR9LgpeyGmXUbC6wb7ERfvrnKZjXoUmmDznezpbZb7ap6r1D3tgFxHmwMkQTPH"
        expected_prv = "xprv9vHkqa6EV4sPZHYqZznhT2NPtPCjKuDKGY38FBWLvgaDx45zo9WQRUT3dKYnjwih2yJD9mkrocEZXo1ex8G81dwSM1fwqWpWkeS3v86pgKt"

        response = client.post(
            "/keypair/from_derivation/",
            json={"seed": self.SEED, "derivation": derivation},
        )
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0_2147483647h(self):
        derivation = "m/0/2147483647'"
        expected_pub = "xpub6ASAVgeehLbnwdqV6UKMHVzgqAG8Gr6riv3Fxxpj8ksbH9ebxaEyBLZ85ySDhKiLDBrQSARLq1uNRts8RuJiHjaDMBU4Zn9h8LZNnBC5y4a"
        expected_prv = "xprv9wSp6B7kry3Vj9m1zSnLvN3xH8RdsPP1Mh7fAaR7aRLcQMKTR2vidYEeEg2mUCTAwCd6vnxVrcjfy2kRgVsFawNzmjuHc2YmYRmagcEPdU9"

        response = client.post(
            "/keypair/from_derivation/",
            json={"seed": self.SEED, "derivation": derivation},
        )
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0_2147483647h_1(self):
        derivation = "m/0/2147483647'/1"
        expected_pub = "xpub6DF8uhdarytz3FWdA8TvFSvvAh8dP3283MY7p2V4SeE2wyWmG5mg5EwVvmdMVCQcoNJxGoWaU9DCWh89LojfZ537wTfunKau47EL2dhHKon"
        expected_prv = "xprv9zFnWC6h2cLgpmSA46vutJzBcfJ8yaJGg8cX1e5StJh45BBciYTRXSd25UEPVuesF9yog62tGAQtHjXajPPdbRCHuWS6T8XA2ECKADdw4Ef"

        response = client.post(
            "/keypair/from_derivation/",
            json={"seed": self.SEED, "derivation": derivation},
        )
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0_2147483647h_1_2147483646h(self):
        derivation = "m/0/2147483647'/1/2147483646'"
        expected_pub = "xpub6ERApfZwUNrhLCkDtcHTcxd75RbzS1ed54G1LkBUHQVHQKqhMkhgbmJbZRkrgZw4koxb5JaHWkY4ALHY2grBGRjaDMzQLcgJvLJuZZvRcEL"
        expected_prv = "xprvA1RpRA33e1JQ7ifknakTFpgNXPmW2YvmhqLQYMmrj4xJXXWYpDPS3xz7iAxn8L39njGVyuoseXzU6rcxFLJ8HFsTjSyQbLYnMpCqE2VbFWc"

        response = client.post(
            "/keypair/from_derivation/",
            json={"seed": self.SEED, "derivation": derivation},
        )
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0_2147483647h_1_2147483646h_2(self):
        derivation = "m/0/2147483647'/1/2147483646'/2"
        expected_pub = "xpub6FnCn6nSzZAw5Tw7cgR9bi15UV96gLZhjDstkXXxvCLsUXBGXPdSnLFbdpq8p9HmGsApME5hQTZ3emM2rnY5agb9rXpVGyy3bdW6EEgAtqt"
        expected_prv = "xprvA2nrNbFZABcdryreWet9Ea4LvTJcGsqrMzxHx98MMrotbir7yrKCEXw7nadnHM8Dq38EGfSh6dqA9QWTyefMLEcBYJUuekgW4BYPJcr9E7j"

        response = client.post(
            "/keypair/from_derivation/",
            json={"seed": self.SEED, "derivation": derivation},
        )
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}


class TestHDWalletGetBip32Errors:
    def test_bip32_seed_missing(self):
        with pytest.raises(RequestValidationError):
            _ = client.get("/keypair/from_derivation/m?seed=")
        with pytest.raises(RequestValidationError):
            _ = client.get("/keypair/from_derivation/m")

    def test_bip32_seed_too_short(self):
        seed = "0123456789abcdef0123456789abcde"
        derivation = "m"
        with pytest.raises(RequestValidationError):
            _ = client.get(f"/keypair/from_derivation/{derivation}?seed={seed}")

    def test_bip32_seed_too_long(self):
        seed = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0"
        derivation = "m"
        with pytest.raises(RequestValidationError):
            _ = client.get(f"/keypair/from_derivation/{derivation}?seed={seed}")

    def test_bip32_derivation_invalid_master(self):
        seed = "0123456789abcdef0123456789abcdef"
        derivation = "a"
        with pytest.raises(RequestValidationError):
            _ = client.get(f"/keypair/from_derivation/{derivation}?seed={seed}")


class TestHDWalletGetBip32SeedVector1:
    SEED: str = "000102030405060708090a0b0c0d0e0f"

    def test_bip32_derivation_root_path(self):
        derivation = "m"
        expected_pub = "xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8"
        expected_prv = "xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi"

        response = client.get(f"/keypair/from_derivation/{derivation}?seed={self.SEED}")
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0h(self):
        derivation = "m/0'"
        expected_pub = "xpub68Gmy5EdvgibQVfPdqkBBCHxA5htiqg55crXYuXoQRKfDBFA1WEjWgP6LHhwBZeNK1VTsfTFUHCdrfp1bgwQ9xv5ski8PX9rL2dZXvgGDnw"
        expected_prv = "xprv9uHRZZhk6KAJC1avXpDAp4MDc3sQKNxDiPvvkX8Br5ngLNv1TxvUxt4cV1rGL5hj6KCesnDYUhd7oWgT11eZG7XnxHrnYeSvkzY7d2bhkJ7"

        response = client.get(f"/keypair/from_derivation/{derivation}?seed={self.SEED}")
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0h_1(self):
        derivation = "m/0'/1"
        expected_pub = "xpub6ASuArnXKPbfEwhqN6e3mwBcDTgzisQN1wXN9BJcM47sSikHjJf3UFHKkNAWbWMiGj7Wf5uMash7SyYq527Hqck2AxYysAA7xmALppuCkwQ"
        expected_prv = "xprv9wTYmMFdV23N2TdNG573QoEsfRrWKQgWeibmLntzniatZvR9BmLnvSxqu53Kw1UmYPxLgboyZQaXwTCg8MSY3H2EU4pWcQDnRnrVA1xe8fs"

        response = client.get(f"/keypair/from_derivation/{derivation}?seed={self.SEED}")
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0h_1_2h(self):
        derivation = "m/0'/1/2'"
        expected_pub = "xpub6D4BDPcP2GT577Vvch3R8wDkScZWzQzMMUm3PWbmWvVJrZwQY4VUNgqFJPMM3No2dFDFGTsxxpG5uJh7n7epu4trkrX7x7DogT5Uv6fcLW5"
        expected_prv = "xprv9z4pot5VBttmtdRTWfWQmoH1taj2axGVzFqSb8C9xaxKymcFzXBDptWmT7FwuEzG3ryjH4ktypQSAewRiNMjANTtpgP4mLTj34bhnZX7UiM"

        response = client.get(f"/keypair/from_derivation/{derivation}?seed={self.SEED}")
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0h_1_2h_2(self):
        derivation = "m/0'/1/2'/2"
        expected_pub = "xpub6FHa3pjLCk84BayeJxFW2SP4XRrFd1JYnxeLeU8EqN3vDfZmbqBqaGJAyiLjTAwm6ZLRQUMv1ZACTj37sR62cfN7fe5JnJ7dh8zL4fiyLHV"
        expected_prv = "xprvA2JDeKCSNNZky6uBCviVfJSKyQ1mDYahRjijr5idH2WwLsEd4Hsb2Tyh8RfQMuPh7f7RtyzTtdrbdqqsunu5Mm3wDvUAKRHSC34sJ7in334"

        response = client.get(f"/keypair/from_derivation/{derivation}?seed={self.SEED}")
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0h_1_2h_2_1000000000(self):
        derivation = "m/0'/1/2'/2/1000000000"
        expected_pub = "xpub6H1LXWLaKsWFhvm6RVpEL9P4KfRZSW7abD2ttkWP3SSQvnyA8FSVqNTEcYFgJS2UaFcxupHiYkro49S8yGasTvXEYBVPamhGW6cFJodrTHy"
        expected_prv = "xprvA41z7zogVVwxVSgdKUHDy1SKmdb533PjDz7J6N6mV6uS3ze1ai8FHa8kmHScGpWmj4WggLyQjgPie1rFSruoUihUZREPSL39UNdE3BBDu76"

        response = client.get(f"/keypair/from_derivation/{derivation}?seed={self.SEED}")
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}


class TestHDWalletGetBip32SeedVector2:
    SEED: str = "fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542"

    def test_chain_m(self):
        derivation = "m"
        expected_pub = "xpub661MyMwAqRbcFW31YEwpkMuc5THy2PSt5bDMsktWQcFF8syAmRUapSCGu8ED9W6oDMSgv6Zz8idoc4a6mr8BDzTJY47LJhkJ8UB7WEGuduB"
        expected_prv = "xprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e2DtALGdso3pGz6ssrdK4PFmM8NSpSBHNqPqm55Qn3LqFtT2emdEXVYsCzC2U"

        response = client.get(f"/keypair/from_derivation/{derivation}?seed={self.SEED}")
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0(self):
        derivation = "m/0"
        expected_pub = "xpub69H7F5d8KSRgmmdJg2KhpAK8SR3DjMwAdkxj3ZuxV27CprR9LgpeyGmXUbC6wb7ERfvrnKZjXoUmmDznezpbZb7ap6r1D3tgFxHmwMkQTPH"
        expected_prv = "xprv9vHkqa6EV4sPZHYqZznhT2NPtPCjKuDKGY38FBWLvgaDx45zo9WQRUT3dKYnjwih2yJD9mkrocEZXo1ex8G81dwSM1fwqWpWkeS3v86pgKt"

        response = client.get(f"/keypair/from_derivation/{derivation}?seed={self.SEED}")
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0_2147483647h(self):
        derivation = "m/0/2147483647'"
        expected_pub = "xpub6ASAVgeehLbnwdqV6UKMHVzgqAG8Gr6riv3Fxxpj8ksbH9ebxaEyBLZ85ySDhKiLDBrQSARLq1uNRts8RuJiHjaDMBU4Zn9h8LZNnBC5y4a"
        expected_prv = "xprv9wSp6B7kry3Vj9m1zSnLvN3xH8RdsPP1Mh7fAaR7aRLcQMKTR2vidYEeEg2mUCTAwCd6vnxVrcjfy2kRgVsFawNzmjuHc2YmYRmagcEPdU9"

        response = client.get(f"/keypair/from_derivation/{derivation}?seed={self.SEED}")
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0_2147483647h_1(self):
        derivation = "m/0/2147483647'/1"
        expected_pub = "xpub6DF8uhdarytz3FWdA8TvFSvvAh8dP3283MY7p2V4SeE2wyWmG5mg5EwVvmdMVCQcoNJxGoWaU9DCWh89LojfZ537wTfunKau47EL2dhHKon"
        expected_prv = "xprv9zFnWC6h2cLgpmSA46vutJzBcfJ8yaJGg8cX1e5StJh45BBciYTRXSd25UEPVuesF9yog62tGAQtHjXajPPdbRCHuWS6T8XA2ECKADdw4Ef"

        response = client.get(f"/keypair/from_derivation/{derivation}?seed={self.SEED}")
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0_2147483647h_1_2147483646h(self):
        derivation = "m/0/2147483647'/1/2147483646'"
        expected_pub = "xpub6ERApfZwUNrhLCkDtcHTcxd75RbzS1ed54G1LkBUHQVHQKqhMkhgbmJbZRkrgZw4koxb5JaHWkY4ALHY2grBGRjaDMzQLcgJvLJuZZvRcEL"
        expected_prv = "xprvA1RpRA33e1JQ7ifknakTFpgNXPmW2YvmhqLQYMmrj4xJXXWYpDPS3xz7iAxn8L39njGVyuoseXzU6rcxFLJ8HFsTjSyQbLYnMpCqE2VbFWc"

        response = client.get(f"/keypair/from_derivation/{derivation}?seed={self.SEED}")
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}

    def test_chain_m_0_2147483647h_1_2147483646h_2(self):
        derivation = "m/0/2147483647'/1/2147483646'/2"
        expected_pub = "xpub6FnCn6nSzZAw5Tw7cgR9bi15UV96gLZhjDstkXXxvCLsUXBGXPdSnLFbdpq8p9HmGsApME5hQTZ3emM2rnY5agb9rXpVGyy3bdW6EEgAtqt"
        expected_prv = "xprvA2nrNbFZABcdryreWet9Ea4LvTJcGsqrMzxHx98MMrotbir7yrKCEXw7nadnHM8Dq38EGfSh6dqA9QWTyefMLEcBYJUuekgW4BYPJcr9E7j"

        response = client.get(f"/keypair/from_derivation/{derivation}?seed={self.SEED}")
        assert response.status_code == 200
        assert response.json() == {"pubkey": expected_pub, "prvkey": expected_prv}
