from app.guardrails.pii import mask_pii, contains_pii


def main():
    text = (
        "My email is test@example.com "
        "and my phone number is 9876543210."
    )

    print("Original:")
    print(text)

    print("\nContains PII:")
    print(contains_pii(text))

    print("\nMasked:")
    print(mask_pii(text))


if __name__ == "__main__":
    main()