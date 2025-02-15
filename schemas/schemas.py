class Schema:
    product_details = {
        "id": {"type": "string", "required": True},
        "sellerId": {"type": "integer", "required": True},
        "name": {"type": "string", "required": True},
        "price": {"type": "integer", "required": True},
        "createdAt": {"type": "string", "required": True},
        "statistics": {
            "type": "dict",
            "nullable": True,
            "required": True,
            "schema": {
                "likes": {"type": "integer", "required": True},
                "viewCount": {"type": "integer", "required": True},
                "contacts": {"type": "integer", "required": True},
            },
        },
    }

    product_stat = {
        "likes": {"type": "integer", "required": True},
        "viewCount": {"type": "integer", "required": True},
        "contacts": {"type": "integer", "required": True},
    }

    create_product_response = {
        "status": {"type": "string", "required": True},
    }
